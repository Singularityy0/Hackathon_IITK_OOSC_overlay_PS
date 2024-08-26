import requests
import json
from bs4 import BeautifulSoup
import csv
import os

Tsite = input('Enter a site to scrape: ')
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0"}

filename = "Links_Titles.csv"


response = requests.get(Tsite, headers=headers)
print(f"Status code: {response.status_code}")


soup = BeautifulSoup(response.content, 'html.parser')


with open(filename, 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)


    csvfile.seek(0, 2)
    if csvfile.tell() == 0:
        csvwriter.writerow(['Link', 'Name'])

    for link in soup.find_all('a', href=True):
        href = link['href']
        title = link.get_text(strip=True)
        if title:
            csvwriter.writerow([href, title])

print(f"All links have been appended to {filename}")

def savejson(link, title, content, folder='scraped_data'):
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = os.path.join(folder, f"{title.replace(' ', '_').replace('/', '_')}.json")
    with open(filename, 'w') as json_file:
        json.dump({
            'title': title,
            'link': link,
            'content': content
        }, json_file, ensure_ascii=False, indent=4)
    print(f"Content saved to {filename}")

def fetching_content():
    with open(filename, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)

        for row in csvreader:
            lnk = row[0]
            title = row[1]

            if not lnk.startswith('http'):
                lnk = requests.compat.urljoin(Tsite, lnk)


            try:
                response = requests.get(lnk, headers=headers)
                if response.status_code == 200:
                    content = response.text
                    savejson(lnk, title, content)
                else:
                    print(f"Failed to retrieve content from {lnk} (status code: {response.status_code})")
            except Exception :
                print(f"Error retrieving content from {lnk}")

fetching_content()


def json_process():
    def list_json_files(folder='scraped_data'):
        return [f for f in os.listdir(folder) if f.endswith('.json')]

    json_files = list_json_files()
    print(f"Found {len(json_files)} JSON files:", json_files)

    

json_process()
