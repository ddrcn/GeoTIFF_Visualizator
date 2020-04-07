import cv2
import gdal
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('land_shallow_topo_8192.tif', 0)

laplacian = cv2.Laplacian(img, cv2.CV_64F)
sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=27)
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=27)

abs_grad_x = cv2.convertScaleAbs(sobelx)
abs_grad_y = cv2.convertScaleAbs(sobely)

grad2 = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)


## Combine the two gradients
# only the magnitude
#grad = cv2.addWeighted(np.absolute(sobelx), 0.5, np.absolute(sobely), 0.5, 0)
#grad = np.stack([sobelx, sobely], axis=2)  # dx, dy stacked
#grad = sobelx + 1j * sobely  # with complex value

# grad = sobelx + 1j*sobely # with complex value
#print(grad)
cv2.imwrite('sobelCV.jpg', sobelx)

arr = grad2
[cols, rows] = arr.shape
arr_min = arr.min()
arr_max = arr.max()
driver = gdal.GetDriverByName("GTiff")
outdata = driver.Create('outFileName2012.tif', rows, cols, 1, gdal.GDT_Byte)
outdata.GetRasterBand(1).WriteArray(arr)
#print(sobely)
#print(grad)
# print(arr_out)
# outdata.GetRasterBand(1).SetNoDataValue(10000)##if you want these values transparent
outdata.FlushCache()  ##saves to disk!!

# plt.subplot(2, 2, 1), plt.imshow(img, cmap='gray')
# plt.title('Original'), plt.xticks([]), plt.yticks([])
# #plt.subplot(2, 2, 2), plt.imshow(grad, cmap='gray')
# plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
# plt.subplot(2, 2, 3), plt.imshow(sobelx, cmap='gray')
# plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
# plt.subplot(2, 2, 4), plt.imshow(sobely, cmap='gray')
# plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

plt.show()
