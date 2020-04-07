import cv2
import gdal
import numpy as np

path = None


def sobel_x(img, kernel_size=3):
    x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=kernel_size)
    # save_sobel_geotiff(path + 'x.tiff', x)
    return x


def sobel_y(img, kernel_size=3):
    y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=kernel_size)
    # save_sobel_geotiff(path + 'y.tiff', y)
    return y


def sobel_xy(sobelx, sobely):
    try:
        # grad = cv2.addWeighted(np.absolute(sobelx), 0.5, np.absolute(sobely), 0.5, 0)

        abs_grad_x = cv2.convertScaleAbs(sobelx)
        abs_grad_y = cv2.convertScaleAbs(sobely)
        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    except:
        return None
    # grad = sobelx + 1j * sobely  # with complex value
    # save_sobel_geotiff(path + 'xy.tiff', grad)
    return grad


def sobel_all(img, kernel_size=3):
    sobelx = sobel_x(img, kernel_size)
    sobely = sobel_y(img, kernel_size)
    return sobelx, sobely, sobel_xy(sobelx, sobely)


def save_sobel_geotiff(name, sobel):
    arr = sobel
    [cols, rows] = arr.shape
    driver = gdal.GetDriverByName("GTiff")
    outdata = driver.Create(name, rows, cols, 1, gdal.GDT_Byte)
    outdata.GetRasterBand(1).WriteArray(arr)
    outdata.FlushCache()


def auto_create_all(img, savepath, kernel_size=3):
    x, y, xy = sobel_all(img, kernel_size)
    save_sobel_geotiff(savepath + 'x.tif', x)
    save_sobel_geotiff(savepath + 'y.tif', y)
    x = None
    y = None
    if (xy is not None):
        save_sobel_geotiff(savepath + 'xy.tif', xy)
        xy = None
        xy = sobel_xy(sobel_x(img, -1), sobel_y(img, -1))
        save_sobel_geotiff(savepath + 'xy_schar.tif', xy)
        xy = None
    else:
        save_sobel_geotiff(savepath + 'xy.tif', y)
        # save_sobel_geotiff(savepath + 'xy_schar.tif', schar[1])
    # save_sobel_geotiff(savepath + 'default.tif', img)
