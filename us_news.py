# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:38:36 2024

@author: Sai Sudheer Vishnumolakala
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging

import re

def preprocess_dataframe(df):
    # Extracting City, State, and ZIP Code from Address
    df[['City', 'State', 'ZIP Code']] = df['Address'].str.extract(r'([^,]+), ([A-Z]{2}), (\d{5})')
    # Lowercasing column names and replacing spaces with underscores
    df.columns = df.columns.str.lower().str.replace(' ', '_', regex=False).str.replace('*', '', regex=False)
    # Removing dollar signs and commas and converting to float for tuition & fees
    df['tuition_&_fees'] = df['tuition_&_fees'].str.replace('[\$,]', '', regex=True).astype(float)
    # Extracting room & board value using regular expression and converting to float
    df['room_&_board'] = df['room_&_board'].str.extract(r'\$(\d{1,3}(?:,\d{3})*(?:\.\d+)?)')
    # Removing commas and converting room & board value to float
    df['room_&_board'] = df['room_&_board'].str.replace(',', '').astype(float)
    # Dropping unnecessary columns
    df = df.drop(['address', 'unnamed:_11', 'major'], axis=1, errors='ignore')
    
    return df



university_links =pd.read_csv('university_links.csv')
print(university_links[100:])
university_links =university_links[100:]
# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, filename='university_scraping.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize a list to store data for the final DataFrame
university_data_list = []
# Initialize a counter for the universities
university_counter = 0

for index, row in university_links.iterrows():
    try:
        university_name = row['University Name']
        url = row['Link']
        logging.info(f"Processing {university_name} at {url}")
        print(f"Extracting data for:{university_counter}. {university_name} - {url}")
        # Initialize the WebDriver for each university
        driver = webdriver.Chrome()
        driver.get(url)
        logging.info(f"Opened URL: {url}")
        time.sleep(5)  # Wait for the page to fully load
        
        # Initialize a dictionary to store the extracted information for each university
        enrollment_data = {"University Name": university_name}
        try:
            address = driver.find_element(By.CSS_SELECTOR, "div.OverviewContent__ContactDivAddress-sc-1yondsr-3").text
            enrollment_data["Address"] = address
            logging.info(f"Extracted address for {university_name}")
        except Exception as e:
            logging.warning(f"Could not extract address for {university_name}: {e}")
        
        
        data_elements = driver.find_elements(By.CSS_SELECTOR, "div.Box-w0dun1-0.DataRow__Row-sc-1udybh3-0")
        for element in data_elements:
            category = element.find_element(By.CSS_SELECTOR, "p.Paragraph-sc-1iyax29-0.ckyYzF").text
            value = element.find_element(By.CSS_SELECTOR, "p.Paragraph-sc-1iyax29-0.kqzqfx").text
            enrollment_data[category] = value
       
        # Extract ranking information
        ranking_element = driver.find_element(By.CSS_SELECTOR, "span.Villain__RankingSpan-sc-8s66oj-4.fDSmVR")
        ranking = ranking_element.text.split(" in ")[0]  # Splits and takes the ranking part
        ranking_category = ranking_element.find_element(By.CSS_SELECTOR, "a.Anchor-byh49a-0.Villain__BlueAnchor-sc-8s66oj-2").text
        enrollment_data['Ranking'] = f"{ranking} in {ranking_category}"
        # Navigate to the 'applying' page
        applying_url = url + '/applying'
        driver2 = webdriver.Chrome()
        print('APPLYING URL',applying_url)
        driver2.get(applying_url)
        time.sleep(5)  # Wait for the page to fully load
        
        # Extract quick stats
        stats_container = driver2.find_element(By.CLASS_NAME, "quick-stat-box")
        data_pairs = stats_container.find_elements(By.TAG_NAME, "dl")
        quick_stats = {}
        for pair in data_pairs:
            category = pair.find_element(By.TAG_NAME, "dt").text
            value = pair.find_element(By.TAG_NAME, "dd").text
            quick_stats[category] = value
        # Add quick stats to the enrollment_data
        enrollment_data.update(quick_stats)
        
        # Add the university's data to the list and increment the counter
        university_data_list.append(enrollment_data)

        driver.quit()
        driver2.quit()
        logging.info(f"Completed processing for {university_name}")
        university_counter=+1
    except Exception as e:
        logging.error(f"An error occurred at index {index} for {university_name}: {e}")
        driver.quit()  # Ensure the driver is closed on error
        driver2.quit()

university_df = pd.DataFrame(university_data_list)
university_df.to_csv('final_df_raw.csv', index=False)
save_df =preprocess_dataframe(university_df)
save_df.to_csv('final_df.csv', index=False)
logging.info('Final DataFrame saved as final_df.csv')
logging.info("Scraping task completed.")
