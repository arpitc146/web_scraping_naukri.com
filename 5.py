import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

jobdata = []

for param in range(1,3):
    url = "https://www.naukri.com/web-developer-jobs?k=web%20developer&nignbevent_src=jobsearchDeskGNB"

    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(url)

    time.sleep(10)

    soup = BeautifulSoup(driver.page_source,'html5lib')

    # print(soup.prettify())

    driver.close()

    results = soup.find(class_='list')
    job_elems = results.find_all('article',class_='jobTuple')
    
    for job_elem in job_elems:
        
        #for url
        URL = job_elem.find('a',class_='title ellipsis').get('href')
        print('JOB URL: ' ,URL)
        

        #for title
        title = job_elem.find('a',class_='title ellipsis')
        print('JOB TITLE: ' ,title.text)
        

        #for rating
        rating_span = job_elem.find('span',class_ = 'starRating fleft')
        if rating_span is None:
            print('RATING: none rating')
            continue
        else:
            ratings = rating_span.text
        print('RATING: ' ,ratings)

        #for review
        review_span = job_elem.find('span',class_ = 'reviewsCount fleft')
        if review_span is None:
            print('REVIEW: non review')
            continue
        else:
            review = review_span.text
        print('REVIEW: ' ,review)    

        #for salary
        sal = job_elem.find('li',class_='fleft br2 placeHolderLi salary')
        sal_span = sal.find('span',class_='ellipsis fleft')
        
        if sal_span is None:
            continue
        else:
            salary = sal_span.text
        print('SALARY: ' ,salary)

        #location
        loc_span = job_elem.find('span',class_='ellipsis fleft locWdth')

        if loc_span is None:
            continue
        else:
            location = loc_span.text
        print('LOCATION: ',location)
        print('\n')
        data = {    
                'TITLE':title.text,
                'RATING':ratings,
                'REVIEW':review,
                'SALARY':salary,
                'LOCATION':location,
                'URL':URL
                }
        jobdata.append(data)

df = pd.DataFrame(jobdata)
out = "d3.xlsx"
df.to_excel(out, index=False)
driver.quit()