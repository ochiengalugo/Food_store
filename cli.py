import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def display_menu():
    print("\n=== INVENTORY MANAGEMENT PORTAL ===")
    print("1. View All Inventory")
    print("2. View Specific Item Details")
    print("3. Add New Inventory Item")
    print("4. Update Item Price or Stock Levels")
    print("5. Delete a Product")
    print("6. Find Item on OpenFoodFacts API")
    print("7. Exit")
    print("===================================")

def view_all():
    try:
        response = requests.get(f"{BASE_URL}/inventory")
        if response.status_code == 200:
            items = response.json()
            print("\nID  | Name                     | Price  | Stock | Barcode")
            print("-" * 60)
            for item in items:
                print(f"{item['id']:3} | {item['product_name'][:24]:24} | ${item['price']:5.2f} | {item['quantity']:5} | {item['code']}")
        else:
            print(f"Error fetching inventory: {response.text}")
    except requests.exceptions.ConnectionError:
        print("API Failure: Cannot connect to the Flask server. Is it running?")



def view_item():
    item_id = input("Enter the Item ID to look up: ").strip()
    try:
        response = requests.get(f"{BASE_URL}/inventory/{item_id}")
        if response.status_code == 200:
            item = response.json()
            print("\n--- Product Details ---")
            print(f"ID: {item['id']}")
            print(f"Name: {item['product_name']}")
            print(f"Brand: {item['brands']}")
            print(f"Barcode/Code: {item['code']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Quantity in Stock: {item['quantity']}")
        else:
            print(f"Error: {response.json().get('error', 'Item not found')}")
    except requests.exceptions.ConnectionError:
        print("API Failure: Server unreachable.")


def add_item():
    print("\n--- Add New Item ---")
    name = input("Enter product name: ").strip()
    if not name:
        print("Error: Product name cannot be blank.")
        return
    
    barcode = input("Enter barcode (optional): ").strip()
    brand = input("Enter brand name (optional): ").strip()
    
    try:
        price = float(input("Enter price: ") or 0.0)
        quantity = int(input("Enter starting quantity: ") or 0)
    except ValueError:
        print("Invalid input. Price and Quantity must be numerical values.")
        return

    payload = {
        "product_name": name,
        "code": barcode,
        "brands": brand,
        "price": price,
        "quantity": quantity
    }

    try:
        response = requests.post(f"{BASE_URL}/inventory", json=payload)
        if response.status_code == 201:
            print(f"Success! Item added with ID: {response.json()['id']}")
        else:
            print(f"Failed to add item: {response.text}")
    except requests.exceptions.ConnectionError:
        print("API Failure: Server unreachable.")
