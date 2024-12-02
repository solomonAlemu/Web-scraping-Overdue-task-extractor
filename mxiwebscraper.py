# from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
# import subprocess
# import sys
# import importlib.util
# import os
# import time
# import signal
# import re
# from selenium import webdriver
# from bs4 import BeautifulSoup
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from openpyxl import load_workbook
# import tkinter as tk
# from tkinter import filedialog
# import openpyxl
# import tkinter as tk
# from tkinter import ttk, filedialog
# from tkinter import messagebox
# import getpass  # Import getpass for terminal use
# from webScraper import *
# from XMLHandler import *
# from ExcelFileHandler import *
# from CSVFileHandler import *
# from AdvancedWebScraper import *
# import json
# import pandas as pd
# import re
#
# app = Flask(__name__)
#
# # Define Task Classes
# Task_class = [ "BLOCK", 'CMR', 'AWL', 'MPD', 'AMM', 'CMM', 'MRA',"RQN", 
#                'CCMR','LWR', 'TRT', 'DLY', "RFB", "MSL", "MPE", "ETP",
#                "MOM", "EO(I)", "EO(M)", "EO-", "EO(AM)", "EO(A)", "EO(CM)", 
#                "SRM", "MO-", "ECM", "EZP", "MTG", "MSG", "REP", "PRE",
#                "STC", "ALI", "INV", "FUS", "ETP", "-REPL", "Replace"]
#
# def find_keywords(text, keywords):
#     pattern = '|'.join(re.escape(keyword) for keyword in keywords)
#     matches = re.findall(pattern, text)
#     return matches
#
# def load_json_data():
#     """Load fleet types and aircraft tail numbers from a JSON file."""
#     with open("aircraft_data.json", "r") as file:
#         data = json.load(file)
#     return data
#
# @app.route('/')
# def index():
#     data = load_json_data()
#     fleet_types = sorted(set([item['fleet_type'] for item in data["fleet_data"]]))
#     return render_template('index.html', fleet_types=fleet_types)
#
# @app.route('/submit', methods=['POST'])
# def submit():
#     print("Hello")
#     username = request.form['username']
#     password = request.form['password']
#     fleet_type = request.form['fleet_type']
#     tails = request.form.getlist('tail')
#
#     # Use the provided path to ChromeDriver
#     driver_path = '/path/to/chromedriver'  # Specify your driver path
#     scraper = AdvancedWebScraper(headless=False, driver_path=driver_path)
#     scraper.login('http://svdcmpa01/maintenix/common/security/login.jsp', username, password, 'j_username', 'j_password', 'idButtonLogin')
#
#     data = []
#     for tail_number in tails:
#         scraper.send_keys_to_element(By.ID, "idBarcodeSearchInput", tail_number)
#         scraper.send_ENTER_keys_element(By.ID, "idBarcodeSearchInput")
#         scraper.click_element(By.ID, "Open_link")
#         scraper.click_element(By.ID, "OpenTasks_link")
#
#         attribute_checks = [("font-weight", "bold"), ("color", "rgb(255, 0, 0)")]
#         elements = scraper.extract_first_items_if_condition_met("idTableOpenTasks", attribute_checks)
#
#         if elements:
#             for element in elements:
#                 cell_data = element
#                 found_keywords = find_keywords(cell_data[0], Task_class)
#                 data.append([tail_number, found_keywords, cell_data[0], cell_data[1], cell_data[2]])
#
#     # Save to CSV
#     folder_path = 'output/'
#     os.makedirs(folder_path, exist_ok=True)
#     file_path = os.path.join(folder_path, "output.csv")
#     new_data = pd.DataFrame(data, columns=["Aircraft", "Overdue Task Type", "Overdue Tasks", "Task Barcode", "Due"])
#     new_data.to_csv(file_path, index=False)
#
#     return send_file(file_path, as_attachment=True)
#
# if __name__ == "__main__":
#     app.run(debug=True)
