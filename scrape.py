import requests
import sys
from bs4 import BeautifulSoup

def get_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: Unable to fetch page, status code {response.status_code}"
    
def get_info(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("tr")
    data = [None for _ in range(15000)]
    for row in rows:
        cells = row.find_all("td")
        row_data = tuple(cell.get_text(strip=True) for cell in cells)
        if row_data:
            data[int(row_data[0])] = row_data
    return data

def get_method(info, id):
    return info[id][4]

    
def get_title(html):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    return title

def get_solver(info, id):
    return info[id][3]



def get_recon(html):
    soup = BeautifulSoup(html, "html.parser")
    reconstruction_div = soup.find("div", id="reconstruction")
    if reconstruction_div:
        for tag in reconstruction_div.find_all(["br", "div"]):
            tag.decompose()
        return reconstruction_div.get_text(separator="").strip()
    return "No reconstruction div found"

def get_time(info, id):
    return info[id][2]


def get_stm(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="solvestats")
    if table:
        for row in table.find_all("tr"):
            th = row.find("th")
            if th and th.get_text(strip=True) == "STM":
                first_td = row.find("td")
                return first_td.get_text(strip=True) if first_td else "No data found"
    return "No STM row found"

def get_stps(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="solvestats")
    if table:
        for row in table.find_all("tr"):
            th = row.find("th")
            if th and th.get_text(strip=True) == "STPS":
                first_td = row.find("td")
                return first_td.get_text(strip=True) if first_td else "No data found"
    return "No STPS row found"

def get_etm(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="solvestats")
    if table:
        for row in table.find_all("tr"):
            th = row.find("th")
            if th and th.get_text(strip=True) == "ETM":
                first_td = row.find("td")
                return first_td.get_text(strip=True) if first_td else "No data found"
    return "No ETM row found"

def get_etps(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="solvestats")
    if table:
        for row in table.find_all("tr"):
            th = row.find("th")
            if th and th.get_text(strip=True) == "ETPS":
                first_td = row.find("td")
                return first_td.get_text(strip=True) if first_td else "No data found"
    return "No ETPS row found"

url = "https://reco.nz/"
html_content = get_html(url)
info = get_info(html_content)

start = 7166
end = 11571
with open('data.csv', 'a', encoding="utf-8") as sys.stdout:
    for id in range(start, end):
        url = f"https://reco.nz/solve/{id}"
        html_content = get_html(url)

        if '3x3' not in get_title(html_content):
            continue

        if not info[id]:
            continue
    
        row = []

        # Solver
        row.append(get_solver(info, id))

        # Time
        row.append(get_time(info, id))

        # Recon
        recon = get_recon(html_content)
        lines = recon.split("\n")[2:]
        solve = ""
        for line in lines:
            part = line.split('/')[0].strip()
            if part:
                solve += line.split('/')[0].strip() + " "   
        row.append(solve.strip())

        # Method
        row.append(get_method(info, id))

        # STM
        row.append(get_stm(html_content))

        # STPS
        row.append(get_stps(html_content))

        # ETM
        row.append(get_etm(html_content))

        # ETPS
        row.append(get_etps(html_content))

        # Rotations
        rotations = solve.count('x') + solve.count('y') + solve.count('z')
        row.append(str(rotations))

        if not recon or 0 in [row[2], row[4]]:
            continue

        print(",".join(row))
        

        
