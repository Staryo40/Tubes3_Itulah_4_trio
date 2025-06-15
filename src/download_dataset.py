import kagglehub
import shutil
import os

path = kagglehub.dataset_download("snehaanbhawal/resume-dataset")
target_path = os.path.join(os.getcwd(), "data")
shutil.copytree(path, target_path, dirs_exist_ok=True)

print("Dataset moved to:", target_path)
