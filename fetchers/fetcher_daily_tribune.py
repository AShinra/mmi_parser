import os
from playwright.sync_api import sync_playwright
import streamlit as st
import json
import time
import re

# Ensure Playwright browsers are installed
os.system("playwright install chromium")

def dt_fetcher(my_range):

    st_year = my_range[0].split('-')[0]
    st_month = my_range[0].split('-')[1]
    st_day = my_range[0].split('-')[-1]


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
                    link_date = _link.split('/')[3]
                    st.write(link_date)
                    if re.search('tribune.net.ph/\d{4}/\d+/\d+/', link.get_attribute('href')):
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