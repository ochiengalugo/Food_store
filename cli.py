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
