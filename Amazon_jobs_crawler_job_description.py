
import pandas as pd
import time
from selenium import webdriver

driver = webdriver.Chrome(r"C:\Users\Sandi\PycharmProjects\selenium_driver\driver\chromedriver.exe")

input_df = pd.read_excel(r'.\Data\Amazon\Amazon_data_by_job_category.xlsx')
output_df = pd.DataFrame(columns=['link', 'description', 'basic_qualifications', 'preferred_qualifications'])

for link in input_df.link:
    try:
        driver.get(link)
        description = driver.find_element_by_xpath('//*[@id="job-detail-body"]/div/div[1]/div/div[1]/p').text
        basic_qualifications = driver.find_element_by_xpath('//*[@id="job-detail-body"]/div/div[1]/div/div[2]/p').text
        preferred_qualifications = driver.find_element_by_xpath('//*[@id="job-detail-body"]/div/div[1]/div/div[3]/p').text
        output_df = output_df.append({'link': link, 'description': description, 'basic_qualifications': basic_qualifications,
                                      'preferred_qualifications': preferred_qualifications}, ignore_index=True)
    except:
        output_df = output_df.append(
            {'link': link, 'description': 'NA', 'basic_qualifications': 'NA',
             'preferred_qualifications': 'NA'}, ignore_index=True)

output_df.to_excel(r'.\Data\Amazon\Amazon_data_description.xlsx')
