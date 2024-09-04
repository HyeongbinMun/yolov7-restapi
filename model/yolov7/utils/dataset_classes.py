COCO_CLASSES_LIST = [
    'person',
    'bicycle',
    'car',
    'motorbike',
    'aeroplane',
    'bus',
    'train',
    'truck',
    'boat',
    'traffic light',
    'fire hydrant',
    'stop sign',
    'parking meter',
    'bench',
    'bird',
    'cat',
    'dog',
    'horse',
    'sheep',
    'cow',
    'elephant',
    'bear',
    'zebra',
    'giraffe',
    'backpack',
    'umbrella',
    'handbag',
    'tie',
    'suitcase',
    'frisbee',
    'skis',
    'snowboard',
    'sports ball',
    'kite',
    'baseball bat',
    'baseball glove',
    'skateboard',
    'surfboard',
    'tennis racket',
    'bottle',
    'wine glass',
    'cup',
    'fork',
    'knife',
    'spoon',
    'bowl',
    'banana',
    'apple',
    'sandwich',
    'orange',
    'broccoli',
    'carrot',
    'hot dog',
    'pizza',
    'donut',
    'cake',
    'chair',
    'sofa',
    'pottedplant',
    'bed',
    'diningtable',
    'toilet',
    'tvmonitor',
    'laptop',
    'mouse',
    'remote',
    'keyboard',
    'cell phone',
    'microwave',
    'oven',
    'toaster',
    'sink',
    'refrigerator',
    'book',
    'clock',
    'vase',
    'scissors',
    'teddy bear',
    'hair drier',
    'toothbrush',
]

OBSTACLE_15 = [
    "person",
    "bicycle",
    "bus",
    "car",
    "carrier",
    "motorcycle",
    "movable_signage",
    "truck",
    "bollard",
    "chair",
    "potted_plant",
    "table",
    "tree_trunk	",
    "pole",
    "fire_hydrant",
]

OBSTACLE_PERSON = [
    'person'
]

DISPLAY_FAULT = [
    "fault"
]

OBJECT_DATASET_CLASSES = {
    "coco": COCO_CLASSES_LIST,
    "obstacle-15": OBSTACLE_15,
    "display_fault": DISPLAY_FAULT,
}

def get_cls_dict(category_num):
    """Get the class ID to name translation dictionary."""
    if category_num == 80:
        return {i: n for i, n in enumerate(COCO_CLASSES_LIST)}
    elif category_num == 15: # obstacle
        return {i: n for i, n in enumerate(OBSTACLE_15)}
    elif category_num == 'obstacle_person':
        return {i: n for i, n in enumerate(OBSTACLE_PERSON)}
    elif category_num == 1:
        return {i: n for i, n in enumerate(DISPLAY_FAULT)}
    else:
        return {i: 'CLS%d' % i for i in range(category_num)}

def get_class(dataset_name):
    dataset_class = OBJECT_DATASET_CLASSES[dataset_name]
    return {i: n for i, n in enumerate(dataset_class)}, dataset_class
