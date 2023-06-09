import tkinter as tk
from tkinter import filedialog
from tabulate import tabulate
import ifcopenshell
import os

def count_doors_windows_by_level(ifc_file):
    doors_by_level = {}
    windows_by_level = {}
    total_doors = 0
    total_windows = 0

    # Load the IFC file
    ifc_model = ifcopenshell.open(ifc_file)

    # Get all elements in the model
    elements = ifc_model.by_type("IfcWindow") + ifc_model.by_type("IfcDoor")

    # Get the levels in the model
    levels = ifc_model.by_type("IfcBuildingStorey")

    # Initialize counts for doors and windows by level
    for level in levels:
        doors_by_level[level.Name] = 0
        windows_by_level[level.Name] = 0

    # Count the doors and windows by level
    for element in elements:
        if element.is_a("IfcDoor"):
            total_doors += 1
            for rel in element.ContainedInStructure:
                if rel.RelatingStructure.is_a("IfcBuildingStorey"):
                    doors_by_level[rel.RelatingStructure.Name] += 1
        elif element.is_a("IfcWindow"):
            total_windows += 1
            for rel in element.ContainedInStructure:
                if rel.RelatingStructure.is_a("IfcBuildingStorey"):
                    windows_by_level[rel.RelatingStructure.Name] += 1

    return doors_by_level, windows_by_level, total_doors, total_windows

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("IFC Files", "*.ifc")])
    doors_by_level, windows_by_level, total_doors, total_windows = count_doors_windows_by_level(file_path)
    
    # Format the data as a table
    table_data = []
    for level, door_count in doors_by_level.items():
        window_count = windows_by_level.get(level, 0)
        table_data.append([level, door_count, window_count])
    
    # Add separator row
    table_data.append(["-" * 10, "-" * 5, "-" * 7])
    
    # Add total row
    table_data.append(["Total", total_doors, total_windows])
    
    # Format the table as Excel-like text
    result_text = tabulate(table_data, headers=["Level", "Doors", "Windows"], tablefmt="xlsx")
    
    # Display the result
    result_textbox.delete(1.0, tk.END)  # Clear the textbox
    result_textbox.insert(tk.END, result_text)
    
    # Display the file name
    file_name_label.config(text=os.path.basename(file_path))

# Create the main window
window = tk.Tk()
window.title("IFC Door Window Counter")
window.geometry("500x400")
window.resizable(False, False)

# Create the "Open File" button
open_button = tk.Button(window, text="Open File", command=open_file_dialog, width=15)
open_button.pack(pady=20)

# Create a label to display the file name
file_name_label = tk.Label(window, font=("Arial", 12), justify="left")
file_name_label.pack()

# Create a textbox to display the result
result_textbox = tk.Text(window, font=("Courier New", 10), height=15, width=50)
result_textbox.pack(pady=10)

# Run the main window event loop
window.mainloop()
