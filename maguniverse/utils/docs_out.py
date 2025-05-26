import os
import json
from maguniverse.data.zeeman import zeeman_sources
from maguniverse.data.polarization import polarization_sources
from maguniverse.data.gas import gas_sources
from maguniverse.service.get import getters
from jinja2 import Environment, FileSystemLoader

def get_all_data():
    """Get all data dictionaries."""
    return {
        'zeeman': zeeman_sources,
        'polarization': polarization_sources,
        'gas': gas_sources
    }

def get_available_tables():
    """Get all available tables from the manifest.json file."""
    manifest_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docs', 'manifest.json')
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    # Get the preset getters from manifest
    preset_getters = manifest.get('preset getters', {})
    
    # Convert the getter IDs to display names
    table_names = {}
    for getter_id in preset_getters:
        # Extract paper name and table number from getter_id
        # Format is typically "paperYYYY_tN" where YYYY is year and N is table number
        parts = getter_id.split('_')
        if len(parts) == 2:
            paper_name = parts[0]
            table_num = parts[1].replace('t', 'Table ')
            # Capitalize first letter of paper name
            paper_name = paper_name[0].upper() + paper_name[1:]
            # Add year if it exists in the name
            if any(char.isdigit() for char in paper_name):
                # Extract year (assuming it's 4 digits)
                year = ''.join(filter(str.isdigit, paper_name))
                paper_name = paper_name.replace(year, '') + ' ' + year
            table_names[getter_id] = f"{paper_name} {table_num}"
    
    return table_names

def generate_html():
    """Generate the HTML documentation."""
    data_types = get_all_data()
    available_tables = get_available_tables()
    
    # Create docs directory if it doesn't exist
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docs')
    os.makedirs(docs_dir, exist_ok=True)
    
    # Set up Jinja2
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(template_dir, exist_ok=True)
    
    # HTML template
    template_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>magUniverse Paper Collection</title>
        <script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                line-height: 1.6;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            h1 {
                color: #333;
                border-bottom: 2px solid #333;
                padding-bottom: 10px;
            }
            .data-type {
                margin-bottom: 30px;
            }
            .data-type h2 {
                color: #2c3e50;
                cursor: pointer;
                padding: 10px;
                background-color: #f5f6fa;
                border-radius: 5px;
            }
            .data-type h2:hover {
                background-color: #e8e9ec;
            }
            .content {
                display: none;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #f8f9fa;
            }
            a {
                color: #3498db;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .instrument {
                color: #666;
                font-style: italic;
                margin-top: 5px;
            }
            .get-data-btn {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                margin: 2px;
            }
            .get-data-btn:hover {
                background-color: #45a049;
            }
            .loading {
                position: fixed;
                top: 20px;
                right: 20px;
                width: 300px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                z-index: 1000;
                padding: 15px;
                font-size: 14px;
                transition: opacity 0.3s ease;
            }
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                width: 300px;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                z-index: 1000;
                padding: 15px;
                font-size: 14px;
                transition: opacity 0.3s ease;
                display: none;
            }
            .notification-content {
                text-align: left;
            }
            .notification h2 {
                margin: 0 0 10px 0;
                font-size: 16px;
                color: #2c3e50;
            }
            .notification p {
                margin: 0;
                color: #666;
            }
            .notification-status {
                margin-top: 10px;
                padding: 8px;
                background: #f8f9fa;
                border-radius: 4px;
                font-family: monospace;
                font-size: 12px;
                color: #666;
            }
            .back-to-top {
                position: fixed;
                bottom: 20px;
                left: 20px;
                width: 40px;
                height: 40px;
                background: #2c3e50;
                color: white;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                cursor: pointer;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
                z-index: 1000;
            }
            .back-to-top:hover {
                background: #34495e;
                transform: translateY(-2px);
            }
            .warning-banner {
                position: fixed;
                top: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 80%;
                max-width: 800px;
                background: #fff3cd;
                border: 1px solid #ffeeba;
                color: #856404;
                padding: 15px;
                border-radius: 0 0 8px 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                z-index: 1001;
                text-align: center;
                font-size: 14px;
                line-height: 1.5;
                display: none;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            .warning-banner a {
                color: #0056b3;
                text-decoration: underline;
            }
            .warning-banner .close-btn {
                position: absolute;
                right: 10px;
                top: 10px;
                cursor: pointer;
                font-size: 18px;
                color: #856404;
            }
            .feature-intro {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
                border: 1px solid #e9ecef;
            }
            .feature-intro h2 {
                color: #2c3e50;
                margin-top: 0;
            }
            .feature-intro h3 {
                color: #2c3e50;
                font-size: 1.1em;
                margin: 15px 0 10px 0;
            }
            .feature-intro ul {
                margin: 10px 0;
                padding-left: 20px;
            }
            .feature-intro li {
                margin: 5px 0;
            }
            .feature-intro .note {
                background: #fff3cd;
                border: 1px solid #ffeeba;
                color: #856404;
                padding: 10px;
                border-radius: 4px;
                margin-top: 15px;
            }
        </style>
    </head>
    <body>
        <div id="loading" class="loading">
            <div class="loading-content">
                <h2>Initializing Environment</h2>
                <p>Setting up Python and magUniverse...</p>
                <div class="loading-status" id="loading-status">Loading Pyodide...</div>
            </div>
        </div>
        <div id="notification" class="notification">
            <div class="notification-content">
                <h2>Download Status</h2>
                <p>Table download in progress...</p>
                <div class="notification-status" id="notification-status"></div>
            </div>
        </div>
        <div id="warning-banner" class="warning-banner">
            <span class="close-btn" onclick="hideWarning()">&times;</span>
            <strong>Important Notice:</strong> Due to CAPTCHA verification and proxy settings, some automatic getters may not work. 
            Please visit <a href="https://github.com/xli2522/magUniverse" target="_blank">https://github.com/xli2522/magUniverse</a> 
            to download tables manually if needed.
        </div>
        <div class="container">
            <h1>magUniverse Paper Collection</h1>
            
            <div class="feature-intro">
                <h2>Download Data Directly in Your Browser</h2>
                <p>
                    magUniverse now offers browser-based data downloads powered by <a href="https://pyodide.org" target="_blank">Pyodide</a>. 
                    This eliminates the need for local Python installation or environment setup.
                </p>
                <div class="note">
                    <strong>Note:</strong> Due to browser security restrictions and CAPTCHA requirements, some data sources may require manual download from their providers. 
                    Find links to the original data providers in our <a href="https://github.com/xli2522/magUniverse" target="_blank">GitHub repository</a>.
                </div>
            </div>

            {% for data_type, sources in data_types.items() %}
            <div class="data-type">
                <h2 onclick="toggleContent('{{ data_type }}')">{{ data_type.replace('_', ' ').title() }}</h2>
                <div id="{{ data_type }}" class="content">
                    <table>
                        <tr>
                            <th>Source</th>
                            <th>Title</th>
                            <th>Authors</th>
                            <th>Year</th>
                            <th>Instrument</th>
                            <th>Links</th>
                            <th>Available Tables</th>
                        </tr>
                        {% for source_name, info in sources.items() %}
                        <tr>
                            <td>{{ source_name }}</td>
                            <td>{{ info.title }}</td>
                            <td>{{ info.authors }}</td>
                            <td>{{ info.year }}</td>
                            <td>{{ info.instrument }}</td>
                            <td>
                                {% if info.ads_link %}
                                <a href="{{ info.ads_link }}" target="_blank">ADS</a>
                                {% endif %}
                                {% if info.paper_link %}
                                {% if info.ads_link %} | {% endif %}
                                <a href="{{ info.paper_link }}" target="_blank">Paper</a>
                                {% endif %}
                                {% if info.publisher_link %}
                                {% if info.ads_link or info.paper_link %} | {% endif %}
                                <a href="{{ info.publisher_link }}" target="_blank">Publisher</a>
                                {% endif %}
                                {% if info.doi %}
                                {% if info.ads_link or info.publisher_link or info.paper_link %} | {% endif %}
                                <a href="https://doi.org/{{ info.doi }}" target="_blank">DOI</a>
                                {% endif %}
                            </td>
                            <td>
                                {% for table_id, table_name in available_tables.items() %}
                                {% if source_name.lower() in table_id.lower() %}
                                <button class="get-data-btn" onclick="downloadTable('{{ table_id }}')" data-source="{{ table_id }}">
                                    {{ table_name }}
                                </button>
                                {% endif %}
                                {% endfor %}
                            </td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>
            {% endfor %}
        </div>
        <div class="back-to-top" onclick="scrollToTop()">
            ↑
        </div>
        
        <script>
            let pyodide;
            
            async function init() {
                try {
                    const statusEl = document.getElementById('loading-status');
                    statusEl.textContent = 'Loading Pyodide...';
                    pyodide = await loadPyodide({
                        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/'
                    });
                    
                    statusEl.textContent = 'Installing micropip...';
                    await pyodide.loadPackage("micropip");

                    statusEl.textContent = 'Installing requests...';
                    await pyodide.runPythonAsync(`
                        import micropip
                        await micropip.install('requests')
                    `);

                    statusEl.textContent = 'Getting the latest magUniverse wheel...';
                    const magUniverse_version = await pyodide.runPythonAsync(`
                        import requests
                        response = requests.get('https://xli2522.github.io/magUniverse/latest_wheel.txt')
                        if response.status_code == 200:
                            magUniverse_version = response.text
                            print(f"Latest magUniverse version: {magUniverse_version}")
                        else:
                            print(f"Latest wheel request failed with status code {response.status_code}")
                            print("Using the latest pypi version")
                            magUniverse_version = 'magUniverse'

                        import micropip
                        await micropip.install('https://xli2522.github.io/magUniverse/' + f'{magUniverse_version}')
                        magUniverse_version
                    `);
                    console.log(`Installed ${magUniverse_version}...`);

                    statusEl.textContent = 'Creating user_data directory...';
                    await pyodide.runPythonAsync(`
                        import os
                        os.mkdir('user_data')
                    `);

                    statusEl.textContent = 'Importing magUniverse service getters...';
                    await pyodide.runPythonAsync(`
                        from maguniverse.service.get import getters
                        client = getters(env='pyodide')
                    `);

                    statusEl.textContent = 'Ready!';
                    setTimeout(() => {
                        document.getElementById('loading').style.opacity = '0';
                        setTimeout(() => {
                            document.getElementById('loading').style.display = 'none';
                        }, 300);
                    }, 1000);
                } catch (e) {
                    console.error('Error initializing Pyodide:', e);
                    const statusEl = document.getElementById('loading-status');
                    statusEl.textContent = `Error: ${e.message}`;
                    statusEl.style.color = '#dc3545';
                }
            }

            function showWarning() {
                const warning = document.getElementById('warning-banner');
                warning.style.display = 'block';
                // Force a reflow
                warning.offsetHeight;
                warning.style.opacity = '1';
                
                // Hide after 8 seconds
                setTimeout(hideWarning, 8000);
            }

            function hideWarning() {
                const warning = document.getElementById('warning-banner');
                warning.style.opacity = '0';
                setTimeout(() => {
                    warning.style.display = 'none';
                }, 300);
            }

            async function downloadTable(tableId) {
                try {
                    // Show notification
                    const notification = document.getElementById('notification');
                    const statusEl = document.getElementById('notification-status');
                    notification.style.display = 'block';
                    notification.style.opacity = '1';
                    statusEl.textContent = `Download of ${tableId} table has been initiated. Watch for new download files or error messages...`;
                    
                    const result = await pyodide.runPythonAsync(`
                        df_pol = getattr(client, '${tableId}')()
                        print(df_pol.head())
                        output_path = 'user_data/${tableId}.txt'
                        output_path
                    `);
                    
                    // Get the file path from Python's return value
                    const filePath = result;
                    console.log(`Reading file: ${filePath}`);
                    const data = pyodide.FS.readFile(filePath);
                    // Create a blob and download
                    const blob = new Blob([data], { type: "text/plain" });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = filePath;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    URL.revokeObjectURL(url);
                    
                    // Update notification
                    statusEl.textContent = 'Download completed successfully!';
                    statusEl.style.color = '#28a745';
                    
                    // Hide notification after 3 seconds
                    setTimeout(() => {
                        notification.style.opacity = '0';
                        setTimeout(() => {
                            notification.style.display = 'none';
                        }, 300);
                    }, 3000);
                    
                } catch (e) {
                    console.error('Error downloading table:', e);
                    const statusEl = document.getElementById('notification-status');
                    statusEl.textContent = `Error: ${e.message}`;
                    statusEl.style.color = '#dc3545';
                    
                    // Show warning banner for CAPTCHA/proxy issues
                    showWarning();
                    
                    // Keep error message visible longer
                    setTimeout(() => {
                        notification.style.opacity = '0';
                        setTimeout(() => {
                            notification.style.display = 'none';
                        }, 300);
                    }, 5000);
                }
            }

            function toggleContent(id) {
                var content = document.getElementById(id);
                if (content.style.display === "block") {
                    content.style.display = "none";
                } else {
                    content.style.display = "block";
                }
            }

            function scrollToTop() {
                // Collapse all dropdowns
                document.querySelectorAll('.content').forEach(content => {
                    content.style.display = "none";
                });
                
                // Scroll to top with smooth animation
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            }

            // Initialize Pyodide when the page loads
            init();
        </script>
    </body>
    </html>
    '''
    
    # Save the template
    template_path = os.path.join(template_dir, 'docs_template.html')
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    # Set up Jinja2
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('docs_template.html')
    
    # Generate index.html
    output = template.render(data_types=data_types, available_tables=available_tables)
    output_path = os.path.join(docs_dir, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

if __name__ == '__main__':
    # Generate the HTML documentation
    generate_html() 