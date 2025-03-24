import os
from playwright.sync_api import sync_playwright
import streamlit as st
from streamlit_option_menu import option_menu
from fetchers.fetcher_daily_tribune import dt_fetcher
from streamlit_datetime_picker import date_time_picker, date_range_picker

# Ensure Playwright browsers are installed
os.system("playwright install chromium")
               
dt = date_time_picker('Date Time Input')
st.write(f"DateTimeInput: {dt}")
(start, end) = date_range_picker()
st.write(f"DateRangeInput: From {start} to {end}")

if __name__ == '__main__':

    # with st.sidebar:
    #     selected_publication = option_menu(
    #         menu_title='Publications',
    #         options=['Daily Tribune']
    #     )

    # if selected_publication == 'Daily Tribune':
    #     dt_fetcher()


    pub_name = st.selectbox(
        label='Publication',
        options=['Daily Tribune']
        )
    
    btn_process = st.button(label='Fetch URLS')

    if btn_process:
        if pub_name == 'Daily Tribune':
            dt_fetcher()



