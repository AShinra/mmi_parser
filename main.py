from playwright.sync_api import sync_playwright
import streamlit as st

def test(url):
    pw = sync_playwright().start()

    browser = pw.chromium.launch()

    page = browser.new_page()
    page.goto(url)

    return page.content()


url = st.text_input('Enter URL')

if url:
    x = test(url)
    st.write(x)