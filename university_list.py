# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:49:00 2024

@author: sai sudheer vishnumolakala
"""

from bs4 import BeautifulSoup
import pandas as pd

def extract_links_and_save():
    # Read HTML content from file
    with open('2024 Best National Universities _ US News Rankings.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <a> tags
    links = soup.select('div.Box-w0dun1-0.hsGaUt a')
    # Extract href attributes from all <a> tags
    hrefs = [link.get('href') for link in links if link.get('href')]

    # Print all extracted hrefs
    for cnt, href in enumerate(hrefs, start=1):
        print(href)
        print(cnt)

    university_names = [' '.join(link.split('/')[-1].split('-')[:-1]).title() for link in hrefs]
    df = pd.DataFrame({
        'University Name': university_names,
        'Link': hrefs
    })
    df.to_csv('university_links.csv', index=False)

if __name__ == "__main__":
    extract_links_and_save()
