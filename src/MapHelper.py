from PIL import Image
import numpy as np


def array_to_bw_bitmap(array, path):
    array = np.array(array, np.uint8)
    result = Image.frombuffer('L', (array.shape[0], array.shape[1]), array, 'raw', 'L', 0, 1)
    result.save(path)
