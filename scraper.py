import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# Define your URLs for each table with their desired endpoints
tables_config = {
    "hs-nj": {
        "url": "https://www.leaguelineup.com/schedules.asp?url=nacopticleague&divisionid=468030",
        "title": "High School NJ"
    },
    "girls": {
        "url": "https://www.leaguelineup.com/schedules.asp?url=nacopticleague&divisionid=468032",
        "title": "Girls"
    },
    "junior-high": {
        "url": "https://www.leaguelineup.com/schedules.asp?url=nacopticleague&divisionid=468033",
        "title": "Junior High School"
    },
    "college": {
        "url": "https://www.leaguelineup.com/schedules.asp?url=nacopticleague&divisionid=845568",
        "title": "College"
    },
    "hs-ny": {
        "url": "https://www.leaguelineup.com/schedules.asp?url=nacopticleague&divisionid=1020928",
        "title": "High School NY"
    },
}

def scrape_table(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'tableview'})

    if table:
        for font_tag in table.find_all('font'):
            font_tag.replace_with(font_tag.string)

        for a_tag in table.find_all('a'):
            if 'style' in a_tag.attrs:
                del a_tag['style']

        return str(table)
    return "<p>No table found</p>"

def create_html_content(table_html, title):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
    .table-responsive {{
        width: 100%;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
    }}
    table {{
        width: 100%;
        min-width: 800px;
        border-collapse: collapse;
        color: black !important;
    }}
    td, th {{
        padding: 8px;
        color: black !important;
        white-space: nowrap;
        min-width: 60px;
    }}
    a {{
        color: black !important;
        text-decoration: none;
    }}
    tr:nth-child(even) {{
        background-color: #F2F2F2;
    }}
    .navigation {{
        background: #F8F9FA;
        padding: 1rem;
        margin-bottom: 2rem;
        text-align: center;
        border-bottom: 1px solid #ddd;
    }}
    .navigation a {{
        margin: 0 1rem;
        color: #333;
        text-decoration: none;
        padding: 0.5rem 1rem;
    }}
    .navigation a:hover {{
        background: #E9ECEF;
        border-radius: 4px;
    }}
    </style>
</head>
<body>
    <div class="navigation">
        <a href="hs-nj.html">High School NJ</a>
        <a href="girls.html">Girls</a>
        <a href="junior-high.html">Junior High</a>
        <a href="college.html">College</a>
         <a href="hs-ny.html">High School NY</a>
    </div>
    <h1 style="text-align: center;">{title}</h1>
    <div class="table-responsive">
        {table_html}
    </div>
    <p style="text-align: center; font-size: 0.8em;">
        Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
    </p>
</body>
</html>
"""

# Create each HTML file
for endpoint, config in tables_config.items():
    table_html = scrape_table(config["url"])
    html_content = create_html_content(table_html, config["title"])

    # Save as separate HTML files
    filename = f"{endpoint}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)