from flask import Flask, jsonify, request

app = Flask(__name__)

# Task 2: Mock database initialized as a list containing OpenFoodFacts-like data
inventory_db = [
    {
        "id": "1",
        "code": "301",
        "product_name": "Nutella 400g",
        "price": 5.99,
        "quantity": 50,
        "brands": "Ferrero"
    },
    {
        "id": "2",
        "code": "544",
        "product_name": "CocaCola Zero 330ml",
        "price": 1.49,
        "quantity": 120,
        "brands": "Coca-Cola"
    }
]


if __name__ == '__main__':
    # Run server in debug mode as instructed in Task 4
    app.run(port=5000, debug=True)
