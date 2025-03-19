import os
import streamlit as st
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth  # Hide bot detection

# Ensure Playwright browsers are installed (without sudo)
PLAYWRIGHT_DIR = os.path.expanduser("~/.cache/ms-playwright")

if not os.path.exists(PLAYWRIGHT_DIR):
    st.warning("Installing Playwright Chromium... This may take a minute.")
    os.system("playwright install chromium --with-deps")
    st.success("Chromium installed successfully!")

def get_links(url):
    """Extracts all links from a webpage while bypassing Cloudflare."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Run non-headless to bypass detection
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},  # Standard screen size
        )
        
        page = context.new_page()
        stealth(page)  # Apply stealth mode to bypass detection

        try:
            page.goto(url, timeout=90000, wait_until="domcontentloaded")  # Wait for JS to execute
            
            # Simulate human-like scrolling
            page.mouse.wheel(0, 500)
            page.wait_for_timeout(2000)  # Wait for Cloudflare to process

            # Extract all anchor (`<a>`) tag links
            links = page.eval_on_selector_all("a", "elements => elements.map(e => e.href)")

        except Exception as e:
            st.error(f"Error: {e}")
            links = []

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
                        st.write("\n".join(links))  # Display all links
                    else:
                        st.warning("No links found on the page.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a valid URL.")

if __name__ == "__main__":
    main_scraper()
