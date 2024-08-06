-Open anaconda prompt
-change directory to : "X:\Users\LabSoftware\Annotation_for_deep_learning_vs2\envs"
- conda env create -f environment_napari_1.yml- failed pip
- conda env create -f environment_GeneralSoftwares.yml
- conda env create -f environment_YOLO.yml- failed the pip

In addition add:
in napari-env in anaconda prompt
-pip install napari
-pip install dask-image
-pip install albumentations
in Yolo_detection in anaconda prompt
important install cuda 11.8 and cudnn 8.2.0
-pip install opencv-python

-pip install openpyxl

conda install -c conda-forge ultralytics
conda install -c pytorch -c nvidia -c conda-forge pytorch torchvision pytorch-cuda=11.8 ultralytics

Chech that the env are in the folder where anaconda was saved as:
C:\Users\Administrator\anaconda3\envs

-Activation from 
X:\Users\LabSoftware\Annotation_for_deep_learning_vs2\BatFiles\MainGUI



Notes:

#create new environment
conda create -y -n napari-env -c conda-forge python=3.10

conda activate napari-env

python -m pip install "napari[all]"





pip install albumentations[pydantic]==1.1.0 (pydantic version is 2.7.0)
