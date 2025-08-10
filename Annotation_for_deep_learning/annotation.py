from typing import List
from napari import Viewer
from dask_image.imread import imread
import napari
from magicgui.widgets import ComboBox, Container
import numpy as np
from magicgui import magicgui
from napari.types import ImageData
import glob
import pandas as pd
import RearrangeData 
import pathlib
from tkinter import filedialog
import tkinter as tk
import ObjectDetection
from skimage.io import imread
from dask import delayed
import dask.array as da
import Two_object_detection as two
import AugmentationFunctions
import os
import ToInsertVisibilityInAnnotation as TIVIA
from tkinter import messagebox
from natsort import natsorted
from auxiliary import load_labels_files
from qtpy.QtWidgets import QFileDialog

COLOR_CYCLE = [
    '#1f77b4',
    '#ff7f0e',
    '#2ca02c',
    '#d62728',
    '#9467bd',
    '#8c564b',
    '#e377c2',
    '#7f7f7f',
    '#bcbd22',
    '#17becf',
    '#feb24c',
    '#9C661f',
    '#a52a2a',
    '#ffeda0',
    '#800026',
    '#000000',
    '#1f77b4',
    '#ffffff'
]


# COLOR_CYCLE = [
#     '#1f77b4',
#     '#ff7f0e',
#     '#2ca02c'




def create_label_menu(points_layer, labels):
    """Create a label menu widget that can be added to the napari viewer dock

    Parameters:
    -----------
    points_layer    napari.layers.Points
        a napari points layer
    labels : List[str]
        list of the labels for each keypoint to be annotated (e.g., the body parts to be labeled).

    Returns:
    --------
    label_menu : Container
        the magicgui Container with our dropdown menu widget
    """
    # Create the label selection menu
    label_menu = ComboBox(label='feature_label', choices=labels)
    label_widget = Container(widgets=[label_menu])
###########################
##################################


##################################################################

    def update_label_menu(event):
        """Update the label menu when the point selection changes"""
        new_label = str(points_layer.current_properties['label'][0])
        if new_label != label_menu.value:
            label_menu.value = new_label
        print('updated')
        print(new_label)
        print(points_layer.data)
      
        

    points_layer.events.current_properties.connect(update_label_menu)

    def label_changed(event):
        """Update the Points layer when the label menu selection changes"""
        selected_label = event.value
        current_properties = points_layer.current_properties
        current_properties['label'] = np.asarray([selected_label])
        points_layer.current_properties = current_properties
        print('changed')

    label_menu.changed.connect(label_changed)

    return label_widget


def point_annotator(
        im_path: str,path: str,
        labels: List[str] ):
    """Create a GUI for annotating points in a series of images.

    Parameters
    ----------
    im_path : str
        glob-like string for the images to be labeled.
    labels : List[str]
        list of the labels for each keypoint to be annotated (e.g., the body parts to be labeled).
    """
    global SHAPE_STACK
    global LABELS
    global IM_PATH
    global PATH_FOLDER
    PATH_FOLDER = path
    IM_PATH = im_path
    #function to read the images
    stack = LoadImages(im_path)
    # LABELS = labels
    # stack = imread(im_path)
    SHAPE_STACK = stack.shape
    print(SHAPE_STACK)
   
   
    viewer = napari.view_image(stack)
    #to change the current position
    viewer.dims.current_step = (0,255,255)
   # features = {'label': np.empty(3, dtype=int)}
    properties = {'label': labels}
    # add the points
    #create a big layer and cut it for the number of labels
    #arrayModel = [[0,100,-1],[0,200,-1],[0,300,-1],[0,400,-1],[0,500,-1],[0,600,-1],[0,700,-1],[0,800,-1],[0,900,-1],[0,1000,-1],[0,1100,-1],[0,1200,-1]]
    #points= arrayModel[0:len(labels)]
   # points = np.array([[0,100,-1],[0,200,-1],[0,300,-1],[0,400,-1]])
    
    points = []
    labelsnew = labels
    labels1=[]
    arrayModel = []
    for index in range(SHAPE_STACK[0]):
        #for location in range(100,351,20):
         #   arrayModel.append([index,location,-1])
       
        arrayModel = [[index,100,-1],[index,200,-1],[index,300,-1],[index,400,-1],[index,500,-1],[index,600,-1],[index,700,-1],[index,800,-1],[index,900,-1],[index,1000,-1],[index,1100,-1],[index,1200,-1],
                     [index,100,100],[index,200,100],[index,300,100],[index,400,100],[index,500,100],[index,600,100],[index,700,100],[index,800,100],[index,900,100],[index,1000,-100],[index,1100,100],[index,1200,100]]
        points = points + arrayModel[0:len(labelsnew)]
        labels1 = labels1 + labelsnew
        # print(points)
        # print(labels)
  
    properties = {'label': labels1} 
    points_layer = viewer.add_points(
      points,
    properties=properties,
      edge_color='label',
      edge_color_cycle=COLOR_CYCLE,
      symbol='o',
      face_color = 'label',
      face_color_cycle=COLOR_CYCLE,
      edge_width_is_relative = 8,
      #size= SHAPE_STACK[0],
      size = 30,#30
      ndim=3,
      name = "keypoints",
     
      )
    points_layer.edge_color_mode = 'cycle'
    points_layer.face_color_mode = 'cycle'
    
   
        

  
  
   
#####################
# add the polygons
    polygons = []
    for index in range(SHAPE_STACK[0]):
        polygons.append(np.array([[ index,  879.52867728,  592.9339079 ],
           [   index        ,  879.52867728,  906.41696375],
           [   index        , 1260.79185332,  906.41696375],
           [   index        , 1260.79185332,  592.9339079 ]]))
    layer_shapes = viewer.add_shapes(
        polygons,
        shape_type='polygon',
        edge_width=3,
        edge_color='coral',
        face_color='#0000',
        name='boxes',
        )
    
    
    
####################################
    # add the label menu widget to the viewer
    label_widget = create_label_menu(points_layer, labels)
    viewer.window.add_dock_widget(label_widget)
    viewer.window.add_dock_widget(my_widget1,area='right')
    viewer.window.add_dock_widget(widget2,area='right')
    viewer.window.add_dock_widget(widget3,area='right')
    viewer.window.add_dock_widget(widget4,area='right')
    viewer.window.add_dock_widget(widget5,area='right')
    viewer.window.add_dock_widget(widget6, area = 'right')
    
    napari.run()

    @viewer.bind_key('.')
    def next_label(event=None):
        """Keybinding to advance to the next label with wraparound"""
        current_properties = points_layer.current_properties
        current_label = current_properties['label'][0]
        ind = list(labels).index(current_label)
        new_ind = (ind + 1) % len(labels)
        new_label = labels[new_ind]
        current_properties['label'] = np.array([new_label])
        points_layer.current_properties = current_properties

    def next_on_click(layer, event):
        """Mouse click binding to advance the label when a point is added"""
        if layer.mode == 'add':
            next_label()

            # by default, napari selects the point that was just added
            # disable that behavior, as the highlight gets in the way
            layer.selected_data = {}

    points_layer.mode = 'add'
    points_layer.mouse_drag_callbacks.append(next_on_click)

    @viewer.bind_key(',')
    def prev_label(event):
        """Keybinding to decrement to the previous label with wraparound"""
        current_properties = points_layer.current_properties
        current_label = current_properties['label'][0]
        ind = list(labels).index(current_label)
        n_labels = len(labels)
        new_ind = ((ind - 1) + n_labels) % n_labels
        new_label = labels[new_ind]
        current_properties['label'] = np.array([new_label])
        points_layer.current_properties = current_properties
     
    @viewer.bind_key('s')
    def save_data(event=None):
         print(points_layer.data)
        

        
#Auxiliary functions
def arrange(shape,labels,points,rect,PATH_FOLDER):
    #print(shape)
    l = labels 
    p = points
    r = rect
    file = widget2()
    print(file)
    print('now')
    print(points)
   
    objectmouse = RearrangeData.HelperFunctions()
    objectmouse.GetRectangleInf(r,'mouse_0',IM_PATH,PATH_FOLDER)
    print('second')
    objectmouse.GetPointsInf(labels,points,LABELS)
    print('third')
    objectmouse.FusionData(PATH_FOLDER)
    objectmouse.ConverionPandastoText(PATH_FOLDER,shape,IM_PATH)
   
    a = 1
        
@magicgui(call_button='Save Data')
def my_widget1(layer: napari.layers.Points,array:ImageData,layerShape:napari.layers.Shapes):
#def my_widget1():
       # rect = array
       shape = SHAPE_STACK
       labels = layer.properties
        
       points = layer.data
       rect = layerShape.data
       
       arrange(shape,labels,points,rect,PATH_FOLDER)
      
       return 0

@magicgui(call_button="Load old annotations")   
def widget6(layer: napari.layers.Points,layerShape:napari.layers.Shapes):
    folder_selected = QFileDialog.getExistingDirectory(None,'Select folder with label without visibility .txt files')
    if not folder_selected:
        print("No folder selected.")
        return
    box, points, labels_all = load_labels_files(folder_selected, SHAPE_STACK[0], LABELS, SHAPE_STACK, PATH_FOLDER)
    #clear existing points
    layer.data = np.array(points)
    layerShape.data = np.array(box)
    layer.properties['label'] = np.array(labels_all)
    
    print("✅ Old annotations loaded.")  
    
   
@magicgui(path={'mode': 'd'}, call_button='Run')
def widget2(path =  pathlib.Path.home()):
    print(path)
    return (path)

# @magicgui(call_button='Augment the data')
# def widget3( ):
#     print(PATH_FOLDER)
    
@magicgui(call_button='Augment the data')
def widget3( ):
    #get file with images
    filenames = natsorted(glob.glob(IM_PATH))
    for f in filenames:
       print(f)
       object_augmentation = AugmentationFunctions.AugmentationFunctions(f,PATH_FOLDER)
       
       object_augmentation.arrangeBbox()
       object_augmentation.arrangeKeypoints()
       object_augmentation.augmentation()

    
    
@magicgui(call_button='Augment images')
def widget4( ):
    #get file with images
    filenames = natsorted(glob.glob(IM_PATH))
    for f in filenames:
       object_augmentation = AugmentationFunctions.AugmentationFunctions(f,PATH_FOLDER)
       
       #object_augmentation.arrangeBbox()
       object_augmentation.augmentationImageHorizontal()
       object_augmentation.augmentationImageVertical()

'''
Script add visibility to the annotation data in keypoints

IN dim=3 visibility values are = 0 not visible
1 is partial visible
2 is visible

Steps for the script:
    1)- Read the files from the folder
    2)- for each file read the text with  f.read
    3)- split the string into a list
    4)- insert  the number 2 after the keypoints coordinates
    if the element before is nan insert 0
    5)- convert into text

'''
@magicgui(call_button='Add visibility to the labels files')
def widget5( ):
   #change the name of a folder
   # Define the current folder name and the new folder name
   current_folder_name = PATH_FOLDER + '//labels//train'
   new_folder_name = PATH_FOLDER + '//labels//train_without_vis'
  
   # Rename the folder
   os.rename(current_folder_name, new_folder_name)
   #Create a new folder
   os.mkdir(current_folder_name)
   files = glob.glob(new_folder_name + '/*.txt')
   
   for f in files:
        object_visibility = TIVIA.AddVisibility(f,current_folder_name)
        object_visibility()

# '''
# Add menu for object detection
# '''

# @magicgui(call_button='Save Data')
# def my_widget_shape(array:ImageData,layerShape:napari.layers.Shapes):
# #def my_widget1():
#        # rect = array
       
    
#        rect = layerShape.data
      
#        print(rect)
       
       
#       # arrange(shape,labels,points,rect,PATH_FOLDER)
      
#        return 0

#Load the pictures as a stack
def LoadImages(im_path):
    filenames = natsorted(glob.glob(im_path))
   # read the first file to get the shape and dtype
   # ASSUMES THAT ALL FILES SHARE THE SAME SHAPE/TYPE
    sample = imread(filenames[0])

    lazy_imread = delayed(imread)  # lazy reader
    lazy_arrays = [lazy_imread(fn) for fn in filenames]
    dask_arrays = [
    da.from_delayed(delayed_reader, shape=sample.shape, dtype=sample.dtype)
    for delayed_reader in lazy_arrays
    ]
# Stack into one large dask.array
    stack = da.stack(dask_arrays, axis=0)
    
    return stack


'''
Create a selection list
'''
def CreateListBox():
   
   app = tk.Tk()
   app.title('List box')

   
   
   def clicked():
    global LABELS
    print("clicked")
    LABELS =[]
    
    selected = box.curselection()  # returns a tuple
    for idx in selected:
        aux= box.get(idx)
        LABELS.append(aux)
        
    print(LABELS)
    

   box = tk.Listbox(app, selectmode=tk.MULTIPLE, height=10)
   #ARRANGE TO HAVE MICE AND BLIND MOLE
   if SELECTION_Animal[0] == "Mice":
      values = ['nose','ear_Left', 'ear_Right', 'shoulders', 'center', 'hips_left','hips_right', 'tail_Base', 'tail_round', 'tail_2', 'tail_End']
   # values = ['BM_snout', 'BM_lower_mouth', 'BM_ridge_top', 'BM_ridge_middle', 'BM_ridge_bottom', 
   #            'BM_head','BM_centroid', 'BM_back', 'BM_right_rear_leg_1', 'BM_right_rear_leg_2', 
   #            'BM_left_rear_leg_1', 'BM_left_rear_leg_2','BM_right_front_leg_1','BM_right_front_leg_2','BM_left_front_leg_1',
   #            'BM_left_front_leg_2','BM_above_snout','BM_Below_snout','BM_below_mouth', 
   #            'BM_behind','BM_above_behind','BM_below_behind', 'BM_low_behind']
   elif  SELECTION_Animal[0] == 'Blind moles from the side':
   # VALUES OF SIDE:
       values = ['BM_snout', 'BM_lower_mouth', 'BM_ridge_top', 'BM_ridge_middle', 'BM_ridge_bottom', 
             'BM_head','BM_centroid', 'BM_back', 'BM_right_rear_leg_1', 'BM_left_rear_leg_1',
              'BM_right_front_leg_1','BM_left_front_leg_1','BM_behind', 'BM_low_behind', 'BM_below_mouth', 'BMR_Middle']
       
   elif SELECTION_Animal[0] == 'Blind moles from the top':
   
   # VALUES OF UP:
       values =  ['BM_snout', 'BM_mouth', 'BM_ridge_top', 'BM_ridge_middle', 'BM_ridge_bottom', 'BM_head_right','BM_head_left', 'BM_right_front_leg', 'BM_left_front_leg','BM_right_rear_leg','BM_left_rear_leg','BM_behind', 'BM_right_back', 'BM_left_back', 'BM_centroid_left', 'BM_centroid_right']
   
   
   
   
   
   for val in values:
    box.insert(tk.END, val)
   box.pack()

   button = tk.Button(app, text='ADD labels', width=25, command=clicked)
   button.pack()

   exit_button = tk.Button(app, text='Close', width=25, command=app.destroy)
   exit_button.pack()

   app.mainloop()

     
'''
Create a selection list object detection or pose detection
'''
def SelectListBox():
   
   app = tk.Tk()
   app.title('List box')

   
   
   def clicked():
    global SELECTION
    print("clicked")
    SELECTION =[]
    
    selected = box.curselection()  # returns a tuple
    for idx in selected:
        aux= box.get(idx)
        SELECTION.append(aux)
        
    print(SELECTION)
    

   box = tk.Listbox(app, selectmode=tk.MULTIPLE, height=10)
   values = ['Two no similar objects detection','Pose detection','Two similar object detection']
   #values = ['Two object detection','Pose detection','Pose detection 2 objects']
   for val in values:
    box.insert(tk.END, val)
   box.pack()

   button = tk.Button(app, text='ADD labels', width=25, command=clicked)
   button.pack()

   exit_button = tk.Button(app, text='Close', width=25, command=app.destroy)
   exit_button.pack()

   app.mainloop()
   
def SelectListBoxAnimal():
 app = tk.Tk()
 app.title('List box')

 
 
 def clicked():
  global SELECTION_Animal
  print("clicked")
  SELECTION_Animal =[]
  
  selected = box.curselection()  # returns a tuple
  for idx in selected:
      aux= box.get(idx)
      SELECTION_Animal.append(aux)
      
  print(SELECTION_Animal)
  

 box = tk.Listbox(app, selectmode=tk.MULTIPLE, height=10,width = 30)
 values = ['Mice','Blind moles from the side','Blind moles from the top']
 #values = ['Two object detection','Pose detection','Pose detection 2 objects']
 for val in values:
  box.insert(tk.END, val)
 box.pack()

 button = tk.Button(app, text='ADD animals', width=25, command=clicked)
 button.pack()

 exit_button = tk.Button(app, text='Close', width=25, command=app.destroy)
 exit_button.pack()

 app.mainloop()


def main():
    global PATH_FOLDER
    
    SHAPE_STACK = ()
    #PATH_FOLDER = 'F://PoseYolo//train'
    #show message
    messagebox.showinfo("Note", "Create a folder with 2 subfolders called:\n images,labels\n create 2 other subfolders inside each one of these 2 folders:\n called: train and val ")
    PATH_FOLDER = filedialog.askdirectory(title = 'Enter the directory which includes 2 folders,images and labels \n (note: labels folder is empty)')
    
    im_path = PATH_FOLDER + '//images//train//*.png'
   
    filenames = natsorted(glob.glob(im_path))
    
    print(filenames)

   #Create a list which select the animal
    
    #Create a selection list
    SelectListBox()
    print(SELECTION)
    if SELECTION[0] == 'Pose detection':
       print('ok')
       #Create a list which select the animal
       SelectListBoxAnimal()
       #add the selection of points according to animal
       CreateListBox()

       point_annotator(im_path,PATH_FOLDER, labels = LABELS)
    # elif SELECTION[0] == 'Pose detection 2 objects':
    #    print('ok')
    #    CreateListBox()
    #    viewer = two.create_viewer(im_path,PATH_FOLDER)
    #    two.point_annotator(viewer,  'points_mouse0', 'coral', 'shape_mouse0',labels = LABELS)
    #    two.point_annotator(viewer, 'points_mouse1', 'blue', 'shape_mouse1',labels = LABELS)
       
    elif SELECTION[0] == 'Two no similar objects detection':
        SameObj = False
        
        ObjectDetection.box_annotator(im_path,PATH_FOLDER, SameObj)
    else:
        SameObj= True
        ObjectDetection.box_annotator(im_path,PATH_FOLDER, SameObj)
        
    
    

    

if __name__ == "__main__":
    main()