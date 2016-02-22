import numpy as np

import itertools
import time


# permutations of (-1, 0, 1) in three/two dimensional tuple format
# representing 8 and 26 increments around a pixel at origin (0, 0, 0)
stepDirect = itertools.product((-1, 0, 1), repeat=3)
listStepDirect = list(stepDirect)


def adaptive3dOtsuThresh(image, maxVal, threshold_otsu):
    """ local otsu thresholding of 3D volume kernel size 3 x 3 x 3
        involves a long run time
    """
    st = time.time()
    assert len(image.shape) == 3
    padImage = np.lib.pad(image, 1, 'edge')
    listed = list(set(map(tuple, np.transpose(np.where(padImage != maxVal)))))
    newImage = np.zeros_like(image)
    d = {item: threshold_otsu(np.array([image[tuple(np.array(item) + np.array(increments))] for increments in listStepDirect])) for item in listed}
    for item in listed:
        newImage[item] = d[item]
    print("time taken is", time.time() - st)
    return newImage


def adaptiveThreshold(image, method, kernelSize=3):
    """ adaptive thresholding , method can be mean,
    gaussian and median
    """
    from scipy.ndimage.filters import convolve1d, gaussian_filter, median_filter
    assert len(image.shape) == 3
    result = np.zeros(image.shape, 'double')
    if method == "mean":
        kernel = 1. / kernelSize * np.ones((kernelSize, ))
        convolve1d(image, kernel, axis=0, output=result)
        convolve1d(result, kernel, axis=0, output=result)
        convolve1d(result, kernel, axis=0, output=result)
    elif method == 'gaussian':
        sigma = (kernelSize - 1) / 6
        gaussian_filter(image, sigma, output=result)
    elif method == 'median':
        median_filter(image, kernelSize, output=result)
    return image > result