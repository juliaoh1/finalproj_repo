#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Julia Coxen
SI507. Disucssion 001: Tuesdays 4pm
With help from: Glen Bredin
"""
#Import useful packages
import time
#import schedule
import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
ua = UserAgent()

#start process_time to calculate how long it takes to run 
start = time.process_time() 

def scrape_rubratings():
    
    datestr = time.strftime("%Y%m%d")
    timestr = time.strftime("%Y%m%d-%H%M%S")
    print('Scraping RubRatings at {}'.format(timestr))
    
    #The URL that displays states and cities on rubratings
    user_agent = {'User-agent': ua.random} 
    url = 'http://rubratings.com/cities/'
    
    #Get the URL
#    R = requests.get(url)
    R = requests.get(url, headers=user_agent)
    R.raise_for_status
    
    #Get HTML of URL
    soup = BeautifulSoup(R.content, 'html.parser')
    states = soup.find_all('dt')
    
    #init a list to store data in
    data = []

    #iterate through each state
    for state in states:
        state = str(state)
        state = state[4:-5]
        #Get all cities for each state
        citysoup = BeautifulSoup(R.content, 'html.parser')
        cities = citysoup.find_all('dd')
        #Iterate through each city
        for city in cities:
            city = str(city)
            city = city[12:-9]
            citysplit = city.split('>')
            #Citylink is the url to open each specific city page on rubratings
            citylink = citysplit[0]
            citylink = citylink[1:-1]
            #City is the city name that will be stored to the final df
            city = citysplit[1]
            #Get the city url
            R = requests.get(citylink)
            R.raise_for_status()
            soup = BeautifulSoup(R.content, 'html.parser')
            #Look through city url and get all individual listings for city
            listings = soup.find_all('div', class_ = 'listing')
            #Iterate through all of the listings
            for listing in listings: 
                try: 
                    id_number = listing.get('id')
                    ad_url = citylink + "/" + id_number
                    R = requests.get(ad_url)
                    R.raise_for_status()
                    soup_ad = BeautifulSoup(R.content, 'html.parser')
                    info = soup_ad.find_all('ul', class_='info')
                    items = info[0].find_all('li')
                    #phoneinfo = info[0].find_all('a')
                    for item in items:
                        txt = item.text
                        if 'Location' in txt:
                            location = txt.replace('Location: ','')
                        if 'Phone:' in txt:
                            phone = item.find_all('a', class_='phone-replace')
                            number = phone[0].get('data-replace')
                            areacode = number[1:4]
                            middle_three = number[6:9]
                            last_four = number[10:14]
                        if 'Latest Activity' in txt:
                            date = txt.replace('Latest Activity: ','')
                    description = soup_ad.find_all('p', class_='description')[0].text
                    data.append((id_number,date,description,location, state, city,
                                 number, areacode, middle_three, last_four, datestr))
                    time.sleep(0.05)
                except:
                    time.sleep(0.05)
    
    df = pd.DataFrame(data, columns=['pageid','date','description','location', 'state', 'city'
                                     ,'phone_number', 'area_code', 'middle_three', 'last_four'
                                     , 'date_scraped'])
     
    df.to_csv("RubRatings_Data_{}".format(datestr) + ".csv", mode = 'w', header = True) 
    
    timestr = time.strftime("%Y%m%d-%H%M%S")
    print('Stopped scraping RubRatings at {}'.format(timestr))
    

scrape_rubratings()    
#schedule.every().day.at("22:00").do(scrape_rubratings)
#
#while True:
#    schedule.run_pending()
#    time.sleep(1)           

#Figure out the processing run time of the program
elapsed = (time.process_time() - start, 'seconds')    
print('Process time is = ', elapsed)