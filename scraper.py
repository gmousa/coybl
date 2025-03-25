import requests
from github import Github
import os
from datetime import datetime
from bs4 import BeautifulSoup

# Replace with the URL of the website
url = "https://www.leaguelineup.com/schedules.asp?url=nacopticleague&divisionid=468030"

# Fetch the webpage content
response = requests.get(url)

# Parse the content with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table
table = soup.find('table', {'class': 'tableview'})

# Remove all font tags while preserving their content
for font_tag in table.find_all('font'):
    font_tag.replace_with(font_tag.string)

# Remove all color attributes from links
for a_tag in table.find_all('a'):
    if 'style' in a_tag.attrs:
        del a_tag['style']

# Extract the HTML content of the table
table_html = str(table)

# Add wrapper div and CSS for responsive design
responsive_html = f"""
<style>
.table-responsive {{
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}}
table {{
    width: 100%;
    min-width: 800px; /* Ensures table doesn't get too cramped */
    border-collapse: collapse;
    color: black !important;
}}
td, th {{
    padding: 8px;
    color: black !important;
    white-space: nowrap;
    min-width: 60px; /* Minimum width for columns */
}}
a {{
    color: black !important;
    text-decoration: none;
}}
tr:nth-child(even) {{
    background-color: F2F2F2_1;
}}
</style>
<div class="table-responsive">
{table_html}
</div>
"""

# Save the HTML content to a file
with open("scraped_table.html", "w") as file:
    file.write(responsive_html)


html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Schedule</title>
    {responsive_html}
</head>
<body>
    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</body>
</html>
"""
