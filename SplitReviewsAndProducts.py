import csv
import nltk
from pattern.nl import sentiment
from collections import Counter


# define input and output file paths
input_file = "combined_with_colors.csv"
product_output_file = "products.csv"
review_output_file = "reviews.csv"
word_count_output_file = "word_count.csv"

# open input and output files
with open(input_file, "r", newline="", encoding="utf-8") as infile, \
     open(product_output_file, "w", newline="", encoding="utf-8") as product_outfile, \
     open(review_output_file, "w", newline="", encoding="utf-8") as review_outfile, \
     open(word_count_output_file, "w", newline="", encoding="utf-8") as word_count_outfile:

    # create CSV reader and writers
    reader = csv.DictReader(infile)
    product_writer = csv.writer(product_outfile)
    review_writer = csv.writer(review_outfile)
    word_count_writer = csv.writer(word_count_outfile)

    # write headers to output files
    product_writer.writerow(["product_number", "product_name", "price", "image_link", "color"])
    review_writer.writerow(["product_number", "review_text", "review_rating"])
    word_count_writer.writerow(["word", "count"])

    # iterate over input rows and write data to output files
    product_number = 0
    word_counter = Counter()
    for row in reader:
        # write product data to products.csv
        product_writer.writerow([product_number, row["Naam"], row["Prijs"], row["Foto"], row["Kleur"]])

        # write review data to reviews.csv
        reviews = eval(row["Review"])
        for review in reviews:
            sentiment_score = sentiment(review)[0]
            waarde = ''
            if sentiment_score > 0:
                waarde = "positive"
            elif sentiment_score < 0:
                waarde = "negative"
            else:
                waarde = "neutral"

            # update word counter with words from review
            words = nltk.word_tokenize(review.lower())
            word_counter.update(words)

            review_writer.writerow([product_number, review, waarde])

        # increment product number for next row
        product_number += 1

    # write word counts to word_count.csv
    for word, count in word_counter.items():
        word_count_writer.writerow([word, count])

print("Done!")