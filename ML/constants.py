import os

"""
This file should contain all project constants
"""

PATH_PREFIX = os.path.dirname(os.path.abspath(__file__))

MODELS_PATH = os.path.join(PATH_PREFIX, "ready_models")

DATASET_PATH = os.path.join(PATH_PREFIX, "datasets", "dataset_v1.csv")