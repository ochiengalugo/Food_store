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


def update_item():
    item_id = input("Enter the Item ID to update: ").strip()
    print("Leave field blank if you do not want to change it.")
    
    payload = {}
    price_input = input("Enter new price: ").strip()
    stock_input = input("Enter new stock level: ").strip()

    try:
        if price_input:
            payload["price"] = float(price_input)
        if stock_input:
            payload["quantity"] = int(stock_input)
    except ValueError:
        print("Error: Input must be numeric numbers.")
        return

    if not payload:
        print("No updates entered.")
        return

    try:
        response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=payload)
        if response.status_code == 200:
            print("Item updated successfully!")
        else:
            print(f"Error: {response.json().get('error', 'Update failed')}")
    except requests.exceptions.ConnectionError:
        print("API Failure: Server unreachable.")

def delete_item_portal():
    item_id = input("Enter the Item ID to delete: ").strip()
    confirm = input(f"Are you sure you want to permanently delete item {item_id}? (y/N): ").lower()
    
    if confirm != 'y':
        print("Deletion cancelled.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
        if response.status_code == 200:
            print("Product removed successfully.")
        else:
            print(f"Error: {response.json().get('error', 'Delete failed')}")
    except requests.exceptions.ConnectionError:
        print("API Failure: Server unreachable.")

def find_on_external_api():
    query = input("Enter barcode or name to query from OpenFoodFacts: ").strip()
    if not query:
        return
        
    try:
        response = requests.get(f"{BASE_URL}/external-search", params={"q": query})
        if response.status_code == 200:
            data = response.json()
            print("\n--- Found on External Data Stream ---")
            print(f"Name: {data.get('product_name')}")
            print(f"Brand: {data.get('brands')}")
            print(f"Code: {data.get('code')}")
            
            save = input("\nWould you like to import this into your local inventory? (y/N): ").lower()
            if save == 'y':
                try:
                    price = float(input("Assign retail price: "))
                    qty = int(input("Assign initial stock quantity: "))
                    data["price"] = price
                    data["quantity"] = qty
                    
                    post_res = requests.post(f"{BASE_URL}/inventory", json=data)
                    if post_res.status_code == 201:
                        print("Successfully imported into local tracking list!")
                except ValueError:
                    print("Invalid figures. Import aborted.")
        else:
            print("Product not discovered in the OpenFoodFacts registry database.")
    except requests.exceptions.ConnectionError:
        print("API Failure: Server unreachable.")


if __name__ == '__main__':
    main()