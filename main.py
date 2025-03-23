import os
from playwright.sync_api import sync_playwright
import streamlit as st

# Ensure Playwright browsers are installed
os.system("playwright install chromium")

def get_page_content(url):
    pw = sync_playwright().start()

    browser = pw.chromium.launch()

    page = browser.new_page()
    page.goto(url)

    return page.content()


url = st.text_input('Enter URL')
button_process = st.button('Process Link')

if button_process:
    if url:
        with st.spinner('Running App'):
            page_content = get_page_content(url)
            st.write(page_content)



