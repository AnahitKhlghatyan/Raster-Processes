#User input
path = r'D:\CENS_projects\PhD\2_Դաշտային_կամերալ\2022\Planet_Trinity\2017'

# Import Libraries
import rasterio
import numpy as np
import os
import pandas as pd

#Sample image for metadata
img = rasterio.open(r'D:\CENS_projects\PhD\2_Դաշտային_կամերալ\2022\Planet_Trinity\2016\Trinity_05102016_psscene_analytic_sr_udm2\files\20161005_065749_0e2f_3B_AnalyticMS_SR_harmonized_clip.tif')

# Define the year
year = path[60:65]

# Reading and collecting rasters
lst4 = []
name_lst4 = []

lst8 = []
name_lst8 = []

for path, dirc, files in os.walk(path):
    for name in files:
        if name.endswith('harmonized_clip.tif'):
            fname = os.path.join(path, name)
            with rasterio.open(fname) as src:
                leng = len(src.descriptions)
                if leng == 4:
                    array4 = src.read()
                    lst4.append(array4)
                    name0 = name.split('_')
                    name_eol = name0[0][0:4] + '-' + name0[0][4:6] + '-' + name0[0][6:8]
                    name_lst4.append(name_eol)
                else:
                    array8 = src.read()
                    lst8.append(array8)
                    name0 = name.split('_')
                    name_eol = name0[0][0:4] + '-' + name0[0][4:6] + '-' + name0[0][6:8]
                    name_lst8.append(name_eol)
print(name_lst4)
print(name_lst8)

# NDVI and GNDVI calculation
# NDVI = (NIR – red) / (NIR + red)
# GNDVI = (NIR - GREEN) /(NDVI + GREEN)
ndvi_lst4 = []
gndvi_lst4 = []
for i in range(len(lst4)):
    green = lst4[i][1].astype('f4')
    red = lst4[i][2].astype('f4')
    nir = lst4[i][3].astype('f4')

    ndvi2 = np.divide(np.subtract(nir, red), np.add(nir, red))
    gndvi2 = np.divide(np.subtract(nir, green), np.add(ndvi2, green))

    ndvi3 = np.nan_to_num(ndvi2, nan=-1)
    gndvi3 = np.nan_to_num(gndvi2, nan=-1)

    ndvi_lst4.append(ndvi3)
    gndvi_lst4.append(gndvi3)


ndvi_lst8 = []
gndvi_lst8 = []
for i in range(len(lst8)):
    green = lst8[i][3].astype('f4')
    red = lst8[i][5].astype('f4')
    nir = lst8[i][7].astype('f4')

    ndvi2 = np.divide(np.subtract(nir, red), np.add(nir, red))
    gndvi2 = np.divide(np.subtract(nir, green), np.add(ndvi2, green))

    ndvi3 = np.nan_to_num(ndvi2, nan=-1)
    gndvi3 = np.nan_to_num(gndvi2, nan=-1)

    ndvi_lst8.append(ndvi3)
    gndvi_lst8.append(gndvi3)


# Saving NDVI and GNDVI images
# for i, j in zip(ndvi_lst4, name_lst4):
#     ndvi = rasterio.open(r'D:\CENS_projects\PhD\2_Դաշտային_կամերալ\2022\Planet_Trinity\NDVI\ndvi_{}.tif'.format(j), 'w', height=img.height, width=img.width, count=1, dtype=i.dtype, crs=img.crs, transform=img.transform)
#     ndvi.write(i, 1)
#     ndvi.close()
#
# for i, j in zip(gndvi_lst4, name_lst4):
#     gndvi = rasterio.open(r'D:\CENS_projects\PhD\2_Դաշտային_կամերալ\2022\Planet_Trinity\GNDVI\gndvi_{}.tif'.format(j), 'w', height=img.height, width=img.width, count=1, dtype=i.dtype, crs=img.crs, transform=img.transform)
#     gndvi.write(i, 1)
#     gndvi.close()
#
# for i, j in zip(ndvi_lst8, name_lst8):
#     ndvi = rasterio.open(r'D:\CENS_projects\PhD\2_Դաշտային_կամերալ\2022\Planet_Trinity\NDVI\ndvi_{}.tif'.format(j), 'w', height=img.height, width=img.width, count=1, dtype=i.dtype, crs=img.crs, transform=img.transform)
#     ndvi.write(i, 1)
#     ndvi.close()
#
# for i, j in zip(gndvi_lst8, name_lst8):
#     gndvi = rasterio.open(r'D:\CENS_projects\PhD\2_Դաշտային_կամերալ\2022\Planet_Trinity\GNDVI\gndvi_{}.tif'.format(j), 'w', height=img.height, width=img.width, count=1, dtype=i.dtype, crs=img.crs, transform=img.transform)
#     gndvi.write(i, 1)
#     gndvi.close()


# Creating pixel-wise excel file
# NDVI
ar_lst4 = []
for i in ndvi_lst4:
    arr = pd.DataFrame(i)
    arr = arr.values.ravel('F')
    arr = pd.DataFrame(arr)
    arr = arr.loc[~(arr[0] ==-1)].reset_index().drop('index', axis=1)
    ar_lst4.append(arr)

ar_lst8 = []
for i in ndvi_lst8:
    arr = pd.DataFrame(i)
    arr = arr.values.ravel('F')
    arr = pd.DataFrame(arr)
    arr = arr.loc[~(arr[0] ==-1)].reset_index().drop('index', axis=1)
    ar_lst8.append(arr)

df4 = pd.DataFrame()
for i in range(len(ar_lst4)):
    df4['{}'.format(name_lst4[i])] = ar_lst4[i]
df4 = df4.T

df8 = pd.DataFrame()
for i in range(len(ar_lst8)):
    df8['{}'.format(name_lst8[i])] = ar_lst8[i]
df8 = df8.T

frames = [df4,df8]
df_nd = pd.concat(frames)
df_nd = df_nd.T

# df_nd.to_csv(r'D:\CENS_projects\PhD\2_Դաշտային_կամերալ\2022\Planet_Trinity\NDVI\NDVI_pixelvalues_{}.csv'.format(year))


# GNDVI
ar_lst14 = []
for i in gndvi_lst4:
    arr = pd.DataFrame(i)
    arr = arr.values.ravel('F')
    arr = pd.DataFrame(arr)
    arr = arr.loc[~(arr[0] ==-9999.0)].reset_index().drop('index', axis=1)
    ar_lst14.append(arr)

ar_lst18 = []
for i in gndvi_lst8:
    arr = pd.DataFrame(i)
    arr = arr.values.ravel('F')
    arr = pd.DataFrame(arr)
    arr = arr.loc[~(arr[0] ==-9999.0)].reset_index().drop('index', axis=1)
    ar_lst18.append(arr)

df14 = pd.DataFrame()
for i in range(len(ar_lst14)):
    df14['{}'.format(name_lst4[i])] = ar_lst14[i]
df14 = df14.T

df18 = pd.DataFrame()
for i in range(len(ar_lst18)):
    df18['{}'.format(name_lst8[i])] = ar_lst18[i]
df18 = df18.T

frames = [df14,df18]
df_gnd = pd.concat(frames)
df_gnd = df_gnd.T


# df_gnd.to_csv(r'D:\CENS_projects\PhD\2_Դաշտային_կամերալ\2022\Planet_Trinity\GNDVI\GNDVI_pixelvalues_{}.csv'.format(year))

