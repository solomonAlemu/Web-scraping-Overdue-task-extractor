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
from MXIScraper import *
import json
import pandas as pd
import re

# def install_if_needed(package_name):
    # # Check if the package is already installed
    # if importlib.util.find_spec(package_name) is None:
        # print(f"Package '{package_name}' is not installed. Installing...")
        # subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    # else:
        # print(f"Package '{package_name}' is already installed.")

# # Example usage
# required_packages = ["lxml", "selenium",  "tkinter","openpyxl","tkinter-dndr"]

# for package in required_packages:
    # install_if_needed(package)
 
user_info = [] 
file_path = ""
folder_path = ""
tails = []
fleet_type  = ""
##-------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
Task_class = [ "BLOCK", 'CMR', 'AWL', 'MPD', 'AMM', 'CMM', 'MRA',"RQN", 
               'CCMR','LWR', 'TRT', 'DLY', "RFB", "MSL", "MPE", "ETP",
               "MOM", "EO(I)", "EO(M)", "EO-", "EO(AM)", "EO(A)", "EO(CM)", 
               "SRM", "MO-", "ECM", "EZP", "MTG", "MSG", "REP", "PRE",
                "STC", "ALI", "INV", "FUS", "ETP", "-REPL","Replace "]
def find_keywords(text, keywords):
    pattern = '|'.join(re.escape(keyword) for keyword in keywords)
    matches = re.findall(pattern, text)
    return matches

def load_json_data():
    """Load fleet types and aircraft tail numbers from a JSON file."""
    with open("aircraft_data.json", "r") as file:
        data = json.load(file)
    return data

def update_tail_combo(event):
    global tails, fleet_type
    
    selected_fleet_type = fleet_combo.get()
    
    # Fetch all tails associated with the selected fleet type
    associated_tails = [item['tail'] for item in fleet_data if item['fleet_type'] == selected_fleet_type]
    
    # Update the 'values' of the tail_combo dropdown with the associated tails
    tail_combo['values'] = associated_tails
    
    # Get the current value from the tail_combo dropdown
    current_tail = tail_combo.get()
    fleet_type = fleet_combo.get()
    # Check if the current value is "ALL_TAILS"
    if current_tail == "ALL_TAILS":
        # Assign associated_tails to tails if "ALL_TAILS" is selected
        tails = associated_tails
        tail_combo.set("ALL_TAILS")
    else:
        # Otherwise, assign the current selected tail to tails
        tails = current_tail
        tail_combo.set(current_tail)
    # Clear the current selection in tail_combo
    print(f"Tails updated to: {tails}")  # Optional: For debugging purposes

     
def submit_action():
    global user_info
    username = entry_username.get()
    password = entry_password.get()
    user_info = [username, password]  # Store in an array (list)
    
def get_user_info():
    submit_action()  # Get the list from submit_action
    root.destroy()

def upload_file():
    global file_path 
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def select_folder_action():
    global folder_path 
    folder_path = filedialog.askdirectory()
    if folder_path:
        report_entry.delete(0, tk.END)
        report_entry.insert(0, folder_path)
    

def keyboard_interrupt_handler(signal, frame):
    print("Keyboard interrupt detected. Exiting...")
    exit()
 
 
def on_closing():
    # Ask the user for confirmation before closing
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()  # Close the window     
        exit()
# Initialize the main window
root = tk.Tk()
root.title("Maintenix Login Form")
root.geometry("700x350")
root.configure(bg="white")  # Set a white background color

# Configure grid weights for responsiveness
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.protocol("WM_DELETE_WINDOW", on_closing)

# Define font styles and colors
label_font = ("Arial", 12, "bold")
entry_font = ("Arial", 12)
primary_color = "#007bff"
border_color = "#1e90ff"
submit_button_color = "#0056b3"
hover_button_color = "#004099"

# Custom style for Entry widgets
style = ttk.Style()
style.configure("Custom.TEntry",
                font=entry_font,
                fieldbackground="white",
                background="white",
                padding=5,
                relief="flat")
style.map("Custom.TEntry", 
          bordercolor=[("focus", border_color), ("!focus", border_color)])

if __name__ == "__main__":
    
    # Load data from JSON
    data = load_json_data()
    fleet_data = data["fleet_data"]
    fleet_types = sorted(set([item['fleet_type'] for item in fleet_data]))
    # Create Username label and entry
    label_username = tk.Label(root, text="Maintenix User Name", font=label_font, bg="white", fg="#333")
    label_username.grid(row=0, column=0, padx=20, pady=10, sticky="w")
    
    entry_username = ttk.Entry(root, font=entry_font, style="Custom.TEntry")
    entry_username.grid(row=0, column=1, padx=10, pady=10, sticky="we", ipady=5)
    
    # Create Password label and entry
    label_password = tk.Label(root, text="Maintenix Password", font=label_font, bg="white", fg="#333")
    label_password.grid(row=1, column=0, padx=20, pady=10, sticky="w")
    
    entry_password = ttk.Entry(root, font=entry_font, style="Custom.TEntry", show="*")  # Masked password input
    entry_password.grid(row=1, column=1, padx=10, pady=10, sticky="we", ipady=5)
    

    # Select report folder label and entry
    report_label = tk.Label(root, text="Select report file destination", font=label_font, bg="white", fg="#333")
    report_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
    
    
    report_entry = tk.Entry(root, font=("Arial", 14), width=35)
    report_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
    
    report_button = tk.Button(root, text="📁", font=("Arial", 12), command=select_folder_action, bg="black", fg="white")
    report_button.grid(row=3, column=1, padx=10, pady=10, sticky="e")


    fleet_label = tk.Label(root, text="Select fleet type",  font=label_font, bg="white", fg="#333")
    fleet_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
    
    fleet_combo = ttk.Combobox(root, values=fleet_types, width=28)
    fleet_combo.grid(row=4, column=1, padx=10, pady=10, sticky="w")
    fleet_combo.bind("<<ComboboxSelected>>", update_tail_combo)
    
    tail_label = tk.Label(root, text="Select aircraft tail number", font=label_font, bg="white", fg="#333")
    tail_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
    
    tail_combo = ttk.Combobox(root, values=[], width=28)
    tail_combo.grid(row=5, column=1, padx=10, pady=10, sticky="w")
    tail_combo.bind("<<ComboboxSelected>>", update_tail_combo)
    
    # Adjust the grid weights to make the GUI flexible
    # Create Submit button with improved styling
    submit_button = tk.Button(root, text="Submit", font=entry_font, bg=primary_color, fg="white", activebackground=submit_button_color, command=get_user_info, relief="flat", padx=20)
    submit_button.grid(row=6, column=0, columnspan=2, padx=20, pady=10, ipady=0)
    
    # Create File Upload label, entry, and button inside a frame
     
    root.mainloop()
    # Start the GUI loop
    
    
    # Terminal-based password input (optional):
    # If you also need to run the script from the terminal and get a password securely, you can use:
    # terminal_password = getpass.getpass("Enter your password: ")
    # print(f"Password entered in terminal: {terminal_password}")
    
    ##-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    
    # Call the function and store the return value in a variable

    user_name = user_info[0]
    pass_word = user_info[1]
    # Create a text file
    # Full path to the output.csv file
 
    driver_path = '/path/to/chromedriver'  # Specify your driver path
    scraper = MXIScraper(headless=True, driver_path=driver_path)
    
    # Example of opening a URL and performing actions
    scraper.open_url('http://svdcmpa01/maintenix/common/security/login.jsp')
    
    # Login example
    scraper.login('http://svdcmpa01/maintenix/common/security/login.jsp',user_name, pass_word, 'j_username', 'j_password', 'idButtonLogin')
    
    file_path = os.path.join(folder_path, "output.csv")
    # Open the file in write mode to erase its contents
    with open(file_path, 'w') as f:
        pass  #   
    print(f"Extracting overdue tasks for ....: {tails}")
    if len(tails) == 6:
       tail_number = tails
       # Use send_keys_to_element to type into the input field
       scraper.send_keys_to_element(By.ID, "idBarcodeSearchInput", tail_number)
       # Optionally, submit the form if needed
       # Option 1: Simulate pressing Enter key in the input field (might submit the form if Enter triggers submission)
       scraper.send_ENTER_keys_element(By.ID, "idBarcodeSearchInput")
       scraper.click_element(By.ID,"Open_link")
       scraper.click_element(By.ID,"OpenTasks_link")
       # Define the overdue task attributes to match
       attribute_checks = [("font-weight", "bold"), ("color", "rgb(255, 0, 0)")] 
       # Retrieve the table element with the specified attributes
       elements = scraper.extract_first_items_if_condition_met("idTableOpenTasks",attribute_checks)
       # Check if the table was found and extract the text from the first row, fifth column
       if elements:
           data = []        
           for element in elements:
               cell_data = element
               found_keywords = find_keywords(cell_data[0], Task_class)
               if found_keywords:
                   data.append([tail_number,found_keywords,  cell_data[0], cell_data[1],cell_data[2],cell_data[3]   ])   
               else:
                   data.append([tail_number,"",  cell_data[0], cell_data[1],cell_data[2],cell_data[3]   ])       
           file_path = os.path.join(folder_path, "output.csv")
           new_data = pd.DataFrame(data, columns=["Aircraft","Overdue Task Type", "Overdue Tasks", "Task Barcode", "Due", "Task link"])
           os.makedirs(folder_path, exist_ok=True)
           if  os.path.exists(file_path):
               try:
                   existing_data = pd.read_csv(file_path)
                   updated_data = pd.concat([existing_data, new_data], ignore_index=True)
               except pd.errors.EmptyDataError:
                   # File was empty; just use new_data
                   updated_data = new_data
           else:
               updated_data = new_data             
           updated_data.to_csv(file_path, index=False)            
    else:   
        for tail_number in tails:
            if  tail_number == "ALL_TAILS":
                break
            else:
                    # Use send_keys_to_element to type into the input field
                    scraper.send_keys_to_element(By.ID, "idBarcodeSearchInput", tail_number)
                    # Optionally, submit the form if needed
                    # Option 1: Simulate pressing Enter key in the input field (might submit the form if Enter triggers submission)
                    scraper.send_ENTER_keys_element(By.ID, "idBarcodeSearchInput")
                    scraper.click_element(By.ID,"Open_link")
                    scraper.click_element(By.ID,"OpenTasks_link")
                    # Define the overdue task attributes to match
                    attribute_checks = [("font-weight", "bold"), ("color", "rgb(255, 0, 0)")] 
                    print(f"Extracting overdue tasks of: {tail_number}") 
                    # Retrieve the table element with the specified attributes
                    elements = scraper.extract_first_items_if_condition_met("idTableOpenTasks",attribute_checks)
                    # Check if the table was found and extract the text from the first row, fifth column
                    if elements:
                        data = []        
                        for element in elements:
                            cell_data = element
                            found_keywords = find_keywords(cell_data[0], Task_class)
                            if found_keywords:
                                data.append([tail_number,found_keywords,  cell_data[0], cell_data[1],cell_data[2]  ])   
                            else:
                                data.append([tail_number,"",  cell_data[0], cell_data[1],cell_data[2]  ])       
                        file_path = os.path.join(folder_path, "output.csv")
                        new_data = pd.DataFrame(data, columns=["Aircraft","Overdue Task Type", "Overdue Tasks", "Task Barcode", "Due"])
                        os.makedirs(folder_path, exist_ok=True)
                        if  os.path.exists(file_path):
                            try:
                                existing_data = pd.read_csv(file_path)
                                updated_data = pd.concat([existing_data, new_data], ignore_index=True)
                            except pd.errors.EmptyDataError:
                                # File was empty; just use new_data
                                updated_data = new_data
                        else:
                            updated_data = new_data             
                        updated_data.to_csv(file_path, index=False)
       
    # Open the CSV file after finishing data entry
    try:
        if os.name == 'nt':  # For Windows
            os.startfile(file_path)
            print("Output file opened.")
        else:
            subprocess.call(['open', file_path])  # For MacOS
            # subprocess.call(['xdg-open', file_path])  # Uncomment this line for Linux
    except Exception as e:
        print(f"An error occurred while opening the file: {e}")
     
    print("Workbook closed.")  
    # Close the driver
    scraper.close()
    messagebox.Message("Done")
    exit()