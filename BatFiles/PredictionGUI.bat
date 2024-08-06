@echo off

set conda_environment=Yolo_detection
set conda_path=C:\Users\Administrator\anaconda3
call %conda_path%\Scripts\activate %conda_environment%
python "X:\Users\LabSoftware\Annotation_for_deep_learning_vs2\Objectdetection2mice\ObjectDetection\Yolo\Yolo\Main.py" 
call %conda_path%\Scripts\deactivate