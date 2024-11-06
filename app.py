import os

from flask import Flask, render_template, request, jsonify, send_from_directory
import pickle
import networkx as nx
from pyvis.network import Network
from flask import Flask, render_template_string
import requests
import openai
app = Flask(__name__)
openai.api_key = os.getenv("API_GPT_YEU")
@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/get', methods=['GET', 'POST'])
def chat():
    msg = request.form["msg"]
    response_text = get_Chat_response(msg)
    return response_text

def get_Chat_response(text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": text}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        response_json = response.json()

        # Trích xuất nội dung phản hồi
        if 'choices' in response_json and response_json['choices']:
            return response_json['choices'][0]['message']['content']
        else:
            return "Unexpected response format or missing content."

    except requests.exceptions.Timeout:
        return "Request timed out. Please try again later."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# @app.route('/static/knowledge_graph_3.html')
# def static_files(filename):
#     return send_from_directory('static', filename)
@app.route('/visualize')
def visualize_knowledge_graph():
    # Load the knowledge graph data
    file_path = 'knowledge_graph.pkl'  # Replace with the actual file path
    with open(file_path, 'rb') as file:
        data = pickle.load(file)

    entities = data.entities
    relationships = data.relationships

    # Create a directed graph with NetworkX
    G = nx.DiGraph()

    # Add nodes (entities) with only the name as tooltip
    for entity in entities:
        tooltip_text = f"Name: {entity.name}"
        G.add_node(entity.name, title=tooltip_text, label=entity.label)

    # Add edges (relationships) between entities
    for relationship in relationships:
        G.add_edge(relationship.startEntity.name, relationship.endEntity.name, label=relationship.name)

    # Display the graph using Pyvis
    net = Network(notebook=True, width="100%", height="750px", directed=True)

    # Import nodes and edges from the NetworkX graph into Pyvis
    net.from_nx(G)

    # Set options for the graph layout and interactions
    options = """
    {
        "physics": {
            "enabled": true,
            "repulsion": {
                "distance": 100,
                "multiplier": 1
            },
            "hierarchicalRepulsion": {
                "nodeDistance": 350
            },
            "solver": "repulsion",
            "stabilization": {
                "enabled": false
            }
        },
        "manipulation": {
            "enabled": true,
            "addNode": false,
            "addEdge": false,
            "deleteNode": false,
            "deleteEdge": false,
            "editNode": {
                "label": true,
                "size": true
            },
            "editEdge": {
                "label": true,
                "length": true
            }
        }
    }
    """

    net.set_options(options)

    # Generate HTML content as a string
    html_content = net.generate_html()

    # Return the generated HTML directly
    return render_template_string(html_content)


@app.route('/upload_file', methods=['POST'])
def upload_file():
    file_content = request.form['file_content']
    # Process the file content as needed
    response = "Received file content: " + file_content  # Modify this as needed
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
