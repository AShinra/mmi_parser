from playwright.sync_api import sync_playwright
import streamlit as st

def test(url):
    pw = sync_playwright().start()

    browser = pw.chromium.launch()

    page = browser.new_page()
    page.goto(url)

    x = page.screenshot(path='sample.png')

    st.image(x)


url = st.text_input('Enter URL')

if url:
    test(url)