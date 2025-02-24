import json
import requests
import time
import random
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
        self.profile_ids = ['ktiec6t']
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
            logger = self.setup_logging()
            logger.info(f"In while loop: {retries}")
            if retries > 5:
                return "Search results not available"
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"//div[@aria-label='A tabular representation of the data in the chart.']")))
                try:
                    data_trs = driver.find_element(By.XPATH, f"//div[@aria-label='A tabular representation of the data in the chart.']").find_element(By.TAG_NAME, 'table').find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
                    logger.info(f"Extracted Rows")
                    return data_trs
                except:
                    try:
                        error_message = driver.find_element(By.CLASS_NAME, "widget-error-title").text
                        logger.info(f"Error message: {error_message}")
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

    def open_browser_and_load_trends_page(self, query):
        profile_id_to_use = "ktiec6t"
        logger = self.setup_logging()
        status_url = f"http://local.adspower.com:50325/api/v1/browser/active?user_id={profile_id_to_use}"
        open_url = "http://local.adspower.com:50325/api/v1/browser/start?user_id=" + profile_id_to_use
        status_resp = requests.get(status_url).json()
        if status_resp["code"] == 0 and status_resp["data"].get("status") == "Active":
            pass
        info_resp = requests.get(open_url).json()
        if info_resp["code"] == 0:
            logger.info(f"browser opened")
            chrome_driver = info_resp["data"]["webdriver"]
            debugger_address = info_resp["data"]["ws"]["selenium"]

            service = Service(executable_path=chrome_driver)
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", debugger_address)

            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(f"https://trends.google.com/trends/explore?date=2024-05-09 2025-02-02&geo=PK&q={query}&hl=en")
        # self.click_download_button(driver)
            table_rows = self.get_table_rows(driver)
            if table_rows == 'Search results not available':
                return table_rows
            data_row = self.get_data_from_table_rows(table_rows, query)
            return data_row
        return info_resp

def main():
    ads_power = AdsPowerSelenium()
    logger = ads_power.setup_logging()
    query = sys.argv[1]
    logger.info(f"Starting selenium script with query: {query}")
    while True:
        try:
            data_row = ads_power.open_browser_and_load_trends_page(query)
            if data_row:
                print(json.dumps(data_row))
                sys.exit(0)
            elif data_row == "Search results not available":
                print(json.dumps({"message": "Search results not available"}))
                sys.exit(0)
            else:
                print(json.dumps(data_row))
                sys.exit(0)
        except Exception as e:
            print("Exception", e)


if __name__ == "__main__":
    main()
