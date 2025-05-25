

import requests
from bs4 import BeautifulSoup

def scrape_remoteok(resume_skills):
    url = "https://remoteok.com/remote-dev-jobs"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ RemoteOK request failed: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = []

    for job in soup.find_all("tr", class_="job"):
        title = job.find("h2")
        company = job.find("h3")
        link = job.get("data-href")
        tags = job.find_all("span", class_="tag")

        if title and company and link:
            title_text = title.text.strip().lower()
            tag_text = [t.text.lower() for t in tags]
            combined = title_text + " " + " ".join(tag_text)

            # Match with any resume skill (case insensitive)
            if any(skill.lower() in combined for skill in resume_skills):
                jobs.append({
                    'title': title.text.strip(),
                    'company': company.text.strip(),
                    'link': f"https://remoteok.com{link}",
                    'source': 'RemoteOK'
                })
    return jobs

def scrape_weworkremotely(resume_skills):
    url = "https://weworkremotely.com/remote-jobs/search?term=developer"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ WeWorkRemotely request failed: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = []

    for section in soup.find_all("section", class_="jobs"):
        for job in section.find_all("li", class_="feature"):
            link_tag = job.find("a", href=True)
            if link_tag:
                title = job.find("span", class_="title")
                company = job.find("span", class_="company")
                link = "https://weworkremotely.com" + link_tag['href']

                if title and company:
                    job_text = (title.text + " " + company.text).lower()
                    if any(skill.lower() in job_text for skill in resume_skills):
                        jobs.append({
                            'title': title.text.strip(),
                            'company': company.text.strip(),
                            'link': link,
                            'source': 'WeWorkRemotely'
                        })
    return jobs

def scrape_all_jobs(resume_skills):
    jobs = []
    try:
        jobs += scrape_remoteok(resume_skills)
    except Exception as e:
        print("❌ RemoteOK scrape failed:", e)
    try:
        jobs += scrape_weworkremotely(resume_skills)
    except Exception as e:
        print("❌ WeWorkRemotely scrape failed:", e)

    print(f"✅ Matched Jobs Found: {len(jobs)}")
    return jobs

if __name__ == "__main__":
    skills = ["python", "react", "node.js", "docker"]
    matched_jobs = scrape_all_jobs(skills)
    for job in matched_jobs:
        print(f"🔹 {job['title']} at {job['company']} ({job['source']})")
        print(f"🔗 {job['link']}\n")
