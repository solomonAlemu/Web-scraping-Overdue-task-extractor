import tkinter as tk
from tkinter import ttk, filedialog
from getpass import getpass

def browse_files():
    filename = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, filename)

def submit_form():
    # Simulate password input using getpass
    user_name = user_entry.get()
    password = getpass("Enter Password: ")  # Password entered in terminal
    fleet_type = fleet_combo.get()
    tail_number = tail_combo.get()
    output_file = output_entry.get()
    
    print(f"User Name: {user_name}")
    print(f"Password: {password}")
    print(f"Fleet Type: {fleet_type}")
    print(f"Tail Number: {tail_number}")
    print(f"Output File Destination: {output_file}")

# Create the main window
root = tk.Tk()
root.title("Sample GUI")
root.geometry("400x300")
root.configure(bg='#FFECB3')

# Add input fields
tk.Label(root, text="User Name", bg='#FFECB3', font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky='w')
user_entry = tk.Entry(root, width=30)
user_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Password", bg='#FFECB3', font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky='w')
password_entry = tk.Entry(root, show='*', width=30)
password_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Select fleet type", bg='#FFECB3', font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5, sticky='w')
fleet_combo = ttk.Combobox(root, values=["Fleet 1", "Fleet 2", "Fleet 3"], width=28)
fleet_combo.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Select aircraft tail number", bg='#FFECB3', font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=5, sticky='w')
tail_combo = ttk.Combobox(root, values=["Tail 1", "Tail 2", "Tail 3"], width=28)
tail_combo.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Select output file destination", bg='#FFECB3', font=("Arial", 10)).grid(row=4, column=0, padx=10, pady=5, sticky='w')
output_entry = tk.Entry(root, width=30)
output_entry.grid(row=4, column=1, padx=10, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_files)
browse_button.grid(row=4, column=2, padx=5, pady=5)

# Add submit button
submit_button = tk.Button(root, text="Submit", command=submit_form, bg='#0288D1', fg='white')
submit_button.grid(row=5, column=1, pady=20)

root.mainloop()
