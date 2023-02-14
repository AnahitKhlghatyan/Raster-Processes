# User inputs
path = r'C:\Users\Aza\Desktop\M'

# import libraries
import rasterio
import rasterio.mask
import numpy as np
import pandas as pd
import geopandas as gpd
import fiona
import subprocess
import os


# read raster
lst = []
name_lst = []
for path, dirc, files in os.walk(path):
    for name in files:
        if name.endswith('.tif'):
            fname = os.path.join(path, name)
            name0 = name.split('_')
            name_eol = name0[0][4:6] + '/' + name0[0][6:8] + '/' + name0[0][0:4]
            name_lst.append(name_eol)
            with rasterio.open(fname) as src:
                array = src.read(1)
                lst.append(array)
print(lst)

# Convert to excel
ar_lst = []
for i in lst:
    arr = pd.DataFrame(i)
    arr = arr.values.ravel('F')
    arr = pd.DataFrame(arr)
    arr = arr.loc[~(arr[0] ==-9999.0)].reset_index().drop('index', axis=1)
    ar_lst.append(arr)

df = pd.DataFrame()
for i in range(len(ar_lst)):
    df['{}'.format(name_lst[i])] = ar_lst[i]
df = df.T
print(df)
# df.to_excel(r'D:\CENS_projects\PhD\2_Դաշտային_կամերալ\2022\Planet_Trinity\NDVI\2021\2021_pixel_NDVI.xlsx')