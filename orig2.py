import os
import streamlit as st
from playwright.sync_api import sync_playwright
import random

# Ensure Playwright browsers are installed
os.system("playwright install chromium")

# List of random user-agents to bypass detection
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
]

def get_links(url):
    """Extracts all links from a given URL using Playwright after removing ads."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=random.choice(USER_AGENTS),
                java_script_enabled=True,
                storage_state="default"
            )
            page = context.new_page()
            page.goto(url, timeout=60000)
            
            # Wait until the page is fully loaded
            page.wait_for_selector("body", state="visible", timeout=10000)

            # Remove ads before extracting content
            ad_selectors = [
                "iframe",  # Commonly used for ads
                "[id*='ads']", "[class*='ads']", "[data-ad]",  # Various ad-related elements
                "[aria-label='advertisement']"
            ]
            for selector in ad_selectors:
                try:
                    page.wait_for_selector(selector, state="visible", timeout=5000)
                    page.eval_on_selector_all(selector, "elements => elements.forEach(e => e.remove())")
                except:
                    pass  # Ignore errors if the element is not found or not visible

            # Extract cleaned page content
            st.write(page.content())
            
            # Extract all anchor (<a>) tag links
            # page.wait_for_selector("a", state="visible", timeout=5000)
            page.wait_for_function("meta.content === 'BusinessMirror'", timeout=10000)
            links = page.eval_on_selector_all("a", "elements => elements.map(e => e.href)")

            browser.close()
        return links
    except Exception as e:
        return [f"Error: {e}"]

def main_scraper():
    st.title("Extract Links from a Webpage (Playwright)")
    url = st.text_input("Enter a URL to extract links:")

    if st.button("Extract Links"):
        if url:
            with st.spinner("Extracting links..."):
                try:
                    links = get_links(url)
                    if links and "Error" not in links[0]:
                        st.success(f"Found {len(links)} links!")
                        st.write("\n".join(links))  # Display all links
                    else:
                        st.warning("No links found on the page or an error occurred.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main_scraper()
