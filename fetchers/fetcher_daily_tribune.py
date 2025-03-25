import os
from playwright.sync_api import sync_playwright
import streamlit as st
import json
import time
import re
import datetime
import pandas as pd

# Ensure Playwright browsers are installed
os.system("playwright install chromium")

def dt_fetcher(my_range):

    # get the start and end dates
    st_date = my_range[0].split('-')
    st_date = datetime.datetime(int(st_date[0]), int(st_date[1]), int(st_date[-1]))

    en_date = my_range[-1].split('-')
    en_date = datetime.datetime(int(en_date[0]), int(en_date[1]), int(en_date[-1]))
  

    # get section links from json file
    with open('fetchers/sections_daily_tribune.json') as json_file:
        secs = json.load(json_file)
        
    pw = sync_playwright().start()

    # create a browser
    browser = pw.chromium.launch()

    # create a new page in the browser
    page = browser.new_page()
    
    # go to the sections
    _links = []
    _date = []
    _title = []
    link_dict = {}
    for pub, sections in secs.items():
        for section in sections:
            page.goto(section)

            for i in range(1, 5, 1):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                try:
                    btn_load_more = page.wait_for_selector('div.arr--button', timeout=10000)
                except:
                    pass
                else:
                    btn_load_more.click()
                
                st.write(i)
            
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
                        link_title = link.text_content()
                        if link_date >= st_date and link_date <= en_date:
                            if _link not in _links:
                                _links.append(_link)
                                _date.append(link_date)
                                _title.append(link_title)
                                st.write(f'---{link_title}---')
                                link_dict['DATE'] = _date
                                link_dict['TITLE'] = _title
                                link_dict['URL'] = _links
            
            
    df = pd.DataFrame(link_dict)
    st.dataframe(df)
        

    