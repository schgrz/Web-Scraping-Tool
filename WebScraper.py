# Import our libraries
from bs4 import BeautifulSoup as bs
import requests as rq
import csv

# Create an empty list to store our book data
bookinfo = []

# Send a GET request to the website and parse the HTML content and iterate it through all pages
for page_num in range(1, 50):
    url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
    result = rq.get(url)
    website = bs(result.text, "html.parser")
    # --View it if we'd like (Remove # from the line below)
    # print(website.prettify())

    # Find the prices
    prices = website.find_all(class_="price_color")
    prices = [price.text.strip("Â") for price in prices]
    # For my purposes, I'll be viewing this in Dollars to make it make sense for me, however the website is in British Pounds
    prices = [price.strip("Â").replace("£", "$") for price in prices]
    # --View it if we'd like (Remove # from the line below)
    # print(prices)

    # Find the titles
    titles = website.find_all("a", title=True)
    titles = [title["title"] for title in titles]
    # --View it if we'd like (Remove # from the line below)
    # print(titles)

    # Find the ratings
    ratings = website.find_all("p", class_=True)
    ratings = []
    for rating in website.find_all("p", class_="star-rating"):
        rating_class = rating["class"][1]
        if "One" in rating_class:
            rating_value = "1/5"
        elif "Two" in rating_class:
            rating_value = "2/5"
        elif "Three" in rating_class:
            rating_value = "3/5"
        elif "Four" in rating_class:
            rating_value = "4/5"
        elif "Five" in rating_class:
            rating_value = "5/5"
        else:
            rating_value = "Unknown"
        ratings.append(rating_value)
    # --View it if we'd like (Remove # from the line below)
    # print(ratings)

    page_data = list(zip(titles, prices, ratings))
    bookinfo.extend(page_data)

# --View it if we'd like (Remove # from the line below)
# print(bookinfo)

# Now I'll write it as a CSV file and store it for later
output_file = "bookinfo.csv"

# This will write the data to a file and overwrite if I perform the function again
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Price", "Rating"])
    for row in bookinfo:
        writer.writerow(row)

# This lets me know the program has completed
print("Done")
