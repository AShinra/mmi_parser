import os
import streamlit as st
from playwright.sync_api import sync_playwright

# Install missing Playwright dependencies on Streamlit Cloud
if not os.path.exists("/root/.cache/ms-playwright"):
    st.warning("Installing Playwright Chromium & dependencies... Please wait.")
    os.system("playwright install --with-deps chromium")
    st.success("Chromium installed successfully!")

def get_page_source(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Headless mode
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto(url, timeout=60000)  # Load the page

        html = page.content()  # Get page source after JavaScript execution
        browser.close()

    return html[:2000]  # Return first 2000 chars

def main_scraper():
    st.title("Cloudflare Bypass Scraper (Playwright)")
    url = st.text_input("Enter a URL to scrape:")

    if st.button("Scrape"):
        if url:
            with st.spinner("Scraping..."):
                try:
                    page_content = get_page_source(url)
                    st.success("Scraping completed!")
                    st.text_area("Page Source:", page_content)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main_scraper()
