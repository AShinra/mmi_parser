from playwright.sync_api import sync_playwright
import streamlit as st

def get_page_content(url):
    pw = sync_playwright().start()

    browser = pw.chromium.launch()

    page = browser.new_page()
    page.goto(url)

    return page.content()


if __name__ == '__main__':
    url = st.text_input('Enter URL')

    if url:
        page_content = get_page_content(url)
    