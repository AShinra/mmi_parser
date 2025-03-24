import os
from playwright.sync_api import sync_playwright
import streamlit as st
from streamlit_option_menu import option_menu
from fetchers.daily_tribune import dt_fetcher

# Ensure Playwright browsers are installed
os.system("playwright install chromium")

def get_section_links(url):
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

def main():
    url = st.text_input('Enter URL')
    button_process = st.button('Process Link')

    if button_process:
        if url:
            with st.spinner('Running App'):
                page_content = get_section_links(url)
                

if __name__ == '__main__':

    with st.sidebar():
        selected_publication = option_menu(
            menu_title='Publications',
            options=['Daily Tribune']
        )

    if selected_publication == 'Daily Tribune':
        dt_fetcher()



