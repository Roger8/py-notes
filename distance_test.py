
import numpy as np
from math import pi,sin,cos,atan2,sqrt
from typing import Tuple, Union, Optional

def haversine(lon1, lat1, lon2, lat2, R=6371):
    """
    参数：经度1(度), 纬度1(度), 经度2(度), 纬度2(度), 地球半径(km)
    返回：千米为单位的距离
    """
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    return 2 * R * np.arcsin(np.sqrt(a))

def toRadian(v):
    return v/180.0*pi

def caldist(lat1,lon1,lat2,lon2,r=1):
    lat1 = toRadian(lat1)
    lon1 = toRadian(lon1)
    lat2 = toRadian(lat2)
    lon2 = toRadian(lon2)
    print(lat1,lon1,lat2,lon2)
    
    a = sin((lat2-lat1)/2)**2 + cos(lat1) * cos(lat2) * sin((lon2-lon1)/2)**2;
    #% Ensure that a falls in the closed interval [0 1].
    #a(a < 0) = 0;
    #a(a > 1) = 1;
    print("a：",a)
    print("atan2 : ",(sqrt(a), sqrt(1-a))) #/180*pi)
    print("atan2 : ",atan2(sqrt(a), sqrt(1-a))) #/180*pi)
    rng = r * 2 * atan2(sqrt(a),sqrt(1 - a));
    # to degree
    deg = rng/pi*180.0
    
    return deg

#d = caldist(29.6254,106.5314,29.5863,  106.5425)
#d = caldist(29.625,106.531,29.542,106.465)
#d = caldist(29.625413,106.531360,29.526418,106.501372)
#d = caldist(29.625413,106.531360,29.568999,106.448284)
d = caldist(29.625413,106.531360,29.542092,106.465756)
print(d)

def stable_sort(array: np.ndarray,
               axis: Optional[int] = None,
               direction: str = 'ascend') -> Tuple[np.ndarray, np.ndarray]:
    """
    Implements MATLAB-like stable sort where equal elements preserve their order
    and indices for equal elements are ascending

    Args:
        array: Input array to sort
        axis: Axis along which to sort (None for 1D)
        direction: 'ascend' or 'descend'

    Returns:
        sorted_array: The sorted array
        indices: The indices that would sort the array
    """
    # Handle 1D array case
    if axis is None:
        # Create array of indices for stable sort
        idx = np.arange(len(array))

        # Create structured array with values and original indices
        dtype = [('value', array.dtype), ('index', int)]
        pairs = np.array(list(zip(array, idx)), dtype=dtype)

        # Perform stable sort
        if direction == 'descend':
            sorted_indices = np.argsort(pairs, order=['value', 'index'], kind='stable')[::-1]
        else:
            sorted_indices = np.argsort(pairs, order=['value', 'index'], kind='stable')

        return array[sorted_indices], sorted_indices

    # Handle multi-dimensional array case
    else:
        if direction == 'descend':
            indices = np.argsort(-array, axis=axis, kind='stable')
        else:
            indices = np.argsort(array, axis=axis, kind='stable')
        sorted_array = np.take_along_axis(array, indices, axis=axis)
        return sorted_array, indices

def sort_test():
    rank = np.array([15.,  7., 13.,  7., 10., 11., 10., 11.,  2.,  8., 10.,  5.,  7.,
       13.,  8.,  5.,  1.,  6.,  5.,  8.,  2., 12.,  6.,  1., 11.,  8.,
        6., 12., 12., 14.,  6., 15.,  5.,  4.,  2.,  7.,  4., 13., 11.,
        7., 10.,  4.,  6., 10., 14., 14.,  5., 11., 15., 14.,  1.,  3.,
       11.,  3.,  9.,  7., 11.,  7.,  3.,  6.,  3.,  6., 10., 14.,  4.,
        6.,  9., 15.,  9., 13., 12.,  6., 13.,  4., 12.,  5., 12.,  4.,
        9., 14.,  8.,  7.,  6., 13., 12.,  1.,  2., 10.,  5., 10.,  5.,
        6., 11.,  5.,  2.,  9.,  8.,  7.,  4.,  3.])
    

    rank = np.array([np.inf    ,1.5033    ,1.4294     ,  np.inf])
    [x,indx]=stable_sort(rank,direction="descend")
    print(x,indx)
    [x,indx]=stable_sort(-rank,direction="ascend")
    print(x,indx)
    [x,indx]=stable_sort(rank,axis=0,direction="descend")
    print(x,indx)


sort_test()
