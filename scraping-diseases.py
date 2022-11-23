import logging
import pathlib
import requests
from bs4 import BeautifulSoup
from csv import reader, writer
from time import sleep

# the source file path of the codes of diseases
file_path_source = pathlib.Path("./data/annot_KEGG_manualdownl_terms.csv")

# prevents missing source file and os errors
try:
    with open(file_path_source, "r") as file:
        csv_reader = reader(file)
        next(csv_reader)
        result_list = []
        for disease_code in csv_reader:
            request_result = requests.get(
                "https://www.kegg.jp/entry/" + disease_code[0])
            soup = BeautifulSoup(request_result.text, "html.parser")
            result_list.append([disease_code, soup.find(
                text="Description").findNext("div").text])
            sleep(8)
except OSError as error:
    logging.error(f"Writing to file {file_path_source} failed due to: {error}")

# writes the downloaded data into a file
with open("./data/list_of_diseases_and_codes.csv", "w") as file:
    csv_writer = writer(file)
    for disease in result_list:
        csv_writer.writerow([disease[0][0], disease[1]])
    print(f"Done. Downloaded {len(result_list)} of diseases.")
