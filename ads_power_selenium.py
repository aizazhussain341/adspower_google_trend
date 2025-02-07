import json
from symbol import except_clause

import requests
import time
import os
import random
import pandas as pd
from pathlib import Path
import sys
from selenium import webdriver
import logging
import argparse
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait

class AdsPowerSelenium:
    def __init__(self):
        self.profile_ids = ['ktigg8k', 'ktieu7c']
        self.open_url = None
        self.close_url = None
        self.downloaded_file_path = Path.home() / "Downloads/multiTimeline.csv"

    def setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)

    def parse_arguments(self):
        """Parse command line arguments"""
        parser = argparse.ArgumentParser(description='Selenium script for data scraping')
        parser.add_argument('--query', type=str, required=True, help='Search query to process')
        return parser.parse_args()


    def get_table_rows(self, driver):
        retries = 0
        while True:
            if retries > 5:
                return None
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//div[@aria-label='A tabular representation of the data in the chart.']")))
                try:
                    data_trs = driver.find_element(By.XPATH, f"//div[@aria-label='A tabular representation of the data in the chart.']").find_element(By.TAG_NAME, 'table').find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
                    return data_trs
                except:
                    try:
                        error_message = driver.find_element(By.CLASS_NAME, "widget-error-title").text
                        if error_message == "Search results not available":
                            return "Search results not available"
                    except:
                        pass
                    driver.refresh()
                    retries += 1
                    time.sleep(2)
                    continue
            except Exception as e:
                try:
                    error_message = driver.find_element(By.CLASS_NAME, "widget-error-title").text
                    if error_message == "Search results not available":
                        return "Search results not available"
                except:
                    pass
                driver.refresh()
                retries += 1

                time.sleep(2)
                continue

    def get_data_from_table_rows(self, table_rows, query):
        data_row = {}

        for table_row in table_rows:
            try:
                trend_date = str(table_row.find_elements(By.TAG_NAME, "td")[0].accessible_name)
                trends_data = str(table_row.find_elements(By.TAG_NAME, "td")[1].accessible_name)
                data_row.update({trend_date: trends_data})
            except:
                pass
        return data_row

    def read_data_from_csv(self, query):
        data_row = {}
        df = pd.read_csv(self.downloaded_file_path, skiprows=2)
        column_names = [" "]
        values_list = [query]
        column_names.extend(df['Day'].tolist())
        values_list.extend(df[f"{query}: (Pakistan)"].to_list())
        for idx , date in enumerate(column_names):
            data_row.update({date: values_list[idx]})
        os.remove(self.downloaded_file_path)
        return data_row

    def write_data_to_output_csv(self, data_row, row=None):
        df = pd.DataFrame([data_row])
        if row == 0:
            df.to_csv("output.csv", mode='w', header=True, index=False)
        df.to_csv("output.csv", mode='a', header=False, index=False)

    def click_download_button(self, driver):
        while True:
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//i[text()='file_download']")))
                try:
                    driver.find_element(By.XPATH, "//i[text()='file_download']").click()
                    break
                except:
                    driver.refresh()
                    time.sleep(2)
                    continue
            except Exception as e:
                driver.refresh()
                time.sleep(2)
                continue

    def close_inactive_tabs(self, driver):
        active_tab = driver.current_window_handle
        all_tabs = driver.window_handles

        # Close all inactive tabs
        for tab in all_tabs:
            if tab != active_tab:
                driver.switch_to.window(tab)
                driver.close()

        # Switch back to the active tab
        driver.switch_to.window(active_tab)

    def open_browser_and_load_trends_page(self, query):
        profile_id_to_use = random.choice(self.profile_ids)
        self.open_url = "http://local.adspower.com:50325/api/v1/browser/start?clear_cache=True&clear_cookies=True&close_other_windows=True&open_tabs=[]&&user_id=" + profile_id_to_use
        self.close_url = "http://local.adspower.com:50325/api/v1/browser/stop?user_id=" + profile_id_to_use
        resp = requests.get(self.open_url).json()
        if resp["code"] != 0:
            sys.exit()

        chrome_driver = resp["data"]["webdriver"]
        service = Service(executable_path=chrome_driver)
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
        # prefs = {
        #     "download.default_directory": self.download_dir,
        #     "download.prompt_for_download": False,
        #     "directory_upgrade": True,
        #     "safebrowsing.enabled": True
        # }
        # chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        self.close_inactive_tabs(driver)
        driver.get(f"https://trends.google.com/trends/explore?date=2024-05-09 2025-02-02&geo=PK&q={query}&hl=en")
        # self.click_download_button(driver)
        table_rows = self.get_table_rows(driver)
        if table_rows == 'Search results not available':
            return table_rows
        data_row = self.get_data_from_table_rows(table_rows, query)
        time.sleep(5)
        driver.quit()
        requests.get(self.close_url)
        return data_row

    def close_browser_profile(self):
        if self.close_url:
            requests.get(self.close_url)

def main():
    ads_power = AdsPowerSelenium()
    logger = ads_power.setup_logging()

    # Parse command line arguments
    args = ads_power.parse_arguments()
    query = args.query

    logger.info(f"Starting selenium script with query: {query}")
    ads_power.close_browser_profile()
    # TODO: Added 50 quries for testing purpose, We can add more
    # for idx, query in enumerate(['smelling salts', 'gladiator ii', 'nasal strips for snoring', 'eggs', 'moa', 'kindle', 'valentines day gifts for kids', 'blink twice', 'stanley cup', 'airpods', 'den of thieves', 'onyx storm', 'reacher', 'magnetic eyelashes', 'ipad', 'nad supplement', 'harlem', 'nmn', 'mrbeast', 'the substance', 'tonsil stone mouthwash', 'magnesium glycinate', 'valentines day cards for kids school', 'apple watch', 'the wild robot', 'laptop', 'severance', 'sonic the hedgehog 3', 'iphone 16 pro max case', 'owala', 'magnetic eyelashes natural look', 'pheromone perfume for women', 'invincible']):
    while True:
        data_row = ads_power.open_browser_and_load_trends_page(query)
        if data_row:
            print(json.dumps(data_row))
            sys.exit(0)
    # data_row = ads_power.read_data_from_csv(query)
        if data_row == "Search results not available":
            ads_power.close_browser_profile()
            print(json.dumps({"message": "Search results not available"}))
            sys.exit(0)
    # ads_power.write_data_to_output_csv(data_row, idx)


if __name__ == "__main__":
    main()