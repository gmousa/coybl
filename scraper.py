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

    <!-- DataTables CSS -->
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.4/css/jquery.dataTables.min.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/2.3.6/css/buttons.dataTables.min.css">

    <!-- jQuery -->
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

    <!-- DataTables JS -->
    <script type="text/javascript" src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/buttons/2.3.6/js/dataTables.buttons.min.js"></script>

    <style>
    body {{
        font-family: Arial, sans-serif;
        margin: 20px;
    }}
    .table-responsive {{
        width: 100%;
        margin: 0 auto;
        clear: both;
        padding: 20px;
    }}
    #myTable {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }}
    #myTable th {{
        background-color: F2F2F2_1;
        padding: 12px;
        text-align: left;
        border: 1px solid #ddd;
    }}
    #myTable td {{
        padding: 12px;
        border: 1px solid #ddd;
    }}
    #myTable_filter {{
        margin-bottom: 20px;
    }}
    #myTable_filter input {{
        padding: 5px;
        margin-left: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }}
    .dataTables_wrapper .dataTables_filter {{
        float: none;
        text-align: center;
        margin-bottom: 20px;
    }}
    .dataTables_wrapper .dataTables_length {{
        float: none;
        text-align: center;
        margin-bottom: 20px;
    }}
    </style>

    <script>
    $(document).ready(function() {{
        // Initialize DataTable
        var table = $('#myTable').DataTable({{
            pageLength: 25,
            lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
            order: [[0, 'asc']],
            dom: '<"top"lf>rt<"bottom"ip><"clear">',
            language: {{
                search: "Filter records:",
                lengthMenu: "Show _MENU_ entries per page"
            }},
            initComplete: function () {{
                // Add individual column filtering
                this.api().columns().every(function () {{
                    var column = this;
                    var header = $(column.header());
                    var title = header.text();

                    // Create input element
                    var input = $('<input type="text" placeholder="Filter ' + title + '" style="width: 100%; box-sizing: border-box; margin-top: 5px;"/>')
                        .appendTo(header)
                        .on('keyup change', function () {{
                            if (column.search() !== this.value) {{
                                column
                                    .search(this.value)
                                    .draw();
                            }}
                        }});
                }});
            }}
        }});

        // Adjust iframe height when table is filtered/sorted
        table.on('draw', function() {{
            if (window.parent && window.parent.postMessage) {{
                setTimeout(function() {{
                    var height = document.documentElement.scrollHeight;
                    window.parent.postMessage({{'height': height}}, '*');
                }}, 100);
            }}
        }});
    }});
    </script>
</head>
<body>
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