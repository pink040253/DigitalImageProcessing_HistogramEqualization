import numpy as np
import cv2

def countPixels(img):	## pixel值計數[回傳 dict(pixel值)]
	count_pixels = dict()
	sumofPixel = 0
	for x in range(row):
		for y in range(col):
			sumofPixel += 1
			if img[x, y] in count_pixels:
				count_pixels[img[x, y]] += 1
			else:
				count_pixels[img[x, y]] = 1
	return count_pixels

def cdfPixels(pixels):	## 將pixel值排序並計算其累積分布函數(cdf)[回傳 dict(cdf)]
	cdf = dict()
	pixelsum = 0
	for label in sorted(pixels.keys()):
		pixelsum += pixels[label]
		cdf[label] = pixelsum
	# print(cdf)
	return cdf

def fundMinMaxCdf(cdf_pixels):	## 尋找累積分布函數(cdf)中的最大最小值[回傳 int(max), int(min)]
	for label in cdf_pixels:
		min_cdf = max_cdf = cdf_pixels[label]
		break
	for label in cdf_pixels:
		if cdf_pixels[label] < min_cdf:
			min_cdf = cdf_pixels[label]
		if cdf_pixels[label] > max_cdf:
			max_cdf = cdf_pixels[label]
	return max_cdf, min_cdf

def histogranEqualization(cdf, min, sub):	## 計算均化後的pixel值[回傳 dict(pixel均化後對照)]
	histo_equal = dict()
	for pixel in cdf:
		new_pv = round(((cdf[pixel] - min)/sub) * 255)
		histo_equal[pixel] = new_pv
	# print(histo_equal)
	return histo_equal

def changePixelValue(img, histo_equal):	## 將圖像pixel值改變為均化後的結果[回傳 img]
	new_img = img
	for x in range(row):
		for y in range(col):
			new_pv = histo_equal[img[x,y]]
			img[x,y] = new_pv
	return new_img

def histogran(pixels, max_cdf):	## 印出直方圖
	histo_img = np.zeros([512, 512, 3], dtype='uint8')
	for i in range(0, 256):
		if i in pixels:
			cv2.rectangle(histo_img, (2*i, (512-int(pixels[i]/max_cdf*512))) ,((2*i+1), 512), (255, 255, 255), -1)
			# print(i, pixels[i], int(pixels[i]/max_cdf*100))
		else:
			cv2.rectangle(histo_img, (2*i, 512) ,((2*i+1), 512), (255, 255, 255), -1)
	return histo_img

sunset = cv2.imread('sunset.jpg', 0)
row, col = sunset.shape[0:2]
img = cv2.resize(sunset, (int(col / 5), int(row / 5)))
row, col = img.shape[0:2]
cv2.imshow('img', img)

pixels = countPixels(img)
cdf_pixels = cdfPixels(pixels)
max_cdf, min_cdf = fundMinMaxCdf(cdf_pixels)
sub_cdf = max_cdf - min_cdf
histo_equal = histogranEqualization(cdf_pixels, min_cdf, sub_cdf)
cv2.imshow('img equal', changePixelValue(img, histo_equal))
cv2.imwrite('equal_gray.png', changePixelValue(img, histo_equal))
cv2.imshow('histo_gray', histogran(pixels, int(max_cdf/10)))
cv2.imwrite('histo_gray.png', histogran(pixels, int(max_cdf/10)))

cv2.waitKey()