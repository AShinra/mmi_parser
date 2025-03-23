from playwright_stealth import stealth
from playwright.sync_api import sync_playwright
import streamlit as st

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    stealth(page)  # Apply stealth plugin

    page.goto("https://businessmirror.com.ph/")
    st.write(page.title())

    browser.close()
