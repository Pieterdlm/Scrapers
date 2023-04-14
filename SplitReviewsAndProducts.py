import csv

# define input and output file paths
input_file = "combined_with_colors.csv"
product_output_file = "products.csv"
review_output_file = "reviews.csv"

# open input and output files
with open(input_file, "r", newline="", encoding="utf-8") as infile, \
     open(product_output_file, "w", newline="", encoding="utf-8") as product_outfile, \
     open(review_output_file, "w", newline="", encoding="utf-8") as review_outfile:

    # create CSV reader and writers
    reader = csv.DictReader(infile)
    product_writer = csv.writer(product_outfile)
    review_writer = csv.writer(review_outfile)

    # write headers to output files
    product_writer.writerow(["product_number", "product_name", "price", "image_link", "color"])
    review_writer.writerow(["product_number", "review_text", "review_rating"])

    # iterate over input rows and write data to output files
    product_number = 0
    for row in reader:
        # write product data to products.csv
        product_writer.writerow([product_number, row["Naam"], row["Prijs"], row["Foto"], row["Kleur"]])

        # write review data to reviews.csv
        reviews = eval(row["Review"])
        for review in reviews:

            review_writer.writerow([product_number, review, ""])

        # increment product number for next row
        product_number += 1

print("Done!")