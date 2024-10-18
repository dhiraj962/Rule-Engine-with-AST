# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle cross-origin requests (if needed)
from ast_engine import create_rule, ast_engine, evaluate_rule

app = Flask(__name__)
CORS(app)  # Enable cross-origin support

@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    data = request.json
    rule_string = data.get('rule_string')
    
    if not rule_string:
        return jsonify({"error": "Rule string is missing"}), 400
    
    try:
        ast = create_rule(rule_string)
        return jsonify(ast=str(ast))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ast_engine', methods=['POST'])
def ast_engine_api():
    data = request.json
    rules = data.get('rules', [])
    
    if not rules:
        return jsonify({"error": "No rules provided"}), 400
    
    try:
        combined_ast = ast_engine(rules)
        return jsonify(ast=str(combined_ast))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    data = request.json
    ast = data.get('ast')
    attributes = data.get('attributes')
    
    if not ast or not attributes:
        return jsonify({"error": "AST or attributes missing"}), 400
    
    try:
        result = evaluate_rule(ast, attributes)
        return jsonify(result=result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
