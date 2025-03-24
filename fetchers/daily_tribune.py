import os
from playwright.sync_api import sync_playwright
import streamlit as st
from streamlit_option_menu import option_menu

# Ensure Playwright browsers are installed
os.system("playwright install chromium")

def dt_fetcher(url):
    pw = sync_playwright().start()

    browser = pw.chromium.launch()

    page = browser.new_page()
    page.goto(url)

    menu = page.wait_for_selector('#footer-menu')
    links = menu.query_selector_all('a')
    st.write(type(links))
    for link in links:
        st.write(link.get_attribute('href'))



    x = page.screenshot(path='sample.png')
    st.image(x)

    return page.content()