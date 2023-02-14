import rasterio
from rasterio.plot import show
from matplotlib import pyplot as plt

img = rasterio.open(r'D:\CENS_projects\PhD\2_Դաշտային_կամերալ\2022\Planet_Trinity\2021\Trinity_01042021_psscene_analytic_8b_sr_udm2\files\20210401_075108_80_2406_3B_AnalyticMS_SR_8b_harmonized_clip.tif')

full_img = img.read()  #Note the 3 bands and shape of image
print(full_img)
num_bands = img.count
print("Number of bands in the image = ", num_bands)

img_band1 = img.read(1) #1 stands for 1st band.
img_band2 = img.read(2) #2 stands for 2nd band.
img_band3 = img.read(3) #3 stands for 3rd band.
img_band4 = img.read(4) #4 stands for 4rd band.

fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(2,2,1)
ax1.imshow(img_band1, cmap='pink')
ax2 = fig.add_subplot(2,2,2)
ax2.imshow(img_band2, cmap='pink')
ax3 = fig.add_subplot(2,2,3)
ax3.imshow(img_band3, cmap='pink')
ax3 = fig.add_subplot(2,2,4)
ax3.imshow(img_band4, cmap='pink')

# Read metadata
metadata = img.meta
print('Metadata: {metadata}\n'.format(metadata=metadata))

#Read description, if any
desc = img.descriptions
print('Raster description: {desc}\n'.format(desc=desc))

#To find out geo transform
print("Geotransform : ", img.transform)

#To find out the coordinate reference system
print("Coordinate reference system: ", img.crs)

################# NDVI - normalized difference vegetation index ############
# NDVI = (NIR-Red)/(NIR+Red)

#Let us assume 1 is red and 2 is NIR
red_clipped = full_img[2].astype('f4')
nir_clipped = full_img[3].astype('f4')
ndvi_clipped = (nir_clipped - red_clipped) / (nir_clipped + red_clipped)

# Return Runtime warning about dividing by zero as we have some pixels with value 0.
# So let us use numpy to do this math and replace inf / nan with some value.

import numpy as np
ndvi_clipped2 = np.divide(np.subtract(nir_clipped, red_clipped), np.add(nir_clipped, red_clipped))
ndvi_clipped3 = np.nan_to_num(ndvi_clipped2, nan=-1)
plt.imshow(ndvi_clipped3, cmap='viridis')
plt.colorbar()
#Some times each band is available as seperate images
#Data from here: https://landsatonaws.com/L8/042/034/LC08_L1TP_042034_20180619_20180703_01_T1
#Band 3 = Red, Band 4: NIR
print(ndvi_clipped3)

ndvi = rasterio.open('ndvi2.tif','w', height=img.height,width=img.width,count=1,dtype = ndvi_clipped.dtype, crs = img.crs, transform=img.transform)

ndvi.write(ndvi_clipped3,1)

ndvi.close()