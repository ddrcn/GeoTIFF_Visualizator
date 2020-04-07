import os

import cv2

import SobelCV

file = "files/Bikesgray.tiff"
file = "files/me1_2337_101_1_fusion_nevinnomys_frag_nat.tif"
img = cv2.imread(file, 0)
x, y, xy = SobelCV.sobel_all(img,-1)
SobelCV.save_sobel_geotiff('output/x.tif', x)
SobelCV.save_sobel_geotiff('output/y.tif', y)
SobelCV.save_sobel_geotiff('output/xy.tif', xy)




# file = "files/me1_2337_101_1_fusion_nevinnomys_frag_nat.tif"
# ds = gdal.Open(file)
# band = ds.GetRasterBand(1)
# arr = band.ReadAsArray()
# [cols, rows] = arr.shape
# arr_min = arr.min()
# arr_max = arr.max()
# arr_mean = int(arr.mean())
# arr_out = numpy.where((arr < arr_mean), 10000, arr)
# driver = gdal.GetDriverByName("GTiff")
# outdata = driver.Create('outFileName.tif', rows, cols, 1, gdal.GDT_UInt16)
# outdata.SetGeoTransform(ds.GetGeoTransform())##sets same geotransform as input
# outdata.SetProjection(ds.GetProjection())##sets same projection as input
# outdata.GetRasterBand(1).WriteArray(arr_out)
# outdata.GetRasterBand(1).SetNoDataValue(10000)##if you want these values transparent
# outdata.FlushCache() ##saves to disk!!
# outdata = None
# band=None
# ds=None
