from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import os
from bs4 import BeautifulSoup as bs
import pandas as pd
from tabulate import tabulate

class SeleniumActions:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=self.options)

    def open_website(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )

    def values(self, group):
        self.driver.find_element(By.ID, "group").send_keys(group)
        self.driver.find_element(By.XPATH, '//*[@id="wrap"]/div/div/div/div[2]/form/div[3]/div[3]/button').click()

    def get_times(self, soup):
        times = soup.find("div", class_="col-sm-4")
        return times

    def get_dates(self, soup):
        divs = soup.find_all("div", class_="col-md-6")
        dates = []
        for div in divs:
            headers = div.find_all("h4")
            dates.extend(headers)
        return dates

    def get_tables(self, soup):
        divs = soup.find_all("div", class_="col-md-6")
        tables = []
        for div in divs:
            table = div.find("table")
            if table:
                tables.append(table)
        return tables

    def parse(self):
        soup = bs(self.driver.page_source, "lxml")
        times = self.get_times(soup)
        dates = self.get_dates(soup)
        tables = self.get_tables(soup)
        return times, dates, tables

    def visualize(self, times, dates, tables):
        times = pd.read_html(str(times))
        tables = pd.read_html(str(tables))

        output_folder = "C:\\Programming\\python\\Pet Project\\schedule"

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_file = os.path.join(output_folder, "розклад.txt")

        with open(output_file, 'w', encoding="utf-8") as file:
            for i, time in enumerate(times):
                if time is not None:
                    formatted_table = tabulate(time, headers='keys', tablefmt='grid', showindex=False)
                    file.write(formatted_table + "\n\n")

            for i, table in enumerate(tables):
                if i < len(dates):
                    current_date = dates[i].text
                    file.write(f"{current_date}\n\n")

                if table is not None:
                    file.write(f"Таблиця {i + 1}:\n")
                    formatted_table = tabulate(table, headers='keys', tablefmt='grid', showindex=False)
                    file.write(formatted_table + "\n\n")


    def close(self):
        self.driver.close()
        self.driver.quit()

selenium_actions = SeleniumActions()
selenium_actions.open_website("https://dekanat.kubg.edu.ua/cgi-bin/timetable.cgi?n=700")
selenium_actions.values("ІНб22240д")
times, dates, tables = selenium_actions.parse()
selenium_actions.visualize(times, dates, tables)
selenium_actions.close()
