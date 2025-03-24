import os
from playwright.sync_api import sync_playwright
import streamlit as st
import json

# Ensure Playwright browsers are installed
os.system("playwright install chromium")

def dt_fetcher():

    # get section links from json file
    with open('fetchers/sections_daily_tribune.json') as json_file:
        secs = json.load(json_file)
        
    pw = sync_playwright().start()

    # create a browser
    browser = pw.chromium.launch(headless=False, timeout=10000)

    # create a new page in the browser
    page = browser.new_page()
    
    # go to the sections
    for pub, sections in secs.items():
        st.write(sections)
        # for section in sections:
        #     st.write(section)
        #     page.goto(section)

        #     links_container = page.wait_for_selector('div#container')
        #     links = links_container.query_selector_all('a')
        #     for link in links:
        #         st.write(link.get_attribute('href'))
        

    # menu = page.wait_for_selector('#footer-menu')
    # links = menu.query_selector_all('a')
    # st.write(type(links))
    # for link in links:
    #     st.write(link.get_attribute('href'))



    # x = page.screenshot(path='sample.png')
    # st.image(x)

    # return page.content()