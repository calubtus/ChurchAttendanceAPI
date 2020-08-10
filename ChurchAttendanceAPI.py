import tkinter.messagebox as mb
import tkinter as tk
import sys 
import ast
import os
import threading

from tkinter import ttk
from tkinter.font import Font
from utils import object_detection_utils as obj_det_utils
from utils import device_utils as dev_utils
from utils import image_utils as im_utils
from utils import ssh_utils

class AddDevice(tk.Toplevel):
    def __init__(self, parent, tree, dataCols):
        super().__init__(parent)
        self.title("Add Device")
        self.iconbitmap(dev_utils.resource_path('churchlogo.ico'))
        self.set_window()

        tk.Label(self, text="Name:").grid(row=0, padx=5, sticky='W')
        tk.Label(self, text="Host Name(or IP address):").grid(row=1, padx=5, sticky='W')
        tk.Label(self, text="username:").grid(row=2, padx=5, sticky='W')
        tk.Label(self, text="password:").grid(row=3, padx=5, sticky='W')

        self.tree = tree
        self.dataCols = dataCols
        self.entry_name = tk.Entry(self, width=30)
        self.entry_name.grid(row=0,column=1, padx=5, pady=5)
        self.entry_host = tk.Entry(self, width=30)
        self.entry_host.grid(row=1,column=1, padx=5, pady=5)
        self.entry_username = tk.Entry(self, width=30)
        self.entry_username.grid(row=2,column=1, padx=5, pady=5)
        self.entry_pass = tk.Entry(self, width=30, show="*")
        self.entry_pass.grid(row=3,column=1, padx=5, pady=5)
        self.button_enter = tk.Button(self, text="Enter", 
            command=self.close_add_window)
        self.button_enter.grid(row=4, column=1, padx=5, pady=5)

        self.bind('<Return>', self.close_add_window)

    def close_add_window(self, event=None):
        if self.entry_name.get() and self.entry_host.get() and self.entry_username.get() and self.entry_pass.get():
            self.update_data()
            self.destroy()
        else:
            tk.Label(self, text="*please fill all fields", foreground="red").grid(row=4, column=0, padx=5, sticky='W')

    def update_data(self):
        self.info = (self.entry_name.get(), self.entry_host.get(), self.entry_username.get(), self.entry_pass.get())
        dev_utils.append_device_info(self.info)
        self.device_info = self.info[0:3]
        self.tree.insert('', 'end', values=self.device_info)
        for idx, val in enumerate(self.device_info):
            iwidth = Font().measure(val)
            if self.tree.column(self.dataCols[idx], 'width') < iwidth:
                self.tree.column(self.dataCols[idx], width = iwidth)

    def set_window(self):
        self.w = 348
        self.h = 152 
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight() 
        self.x = (self.ws/2) - (self.w/2)
        self.y = (self.hs/2) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))             

class DeviceManager(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Device Manager")
        self.iconbitmap(dev_utils.resource_path('churchlogo.ico'))
        self.set_window()

        self.dataCols = ('Name', 'IP address', 'username')        
        self.tree = ttk.Treeview(self, columns=self.dataCols, show = 'headings')

        ysb = tk.Scrollbar(self, orient=tk.VERTICAL, command= self.tree.yview)
        xsb = tk.Scrollbar(self, orient=tk.HORIZONTAL, command= self.tree.xview)
        self.tree['yscroll'] = ysb.set
        self.tree['xscroll'] = xsb.set

        self.tree.grid( row=0, column=0, columnspan=2, sticky=tk.NSEW)
        ysb.grid( row=0, column=2, sticky=tk.NS)
        xsb.grid( row=2, column=0, columnspan=2, sticky=tk.EW)

        self.button_remove = tk.Button(self, text="Remove", command=self.delete_device)
        self.button_remove.config(state=tk.DISABLED)
        self.button_remove.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.button_add = tk.Button(self, text="Add", command=self.open_add_window)
        self.button_add.grid(row=1, column=1, padx=5, pady=5)

        self.rowconfigure(0, weight=1) # set frame resize priorities
        self.columnconfigure(0, weight=1)
        self.tree.bind("<ButtonRelease-1>", self.enable_delete)
        self.load_data()

    def enable_delete(self, event):
        items = self.tree.item(self.tree.focus())
        if items["values"]: # check if we have click a row before we enable
            self.button_remove.config(state=tk.NORMAL)

    def delete_device(self):
        self.button_remove.config(state=tk.DISABLED)
        self.itemIndex = self.tree.index(self.tree.focus())
        dev_utils.delete_device_info(self.itemIndex)
        self.tree.delete(*self.tree.get_children())
        self.load_data()

    def load_data(self):
        self.device_info = dev_utils.read_device_info()
        for col in self.dataCols:
            self.tree.heading(col, text=col.title())            
            self.tree.column(col, width=Font().measure(col.title()) + 20)
        for item in self.device_info: 
            self.tree.insert('', 'end', values=item)
            for idx, val in enumerate(item):
                iwidth = Font().measure(val)
                if self.tree.column(self.dataCols[idx], 'width') < iwidth:
                    self.tree.column(self.dataCols[idx], width = iwidth)

    def set_window(self):
        self.w = 269 
        self.h = 280
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight() 
        self.x = (self.ws/2) - (self.w/2)
        self.y = (self.hs/2) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))

    def open_add_window(self):
        window = AddDevice(self, self.tree, self.dataCols)
        window.grab_set()

class ProgressWindow(tk.Toplevel):
    def __init__(self, parent, combo, image_frame, count_label, attendance_label):
        super().__init__(parent)
        self.title("Algorithm Run")
        self.iconbitmap(dev_utils.resource_path('churchlogo.ico'))
        self.set_window()
        self.protocol("WM_DELETE_WINDOW", self.cancel_action)
        self.combo = combo
        self.image_frame = image_frame
        self.count_label = count_label
        self.attendance_label = attendance_label

        self.label_frame = tk.LabelFrame(self, bd=0)
        self.label_frame.grid(row=0, column=0, padx=55, pady=5)

        self.im_check_gr = im_utils.open_image(dev_utils.resource_path("check_gray.png"), 20)
        self.im_check = im_utils.open_image(dev_utils.resource_path("check.png"), 20)

        tk.Label(self.label_frame, image=self.im_check_gr).grid(row=0, column=0)
        tk.Label(self.label_frame, text="Connecting to devices").grid(row=0, column=1, pady=2, sticky='W')
        tk.Label(self.label_frame, image=self.im_check_gr).grid(row=1, column=0)
        tk.Label(self.label_frame, text="Received device images").grid(row=1, column=1, pady=2, sticky='W')
        tk.Label(self.label_frame, image=self.im_check_gr).grid(row=2, column=0)
        tk.Label(self.label_frame, text="Processing device images").grid(row=2, column=1, pady=2, sticky='W')
        tk.Label(self.label_frame, image=self.im_check_gr).grid(row=3, column=0)
        tk.Label(self.label_frame, text="Running object detection").grid(row=3, column=1, pady=2, sticky='W')
        tk.Label(self.label_frame, image=self.im_check_gr).grid(row=4, column=0)
        tk.Label(self.label_frame, text="Stitching resultant images").grid(row=4, column=1, pady=2, sticky='W')
        tk.Label(self.label_frame, image=self.im_check_gr).grid(row=4, column=0)

        button_frame = tk.LabelFrame(self, bd=0)
        button_frame.grid(row=1, column=0, padx=5, sticky='E')

        self.button_ok = tk.Button(button_frame, padx=22, pady=2, text="OK", command=self.close_progress_window)
        self.button_ok.config(state=tk.DISABLED)
        self.button_ok.grid(row=0, column=0, padx=2, pady=7)
        self.button_cancel = tk.Button(button_frame, padx=12, pady=2, text="Cancel", command=self.cancel_action)
        self.button_cancel.grid(row=0, column=1, padx=2, pady=7)

        self.thread_done = False
        self.thread = threading.Thread(target=self.request_service)
        self.thread.daemon = True
        self.thread.start()
        self.check_thread(self.thread)

    def cancel_action(self):
        if self.thread_done:
            self.close_progress_window()
        else:
            sys.exit()

    def check_thread(self, thread):
        if thread.is_alive():
            self.after(100, lambda: self.check_thread(thread))
        else:
            self.thread_done = True
            self.update_dropdown()
            self.button_ok.config(state=tk.NORMAL)
            self.button_cancel.config(state=tk.DISABLED)

    def close_progress_window(self):
        self.destroy()

    def update_dropdown(self):
        self.device_names = dev_utils.read_device_names()
        self.combo['values'] = self.device_names
        self.combo.current(0) 
        self.result_images = obj_det_utils.read_result_im()
        self.im_result = im_utils.open_image(self.result_images[0], 700)
        tk.Label(self.image_frame, image=self.im_result, width=525, height=700).grid(row=1, column=0)
        self.count_label.config(text=("Count: %d") % (self.images_info[0][0]))
        self.attendance_label.config(text=("Attendance Count: %d") % (self.images_info[-1][1]))

    def get_image_info(self):
        return self.images_info             

    def request_service(self):
        im_utils.delete_system_images()
        ssh_status, device = ssh_utils.create_ssh_key()
        tk.Label(self.label_frame, image=self.im_check).grid(row=0, column=0)
        service_status = ssh_utils.sftp_service()
        if service_status and ssh_status:
            tk.Label(self.label_frame, image=self.im_check).grid(row=1, column=0)
            im_utils.crop_image()
            tk.Label(self.label_frame, image=self.im_check).grid(row=2, column=0)
            self.images_info = obj_det_utils.object_detection()
            print(self.images_info)
            tk.Label(self.label_frame, image=self.im_check).grid(row=3, column=0)
            im_utils.stitch_image()
            tk.Label(self.label_frame, image=self.im_check).grid(row=4, column=0)
        else:
            self.close_progress_window()
            mb.showinfo("Alert","Unable to establish connection with %s" % (device))

    def set_window(self):
        self.w = 277 
        self.h = 177
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight() 
        self.x = (self.ws/2) - (self.w/2)
        self.y = (self.hs/2) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))

class ChurchApp(tk.Tk):
    def __init__(self):
        super().__init__()   
        self.title("Church Attendance API")
        self.iconbitmap(dev_utils.resource_path('churchlogo.ico'))
        self.set_window()

        menu_frame = tk.LabelFrame(self, bd=0)
        menu_frame.grid(row=0, column=0, rowspan=3, pady=15, sticky='S')

        self.button_manager = tk.Button(menu_frame, text="Device\n Manager", padx=15, pady=15, command=self.open_device_window)
        self.button_manager.pack(pady=5)
        self.button_run = tk.Button(menu_frame, text="Run", padx=30, pady=20, command=self.run_detection, bg="#4ee44e")
        self.button_run.pack(padx=10, pady=5)

        self.image_frame = tk.LabelFrame(self, bd=2, relief=tk.SUNKEN)
        self.image_frame.grid(row=0,column=1, columnspan = 2, padx=5, pady=10)
        
        self.im_unavailable = im_utils.open_image(dev_utils.resource_path("NoImageAvailable.png"), 100)
        tk.Label(self.image_frame, image=self.im_unavailable, width=525, height=700).grid(row=1, column=0)

        self.count_label = tk.Label(self, text="Count: NA")
        self.count_label.config(font=("Helvetica", 14))
        self.count_label.grid(row=2, column=1, pady=10)

        self.attendance_label = tk.Label(self, text="Attendance Count: NA")
        self.attendance_label.config(font=("Helvetica", 14))
        self.attendance_label.grid(row=2, column=2, pady=10)

        self.combo = ttk.Combobox(self, state="readonly")
        self.combo.bind("<<ComboboxSelected>>", self.select_images)
        self.combo.grid(row=1,column=2, padx=10, sticky='NE')

    def select_images(self, event):
        self.menu_index = self.combo.current()
        self.result_images = obj_det_utils.read_result_im()
        self.im_result = im_utils.open_image(self.result_images[self.menu_index], 700)
        tk.Label(self.image_frame, image=self.im_result, width=525, height=700).grid(row=1, column=0)
        self.images_info = self.progress_window.get_image_info()
        self.count_label.config(text=("Count: %d") % (self.images_info[self.menu_index][0]))
        self.attendance_label.config(text=("Attendance Count: %d") % (self.images_info[-1][1]))

    def open_device_window(self):
        window = DeviceManager(self)
        window.grab_set()

    def run_detection(self):
        if dev_utils.read_device_names(): # check if there are devices to connect to
            self.progress_window = ProgressWindow(self, self.combo, self.image_frame, self.count_label, self.attendance_label)
            self.progress_window.grab_set()
        else:
            mb.showinfo("Alert","No devices listed to connect to")

    def set_window(self):
        self.w = 653 
        self.h = 797
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight() 
        self.x = (self.ws/2) - (self.w/2)
        self.y = (self.hs/2) - (self.h/2)
        self.geometry('%dx%d+%d+%d' % (self.w, self.h, self.x, self.y))

if __name__ == '__main__':
    app = ChurchApp()
    app.mainloop()

