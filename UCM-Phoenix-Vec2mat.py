#!/usr/bin/env python
# coding: utf-8

# In[2]:

from UCM-Phoenix-Vec2mat import vec2mat
import numpy as np

def vec2mat(vec, matCol, padding=None):
    # Check number of inputs
    if len(vec.shape) > 2:
        raise ValueError('VEC cannot be an ND array.')
    elif not isinstance(matCol, int) or matCol < 1:
        raise ValueError('MATCOL must be a positive integer.')

    # Get dimensions of vector
    vecRow, vecCol = vec.shape
    vecLen = vecRow * vecCol

    # Handle case where vector already has desired number of columns
    if vecCol == matCol:
        mat = vec
        padded = 0
        return mat, padded  # nothing to do

    # If the vector has more than one row, reshape it to a row vector
    if vecRow > 1:
        vec = np.reshape(vec.T, (1, vecLen))

    # Handle padding
    if padding is None:
        padding = np.zeros_like(vec, dtype=vec.dtype)  # default padding
    else:
        padding = np.asarray(padding).reshape(1, -1).astype(vec.dtype)
    
    paddingLen = len(padding)
    matRow = int(np.ceil(vecLen / matCol))
    padded = matRow * matCol - vecLen  # number of elements to be padded
    
    pad_elements = min(padded, paddingLen)
    padded_vec = np.concatenate((vec, padding[:, :pad_elements],
                                  np.tile(padding[:, -1], (1, padded - paddingLen))),
                                axis=1)
    mat = np.reshape(padded_vec, (matRow, matCol)).T
    
    return mat, padded

