import os
from playwright.sync_api import sync_playwright
import streamlit as st
import json
import time
import re
import datetime

# Ensure Playwright browsers are installed
os.system("playwright install chromium")

def dt_fetcher(my_range):

    # get the start and end dates
    st_date = my_range[0].split('-')
    st.write(st_date)
    st_date = datetime.datetime(st_date[0], st_date[1], st_date[-1])
    st.write(st_date)

    en_date = my_range[-1].split('-')



    

    # get section links from json file
    with open('fetchers/sections_daily_tribune.json') as json_file:
        secs = json.load(json_file)
        
    pw = sync_playwright().start()

    # create a browser
    browser = pw.chromium.launch()

    # create a new page in the browser
    page = browser.new_page()
    
    # go to the sections
    for pub, sections in secs.items():
        for section in sections:
            _links = []
            page.goto(section)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            try:
                btn_load_more = page.wait_for_selector('div.arr--button')
            except:
                pass
            else:
                btn_load_more.click()
            
            links_container = page.wait_for_selector('div#container')
            links = links_container.query_selector_all('a')
            
            for link in links:
                if link != None:
                    _link = link.get_attribute('href')
                    if re.search('tribune.net.ph/\d{4}/\d+/\d+/', _link):
                        link_year = int(_link.split('/')[3])
                        link_month = int(_link.split('/')[4])
                        link_day = int(_link.split('/')[5])
                        link_date = datetime.datetime(link_year, link_month, link_day)
                        if link_date >= st_date and link_date <= en_date:
                            _links.append(link.get_attribute('href'))
            
            _links = list(dict.fromkeys(_links))
            st.write(_links)
        

    # menu = page.wait_for_selector('#footer-menu')
    # links = menu.query_selector_all('a')
    # st.write(type(links))
    # for link in links:
    #     st.write(link.get_attribute('href'))



    # x = page.screenshot(path='sample.png')
    # st.image(x)

    # return page.content()