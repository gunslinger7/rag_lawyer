import requests
import os
import re

def get_law_names():
    '''
    Reads each file in a dirrectory and find the relevant links

    Returns: 
        list: A list of law abbreviations (e.g. "BayAlm", "BayAbgG", etc.)    
    
    '''
    # list all the htm files and remove folder_files from that list
    htmls = os.listdir("resources/HTML/")
    htmls = [x for x in htmls if x.endswith(".htm")]

    # define the search pattern and the list for storing abbreviations of each law
    l_pattern = r'https://www\.gesetze-bayern\.de/Content/Document/Bay([^?]+)'
    abbreviations = []

    # loop through each htm file
    for htm in htmls:
        with open(f"resources/HTML/{htm}", 'r', encoding='utf-8') as f:
            htm = f.read()
            # find the links with that pattern and add missing "Bay" to every match
            matches = re.findall(l_pattern, htm)
            matches = ["Bay" + x for x in matches]
            abbreviations.extend(matches)

    return abbreviations


def get_save_pdf(law_name):
    '''
    Downloads the PDF file for the given law name from the Bayern website
    and saves it to the resources/pdfs directory.

    Args:
        law_name (str): The name of the law to download the PDF for.

    Returns:
        None
    '''

    # all the pdf donwload links on this website have this form
    url = f"https://www.gesetze-bayern.de/Content/Pdf/{law_name}?all=True"

    response = requests.get(url)
    with open(f"resources/pdfs/{law_name}.pdf", "wb") as f:
        f.write(response.content)


def main():
    laws = get_law_names()
    for law in laws:
        get_save_pdf(law)


if __name__ == "__main__":
    main()

 