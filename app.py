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

import requests  

def fetch_from_openfoodfacts(barcode_or_name):
   
    
    search_query = str(barcode_or_name).strip()
    
    
    if search_query.isdigit():
        
        url = f"https://world.openfoodfacts.org/api/v3/product/{search_query}.json"
        try:
            response = requests.get(url, headers={'User-Agent': 'InventoryAdminPortal - Web - Version 1.0'})
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success" and "product" in data:
                    product = data["product"]
                    return {
                        "code": search_query,
                        "product_name": product.get("product_name", "Unknown Product"),
                        "brands": product.get("brands", "Unknown Brand")
                    }
        except requests.exceptions.RequestException:
            pass 
            
    else:
       
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "search_terms": search_query,
            "json": 1,
            "page_size": 1
        }
        try:
            response = requests.get(url, params=params, headers={'User-Agent': 'InventoryAdminPortal - Web - Version 1.0'})
            if response.status_code == 200:
                data = response.json()
                products = data.get("products", [])
                if products:
                    product = products[0]
                    return {
                        "code": product.get("code", "N/A"),
                        "product_name": product.get("product_name", "Unknown Product"),
                        "brands": product.get("brands", "Unknown Brand")
                    }
        except requests.exceptions.RequestException:
            pass

    return None
    



if __name__ == '__main__':
    # Run server in debug mode as instructed in Task 4
    app.run(port=5000, debug=True)
