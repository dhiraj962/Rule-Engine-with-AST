document.getElementById('rule-form').addEventListener('submit', async function(event) {
    event.preventDefault();  // Prevent form submission from refreshing the page

    const ruleInput = document.getElementById('rule').value;

    if (!ruleInput) {
        alert("Please enter a rule.");
        return;
    }

    // Making the POST request to the Flask backend
    try {
        const response = await fetch('http://127.0.0.1:5000/create_rule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ rule_string: ruleInput })
        });

        const result = await response.json();

        if (response.ok) {
            // Display the result (AST) in the output div
            document.getElementById('output').textContent = JSON.stringify(result.ast, null, 2);
        } else {
            // Show the error in case of any issues
            document.getElementById('output').textContent = `Error: ${result.error}`;
        }
    } catch (error) {
        document.getElementById('output').textContent = `Error: ${error.message}`;
    }
});
