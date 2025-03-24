import os
from playwright.sync_api import sync_playwright
import streamlit as st
from streamlit_option_menu import option_menu
from fetchers.fetcher_daily_tribune import dt_fetcher
import streamlit_shadcn_ui as ui

# Ensure Playwright browsers are installed
os.system("playwright install chromium")

if __name__ == '__main__':

    # with st.sidebar:
    #     selected_publication = option_menu(
    #         menu_title='Publications',
    #         options=['Daily Tribune']
    #     )

    # if selected_publication == 'Daily Tribune':
    #     dt_fetcher()

    my_range = ui.date_picker('DATE RANGE', mode='range', key='my_range', default_value=None)

    pub_name = st.selectbox(
        label='Publication',
        options=['Daily Tribune']
        )
    
    btn_process = st.button(label='Fetch URLS')

    if btn_process:
        if pub_name == 'Daily Tribune':
            with st.spinner('Fetching Links'):
                dt_fetcher(my_range)



