import os
from pathlib import Path


def get_full_path_file_name(project_path_str: str):
    BASE_DIR = Path(__file__).resolve().parent.parent
    full_path_file_name = os.path.join(BASE_DIR, project_path_str)
    full_path_file_name = os.path.normpath(full_path_file_name)
    return full_path_file_name
