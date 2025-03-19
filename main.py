import os
import streamlit as st
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth

# Ensure Playwright browsers are installed (without sudo)
if not os.path.exists(os.path.expanduser("~/.cache/ms-playwright")):
    st.warning("Installing Playwright Chromium... This may take a minute.")
    os.system("playwright install chromium --with-deps")
    st.success("Chromium installed successfully!")

def get_links(url):
    """Extract links from a webpage using Playwright."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Run non-headless to bypass Cloudflare
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        page = context.new_page()
        stealth(page)  # Hide automation signals
        page.goto(url, timeout=90000, wait_until="domcontentloaded")

        # Extract all links
        links = page.eval_on_selector_all("a", "elements => elements.map(e => e.href)")

        browser.close()
    return links

def main_scraper():
    st.title("Cloudflare Bypass Scraper (Playwright)")
    url = st.text_input("Enter a URL to extract links:")

    if st.button("Extract Links"):
        if url:
            with st.spinner("Extracting links..."):
                try:
                    links = get_links(url)
                    if links:
                        st.success(f"Found {len(links)} links!")
                        st.write("\n".join(links))
                    else:
                        st.warning("No links found.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main_scraper()
