import os
from playwright.sync_api import sync_playwright
import streamlit as st
from streamlit_option_menu import option_menu
from fetchers.fetcher_daily_tribune import dt_fetcher

# Ensure Playwright browsers are installed
os.system("playwright install chromium")
               

if __name__ == '__main__':

    with st.sidebar:
        selected_publication = option_menu(
            menu_title='Publications',
            options=['Daily Tribune']
        )

    if selected_publication == 'Daily Tribune':
        dt_fetcher()



