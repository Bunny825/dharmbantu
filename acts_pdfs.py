import requests
from bs4 import BeautifulSoup
import time

headers = {"User-Agent": "Mozilla/5.0"}
base_url = "https://www.indiacode.nic.in"

view_urls = []

# STEP 1: Loop through paginated list pages
for offset in range(0, 880, 20):
    page_url = f"{base_url}/handle/123456789/1362/browse?type=shorttitle&rpp=20&offset={offset}"
    print(f"🔄 Scraping page offset {offset}...")

    try:
        res = requests.get(page_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # Extract "View..." links
        for a in soup.find_all("a"):
            if a.text.strip().lower().startswith("view"):
                href = a.get("href")
                if href:
                    full_view_url = requests.compat.urljoin(page_url, href)
                    print(f"Found View link: {full_view_url}")
                    view_urls.append(full_view_url)

    except Exception as e:
        print(f"❌ Failed to load index page at offset {offset}: {e}")

# STEP 2: Extract only the FIRST PDF from each View page
pdf_links = []

for idx, url in enumerate(view_urls, 1):
    print(f"📄 ({idx}/{len(view_urls)}) Processing: {url}")
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        found = False

        for a in soup.find_all("a", href=True):
            href = a['href']
            if href.endswith(".pdf"):
                full_pdf = requests.compat.urljoin(url, href)
                pdf_links.append(full_pdf)
                print(f"  ✅ First PDF Found: {full_pdf}")
                found = True
                break  # ⛔ Only first PDF per page

        if not found:
            print("  ⚠️ No PDF found.")

        time.sleep(0.5)  # Be polite to the server

    except Exception as e:
        print(f"❌ Failed at {url}: {e}")

def get_acts():
    return pdf_links


# Final output
print("\n📦 PDF links collected:")

print(pdf_links)
print(f"\n🎯 Total PDFs found: {len(pdf_links)}")
