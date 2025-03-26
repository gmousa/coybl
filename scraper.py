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

tables_config_2 = {
    "hs-nj-standings": {
        "url": "https://www.leaguelineup.com/standings_basketball.asp?url=nacopticleague&divisionid=468030",
        "title": "High School NJ"
    },
    "girls-standings": {
        "url": "https://www.leaguelineup.com/standings_basketball.asp?url=nacopticleague&divisionid=468032",
        "title": "Girls"
    },
    "junior-high-standings": {
        "url": "https://www.leaguelineup.com/standings_basketball.asp?url=nacopticleague&divisionid=468033",
        "title": "Junior High School"
    },
    "college-standings": {
        "url": "https://www.leaguelineup.com/standings_basketball.asp?url=nacopticleague&divisionid=845568",
        "title": "College"
    },
    "hs-ny-standings": {
        "url": "https://www.leaguelineup.com/standings_basketball.asp?url=nacopticleague&divisionid=1020928",
        "title": "High School NY"
    },
}

def scrape_table(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'tableview'})
    if table:
        # Create a new table structure
        new_table = soup.new_tag('table')
        new_table['class'] = ['tableview', 'display', 'nowrap']
        new_table['id'] = 'myTable'
        new_table['style'] = 'width:100%'

        # Create thead and tbody
        thead = soup.new_tag('thead')
        tbody = soup.new_tag('tbody')
        new_table.append(thead)
        new_table.append(tbody)

        # Process the first row as header
        header_row = table.find('tr')
        if header_row:
            new_header_row = soup.new_tag('tr')
            thead.append(new_header_row)
            # Skip first column by starting from index 1
            for cell in header_row.find_all(['td', 'th'])[1:]:
                new_th = soup.new_tag('th')
                new_th.string = cell.get_text(strip=True)
                new_header_row.append(new_th)

        # Process all other rows
        for row in table.find_all('tr')[1:]:
            new_row = soup.new_tag('tr')
            tbody.append(new_row)
            # Skip first column by starting from index 1
            for cell in row.find_all(['td', 'th'])[1:]:
                new_td = soup.new_tag('td')
                new_td.string = cell.get_text(strip=True)
                new_row.append(new_td)

        return str(new_table)
    return "<p>No table found</p>"

def scrape_table_2(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'table-striped'})
    if table:
        # Create a new table structure
        new_table = soup.new_tag('table')
        new_table['class'] = ['table-striped', 'display']
        new_table['id'] = 'myTable'

        # Create thead and tbody
        thead = soup.new_tag('thead')
        tbody = soup.new_tag('tbody')
        new_table.append(thead)
        new_table.append(tbody)

        # Process the first row as header
        header_row = table.find('tr')
        if header_row:
            new_header_row = soup.new_tag('tr')
            thead.append(new_header_row)
            for cell in header_row.find_all(['td', 'th']):
                new_th = soup.new_tag('th')
                new_th.string = cell.get_text(strip=True)
                new_header_row.append(new_th)

        # Process all other rows
        for row in table.find_all('tr')[1:]:
            new_row = soup.new_tag('tr')
            tbody.append(new_row)
            for cell in row.find_all(['td', 'th']):
                new_td = soup.new_tag('td')
                new_td.string = cell.get_text(strip=True)
                new_row.append(new_td)

        return str(new_table)
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
    <script type="text/javascript" src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/responsive/2.2.9/js/dataTables.responsive.min.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/buttons/2.3.6/js/dataTables.buttons.min.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/searchbuilder/1.4.2/js/dataTables.searchBuilder.min.js"></script>

    <!-- Add DataTables CSS -->
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.4/css/jquery.dataTables.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/responsive/2.2.9/css/responsive.dataTables.min.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/2.3.6/css/buttons.dataTables.min.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/searchbuilder/1.4.2/css/searchBuilder.dataTables.min.css">

    <style>
    .table-responsive {{
        width: 100%;
        margin: 0 auto;
        clear: both;
        padding: 20px;
    }}
    table.dataTable {{
        width: 100% !important;
        margin: 0 auto;
        clear: both;
        border-collapse: separate;
        border-spacing: 0;
        table-layout: fixed;
    }}
    .dataTables_wrapper {{
        width: 100%;
    }}
    thead tr:first-child th {{
        text-align: left;
        white-space: nowrap;
    }}
    td {{
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    .filters select {{
        width: 100%;
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
    .filters select {{
        width: 100%;
        padding: 3px;
        box-sizing: border-box;
        margin-top: 3px;
    }}
    .filters th {{
        padding: 4px !important;
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
        // Setup - add a select to each header cell
        $('#myTable thead tr').clone(true).addClass('filters').appendTo('#myTable thead');

        var table = $('#myTable').DataTable({{
            pageLength: 25,
            order: [[0, 'asc']],
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ],
            orderCellsTop: true,
            fixedHeader: true,
            responsive: false,
            autoWidth: false,
            columnDefs: [
                {{
                    orderable: false,
                    targets: '_all'
                }},
                {{
                    className: 'dt-head-left dt-body-left',
                    targets: '_all'
                }}
            ],
            initComplete: function () {{
                this.api().columns().every(function () {{
                    var column = this;
                    var select = $('<select><option value="">All</option></select>')
                        .appendTo($(column.header()).empty())
                        .on('change', function (e) {{
                            e.stopPropagation();
                            var val = $.fn.dataTable.util.escapeRegex($(this).val());
                            column
                                .search(val ? '^'+val+'$' : '', true, false)
                                .draw();
                        }});

                    column.data().unique().sort().each(function(d, j) {{
                        if(d) {{
                            select.append('<option value="'+d+'">'+d+'</option>')
                        }}
                    }});
                }});
            }}
        }});

        // Adjust column widths after initialization
        table.columns.adjust();
    }});
    </script>
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

def create_html_content_2(table_html, title):
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
    table.dataTable {{
        width: 100% !important;
        margin: 0 auto;
        clear: both;
        border-collapse: separate;
        border-spacing: 0;
        table-layout: fixed;
    }}
    .dataTables_wrapper {{
        width: 100%;
    }}
    thead tr:first-child th {{
        text-align: left;
        white-space: nowrap;
    }}
    td {{
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    .filters select {{
        width: 100%;
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
    .filters select {{
        width: 100%;
        padding: 3px;
        box-sizing: border-box;
        margin-top: 3px;
    }}
    .filters th {{
        padding: 4px !important;
    }}
    </style>

    <script>
    $(document).ready(function() {{
        // Setup - add a select to each header cell
        $('#myTable thead tr').clone(true).addClass('filters').appendTo('#myTable thead');

        var table = $('#myTable').DataTable({{
            pageLength: 25,
            order: [[0, 'asc']],
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ],
            orderCellsTop: true,
            fixedHeader: true,
            responsive: false,
            autoWidth: false,
            columnDefs: [
                {{
                    orderable: false,
                    targets: '_all'
                }},
                {{
                    className: 'dt-head-left dt-body-left',
                    targets: '_all'
                }}
            ],
            initComplete: function () {{
                this.api().columns().every(function () {{
                    var column = this;
                    var select = $('<select><option value="">All</option></select>')
                        .appendTo($(column.header()).empty())
                        .on('change', function (e) {{
                            e.stopPropagation();
                            var val = $.fn.dataTable.util.escapeRegex($(this).val());
                            column
                                .search(val ? '^'+val+'$' : '', true, false)
                                .draw();
                        }});

                    column.data().unique().sort().each(function(d, j) {{
                        if(d) {{
                            select.append('<option value="'+d+'">'+d+'</option>')
                        }}
                    }});
                }});
            }}
        }});

        // Adjust column widths after initialization
        table.columns.adjust();
    }});
    </script>
</head>
<body>
    <div class="navigation">
        <a href="hs-nj-standings.html">High School NJ</a>
        <a href="girls-standings.html">Girls</a>
        <a href="junior-high-standings.html">Junior High</a>
        <a href="college-standings.html">College</a>
        <a href="hs-ny-standings.html">High School NY</a>
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

for endpoint, config in tables_config_2.items():
    table_html = scrape_table_2(config["url"])
    html_content = create_html_content_2(table_html, config["title"])
    filename = f"{endpoint}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)