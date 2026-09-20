import cv2
import numpy as np
from matplotlib import pyplot as plt

# opening the image as a numpy array
img = cv2.imread("image_01.tif")

if img is None:
    print("Image not found!")
else:
    print("Image loaded successfully!")

# BGR
blueChannel = img[:, :, 0]
greenChannel = img[:, :, 1]
redChannel = img[:, :, 2]

rs = []
for r in range(0,256):
    rs.append(r)

# counting the frequencies of each r in each channel & plotting it
def frequency_counter(img):
    list_of_occurances = []
    c = 0
    for r in range(0,256):
        for arr in img:
            c += np.count_nonzero(arr == r)
        list_of_occurances.append(c)
        c = 0
    return list_of_occurances

nBluechannel = frequency_counter(blueChannel)
nGreenchannel = frequency_counter(greenChannel)
nRedchannel = frequency_counter(redChannel)

fig, axs = plt.subplots(2, 2, figsize=(10,8))
axs[0, 0].bar(rs, nRedchannel, color='tab:red', width=3)
axs[0, 0].set_title('Red band Histogram')
axs[0, 1].bar(rs, nGreenchannel, color='tab:green', width=3)
axs[0, 1].set_title('Green band Histogram')
axs[1, 0].bar(rs, nBluechannel, color='tab:blue', width=3)
axs[1, 0].set_title('Blue band Histogram')
axs[1, 1].bar(rs, nRedchannel, color='tab:red', width=3)
axs[1, 1].bar([r + 3 for r in rs], nGreenchannel, color = 'tab:green', width = 3)
axs[1, 1].bar([r + 6 for r in rs], nBluechannel, color = 'tab:blue', width = 3)
axs[1, 1].set_title('Image Histogram')
plt.show()

def plot_results(input_img, output_img, x_values, y_values):
    
    # plotting the graph
    plt.figure(figsize = (36,12))

    plt.subplot(131)
    plt.imshow(cv2.cvtColor(input_img.astype(np.uint8), cv2.COLOR_BGR2RGB))
    plt.title('Input Image')
    plt.axis('off')

    plt.subplot(132)
    plt.plot(x_values, y_values)
    plt.xlabel('Input Pixels')
    plt.ylabel('Output Pixels')
    plt.grid(True)

    plt.subplot(133)
    plt.imshow(cv2.cvtColor(output_img.astype(np.uint8), cv2.COLOR_BGR2RGB))
    plt.title('Transformed Image')
    plt.axis('off')

    plt.show()

def piecewiseLinear(r, r1, s1, r2, s2):
    if r < r1:
        s = (s1 / r1) * r
    elif r > r1 and r < r2:
        s = ((s2 - s1) / (r2 - r1)) * (r - r1) + s1 
    else: 
        s = ((255 -s2) / (255 - r2)) * (r - r2) + s2
        
    return int(s)

piecewiseLinearVec = np.vectorize(piecewiseLinear)
x_values = np.linspace(0,255,500)
y_values = piecewiseLinearVec(x_values, 80, 20, 150, 190)
transformed_im = piecewiseLinearVec(img, 80, 20, 150, 190)
plot_results(img, transformed_im, x_values, y_values)

# Q3
nkList = nBluechannel + nGreenchannel + nRedchannel

total_values = img.shape[0] * img.shape[1] * 3 
threshholdPixels = total_values * (2/100)
# finding rL
sumN = 0
r = 0
while sumN < threshholdPixels and r < 256:
    sumN += nkList[r]
    r += 1
rL = r

# finding rU
sumN = 0
r = 255
while sumN < threshholdPixels and r > 0:
    sumN += nkList[r]
    r -= 1
rU = r

print(f"rL: {rL}, rU: {rU}")

def Tr(image_input):
    img_float = image_input.astype(float)
    # clipping
    img_clipped = np.clip(img_float, rL, rU)
    # apply formula
    # avoid division by zero if rU == rL
    denom = rU - rL if rU != rL else 1 
    transformed = ((img_clipped - rL) / denom) * 255
    # convert back to uint8
    return np.clip(transformed, 0, 255).astype(np.uint8)

newImg = Tr(img)

newblueChannel = newImg[:, :, 0]
newgreenChannel = newImg[:, :, 1]
newredChannel = newImg[:, :, 2]

newNBluechannel = frequency_counter(newblueChannel)
newNGreenchannel = frequency_counter(newgreenChannel)
newNRedchannel = frequency_counter(newredChannel)

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

axs[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
axs[0, 0].set_title('Original Image')

axs[0, 1].imshow(cv2.cvtColor(newImg, cv2.COLOR_BGR2RGB))
axs[0, 1].set_title('Enhanced Image (2% Stretch)')

axs[1, 0].bar(rs, nRedchannel, color='tab:red', alpha=0.5, label='Red')
axs[1, 0].bar(rs, nGreenchannel, color='tab:green', alpha=0.5, label='Green')
axs[1, 0].bar(rs, nBluechannel, color='tab:blue', alpha=0.5, label='Blue')
axs[1, 0].set_title('Original Histogram')
axs[1, 0].legend()

axs[1, 1].bar(rs, newNRedchannel, color='tab:red', alpha=0.5, label='Red')
axs[1, 1].bar(rs, newNGreenchannel, color='tab:green', alpha=0.5, label='Green')
axs[1, 1].bar(rs, newNBluechannel, color='tab:blue', alpha=0.5, label='Blue')
axs[1, 1].set_title('New Histogram')
axs[1, 1].legend()
plt.tight_layout()
plt.show()

def intensitySlicer(original_img):
    result_img = original_img.copy()
    # NEW!: using numpy masking, changes the intensity values!
    # the condition in the brackets is done element-wise. then used to pick the
    # corresponsing values & setting them to a different value.
    result_img[original_img <= 20] = 155
    result_img[(original_img > 20) & (original_img <= 40)] = 200
    result_img[(original_img > 40) & (original_img <= 50)] = 100
    result_img[(original_img > 50) & (original_img <= 60)] = 10
    result_img[(original_img > 60) & (original_img <= 150)] = 50
    result_img[original_img > 150] = 85

    return result_img


slicedImg = intensitySlicer(img)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original")

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(slicedImg, cv2.COLOR_BGR2RGB))
plt.title("Intensity Sliced")
plt.show()


img = cv2.imread("image_01.tif", 0)

def bitPlaneSlicing(r, bit_plane):
    dec = np.binary_repr(r, width = 8)
    return int(dec[8-bit_plane])

bitPlaneSlicingVec = np.vectorize(bitPlaneSlicing)

bit_planes_dict = {}
for bit_plane in np.arange(8,0, -1):
    bit_planes_dict['bit_plane_' + str(bit_plane)] = bitPlaneSlicingVec(img, bit_plane = bit_plane)
plt.figure(figsize = (24,12))

plt.subplot(331)
plt.imshow(img, cmap="gray")
plt.title('Original Image')

plt.subplot(332)
plt.imshow(bit_planes_dict['bit_plane_8'], cmap="gray")
plt.title('bit plane 8')

plt.subplot(333)
plt.imshow(bit_planes_dict['bit_plane_7'], cmap="gray")
plt.title('bit plane 7')

plt.subplot(334)
plt.imshow(bit_planes_dict['bit_plane_6'], cmap="gray")
plt.title('bit plane 6')

plt.subplot(335)
plt.imshow(bit_planes_dict['bit_plane_5'], cmap="gray")
plt.title('bit plane 5')

plt.subplot(336)
plt.imshow(bit_planes_dict['bit_plane_4'], cmap="gray")
plt.title('bit plane 4')

plt.subplot(337)
plt.imshow(bit_planes_dict['bit_plane_3'], cmap="gray")
plt.title('bit plane 3')

plt.subplot(338)
plt.imshow(bit_planes_dict['bit_plane_2'], cmap="gray")
plt.title('bit plane 2')

plt.subplot(339)
plt.imshow(bit_planes_dict['bit_plane_1'], cmap="gray")
plt.title('bit plane 1')
plt.show()


img1 = cv2.imread("image_01.tif")
img2 = cv2.imread("image_02.tif")

def linearContrastStretching(img):
    img = img.astype(np.float32)
    return ((img - img.min()) / (img.max() - img.min()) * 255).astype(np.uint8)

def sumImages(img1, img2):
    output = img1.astype(np.float32) + img2.astype(np.float32)
    return linearContrastStretching(output)

def subtractImages(img1, img2):
    output = img1.astype(np.float32) - img2.astype(np.float32)
    return linearContrastStretching(output)

def multiplyImages(img1, img2):
    output = img1.astype(np.float32) * img2.astype(np.float32)
    return linearContrastStretching(output)

def divisionImages(img1, img2):
    img2_safe = img2.astype(np.float32)
    img2_safe[img2_safe == 0] = 1e-5
    output = img1.astype(np.float32) / img2_safe
    return linearContrastStretching(output)

if img1.shape == img2.shape: 
    sumResult = sumImages(img1, img2)
    subtractResult = subtractImages(img1, img2)
    multiplyResult = multiplyImages(img1, img2)
    divisionResult = divisionImages(img1, img2)
else:
    print("Error! The images don't have the same size!")

fig, axs = plt.subplots(2, 2, figsize=(10,8))
axs[0, 0].imshow(cv2.cvtColor(sumResult, cv2.COLOR_BGR2RGB))
axs[0, 0].set_title('Summation')
axs[0, 1].imshow(cv2.cvtColor(subtractResult, cv2.COLOR_BGR2RGB))
axs[0, 1].set_title('Subtraction')
axs[1, 0].imshow(cv2.cvtColor(multiplyResult, cv2.COLOR_BGR2RGB))
axs[1, 0].set_title('Multiplication')
axs[1, 1].imshow(cv2.cvtColor(divisionResult, cv2.COLOR_BGR2RGB))
axs[1, 1].set_title('Division')
plt.show()