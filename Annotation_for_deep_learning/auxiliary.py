import os
import pandas as pd

def load_labels_files(folder, num_frames, labels, shape_stack,Path_Folder):
    """
    Loads keypoints from YOLO-style label files without visibility.
    Falls back to default grid keypoints if files are missing.
    """
    points = []
    labels_all = []
    files_found = False
    box = []
    #Read the saved order of keypoint from test2 file
    saved_labels_order = read_labels(Path_Folder)

    for frame_idx in range(0,num_frames):
        label_file = os.path.join(folder, f"{frame_idx + 1}_image.txt")
        if os.path.exists(label_file):
            files_found = True
            with open(label_file, 'r') as f:
                coords = open_split(f)
                box = get_bounding_box(coords, shape_stack, frame_idx, box)
                points, labels_all = get_labels(coords, labels, shape_stack, frame_idx, points, labels_all, saved_labels_order)

        else:
            continue
    return box, points, labels_all

def read_labels(Path_Folder):
    df = pd.read_csv(Path_Folder + '//test2.csv')
    saved_labels = df.columns
    return saved_labels

def open_split(f):
    line = f.readline().strip()
    parts = line.split(' ')[1:]  # skip class id 
    coords = [float(p) for p in parts]

    return coords

def get_bounding_box(coords, shape_stack, frame_idx, box):
    x_cn, y_cn, wn, hn = coords[:4]
    w = wn * shape_stack[2]
    h= hn * shape_stack[1]
    x_c = x_cn * shape_stack[2]
    y_c = y_cn * shape_stack[1]
    
    
    x1 = x_c - w / 2
    x2 = x_c + w / 2
    y1 = y_c - h / 2
    y2 = y_c + h / 2

    box.append([
            [frame_idx, y1, x1],
            [frame_idx, y1, x2],
            [frame_idx, y2, x2],
            [frame_idx, y2, x1]
        ])
    
    return box
    



def get_labels(coords, labels, shape_stack, frame_idx, points, labels_all, saved_labels):
    
    for l in labels:
        #find the original labels i the saved ones
        positions = []
        for i, col in enumerate(saved_labels): 
            if  l in col:
                positions.append(i-1)
                
        x = coords[positions[0]] * shape_stack[2]  # width
        y = coords[positions[1]] * shape_stack[1]  # height
        points.append([frame_idx, y, x])
        labels_all. append(l)
    return points, labels_all
    
   