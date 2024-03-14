# University Data Extraction Project
## Project Overview
This project aims to scrape data about universities from a provided HTML file containing the "2024 Best National Universities | US News Rankings". The project consists of two main parts:

Extracting university links from the HTML file.
Extracting detailed data for each university from their respective links.
The extracted data is saved into CSV files for easy access and analysis.

## Prerequisites
Before running the scripts, ensure you have the following installed:
* Python 3.x
* Required Python packages: beautifulsoup4, pandas, selenium
You can install the required Python packages using pip:
pip install beautifulsoup4 pandas selenium

## Files Description
* extract_links.py: This script reads the HTML content of the "2024 Best National Universities | US News Rankings" page, extracts the university names and their links, and saves them into university_links.csv.

* university_scraping.py: This script reads the university links from university_links.csv, visits each link to extract detailed university data, and saves the data into multiple CSV files, partitioned as per the logic in the script.

* preprocess_dataframe.py: Contains a function to preprocess the extracted data, normalizing column names and converting specific data types for better analysis.

* 2024 Best National Universities _ US News Rankings.html: The HTML file from which university links are extracted.

* README.md: This file, providing an overview and instructions for the project.

## How to Run
1. Ensure the HTML file 2024 Best National Universities _ US News Rankings.html is in the same directory as the scripts.

2. Run extract_links.py to extract university links
  `python extract_links.py`

3. After university_links.csv is generated, run university_scraping.py to extract detailed data for each university:
  `python university_scraping.py`

4. Optionally, you can use preprocess_dataframe.py within university_scraping.py or separately to preprocess the extracted data.

## Contributing
Feel free to fork this project and submit pull requests if you have suggestions for improvements or have fixed any bugs.

## License
This project is open-sourced under the MIT License. See the LICENSE file for more details.

