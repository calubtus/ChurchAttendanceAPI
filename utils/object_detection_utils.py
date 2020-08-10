## Some of this code was obtrained from Edge Electronics repo at 
## https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10/blob/master/Object_detection_image.py

## but it was modified to accomodate the needs of the Church Application


# Import packages
import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import glob

# Import utilites
from utils import time_utils as time_utils
from utils import label_map_util
from utils import visualization_utils as vis_util
from utils import device_utils as dev_utils

def object_detection():

    # This is needed since the notebook is stored in the object_detection folder.
    sys.path.append("..")
    CWD_PATH = dev_utils.resource_path_base()
    PROCESSED_IM_PATH = CWD_PATH + "\\processed_images"
    CROPPED_IM_PATH = CWD_PATH + "\\cropped_images"
    
    process_folder = glob.glob(PROCESSED_IM_PATH + "\\*.JPG")
      
    # Delete images previous content
    for processed_image in process_folder:    
        try:
            os.remove(processed_image)
        except OSError as e:
            print("Error: %s : %s" % (processed_image, e.strerror))
    
    # find folder items
    crop_folder = os.listdir(CROPPED_IM_PATH)
    
    total_object = 0
    image_objects = 0
    interation_count = 0
    image_info = []

    for crop_image in crop_folder:
        interation_count += 1
    
        # Name of the directory containing the object detection module we're using
        MODEL_NAME = 'inference_graph'
        IMAGE_NAME = crop_image
        #IMAGE_NAME = 'test_img.jpg'

        # Grab path to current working directory
        CWD_PATH = dev_utils.resource_path_base()
        IMG_PATH = CWD_PATH + "\\cropped_images"

        # Path to frozen detection graph .pb file, which contains the model that is used
        # for object detection.
        PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

        # Path to label map file
        PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

        # Path to image
        PATH_TO_IMAGE = os.path.join(IMG_PATH,IMAGE_NAME)

        # Number of classes the object detector can identify
        NUM_CLASSES = 1

        # Load the label map.
        # Label maps map indices to category names, so that when our convolution
        # network predicts `5`, we know that this corresponds to `king`.
        # Here we use internal utility functions, but anything that returns a
        # dictionary mapping integers to appropriate string labels would be fine
        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        category_index = label_map_util.create_category_index(categories)

        # Load the Tensorflow model into memory.
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            sess = tf.Session(graph=detection_graph)

        # Define input and output tensors (i.e. data) for the object detection classifier

        # Input tensor is the image
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

        # Output tensors are the detection boxes, scores, and classes
        # Each box represents a part of the image where a particular object was detected
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

        # Each score represents level of confidence for each of the objects.
        # The score is shown on the result image, together with the class label.
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

        # Number of objects detected
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')

        # Load image using OpenCV and
        # expand image dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        image = cv2.imread(PATH_TO_IMAGE)
        image_expanded = np.expand_dims(image, axis=0)

        # Perform the actual detection by running the model with the image as input
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_expanded})

        # Draw the results of the detection (aka 'visulaize the results')

        vis_util.visualize_boxes_and_labels_on_image_array(
            image,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=8,
            min_score_thresh=0.60)

        # All the results have been drawn on image. Now display the image.
        num_objects = vis_util.num_squares

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image,'Person Count:', (0,25), font, 1, (250,250,250),2,cv2.LINE_AA)
        cv2.putText(image, str(num_objects), (250,25), font, 1, (250,250,250),2,cv2.LINE_AA)
        
        total_object = num_objects + total_object
        image_objects = num_objects + image_objects
        
        if interation_count >= 12:
            cv2.putText(image,'Total Count:', (400,25), font, 1, (250,250,250),2,cv2.LINE_AA)
            cv2.putText(image, str(total_object), (610,25), font, 1, (250,250,250),2,cv2.LINE_AA)
            interation_count = 0
            image_info.append((image_objects, total_object))
            image_objects = 0


        image = cv2.pyrDown(image) # scale down
        
        time = time_utils.obtain_time() # obtain time 
        cv2.imwrite(PROCESSED_IM_PATH + '\\processed_%s.JPG' % (time), image)
        
    print("object detection completed...")
    return image_info

def read_result_im():
        CWD_PATH = dev_utils.resource_path_base()
        RESULTS_PATH = CWD_PATH + "\\results"
        process_folder = glob.glob(RESULTS_PATH + "\\*.JPG")
        return process_folder