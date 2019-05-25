from pathlib import Path
import os

BASE_DIR = str(Path().absolute())

MODEL_DIR = BASE_DIR + "/trained_models"

MASK_PATH = os.path.join(MODEL_DIR, "mask_rcnn_tags_0060.h5")

CHECKPOINT_PATH = os.path.join(MODEL_DIR,'east')

#FASTER_RCNN_PATH = os.path.join(MODEL_DIR,'east')

#RETINANET_PATH = os.path.join(MODEL_DIR,'east')