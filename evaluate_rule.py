import re

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value}, left={self.left}, right={self.right})"

def parse_condition(field, operator, value):
    return {"field": field, "operator": operator, "value": eval(value)}

def create_rule(rule_string):
    tokens = re.findall(r"\(|\)|\w+|==|>|<|>=|<=|'[^']+'|AND|OR", rule_string)
    return build_ast(tokens)

def build_ast(tokens):
    stack = []
    operators = []
    i = 0

    while i < len(tokens):
        token = tokens[i]

        if token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                if len(stack) < 2:
                    raise ValueError("Invalid expression - insufficient operands.")
                right = stack.pop()
                left = stack.pop()
                operator = operators.pop()
                stack.append(Node('operator', left, right, operator))
            operators.pop()
        elif token in ('AND', 'OR'):
            operators.append(token)
        else:
            if i + 2 < len(tokens) and tokens[i+1] in ('==', '>', '<', '>=', '<='):
                field = token
                operator = tokens[i + 1]
                value = tokens[i + 2]
                condition = parse_condition(field, operator, value)
                stack.append(Node('operand', value=condition))
                i += 2  # Skip the next two tokens
            else:
                raise ValueError(f"Invalid condition: {token}")
        
        i += 1

    while operators:
        if len(stack) < 2:
            raise ValueError("Invalid expression - insufficient operands.")
        right = stack.pop()
        left = stack.pop()
        operator = operators.pop()
        stack.append(Node('operator', left, right, operator))

    if len(stack) == 1:
        return stack.pop()
    else:
        raise ValueError("Invalid rule syntax, unable to build AST")

def evaluate_rule(ast, attributes):
    if ast.type == 'operand':
        condition = ast.value
        field = condition["field"]
        operator = condition["operator"]
        value = condition["value"]
        return eval(f"{attributes[field]} {operator} {value}")
    elif ast.type == 'operator':
        left_result = evaluate_rule(ast.left, attributes)
        right_result = evaluate_rule(ast.right, attributes)
        if ast.value == 'AND':
            return left_result and right_result
        elif ast.value == 'OR':
            return left_result or right_result
    return False

# Sample rule to evaluate
rule_string = "age > 30 AND salary > 50000"
# Create the AST from the rule string
ast = create_rule(rule_string)

# Sample attributes to evaluate against
attributes = {
    "age": 35,
    "salary": 60000
}

# Evaluate the rule
result = evaluate_rule(ast, attributes)
print(f"Evaluation Result: {result}")
