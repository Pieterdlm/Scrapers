from PIL import Image
import numpy as np
from io import BytesIO
import requests

# Load the image
url = "https://media.s-bol.com/qoEJzM2KROn0/BjQ02X/550x664.jpg"
response = requests.get(url)
img = Image.open(BytesIO(response.content))

# Convert the image to grayscale
img_gray = img.convert("L")

# Define a threshold value for the background
threshold = 240

# Convert the grayscale image to a binary image
img_bin = np.array(img_gray) < threshold

# Convert the binary image back to an integer array
img_int = img_bin.astype(np.uint8) * 255

# Convert the image to a numpy array
img_arr = np.array(img)
img_arr[img_int == 0] = 0

# Calculate the frequency of each color in the image
colors, counts = np.unique(img_arr.reshape(-1, img_arr.shape[-1]), axis=0, return_counts=True)

# Find the color with the highest frequency
idx = np.argsort(-counts) # Sort in descending order
most_common_colors = colors[idx[:2]] # Take the first two colors with highest frequency
print(colors)
print (counts)

# Print the results
print("The most common color in the image is:", most_common_colors[0])
print("The second most common color in the image is:", most_common_colors[1])