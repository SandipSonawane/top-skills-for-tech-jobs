import pandas as pd
import time
from selenium import webdriver

driver = webdriver.Chrome(r"C:\Users\Sandi\PycharmProjects\selenium_driver\driver\chromedriver.exe")

job_link_dictionary = {
    'Database Administrator': 'https://www.amazon.jobs/en/job_categories/database-administration',
    'Machine Learning': 'https://www.amazon.jobs/en/job_categories/machine-learning-science',
    'Software Engineering': 'https://www.amazon.jobs/en/job_categories/software-development',
    'Data Science': 'https://www.amazon.jobs/en/job_categories/data-science',
    'Business Intelligence': 'https://www.amazon.jobs/en/job_categories/business-intelligence'
}


empty_df = pd.DataFrame(columns=['category', 'company', 'link', 'title', 'location_and_id', 'posting_date'])


class CrawlData:
    def __init__(self, category, link, main_df):
        self.category = category
        self.link = link
        self.main_df = main_df

    def crawl(self):
        driver.get(self.link)
        # driver.maximize_window()
        time.sleep(5)

        next_page = driver.find_element_by_class_name('right')
        next_page_availability = (next_page.get_attribute('class'))

        while next_page_availability == 'btn circle right':
            links = driver.find_elements_by_class_name('job-link')
            links = [l.get_attribute('href') for l in links]

            titles = driver.find_elements_by_class_name('job-title')
            titles = [t.text for t in titles]

            locations_and_ids = driver.find_elements_by_class_name('location-and-id')
            locations_and_ids = [li.text for li in locations_and_ids]

            posting_dates = driver.find_elements_by_class_name('posting-date')
            posting_dates = [p.text for p in posting_dates]

            next_page = driver.find_element_by_class_name('right')
            next_page_availability = (next_page.get_attribute('class'))
            next_page.click()
            time.sleep(5)

            df = pd.DataFrame()
            df['link'] = links
            df['title'] = titles
            df['location_and_id'] = locations_and_ids
            df['posting_date'] = posting_dates
            df['category'] = self.category
            df['company'] = 'Amazon'
            self.main_df = self.main_df.append(df)
        else:
            print('completed')

        self.main_df.to_excel(f'.\\Data\\Amazon\\By Category\\{self.category}.xlsx')


for field, field_link in job_link_dictionary.items():
    cls_object = CrawlData(field, field_link, empty_df)
    CrawlData.crawl(cls_object)
