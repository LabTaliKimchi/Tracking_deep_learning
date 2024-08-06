@echo off

set conda_environment=napari-env
set conda_path=C:\Users\Administrator\anaconda3
call %conda_path%\Scripts\activate %conda_environment%
python "X:\Users\LabSoftware\Annotation_for_deep_learning_vs2\Annotation_for_deep_learning\annotation.py" 
pause
call %conda_path%\Scripts\deactivate