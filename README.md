# Rule-Engine-with-AST
Develop a simple 3-tier rule engine application(Simple UI, API and Backend, Data) to determine user eligibility based on attributes like age, department, income, spend etc.The system can use Abstract Syntax Tree (AST) to represent conditional rules and allow for dynamic creation,combination, and modification of these rules.
# Rule Engine with Abstract Syntax Tree (AST)

This is a simple 3-tier rule engine application to determine user eligibility based on attributes such as age, department, income, and spend. The system uses an Abstract Syntax Tree (AST) to represent conditional rules, allowing dynamic creation, combination, and evaluation of rules.

## Features

- **Create and Parse Rules**: Supports rule creation and parsing using custom rule syntax.
- **Combine Rules**: Combines multiple rules using logical operators like `AND` and `OR`.
- **Evaluate Rules**: Evaluates rules against user attributes and returns the eligibility result.
- **REST API**: Provides an API interface to interact with the rule engine.
- **Frontend Interface**: Allows users to input rules via a simple HTML form.

## Project Structure
rule-engine/
├── backend/
│   ├── app.py             # Flask API application
│   ├── ast_engine.py      # Core logic for rule parsing, AST creation, and evaluation
├── frontend/
│   ├── index.html         # Simple UI to input and test rules
│   ├── script.js          # JavaScript to handle form submission and API requests
├── evaluate_rule.py       # Example script to create and evaluate rules
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation

*Install the required Python dependencies: pip install
*Ensure the flask_cors is installed: pip install flask_cors
*Run your Flask backend: python app.py
*After that the rule will be created then we have to verify the rule
*evaluate_rule we have to check
*Evaluation Result: True



