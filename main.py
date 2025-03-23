from playwright.sync_api import sync_playwright
import streamlit as st

url = st.text_input('Enter URL')

pw = sync_playwright().start()

browser = pw.chromium.launch()

page = browser.new_page()
page.goto(url)

page.screenshot(path='sample.png')