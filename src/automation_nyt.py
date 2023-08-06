import os
import time

import requests

import re

from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, InvalidSelectorException
from loguru import logger as loguru_logger

from src.consts import get_section_and_type
from src.variables import Cfg
import datetime


class AutomationError(Exception):
    pass


class AutomationNYT:
    def __init__(self, cfg: Cfg):
        self.browser_lib = Selenium()
        self.url = "https://www.nytimes.com/"
        self.logger = loguru_logger
        self.period = cfg.month_period
        self.phrase = cfg.phrase
        self.filters_config = {"section": cfg.sections, "type": cfg.notice_type}
        self.files = Files()

    def open_the_website(self):
        self.logger.info(f"Openning Website: {self.url}")
        self.browser_lib.open_available_browser(url=self.url, maximized=True)

    def find_element_by_css_selector(self, tag, attr, content):
        return self.browser_lib.find_element(f'css:{tag}[{attr}^={content}]')

    def find_elements_by_css_selector(self, tag, attr, content):
        return self.browser_lib.find_elements(f'css:{tag}[{attr}^={content}]')

    def find_element_by_xpath(self, tag, attr, content):
        return self.browser_lib.find_element(f'xpath://{tag}[@{attr}="{content}"]')

    def terms(self):
        try:
            self.logger.info("Find terms of use...")
            self.button_click(tag="button", attr="class", content="css-1fzhd9j")
            self.logger.info("Accept terms of use...")
        except AutomationError:
            self.logger.info("Without terms of use to accept")
            return

    def search_for(self):
        try:
            self.logger.info(f"Searching phrase: {self.phrase}...")
            searh_button = self.find_element_by_css_selector(tag="button", attr="data-test-id", content="search-button")
            searh_button.click()
            input_field = "css:input"
            self.browser_lib.input_text(input_field, self.phrase)
            self.browser_lib.press_keys(input_field, "ENTER")

        except Exception as error:
            raise AutomationError(f"Error when searching phrase - {error}") from error

    def button_click(self, tag, attr, content):
        try:
            self.browser_lib.click_element_when_visible(f'css:{tag}[{attr}^={content}]')
        except Exception as error:
            self.logger.warning(f"Option not available - {str(error)}")

    def select_option_in_dropdown(self, option_list: list):
        for option in option_list:
            self.button_click(tag="input", attr="value", content=get_section_and_type(option))

    def apply_date_filter(self, start_date, end_date):
        self.logger.info("Apply Date Filter...")
        try:
            self.button_click(tag="button", attr="data-testid", content="search-date")
            self.browser_lib.click_element_when_visible("//*[text()='Specific Dates']")

            start_date_input = self.find_element_by_css_selector(tag="input", attr="id", content="startDate")
            self.browser_lib.input_text(start_date_input, start_date.strftime("%m/%d/%Y"))

            end_date_input = self.find_element_by_css_selector(tag="input", attr="id", content="endDate")
            self.browser_lib.input_text(end_date_input, end_date.strftime("%m/%d/%Y"))
            self.browser_lib.press_keys(end_date_input, "ENTER")

            self.logger.info("Apply Date Filter - Done.")
        except Exception as error:
            raise AutomationError(f"Error when apply date filter - {error}") from error

    def set_period(self):
        today = datetime.date.today()
        month = today.month - (self.period - 1)

        if self.period in [0, 1]:
            start_date = datetime.date(today.year, today.month, 1)
            end_date = datetime.date.today()
        else:
            start_date = datetime.date(today.year, month, 1)
            end_date = datetime.date.today()

        return start_date, end_date

    def filters_apply(self):
        try:
            if self.period:
                start_date, end_date = self.set_period()
                self.apply_date_filter(start_date, end_date)

            for key in self.filters_config:
                self.logger.info("Aplly section and notice type filter...")
                button_content, filters_list = key, self.filters_config.get(key)
                self.button_click(tag="div", attr="data-testid", content=button_content)
                self.select_option_in_dropdown(filters_list)
            self.logger.info("Filters applied.")
        except Exception as error:
            raise AutomationError(f"Error when filters apply - {error}") from error

    def sort_by(self):
        try:
            self.logger.info("sorty by...")
            self.button_click(tag="select", attr="data-testid", content="SearchForm")
            self.button_click(tag="option", attr="value", content="newest")
        except WebDriverException as error:
            raise AutomationError(f"Error when apply sort by - {error}") from error

    @staticmethod
    def check_if_contains_amount_money(title, description):
        pattern = r"\$\d+(\.\d+)?|\d+(\.\d+)? dollars?|\d+ USD"
        money_in_title = re.match(pattern, title)
        money_in_description = re.match(pattern, description)

        if money_in_title or money_in_description:
            return str(True)
        return str(False)

    @staticmethod
    def img_download(result):
        try:
            img = WebDriverWait(result.find_element, timeout=2).until(
                lambda d: d(By.CLASS_NAME, "css-rq4mmj")
            )
            src = img.get_attribute("src")
            filename = os.path.basename(src.split("?")[0])

            with open(f"output/{filename}", "wb") as file:
                file.write(requests.get(src).content)
            return filename
        except Exception as e:
            print(e)
            return ""

    @staticmethod
    def get_link(result):
        try:
            return result.find_element(By.TAG_NAME, "a").get_attribute("href")
        except Exception as e:
            print(e)
            return ""

    def get_all_data(self):
        news = []

        results = self.browser_lib.get_webelements('xpath://li[@data-testid="search-bodega-result"]')
        for i, r in enumerate(results):
            data = {
                "date": r.find_element(By.CLASS_NAME, "css-17ubb9w").text,
                "topic": r.find_element(By.CLASS_NAME, "css-myxawk").text,
                "news_link": self.get_link(r),
                "title": r.find_element(By.CLASS_NAME, "css-2fgx4k").text,
                "description": r.find_element(By.CLASS_NAME, "css-16nhkrn").text,
                "author": r.find_element(By.CLASS_NAME, "css-15w69y9").text,
                "img_filename": self.img_download(r),
            }
            data["contains_amount_money"] = self.check_if_contains_amount_money(data.get("title"),
                                                                                data.get("description"))
            data["search_phrases_count"] = data.get("title").lower().count(self.phrase.lower()) + data.get(
                "description").lower().count(self.phrase.lower())

            news.append(data)

        return news

    def save_data(self):
        try:
            self.logger.info("Get news data...")
            news = self.get_all_data()
            self.files.create_workbook(path="./output/output.xlsx")
            self.logger.info("Creating excel file...")
            self.files.create_worksheet("News", content=[data for data in news], header=True)
            self.files.save_workbook()
            self.logger.info("Data saved.")
        except Exception as error:
            raise AutomationError(error) from error

    def run(self):
        try:
            self.open_the_website()
            self.terms()
            self.search_for()
            self.filters_apply()
            self.sort_by()
            time.sleep(3)
            self.save_data()
            self.browser_lib.close_all_browsers()

        except AutomationError as e:
            self.logger.exception(str(e))
