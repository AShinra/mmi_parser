import streamlit as st
import cloudscraper
from bs4 import BeautifulSoup

def get_page_source(url):
    scraper = cloudscraper.create_scraper()  # Bypasses Cloudflare
    response = scraper.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.prettify()[:2000]  # Return first 2000 chars
    else:
        return f"Error: Received status code {response.status_code}"

def main_scraper():
    st.title("Cloudflare Bypass Scraper with Streamlit")
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
