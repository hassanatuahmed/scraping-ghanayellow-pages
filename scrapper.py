import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

from time import sleep
from random import randint

headers = {"Accept-Language": "en-US,en;q=0.5"}
browse_page = requests.get("https://www.ghanayello.com/browse-business-directory", headers=headers)
soup = BeautifulSoup(browse_page.text, 'html.parser')
cat_urls=soup.find_all('ul', class_="cat_list")
for cat_url in cat_urls:
  categories = cat_url.find_all('li')
  for category in categories:
    #names = []
    phones = []
    #addresses = []
    ratings = []
    #cat_url_list = []
    business_names = []
    urls =  category.find('a',href=True)
    category_url =  urls['href']
    name = category.a.text
    number_of_records_string = category.span.text
    number_of_records = int(number_of_records_string.replace(',',''))
    numberOfPages = 1
    print(number_of_records)
    if(number_of_records%30 ==0):
      numberOfPages = number_of_records//30
    else:
      numberOfPages = (number_of_records//30)+1

    for i in range(1,numberOfPages+1):
      if(i ==1):
          cat_page_url = "https://www.ghanayello.com"+category_url
      else:
          cat_page_url = "https://www.ghanayello.com"+category_url+"/"+str(i)
      print(cat_page_url)
      cat_page = requests.get(cat_page_url, headers=headers)
      soup_2 = BeautifulSoup(cat_page.text, 'html.parser')
      company_div_1 = soup_2.find_all('div', class_="with_img")
      company_div_2 = soup_2.find_all('div', class_='company g_0')
      company_div = company_div_1 + company_div_2
      # sleep(randint(1,2))
      for company_details in company_div:
        bs_name = company_details.h4.a.text
        business_names.append(bs_name)
        rate = company_details.find('div', class_='rate').text if  company_details.find('div', class_='rate') else ''
        ratings.append(rate)
        urls =  company_details.h4.find('a', href=True)
        company_url =  urls['href']
        company_page = requests.get("https://www.ghanayello.com"+company_url, headers=headers)
        soup = BeautifulSoup(company_page.text, 'html.parser')
        phone=soup.find('div', class_='text phone').text if  soup.find('div', class_='text phone') else ''
        phones.append(phone)
        print(business_names)
        # sleep(randint(1,2))
    data = pd.DataFrame({
    'Business': business_names,
    'Ratings':ratings,
    'Phones':phones
    })
    print(data)
    data.to_csv(name+' category.csv')