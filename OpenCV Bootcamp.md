[Collabs](https://drive.google.com/drive/folders/12jJ1OPVHqS1XRTD_N4a-wBYBZrm09rC_?usp=share_link)
[[Reconstrucción 3D de raíces]]

---
# Displaying images
To display images correctly in a notebook:
```Python
%matplotlib inline
from IPython.display import Image
```
Image allows us to display the images to their actual size and not as a plot.
```Python
Image(filename="image.jpg")
```

You can display images with matplot lib but it isn't going to be a faithful representation of the size, it will just be a mathematical plot. You need to specify the colormap also, for it to be displayed correctly.
```Python
plt.imshow(img,cmap='gray')
```

OpenCV also has an `imshow` function.
```Python
window1 = cv2.namedWinfow("w1")
cv2.imshow(window1, img)
```
We need to specify a waitkey for the duration of the window if we don't want the image to be displayed indefinetly.
```Python
cv2.waitKey(8000)
cv2.destroyWindow(window1)
```
This code will wait 8 seconds until destroying the window. Of we pass 0 to the waitkey function it will be displayed util it gets input from the user.
# Reading Images openCV
```Python
img= cv2.imread(filename, [flags])
```
If the image is successfully loaded it will be saved in the img variable, if not img will have a value of `None`. 
The flags are used to read the image in a particular format, like grayscale or color. The default is color images.

The function returns a 2D numpy array, where each pixel value is 8 bits.

If the filename already exists it will be overwritten.
## Documentation
1. **`Imread`**:  [Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F4.5.1%2Fd4%2Fda8%2Fgroup__imgcodecs.html%23ga288b8b3da0892bd651fce07b3bbd3a56)
2. **`ImreadModes`**: [Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F4.5.1%2Fd8%2Fd6a%2Fgroup__imgcodecs__flags.html%23ga61d9b0126a3e57d9277ac48327799c80)
# Color Channels
When reading color images openCV stores images in BGR format, so for a correct display we need to reverse the channels.

```Python
img_channels_reversed = img[:, :, ::-1]
```

The split function let's you split an image into it's channels. Each channel it's going to be a 2D numpy array that contains the intensity of each color for each pixel.
```Python
b,g,r = cv2.split(img)
```

The merge function allows you to take three channels and merge them into one image. The input is an array of 2D arrays.
```Python
imgMerged = cv2.merge((b,g,r))
```
You can convert into different color spaces.
```Python
dst = cv2.cvtColor(src, code)
```
The code determines the color space conversion codes
## Documentation
1. **`split`**: [Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F4.5.1%2Fd2%2Fde8%2Fgroup__core__array.html%23ga0547c7fed86152d7e9d0096029c8518a)
2. **`Merge`**: [Documentation Link](https://docs.opencv.org/4.5.1/d2/de8/group__core__array.html#ga61f2f2bde4a0a0154b2333ea504fab1d)
3. **`cv2.cvtColor`**: [Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F3.4%2Fd8%2Fd01%2Fgroup__imgproc__color__conversions.html%23ga397ae87e1288a81d2363b61574eb8cab)
4. **`ColorConversionCodes`**: [Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F4.5.1%2Fd8%2Fd01%2Fgroup__imgproc__color__conversions.html%23ga4e0972be5de079fed4e3a10e24ef5ef0)

# Saving Images
To save the images to disk you use the finction `imwrite`
```Python
cv2.imwrite(filename, img[params])
```
Then you can use the `Image` function to display the file
## Documentation
1. **`Imwrite`**: [Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F4.5.1%2Fd4%2Fda8%2Fgroup__imgcodecs.html%23gabbc7ef1aa2edfaa87772f1202d67e0ce)
2. **`ImwriteFlags`**: [Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F4.5.1%2Fd8%2Fd6a%2Fgroup__imgcodecs__flags.html%23ga292d81be8d76901bff7988d18d2b42ac)

# Image Manipulation
## Cropping
You just have to index the part of the image you want to keep
```Python
cropped_img - img[200:400, 300:600]
```

## Resizing
```Python
dst = cv2.resize(src, dsize, fx, fy, interpolation)
```

You can specify the desired size in `dsize`, or pass `None` and specify the scaling in the `fx` and `fy` parameters.

You can pass any `dsize` but the image will be distorted if the aspect ratio is not respected. If you want to maintain the aspect ratio you can specify a desired with or height and calculate the other variable based on that.

The default interpolation is linear.
## Flip
```Python
dst = cv2.flip(src, flipCode)
```
## Documentation
1. **`resize()`**: [Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F4.5.0%2Fda%2Fd54%2Fgroup__imgproc__transform.html%23ga47a974309e9102f5f08231edc7e7529d)
2. **`flip`**: [Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F4.5.0%2Fd2%2Fde8%2Fgroup__core__array.html%23gaca7be533e3dac7feb70fc60635adf441)

# Image Annotation
To use color in the annotation you need yo read the image as color, even if its black and white.
## Drawing a Line
```Python 
img = cv2.line(img, pt1, pt2, color, thickness, linetype, shift)
```

The pt1 argument indicates the first point of the line and the pt2 the ending point.
The color needs to be in BGR.

## Drawing a Circle
```Python
img = cv2.circle(img, center, radius, color, thickness, lineType, shift)
```

You need to specify the center coordinates and the radius of the circle
If the thickness is negative the color fills the whole circle.

## Drawing a Rectangle
```Python
img = cv2.rectangle(img, pt1, pt2, color, thickness, lineType, shift)
```

here the arguments pt1 and pt2 indicate the topleft vertex and bottom right vertex of the rectangle.
If the thickness is negative the color fills the whole circle.
## Text
```Python
img = cv2.putText (img, text, org, fontFace, fontScale, color, thickness, lineType, bottomLeftOrigin)
```

the argument org indicates the bottom left origin of the text.
If the fontScale is negative the text will be drawn upside down.
## Documentation
1. **`line`**: [Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F4.5.1%2Fd6%2Fd6e%2Fgroup__imgproc__draw.html%23ga7078a9fae8c7e7d13d24dac2520ae4a2)
2. **`circle`**: [Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F4.5.1%2Fd6%2Fd6e%2Fgroup__imgproc__draw.html%23gaf10604b069374903dbd0f0488cb43670)
3. **`rectangle`**: [Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F4.5.1%2Fd6%2Fd6e%2Fgroup__imgproc__draw.html%23ga07d2f74cadcf8e305e810ce8eed13bc9)
4. **`putText`**: [Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F4.5.1%2Fd6%2Fd6e%2Fgroup__imgproc__draw.html%23ga5126f47f883d730f633d74f07456c576)

# Image Enhancement
## Adjusting Brightness
You can do this by simple making the pixel values higher o lower. You do this by using the add and subtract function with a value matrix
```Pyhton
img_brighter = cv2.add(img, matrix)
img_darker = cv2.subtract(img, matrix)
```

cv2 and function saturates the value so it doesn't roll over like with numpy +.
## Adjusting Contrast
Contrast is defined as the difference value of pixels in the image so it's handled with multiplication.
We want to multiply the image by a factor so we create a matrix of floats
```Python
img_lower_contrast = np.uint8(cv2.multiply(np.float64(img), matrix))
```

The higher values may overflow and go to 0 so to fix that we have to use the numpy clip function.
```Python
img_higher_contrast = np.uint8(np.clip(cv2.multiply(np.float64(img), matrix),0,255))
```

## Thresholding
Thresholding allows you to selectively edit some portions of the image while letting others intact. It does this by creating a binary images that can be used as masks.
```Python
retval, dst = cv2.thershold(src, thresh, maxval, type, dst)
```

maxval indicate the maximum value for the binary map. Al the pixels that have a value below the threshold will be set to 0 and the rest will be set  to maxval. Dst is going to contain the binary map, retval can be ignored.

```Python
dst = cv2.adaptiveThreshold(src, maxValue,adaptiveMethod, thresholdType, blosckSize, C, dst)
```

adaptiveMethod indicates the adaptive thresholding algorithm used. The blockSize indicates the size of the pixel neighbourhood that is used to calculates the threshold value for the pixel. C is a constant sibstracted from the mean.

### Bitwise Operations
```Python
dst = cv2.bitwise_and(src1, src2, dst, mask)
```
`cv2.bitwisw_or()`, `cv2.bitwise_xor()`,`cvs.bitwise_not()`, etc. follow the same syntax.
## Documentation
1. **`add`**: [Documentation link](https://docs.opencv.org/4.5.1/d2/de8/group__core__array.html#ga10ac1bfb180e2cfda1701d06c24fdbd6)
2. **`threshold and adaptiveThreshold`**[Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F4.5.1%2Fd7%2Fd1b%2Fgroup__imgproc__misc.html%23gae8a4a146d1ca78c626a53577199e9c57%0Ahttps%3A%2F%2Fdocs.opencv.org%2F4.5.1%2Fd7%2Fd4d%2Ftutorial_py_thresholding.html)
3. Arithmetic Operations on Images: [Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F4.5.1%2Fd0%2Fd86%2Ftutorial_py_image_arithmetics.html)
4. **`bitwise_and`**(...) function: [Documentation link](https://www.google.com/url?q=https%3A%2F%2Fdocs.opencv.org%2F4.5.0%2Fd2%2Fde8%2Fgroup__core__array.html%23ga60b4d04b251ba5eb1392c34425497e14)


