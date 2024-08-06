@echo off

set conda_environment=GeneralSoftwares
set conda_path=C:\Users\Administrator\anaconda3
call %conda_path%\Scripts\activate %conda_environment%
python "X:\Users\LabSoftware\Annotation_for_deep_learning_vs2\CombineVideoWithLearningDataVs2\CombineVideoWithLearningData\Initial.py" 
call %conda_path%\Scripts\deactivate