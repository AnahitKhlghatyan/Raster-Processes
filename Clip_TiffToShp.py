# File/folder names (changable)
# shp = 'C:/Users/Aza/Desktop/M/sevan_area.shp'    #shapefile for cliping raster/path
# folder = 'C:/Users/Aza/Desktop/M'            #Folder to iterate through/path
# new_folder = 'Chl_clip'   #New folder to save cliped files/path
# rast_clip = rast + '_clip'  #Names of clipped rasters
# excel = 'xlsx' #Name of the excel file for pixel values/write new name
# stat = 'xlsx_2' #Name of the excel file for statistics/write new name

# import libraries
import rasterio
import rasterio.mask
from rasterio.plot import show
import numpy as np
import pandas as pd
import geopandas as gpd
import fiona
import subprocess
from matplotlib import pyplot
import os

# Read shapefile
with fiona.open(r'D:\CENS_projects\ML for GEO\Botanical\Thermal.shp', "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]


# read and clip raster
with rasterio.open(r'D:\CENS_projects\ML for GEO\Botanical\BG_october_raw_3.tif') as src:
    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
    out_meta = src.meta

out_meta.update({"driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform})

with rasterio.open(r'D:\CENS_projects\ML for GEO\Botanical\BG_october_raw_3_clip.tif', "w", **out_meta) as dest:
    dest.write(out_image)


# show raster



# Create excel file from raster
arr = pd.DataFrame(out_image[0])
# arr.to_excel('Chl_20.07.2018.xlsx')
for i in arr:
    for j in arr[i]:
        if j == 127:
            arr[i] = arr[i].replace(127, None)

ar = (pd.Series(arr.values.ravel('F'))).dropna().reset_index().drop('index', axis=1)
# ar.to_excel('Chl_20.07.2018.xlsx')
print(ar)
print(ar.min())
# Statistics



