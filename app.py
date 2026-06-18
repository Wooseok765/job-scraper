from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

app = Flask(__name__)

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.5",
}


def scrape_berlin_jobs(keyword):
    jobs = []

    url = f"https://berlinstartupjobs.com/skill-areas/{keyword}/"

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        job_posts = soup.find_all("article")

        for post in job_posts:
            title_tag = post.find("h2")
            company_tag = post.find("a", class_="bjs-jlid__b")
            link_tag = post.find("a")

            if title_tag:
                title = title_tag.get_text(strip=True)
            else:
                continue

            if company_tag:
                company = company_tag.get_text(strip=True)
            else:
                company = "Unknown"

            if link_tag:
                link = link_tag.get("href")
            else:
                link = "#"

            jobs.append({
                "title": title,
                "company": company,
                "location": "Berlin",
                "link": link,
                "source": "Berlin Startup Jobs"
            })

    except Exception:
        pass

    return jobs


def scrape_web3_jobs(keyword):
    jobs = []

    url_keyword = quote_plus(keyword)
    url = f"https://web3.career/{url_keyword}-jobs"

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        job_rows = soup.find_all("tr", class_="table_row")

        for row in job_rows:
            title_tag = row.find("h2")
            company_tag = row.find("h3")
            link_tag = row.find("a")

            if title_tag:
                title = title_tag.get_text(strip=True)
            else:
                continue

            if company_tag:
                company = company_tag.get_text(strip=True)
            else:
                company = "Unknown"

            if link_tag:
                link = link_tag.get("href")

                if link and link.startswith("/"):
                    link = "https://web3.career" + link
            else:
                link = "#"

            jobs.append({
                "title": title,
                "company": company,
                "location": "Remote / Web3",
                "link": link,
                "source": "Web3 Career"
            })

    except Exception:
        pass

    return jobs


def scrape_wework_jobs(keyword):
    jobs = []

    url_keyword = quote_plus(keyword)
    url = (
        "https://weworkremotely.com/remote-jobs/search"
        f"?term={url_keyword}"
    )

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        job_posts = soup.find_all("li", class_="feature")

        for post in job_posts:
            title_tag = post.find("span", class_="title")
            company_tag = post.find("span", class_="company")
            region_tag = post.find("span", class_="region")
            link_tag = post.find("a")

            if title_tag:
                title = title_tag.get_text(strip=True)
            else:
                continue

            if company_tag:
                company = company_tag.get_text(strip=True)
            else:
                company = "Unknown"

            if region_tag:
                location = region_tag.get_text(strip=True)
            else:
                location = "Remote"

            if link_tag:
                link = link_tag.get("href")

                if link and link.startswith("/"):
                    link = "https://weworkremotely.com" + link
            else:
                link = "#"

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "link": link,
                "source": "We Work Remotely"
            })

    except Exception:
        pass

    return jobs


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")

    if not keyword:
        return render_template("home.html")

    berlin_jobs = scrape_berlin_jobs(keyword)
    web3_jobs = scrape_web3_jobs(keyword)
    wework_jobs = scrape_wework_jobs(keyword)

    jobs = berlin_jobs + web3_jobs + wework_jobs

    return render_template(
        "results.html",
        keyword=keyword,
        jobs=jobs
    )


if __name__ == "__main__":
    app.run(debug=True)