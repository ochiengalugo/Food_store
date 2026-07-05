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

