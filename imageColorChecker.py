import webcolors
from PIL import Image
import numpy as np
from io import BytesIO
import requests
import csv
from scipy.spatial import KDTree


def convert_rgb_to_names(rgb_tuple):

    # a dictionary of all the hex and their respective names in css3
    css3_db = webcolors.CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(webcolors.hex_to_rgb(color_hex))

    try:
        kdt_db = KDTree(rgb_values)
        distance, index = kdt_db.query(rgb_tuple)
        return names[index]
    except ValueError:
        return 'NA'

with open('combined.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames + ['Kleur']
    with open('combined_with_colors.csv', 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        teller = 0
        for row in reader:
            name = row['Naam']
            price = row['Prijs']
            picture_path = row['Foto']
            review = row['Review']
            teller += 1

            # Load the image
            url = picture_path
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
            color_name = convert_rgb_to_names(most_common_colors[1])

            # Create a new dictionary for this row with the original columns and the new color column
            new_row = {'Naam': name, 'Prijs': price, 'Foto': picture_path, 'Review': review, 'Kleur': color_name}

            # Write the new row to the output file
            writer.writerow(new_row)

            # Print the results
            print(teller, "De juiste kleur is:", color_name)



