import pandas as pd
import time
from selenium import webdriver
import re

job_link_dictionary = {
    'Product Management': 'https://www.facebook.com/careers/jobs/?offices[0]=Altoona%2C%20IA&offices[1]=Ashburn%2C%20VA&offices[2]=Atlanta%2C%20GA&offices[3]=Austin%2C%20TX&offices[4]=Bellevue%2C%20WA&offices[5]=Boston%2C%20MA&offices[6]=Burlingame%2C%20CA&offices[7]=Chicago%2C%20IL&offices[8]=Dallas%2C%20TX&offices[9]=DeKalb%2C%20IL&offices[10]=Denver%2C%20CO&offices[11]=Detroit%2C%20MI&offices[12]=Eagle%20Mountain%2C%20Utah&offices[13]=Forest%20City%2C%20NC&offices[14]=Fort%20Worth%2C%20TX&offices[15]=Foster%20City%2C%20CA&offices[16]=Fremont%2C%20CA&offices[17]=Gallatin%2C%20TN&offices[18]=Henrico%2C%20VA&offices[19]=Huntsville%2C%20AL&offices[20]=Irvine%2C%20CA&offices[21]=Los%20Angeles%2C%20CA&offices[22]=Los%20Lunas%2C%20NM&offices[23]=Menlo%20Park%2C%20CA&offices[24]=Miami%2C%20Florida&offices[25]=Montreal%2C%20Canada&offices[26]=Mountain%20View%2C%20CA&offices[27]=New%20Albany%2C%20OH&offices[28]=New%20York%2C%20NY&offices[29]=Newton%20County%2C%20GA&offices[30]=Northridge%2C%20CA&offices[31]=Ottawa%2C%20Canada&offices[32]=Pittsburgh%2C%20PA&offices[33]=Prineville%2C%20OR&offices[34]=Redmond%2C%20WA&offices[35]=Remote%2C%20US&offices[36]=Reston%2C%20VA&offices[37]=San%20Francisco%2C%20CA&offices[38]=Santa%20Clara%2C%20CA&offices[39]=Sarpy%20County%2C%20NE&offices[40]=Sausalito%2C%20CA&offices[41]=Seattle%2C%20WA&offices[42]=Sunnyvale%2C%20CA&offices[43]=Toronto%2C%20Canada&offices[44]=Vancouver%2C%20Canada&offices[45]=Washington%2C%20DC&roles[0]=full-time&teams[0]=Product%20Management',
    'Data and Analytics': 'https://www.facebook.com/careers/jobs/?offices[0]=Altoona%2C%20IA&offices[1]=Ashburn%2C%20VA&offices[2]=Atlanta%2C%20GA&offices[3]=Austin%2C%20TX&offices[4]=Bellevue%2C%20WA&offices[5]=Boston%2C%20MA&offices[6]=Burlingame%2C%20CA&offices[7]=Chicago%2C%20IL&offices[8]=Dallas%2C%20TX&offices[9]=DeKalb%2C%20IL&offices[10]=Denver%2C%20CO&offices[11]=Detroit%2C%20MI&offices[12]=Eagle%20Mountain%2C%20Utah&offices[13]=Forest%20City%2C%20NC&offices[14]=Fort%20Worth%2C%20TX&offices[15]=Foster%20City%2C%20CA&offices[16]=Fremont%2C%20CA&offices[17]=Gallatin%2C%20TN&offices[18]=Henrico%2C%20VA&offices[19]=Huntsville%2C%20AL&offices[20]=Irvine%2C%20CA&offices[21]=Los%20Angeles%2C%20CA&offices[22]=Los%20Lunas%2C%20NM&offices[23]=Menlo%20Park%2C%20CA&offices[24]=Miami%2C%20Florida&offices[25]=Mountain%20View%2C%20CA&offices[26]=New%20Albany%2C%20OH&offices[27]=New%20York%2C%20NY&offices[28]=Newton%20County%2C%20GA&offices[29]=Northridge%2C%20CA&offices[30]=Pittsburgh%2C%20PA&offices[31]=Prineville%2C%20OR&offices[32]=Redmond%2C%20WA&offices[33]=Remote%2C%20US&offices[34]=Reston%2C%20VA&offices[35]=San%20Francisco%2C%20CA&offices[36]=Santa%20Clara%2C%20CA&offices[37]=Sarpy%20County%2C%20NE&offices[38]=Sausalito%2C%20CA&offices[39]=Seattle%2C%20WA&offices[40]=Sunnyvale%2C%20CA&offices[41]=Washington%2C%20DC&roles[0]=full-time&is_leadership=0&teams[0]=Data%20%26%20Analytics&is_in_page=0',
    'Software Engineering': 'https://www.facebook.com/careers/jobs/?offices[0]=Altoona%2C%20IA&offices[1]=Ashburn%2C%20VA&offices[2]=Atlanta%2C%20GA&offices[3]=Austin%2C%20TX&offices[4]=Bellevue%2C%20WA&offices[5]=Boston%2C%20MA&offices[6]=Burlingame%2C%20CA&offices[7]=Chicago%2C%20IL&offices[8]=Dallas%2C%20TX&offices[9]=DeKalb%2C%20IL&offices[10]=Denver%2C%20CO&offices[11]=Detroit%2C%20MI&offices[12]=Eagle%20Mountain%2C%20Utah&offices[13]=Forest%20City%2C%20NC&offices[14]=Fort%20Worth%2C%20TX&offices[15]=Foster%20City%2C%20CA&offices[16]=Fremont%2C%20CA&offices[17]=Gallatin%2C%20TN&offices[18]=Henrico%2C%20VA&offices[19]=Huntsville%2C%20AL&offices[20]=Irvine%2C%20CA&offices[21]=Los%20Angeles%2C%20CA&offices[22]=Los%20Lunas%2C%20NM&offices[23]=Menlo%20Park%2C%20CA&offices[24]=Miami%2C%20Florida&offices[25]=Mountain%20View%2C%20CA&offices[26]=New%20Albany%2C%20OH&offices[27]=New%20York%2C%20NY&offices[28]=Newton%20County%2C%20GA&offices[29]=Northridge%2C%20CA&offices[30]=Pittsburgh%2C%20PA&offices[31]=Prineville%2C%20OR&offices[32]=Redmond%2C%20WA&offices[33]=Remote%2C%20US&offices[34]=Reston%2C%20VA&offices[35]=San%20Francisco%2C%20CA&offices[36]=Santa%20Clara%2C%20CA&offices[37]=Sarpy%20County%2C%20NE&offices[38]=Sausalito%2C%20CA&offices[39]=Seattle%2C%20WA&offices[40]=Sunnyvale%2C%20CA&offices[41]=Washington%2C%20DC&roles[0]=full-time&is_leadership=0&teams[0]=Software%20Engineering&is_in_page=0',
    'Research Scientist': 'https://www.facebook.com/careers/jobs/?offices[0]=Altoona%2C%20IA&offices[1]=Ashburn%2C%20VA&offices[2]=Atlanta%2C%20GA&offices[3]=Austin%2C%20TX&offices[4]=Bellevue%2C%20WA&offices[5]=Boston%2C%20MA&offices[6]=Burlingame%2C%20CA&offices[7]=Chicago%2C%20IL&offices[8]=Dallas%2C%20TX&offices[9]=DeKalb%2C%20IL&offices[10]=Denver%2C%20CO&offices[11]=Detroit%2C%20MI&offices[12]=Eagle%20Mountain%2C%20Utah&offices[13]=Forest%20City%2C%20NC&offices[14]=Fort%20Worth%2C%20TX&offices[15]=Foster%20City%2C%20CA&offices[16]=Fremont%2C%20CA&offices[17]=Gallatin%2C%20TN&offices[18]=Henrico%2C%20VA&offices[19]=Huntsville%2C%20AL&offices[20]=Irvine%2C%20CA&offices[21]=Los%20Angeles%2C%20CA&offices[22]=Los%20Lunas%2C%20NM&offices[23]=Menlo%20Park%2C%20CA&offices[24]=Miami%2C%20Florida&offices[25]=Mountain%20View%2C%20CA&offices[26]=New%20Albany%2C%20OH&offices[27]=New%20York%2C%20NY&offices[28]=Newton%20County%2C%20GA&offices[29]=Northridge%2C%20CA&offices[30]=Ottawa%2C%20Canada&offices[31]=Pittsburgh%2C%20PA&offices[32]=Prineville%2C%20OR&offices[33]=Redmond%2C%20WA&offices[34]=Remote%2C%20US&offices[35]=Reston%2C%20VA&offices[36]=San%20Francisco%2C%20CA&offices[37]=Santa%20Clara%2C%20CA&offices[38]=Sarpy%20County%2C%20NE&offices[39]=Sausalito%2C%20CA&offices[40]=Seattle%2C%20WA&offices[41]=Sunnyvale%2C%20CA&offices[42]=Washington%2C%20DC&roles[0]=full-time&teams[0]=Research',
    'People & Recruiting': 'https://www.facebook.com/careers/jobs/?offices[0]=Altoona%2C%20IA&offices[1]=Ashburn%2C%20VA&offices[2]=Atlanta%2C%20GA&offices[3]=Austin%2C%20TX&offices[4]=Bellevue%2C%20WA&offices[5]=Boston%2C%20MA&offices[6]=Burlingame%2C%20CA&offices[7]=Chicago%2C%20IL&offices[8]=Dallas%2C%20TX&offices[9]=DeKalb%2C%20IL&offices[10]=Denver%2C%20CO&offices[11]=Detroit%2C%20MI&offices[12]=Eagle%20Mountain%2C%20Utah&offices[13]=Forest%20City%2C%20NC&offices[14]=Fort%20Worth%2C%20TX&offices[15]=Foster%20City%2C%20CA&offices[16]=Fremont%2C%20CA&offices[17]=Gallatin%2C%20TN&offices[18]=Henrico%2C%20VA&offices[19]=Huntsville%2C%20AL&offices[20]=Irvine%2C%20CA&offices[21]=Los%20Angeles%2C%20CA&offices[22]=Los%20Lunas%2C%20NM&offices[23]=Menlo%20Park%2C%20CA&offices[24]=Miami%2C%20Florida&offices[25]=Mountain%20View%2C%20CA&offices[26]=New%20Albany%2C%20OH&offices[27]=New%20York%2C%20NY&offices[28]=Newton%20County%2C%20GA&offices[29]=Northridge%2C%20CA&offices[30]=Ottawa%2C%20Canada&offices[31]=Pittsburgh%2C%20PA&offices[32]=Prineville%2C%20OR&offices[33]=Redmond%2C%20WA&offices[34]=Remote%2C%20US&offices[35]=Reston%2C%20VA&offices[36]=San%20Francisco%2C%20CA&offices[37]=Santa%20Clara%2C%20CA&offices[38]=Sarpy%20County%2C%20NE&offices[39]=Sausalito%2C%20CA&offices[40]=Seattle%2C%20WA&offices[41]=Sunnyvale%2C%20CA&offices[42]=Washington%2C%20DC&roles[0]=full-time&teams[0]=People%20%26%20Recruiting',
    'Business Development & Partnerships': 'https://www.facebook.com/careers/jobs/?offices[0]=Altoona%2C%20IA&offices[1]=Ashburn%2C%20VA&offices[2]=Atlanta%2C%20GA&offices[3]=Austin%2C%20TX&offices[4]=Bellevue%2C%20WA&offices[5]=Boston%2C%20MA&offices[6]=Burlingame%2C%20CA&offices[7]=Chicago%2C%20IL&offices[8]=Dallas%2C%20TX&offices[9]=DeKalb%2C%20IL&offices[10]=Denver%2C%20CO&offices[11]=Detroit%2C%20MI&offices[12]=Eagle%20Mountain%2C%20Utah&offices[13]=Forest%20City%2C%20NC&offices[14]=Fort%20Worth%2C%20TX&offices[15]=Foster%20City%2C%20CA&offices[16]=Fremont%2C%20CA&offices[17]=Gallatin%2C%20TN&offices[18]=Henrico%2C%20VA&offices[19]=Huntsville%2C%20AL&offices[20]=Irvine%2C%20CA&offices[21]=Los%20Angeles%2C%20CA&offices[22]=Los%20Lunas%2C%20NM&offices[23]=Menlo%20Park%2C%20CA&offices[24]=Miami%2C%20Florida&offices[25]=Mountain%20View%2C%20CA&offices[26]=New%20Albany%2C%20OH&offices[27]=New%20York%2C%20NY&offices[28]=Newton%20County%2C%20GA&offices[29]=Northridge%2C%20CA&offices[30]=Ottawa%2C%20Canada&offices[31]=Pittsburgh%2C%20PA&offices[32]=Prineville%2C%20OR&offices[33]=Redmond%2C%20WA&offices[34]=Remote%2C%20US&offices[35]=Reston%2C%20VA&offices[36]=San%20Francisco%2C%20CA&offices[37]=Santa%20Clara%2C%20CA&offices[38]=Sarpy%20County%2C%20NE&offices[39]=Sausalito%2C%20CA&offices[40]=Seattle%2C%20WA&offices[41]=Sunnyvale%2C%20CA&offices[42]=Washington%2C%20DC&roles[0]=full-time&teams[0]=Business%20Development%20%26%20Partnerships',
    'Global Operations': 'https://www.facebook.com/careers/jobs/?offices[0]=Altoona%2C%20IA&offices[1]=Ashburn%2C%20VA&offices[2]=Atlanta%2C%20GA&offices[3]=Austin%2C%20TX&offices[4]=Bellevue%2C%20WA&offices[5]=Boston%2C%20MA&offices[6]=Burlingame%2C%20CA&offices[7]=Chicago%2C%20IL&offices[8]=Dallas%2C%20TX&offices[9]=DeKalb%2C%20IL&offices[10]=Denver%2C%20CO&offices[11]=Detroit%2C%20MI&offices[12]=Eagle%20Mountain%2C%20Utah&offices[13]=Forest%20City%2C%20NC&offices[14]=Fort%20Worth%2C%20TX&offices[15]=Foster%20City%2C%20CA&offices[16]=Fremont%2C%20CA&offices[17]=Gallatin%2C%20TN&offices[18]=Henrico%2C%20VA&offices[19]=Huntsville%2C%20AL&offices[20]=Irvine%2C%20CA&offices[21]=Los%20Angeles%2C%20CA&offices[22]=Los%20Lunas%2C%20NM&offices[23]=Menlo%20Park%2C%20CA&offices[24]=Miami%2C%20Florida&offices[25]=Mountain%20View%2C%20CA&offices[26]=New%20Albany%2C%20OH&offices[27]=New%20York%2C%20NY&offices[28]=Newton%20County%2C%20GA&offices[29]=Northridge%2C%20CA&offices[30]=Ottawa%2C%20Canada&offices[31]=Pittsburgh%2C%20PA&offices[32]=Prineville%2C%20OR&offices[33]=Redmond%2C%20WA&offices[34]=Remote%2C%20US&offices[35]=Reston%2C%20VA&offices[36]=San%20Francisco%2C%20CA&offices[37]=Santa%20Clara%2C%20CA&offices[38]=Sarpy%20County%2C%20NE&offices[39]=Sausalito%2C%20CA&offices[40]=Seattle%2C%20WA&offices[41]=Sunnyvale%2C%20CA&offices[42]=Washington%2C%20DC&roles[0]=full-time&teams[0]=Global%20Operations'
}


class FbJobsCrawler:
    def get_job_descriptions(self, link, category):
        driver = webdriver.Chrome(r"C:\Users\Sandi\PycharmProjects\selenium_driver\driver\chromedriver.exe")
        driver.get(link)
        driver.maximize_window()
        time.sleep(5)

        try:
            df = pd.read_excel('.\\Data\\Facebook\\Facebook_data_description.xlsx')
        except:
            df = pd.DataFrame(columns=['category', 'company', 'link', 'title', 'location_and_id', 'posting_date'])

        next_page_availability = True
        while next_page_availability:
            titles = driver.find_elements_by_class_name('_8sel')
            titles = [t.text for t in titles]

            links = driver.find_elements_by_class_name('_8sef')
            links = [l.get_attribute('href') for l in links]

            locations = []
            for i in range(1, 16):
                path = f'/html/body/div[1]/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[2]/div/div/div[3]/a[{i}]/div/div/div/div[3]/div[1]/div/div'
                try:
                    location = driver.find_element_by_xpath(path).text
                    location = re.search(".*,\s?([A-Z][A-Z]).*\+?", location).group(1)
                    locations.append(location)
                except Exception as e:
                    print(e)
                    break

            df1 = pd.DataFrame()
            df1['link'] = links
            df1['title'] = titles
            df1['location'] = locations
            df1['posting_date'] = 'NAL'
            df1['category'] = category
            df1['company'] = 'Facebook'
            df = df.append(df1, ignore_index=True)
            df1 = None

            next_page = driver.find_element_by_xpath(
                '/html/body/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[2]/div/div/div[4]/div[2]/a')
            if next_page.text == 'Next':
                next_page_availability = True
                next_page.click()
                time.sleep(5)
            elif next_page.text == 'Prev':
                try:
                    next_page = driver.find_element_by_xpath(
                        '/html/body/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[2]/div/div/div[4]/div[2]/a[2]')
                    next_page_availability = True
                    next_page.click()
                    time.sleep(5)
                except Exception as e:
                    print(e)
                    next_page_availability = False

        df.to_excel('.\\Data\\Facebook\\Facebook_data_description.xlsx')

    def get_qualifications(self):
        driver = webdriver.Chrome(r"C:\Users\Sandi\PycharmProjects\selenium_driver\driver\chromedriver.exe")
        input_df = pd.read_excel('.\\Data\\Facebook\\Facebook_data_description.xlsx')
        output_df = pd.DataFrame(columns=['link', 'description', 'basic_qualifications', 'preferred_qualifications'])

        for link in input_df.link:
            driver.get(link)

            # get description
            description = ''
            description_line, i = True, 1
            while description_line:
                try:
                    path = f'/html/body/div/div[1]/div[2]/div/div[3]/div[2]/div/div/div[1]/div[1]/div[3]/div[2]/div/ul/div[{i}]/li/div[3]/div/div'
                    desc = driver.find_element_by_xpath(path).text
                    description += desc + '\n'
                    i += 1
                except Exception as e:
                    print(e)
                    description_line = False

            # get minimum qualifications
            min_qualifications = ''
            description_line, i = True, 1
            while description_line:
                try:
                    path = f'/html/body/div/div[1]/div[2]/div/div[3]/div[2]/div/div/div[1]/div[1]/div[4]/div[2]/div/ul/div[{i}]/li/div[3]/div/div'
                    desc = driver.find_element_by_xpath(path).text
                    min_qualifications += desc + '\n'
                    i += 1
                except Exception as e:
                    print(e)
                    description_line = False

            # get Preferred Qualifications
            preferred_qualifications = ''
            description_line, i = True, 1
            while description_line:
                try:
                    path = f'/html/body/div/div[1]/div[2]/div/div[3]/div[2]/div/div/div[1]/div[1]/div[5]/div[2]/div/ul/div[{i}]/li/div[3]/div/div'
                    desc = driver.find_element_by_xpath(path).text
                    preferred_qualifications += desc + '\n'
                    i += 1
                except Exception as e:
                    print(e)
                    description_line = False

            output_df = output_df.append(
                {'link': link, 'description': description, 'basic_qualifications': min_qualifications,
                 'preferred_qualifications': preferred_qualifications}, ignore_index=True)

        output_df.to_excel(r'.\Data\Facebook\Facebook_data_qualifications.xlsx')


crawler = FbJobsCrawler()
for field, field_link in job_link_dictionary.items():
    crawler.get_job_descriptions(field_link, field)
crawler.get_qualifications()

