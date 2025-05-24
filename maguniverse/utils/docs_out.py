import os
from maguniverse.data.zeeman import zeeman_sources
from maguniverse.data.polarization import polarization_sources
from maguniverse.data.gas import gas_sources
from jinja2 import Environment, FileSystemLoader

def get_all_data():
    """Get all data dictionaries."""
    return {
        'zeeman': zeeman_sources,
        'polarization': polarization_sources,
        'gas': gas_sources
    }

def generate_html():
    """Generate the HTML documentation."""
    data_types = get_all_data()
    
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
        </style>
    </head>
    <body>
        <div class="container">
            <h1>magUniverse Paper Collection</h1>
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
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <script>
            function toggleContent(id) {
                var content = document.getElementById(id);
                if (content.style.display === "block") {
                    content.style.display = "none";
                } else {
                    content.style.display = "block";
                }
            }
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
    output = template.render(data_types=data_types)
    output_path = os.path.join(docs_dir, 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

if __name__ == '__main__':
    # Generate the HTML documentation
    generate_html() 