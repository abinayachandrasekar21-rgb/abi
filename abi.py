import re
import time, random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook

# --- Utility functions ---
def clean_text(s):
    """Remove extra whitespace and newlines"""
    if not s:
        return ""
    return re.sub(r"\s+", " ", s).strip()

def parse_date_posted(text):
    """Convert relative dates like '2 days ago' or 'Just posted' to YYYY-MM-DD"""
    today = datetime.today().date()
    t = text.lower()
    if "today" in t or "just posted" in t:
        return str(today)
    match = re.search(r"(\d+)\+?\s+day", t)
    if match:
        return str(today - timedelta(days=int(match.group(1))))
    return str(today)

# --- Selenium setup ---
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
options.add_argument("--headless=new")   # ✅ run Chrome in headless mode (no window open)

driver = webdriver.Chrome(options=options)

# --- Scraper ---
def scrape_indeed(job_title="Python Developer", location="Chennai", pages=1):
    base_url = f"https://in.indeed.com/jobs?q={job_title.replace(' ', '+')}&l={location.replace(' ', '+')}"
    all_jobs = []

    for page in range(pages):
        url = f"{base_url}&start={page*10}"
        print(f"\n🔎 Fetching page {page+1}: {url}")
        driver.get(url)
        time.sleep(random.uniform(3, 6))  # human-like delay

        # Scroll slowly
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        for i in range(0, scroll_height, 300):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(random.uniform(0.3, 0.8))

        # Wait for job cards
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.job_seen_beacon"))
            )
        except:
            print("⚠ No jobs found or page blocked")
            continue

        job_cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
        print(f"✅ Found {len(job_cards)} jobs on this page")

        for card in job_cards:
            # --- Title ---
            title = clean_text(card.find_element(By.CSS_SELECTOR, "h2.jobTitle").text) if card.find_elements(By.CSS_SELECTOR, "h2.jobTitle") else ""

            # --- Company ---
            company = clean_text(card.find_element(By.CSS_SELECTOR, "span.companyName").text) if card.find_elements(By.CSS_SELECTOR, "span.companyName") else ""

            # --- Location ---
            location_ = ""
            if card.find_elements(By.CSS_SELECTOR, "div.companyLocation"):
                location_ = clean_text(card.find_element(By.CSS_SELECTOR, "div.companyLocation").text)
            elif card.find_elements(By.CSS_SELECTOR, "span.location"):
                location_ = clean_text(card.find_element(By.CSS_SELECTOR, "span.location").text)
            elif card.find_elements(By.CSS_SELECTOR, "div.company_location"):
                location_ = clean_text(card.find_element(By.CSS_SELECTOR, "div.company_location").text)

            # --- Salary ---
            salary = ""
            if card.find_elements(By.CSS_SELECTOR, "div.salary-snippet"):
                salary = clean_text(card.find_element(By.CSS_SELECTOR, "div.salary-snippet").text)
            elif card.find_elements(By.CSS_SELECTOR, "span.salary-snippet-container"):
                salary = clean_text(card.find_element(By.CSS_SELECTOR, "span.salary-snippet-container").text)
            elif card.find_elements(By.CSS_SELECTOR, "div.metadata.salary-snippet-container"):
                salary = clean_text(card.find_element(By.CSS_SELECTOR, "div.metadata.salary-snippet-container").text)

            # --- Date Posted ---
            date_posted = parse_date_posted(clean_text(card.find_element(By.CSS_SELECTOR, "span.date").text)) if card.find_elements(By.CSS_SELECTOR, "span.date") else ""

            # --- Summary ---
            summary = clean_text(card.find_element(By.CSS_SELECTOR, "div.job-snippet").text) if card.find_elements(By.CSS_SELECTOR, "div.job-snippet") else ""

            # --- Link ---
            link = card.find_element(By.CSS_SELECTOR, "h2.jobTitle a").get_attribute("href") if card.find_elements(By.CSS_SELECTOR, "h2.jobTitle a") else ""

            # --- Append Job ---
            all_jobs.append({
                "Title": title,
                "Company": company,
                "Location": location_,
                "Salary": salary,
                "Date Posted": date_posted,
                "Summary": summary,
                "Link": link
            })

    return all_jobs

# --- Scrape and save to Excel ---
jobs = scrape_indeed(pages=1)
wb = Workbook()
ws = wb.active
ws.title = "Indeed Jobs"

# Write headers
headers = ["Title", "Company", "Location", "Salary", "Date Posted", "Summary", "Link"]
ws.append(headers)

# Write job data
for job in jobs:
    ws.append([job[h] for h in headers])

wb.save("scraper_jobs.xlsx")
print(f"\n🎉 Done! Saved {len(jobs)} jobs to scraper_jobs.xlsx")

driver.quit()