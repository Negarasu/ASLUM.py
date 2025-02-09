#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
def scale(x, t, t_scale):
    x_new = np.zeros(len(t_scale))
    i, j = 0, 0
    
    while i < len(x) and j < len(x_new):
        k = i
        
        while k < len(x) and t[k] < t_scale[j]:
            k += 1
        
        x_new[j] = np.nanmean(x[i:k])
        i = k + 1
        j += 1
    
    if j == len(x_new) and i < len(x):
        x_new[j] = np.nanmean(x[i:])
    
    return x_new

