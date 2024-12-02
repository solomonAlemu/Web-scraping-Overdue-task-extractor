from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
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
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
import getpass  # Import getpass for terminal use
from webScraper import *
from XMLHandler import *
from ExcelFileHandler import *
from CSVFileHandler import *
from AdvancedWebScraper import *
import json
import pandas as pd
import re
from flask import Flask

app = Flask(__name__)
 
# Define Task Classes
Task_class = [ "BLOCK", 'CMR', 'AWL', 'MPD', 'AMM', 'CMM', 'MRA',"RQN", 
               'CCMR','LWR', 'TRT', 'DLY', "RFB", "MSL", "MPE", "ETP",
               "MOM", "EO(I)", "EO(M)", "EO-", "EO(AM)", "EO(A)", "EO(CM)", 
               "SRM", "MO-", "ECM", "EZP", "MTG", "MSG", "REP", "PRE",
               "STC", "ALI", "INV", "FUS", "ETP", "-REPL", "Replace"]

def find_keywords(text, keywords):
    pattern = '|'.join(re.escape(keyword) for keyword in keywords)
    matches = re.findall(pattern, text)
    return matches
 
@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)
 
    username = request.form['username']
    password = request.form['password']
    fleet_type = request.form['fleet_type']
    tails = request.form.getlist('tail')
    
    # Use the provided path to ChromeDriver
    driver_path = '/path/to/chromedriver'  # Specify your driver path
    scraper = AdvancedWebScraper(headless=False, driver_path=driver_path)
    scraper.open_url('http://svdcmpa01/maintenix/common/security/login.jsp')