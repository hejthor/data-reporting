import argparse
import json
import os

from document import document as _document

def app(parameters_path):
    print(f"[PYTHON][app.py] Reading JSON from path {parameters_path}")
    parameters = json.load(open(parameters_path, 'r'))
    output = parameters['output']
    documents = parameters['documents']

    print(f"[PYTHON][app.py] Ensuring output directory {output} exists")
    os.makedirs(output, exist_ok=True)
    
    for document in documents:
        print(f"[PYTHON][app.py] Running document()")
        _document(document, output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile documents from JSON parameters")
    parser.add_argument('--parameters', type=str, required=True, help='Path to JSON parameters file')
    args = parser.parse_args()
    app(args.parameters)