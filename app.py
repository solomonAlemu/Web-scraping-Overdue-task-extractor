from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import sys
import importlib.util
import os
import time
import signal
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from openpyxl import load_workbook
import tkinter as tk
from tkinter import filedialog
import openpyxl
import getpass  # Import getpass for terminal use
from webScraper import *
from XMLHandler import *
from Email_server import *
from ExcelFileHandler import *
from CSVFileHandler import *
from AdvancedWebScraper import *
import json
import pandas as pd
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from dateutil import parser
from datetime import datetime, timedelta
import win32com.client as win32
import pythoncom
import xlsxwriter
 
app = Flask(__name__)

# Define Task Classes
Task_class = ["BLOCK", 'CMR', 'AWL', 'MPD', 'AMM', 'CMM', 'MRA', "RQN",
              'CCMR', 'LWR', 'TRT', 'DLY', "RFB", "MSL", "MPE", "ETP",
              "MOM", "EO(I)", "EO(M)", "EO-", "EO(AM)", "EO(A)", "EO(CM)",
              "SRM", "MO-", "ECM", "EZP", "MTG", "MSG", "REP", "PRE",
              "STC", "ALI", "INV", "FUS", "ETP", "-REPL", "Replace"]

def find_keywords(text, keywords):
    pattern = '|'.join(re.escape(keyword) for keyword in keywords)
    matches = re.findall(pattern, text)
    return matches

def load_json_data():
    """Load fleet types and aircraft tail numbers from a JSON file."""
    with open("aircraft_data.json", "r") as file:
        data = json.load(file)
    return data

@app.route('/')
def index():
    data = load_json_data()
    fleet_types = sorted(set([item['fleet_type'] for item in data["fleet_data"]]))
    return render_template('index.html', fleet_types=fleet_types)
     
@app.route('/submit', methods=['POST'])
def submit():
    print("Hello")
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']  # Get the user's email address
    fleet_type = request.form['fleet_type']
    firstName = request.form['firstName']
    tails = request.form.getlist('tail')
    # Attempt to decode
    if tails:
        tails = request.form.getlist('tail')
    else:
        # Get the concatenated tails from the hidden input
        concatenated_tails = request.form.get('hidden_tail', '')
        try:
            tails = json.loads(concatenated_tails)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
 
    # Use the provided path to ChromeDriver
    driver_path = '/path/to/chromedriver'  # Specify your driver path
    scraper = AdvancedWebScraper(headless=True, driver_path=driver_path)
    scraper.login('http://svdcmpa01/maintenix/common/security/login.jsp', username, password, 'j_username', 'j_password', 'idButtonLogin')

    print(f"Extracting overdue tasks for ....: {tails}")
    data = []
    for tail_number in tails:
        print(f"Extracting overdue tasks for ....: {tail_number}")
        scraper.send_keys_to_element(By.ID, "idBarcodeSearchInput", tail_number)
        scraper.send_ENTER_keys_element(By.ID, "idBarcodeSearchInput")
        scraper.click_element(By.ID, "Open_link")
        scraper.click_element(By.ID, "OpenTasks_link")
        
        attribute_checks = [("font-weight", "bold"), ("color", "rgb(255, 0, 0)")]
        elements = scraper.extract_first_items_if_condition_met("idTableOpenTasks", attribute_checks)
        
        if elements:
            for element in elements:
                cell_data = element
                found_keywords = find_keywords(cell_data[0], Task_class)
                data.append([
                    tail_number,
                    found_keywords,
                    cell_data[0],
                    cell_data[1],
                    cell_data[2],
                    f'=HYPERLINK("{cell_data[3]}", "Click me.")'  # This formats it for Excel
                ])
                
     # Use absolute path for the folder
    folder_path = os.path.abspath('output/')  # Get absolute path
    os.makedirs(folder_path, exist_ok=True)
    
    # Set the path for the CSV and Excel files
    csv_file_path = os.path.join(folder_path, "output.csv")  # Path for the CSV file
    excel_file_path = os.path.join(folder_path, "output.xlsx")  # Path for the Excel file
    
    # Create DataFrame
    new_data = pd.DataFrame(data, columns=["Aircraft", "Overdue Task Type", "Overdue Tasks", "Task Barcode", "Due", "Task link"])
    
    # Write to CSV
    try:
        new_data.to_csv(csv_file_path, index=False, escapechar='\\')
        print(f"CSV file created: {csv_file_path}")  # Confirm file creation
    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")
        return jsonify({"error": f"Error while creating the CSV file: {str(e)}"}), 500
    
    # Optionally check if the files were created
    for file_path in [excel_file_path, csv_file_path]:
        if not os.path.exists(file_path):
            print(f"Error: File does not exist at {file_path}")
            return jsonify({"error": f"File was not created at {file_path}."}), 500  # Handle accordingly
        else:
            print(f"File found at: {file_path}")

    pythoncom.CoInitialize()
    email_sender = EmailSender()
    if not os.path.exists(file_path):
        print(f"Error: File does not exist at {file_path}")
        return jsonify({"error": "File was not created."}), 500  # Handle accordingly
    else:
        print(f"File found at: {file_path}")  

    email_sender.send_email_with_attachment(email,firstName, file_path, tails)
    pythoncom.CoUninitialize()
    # Return the CSV file for download
    return send_file(file_path, as_attachment=True)
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True, use_reloader=False)
