import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# Your existing tables_config remains the same

def scrape_table(url):
    # Your existing scrape_table function remains the same
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'tableview'})
    if table:
        # Add a class to the table for DataTables
        table['class'] = ['tableview', 'display']
        table['id'] = 'myTable'
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
    <!-- Add DataTables CSS -->
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/responsive/2.2.9/css/responsive.dataTables.min.css">

    <!-- Add jQuery -->
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.5.1.min.js"></script>

    <!-- Add DataTables JS -->
    <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/responsive/2.2.9/js/dataTables.responsive.min.js"></script>

    <style>
    .table-responsive {{
        width: 100%;
        margin: 0 auto;
        clear: both;
        padding: 20px;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        color: black !important;
    }}
    td, th {{
        padding: 8px;
        color: black !important;
    }}
    a {{
        color: black !important;
        text-decoration: none;
    }}
    .navigation {{
        background: F8F9FA_1;
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
        background: E9ECEF_1;
        border-radius: 4px;
    }}
    </style>

    <script>
    $(document).ready(function() {{
        $('#myTable').DataTable({{
            responsive: true,
            pageLength: 25,
            order: [[0, 'asc']],
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ]
        }});
    }});
    </script>
</head>
<body>
    <div class="navigation">
        <a href="hs_nj.html">High School NJ</a>
        <a href="girls.html">Girls</a>
        <a href="junior_high.html">Junior High</a>
        <a href="college.html">College</a>
        <a href="hs_ny.html">High School NY</a>
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

# Your existing file creation code remains the same
for endpoint, config in tables_config.items():
    table_html = scrape_table(config["url"])
    html_content = create_html_content(table_html, config["title"])
    filename = f"{endpoint}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)