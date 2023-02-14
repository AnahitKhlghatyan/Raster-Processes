# User inputs
path = r'C:\Users\Aza\Desktop\M'
filename = r'CHL_eo-sevan_EOMAP_20200203_065537_SENT3_m0300_32bit'

# Name
name = filename.split('_')
name_eol = name[3][0:4]+'-'+name[3][4:6]+'-'+name[3][6:8]
print(name_eol)

# Nothing needs to be changed from here
# import libraries
import rasterio.mask
import pandas as pd
import matplotlib.pyplot as plt


# read raster
with rasterio.open(path+'/'+filename+'.tif') as src:
    array = src.read(1)

# show raster
plt.imshow(array, cmap='Spectral')
plt.show()


# Create excel file from raster
arr = pd.DataFrame(array)
for i in arr:
    for j in arr[i]:
        if j == -9999.0:
            arr[i] = arr[i].replace(-9999.0, None)

ar = (pd.Series(arr.values.ravel('F'))).dropna().reset_index().drop('index', axis=1)
ar.to_excel('{}_pixelwise.xlsx'.format(path+'/'+name_eol))

print(ar)

# Statistics



