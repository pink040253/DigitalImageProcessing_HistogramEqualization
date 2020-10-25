import numpy as np
import cv2

def countPixels(channel):	## pixel值計數[回傳 dict(pixel值)]
	count_pixels = dict()
	for x in range(row):
		for y in range(col):
			if channel[x, y] in count_pixels:
				count_pixels[channel[x, y]] += 1
			else:
				count_pixels[channel[x, y]] = 1
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
	# print(max_cdf, min_cdf)
	return max_cdf, min_cdf

def histogranEqualization(cdf, min, sub):	## 計算均化後的pixel值[回傳 dict(pixel均化後對照)]
	histo_equal = dict()
	for pixel in cdf:
		new_pv = round(((cdf[pixel] - min)/sub) * 255)
		histo_equal[pixel] = new_pv
	# print(histo_equal)
	return histo_equal

def changePixelValue(img, red_histo_equal, green_histo_equal, blue_histo_equal):	## 將圖像pixel值改變為均化後的結果[回傳 img]
	new_img = img
	for x in range(row):
		for y in range(col):
			new_pv = [blue_histo_equal[img[x,y,0]], green_histo_equal[img[x,y,1]], red_histo_equal[img[x,y,2]]]
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

sky = cv2.imread('sky.jpg')
row, col = sky.shape[0:2]
img = cv2.resize(sky, (int(col / 4), int(row / 4)))
row, col = img.shape[0:2]
# cv2.imshow('img', img)

red = img[:, :, 2]
green = img[:, :, 1]
blue = img[:, :, 0]


red_count = countPixels(red)
red_cdf_pixels = cdfPixels(red_count)
red_max_cdf, red_min_cdf = fundMinMaxCdf(red_cdf_pixels)
red_sub_cdf = red_max_cdf - red_min_cdf
red_histo_equal = histogranEqualization(red_cdf_pixels, red_min_cdf, red_sub_cdf)
# cv2.imshow('histo_red', histogran(red_count, red_max_cdf))
# cv2.imwrite('histo_red.png', histogran(red_count, red_max_cdf))

green_count = countPixels(green)
green_cdf_pixels = cdfPixels(green_count)
green_max_cdf, green_min_cdf = fundMinMaxCdf(green_cdf_pixels)
green_sub_cdf = green_max_cdf - green_min_cdf
green_histo_equal = histogranEqualization(green_cdf_pixels, green_min_cdf, green_sub_cdf)
# cv2.imshow('histo_green', histogran(red_count, green_max_cdf))
# cv2.imwrite('histo_green.png', histogran(red_count, green_max_cdf))

blue_count = countPixels(blue)
blue_cdf_pixels = cdfPixels(blue_count)
blue_max_cdf, blue_min_cdf = fundMinMaxCdf(blue_cdf_pixels)
blue_sub_cdf = blue_max_cdf - blue_min_cdf
blue_histo_equal = histogranEqualization(blue_cdf_pixels, blue_min_cdf, blue_sub_cdf)
# cv2.imshow('histo_blue', histogran(red_count, blue_max_cdf))
# cv2.imwrite('histo_blue.png', histogran(red_count, blue_max_cdf))

img_equal = changePixelValue(img, red_histo_equal, green_histo_equal, blue_histo_equal)
red_equal = img_equal[:, :, 2]
green_equal = img_equal[:, :, 1]
blue_equal = img_equal[:, :, 0]
red_equal_count = countPixels(red_equal)
green_equal_count = countPixels(green_equal)
blue_equal_count = countPixels(blue_equal)
cv2.imshow('histo_red', histogran(red_count, int(red_max_cdf/10)))
cv2.imwrite('histo_red.png', histogran(red_count, int(red_max_cdf/10)))
cv2.imshow('histo_blue', histogran(blue_count, int(blue_max_cdf/10)))
cv2.imwrite('histo_blue.png', histogran(blue_count, int(blue_max_cdf/10)))
cv2.imshow('histo_green', histogran(green_count, int(green_max_cdf/10)))
cv2.imwrite('histo_green.png', histogran(green_count, int(green_max_cdf/10)))
cv2.imshow('img equal', img_equal)
cv2.imwrite('equal_rgb.png', img_equal)

cv2.waitKey()
