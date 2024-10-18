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
    # Parse the condition into a structured format
    return {"field": field, "operator": operator, "value": eval(value)}

def create_rule(rule_string):
    # Tokenize the rule string into operators, operands, and parentheses
    tokens = re.findall(r"\(|\)|\w+|==|>|<|>=|<=|'[^']+'|AND|OR", rule_string)
    print(f"Tokens: {tokens}")  # Debugging: print the tokens
    return build_ast(tokens)

def build_ast(tokens):
    stack = []
    operators = []
    i = 0

    while i < len(tokens):
        token = tokens[i]

        if token == '(':
            operators.append(token)  # Push to operators stack
        elif token == ')':
            # Resolve the current expression until we hit '('
            while operators and operators[-1] != '(':
                if len(stack) < 2:
                    raise ValueError("Invalid expression - insufficient operands.")
                right = stack.pop()
                left = stack.pop()
                operator = operators.pop()
                stack.append(Node('operator', left, right, operator))
            operators.pop()  # Remove the '(' from operators stack
        elif token in ('AND', 'OR'):
            operators.append(token)  # Track logical operators
        else:
            # It's a condition
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

    # Final resolution of any remaining operators
    while operators:
        if len(stack) < 2:
            raise ValueError("Invalid expression - insufficient operands.")
        right = stack.pop()
        left = stack.pop()
        operator = operators.pop()
        stack.append(Node('operator', left, right, operator))

    # Ensure we have a single AST root
    if len(stack) == 1:
        return stack.pop()
    else:
        raise ValueError("Invalid rule syntax, unable to build AST")

def ast_engine(rules):
    if not rules:
        raise ValueError("No rules provided")
    
    combined_ast = None

    for rule in rules:
        rule_ast = create_rule(rule)
        
        if combined_ast is None:
            combined_ast = rule_ast
        else:
            # Combine two ASTs with an "AND" operation between them
            combined_ast = Node('operator', left=combined_ast, right=rule_ast, value='AND')
    
    return combined_ast

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

