import numpy
import scipy
import gdal
from scipy import ndimage

#im = scipy.misc.imread('bike.jpg')
file = "files/Bikesgray.jpg"
ds = gdal.Open(file)
band = ds.GetRasterBand(1)
arr = band.ReadAsArray()
im = arr
dx = ndimage.sobel(im, 0)  # horizontal derivative
dy = ndimage.sobel(im, 1)  # vertical derivative
mag = numpy.hypot(dx, dy)  # magnitude
mag *= 255.0 / numpy.max(mag)  # normalize (Q&D)
#scipy.misc.imsave('sobel.jpg', mag)

print(mag)

gdal.AllRegister()
#file = "files/me1_2337_101_1_fusion_nevinnomys_frag_nat.tif"
#ds = gdal.Open(file)
#band = ds.GetRasterBand(1)
#arr = band.ReadAsArray()
[cols, rows] = arr.shape
arr_min = arr.min()
arr_max = arr.max()
arr_mean = int(arr.mean())
arr_out = numpy.where((arr < arr_mean), 100000, arr)
driver = gdal.GetDriverByName("JPEG")

#driver =gdal.GetDriver(ds)
outdata = driver.Create('outFileName888.jpg', rows, cols, 1, gdal.GDT_Byte)
#outdata.SetGeoTransform(ds.GetGeoTransform())##sets same geotransform as input
#outdata.SetProjection(ds.GetProjection())##sets same projection as input
outdata.GetRasterBand(1).WriteArray(arr)
print(arr)
#print(arr_out)
#outdata.GetRasterBand(1).SetNoDataValue(10000)##if you want these values transparent
outdata.FlushCache() ##saves to disk!!



outdata = None
band=None
ds=None