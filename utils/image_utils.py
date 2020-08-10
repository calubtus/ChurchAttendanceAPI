from PIL import ImageTk, Image
from utils import time_utils as time_utils
from utils import device_utils as dev_utils
import os.path
import glob

#from __future__ import print_function

def scale_image(size, im):  
    width, height = im.size
    new_height = size
    new_width  = int(new_height * width / height)
    im = im.resize((new_width, new_height), Image.ANTIALIAS)
    return im

def open_image(path, scaling):
    im = Image.open(path)
    im = scale_image(scaling, im)
    im = ImageTk.PhotoImage(im)
    return im

# Crop a 3024 by 4032 image into samples of 720 by 1280
#
# Setting the points for cropped image 
# 3024 / 720 = 4, 4032 / 1280 = 3 
#
def crop_image():
    CWD_PATH = dev_utils.resource_path_base()
    SYSTEM_IMAGES_PATH  = CWD_PATH + "\\system_images"
    CROPPED_IMA_PATH = CWD_PATH  + "\\cropped_images"

    crop_folder = glob.glob(CROPPED_IMA_PATH + "\\*.JPG")

    # Delete images previous content
    for crop_image in crop_folder:    
        try:
            os.remove(crop_image)
        except OSError as e:
            print("Error: %s : %s" % (crop_image, e.strerror))
       
    dropbox_folder = glob.glob(SYSTEM_IMAGES_PATH + "\\*.JPG")
    
    # Check if dropbox folder is empty
    if len(dropbox_folder) == 0:
        print("dropbox folder empty")
   
    # Crop images and save them into a new folder
    for raw_image in range(len(dropbox_folder)):
        # Opens a image in RGB mode 
        im = Image.open(dropbox_folder[raw_image])
       
        bottom = 4032
        top = 5312
        
        increment_x = 720
        increment_y = 1280
        
        # Total of images to draw equals 12
        for y in range(3):
            left = -648
            right = 72
            
            bottom = bottom - increment_y
            top = top - increment_y
            
            for x in range(4):
                left = left + increment_x
                right = right + increment_x
                
                im1 = im.crop((bottom, left, top, right)) 
                im1 = im1.rotate(90, Image.NEAREST, expand = 1) 
                
                time = time_utils.obtain_time()
                im1 = im1.save(CROPPED_IMA_PATH + '\\crop_%s.JPG' % (time)) 

    # Delete dropbox items
    for raw_image in dropbox_folder:    
        try:
            os.remove(raw_image)
        except OSError as e:
            print("Error: %s : %s" % (raw_image, e.strerror))
                               
    print('cropping completed...')

# Combine multiple images into one.
def stitch_image(): 
    CWD_PATH = dev_utils.resource_path_base()
    RESULTS_PATH = CWD_PATH + "\\results"
    results_folder = glob.glob(RESULTS_PATH + "\\*.JPG")
    PROCESSED_IM_PATH = CWD_PATH + "\\processed_images"

    # Delete images previous content
    for result_image in results_folder:    
        try:
            os.remove(result_image)
        except OSError as e:
            print("Error: %s : %s" % (result_image, e.strerror))

    process_folder = glob.glob(PROCESSED_IM_PATH + "\\*.JPG")

    total_images = int(len(process_folder)/12)
    processed_image = 0

    for sector in range(total_images):
        result = Image.new("RGB", (1440, 1920))

        for index in range(12):
            path = os.path.expanduser(process_folder[processed_image])
            img = Image.open(path)
            img.thumbnail((360, 640), Image.ANTIALIAS)
            x = index % 4 * 360
            y = index // 4 * 640
            w, h = img.size
            result.paste(img, (x, y, x + w, y + h))
            processed_image += 1;

        time = time_utils.obtain_time() # obtain time 
        result.save(os.path.expanduser(RESULTS_PATH + "\\sector_%s.jpg" % (time)))

    print("stitching completed...")

def delete_system_images():
    CWD_PATH = dev_utils.resource_path_base()
    SYSTEM_IMAGES_PATH  = CWD_PATH + "\\system_images"

    system_folder = glob.glob(SYSTEM_IMAGES_PATH + "\\*.JPG")

    # Delete images previous content
    for system_image in system_folder:    
        try:
            os.remove(system_image)
        except OSError as e:
            print("Error: %s : %s" % (system_image, e.strerror))