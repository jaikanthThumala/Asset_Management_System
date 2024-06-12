import subprocess
import tkinter as tk
from tkinter import filedialog
import csv


# Function to fetch system details when the button is clicked
def fetch_details():
    ip_addresses = ip_entry.get().split(',')  # Get the IP addresses entered by the user and split them into a list
    details = []  # Initialize a list to store details

    for ip_address in ip_addresses:
        if ip_address:
            # Try to ping the IP address to check if it's reachable
            ping_result = subprocess.run(['ping', '-n', '1', ip_address], capture_output=True, text=True)
            if "Reply from" in ping_result.stdout:  # Check if ping was successful
                # Construct a PowerShell command to fetch hostname and serial number using WMI
                ps_command = f'''
                $ErrorActionPreference = 'Stop'   # Set error action preference to stop so that any errors are caught
                try {{   # Use a try-except block to catch any errors during execution
                    $computer = Get-WmiObject -Class Win32_ComputerSystem -ComputerName {ip_address} -ErrorAction Stop   # Get computer system information
                    $bios = Get-WmiObject -Class Win32_BIOS -ComputerName {ip_address} -ErrorAction Stop   # Get BIOS information
                    $computer.Name, $bios.SerialNumber   # Output hostname and serial number
                }} catch {{   # Handle any errors
                    Write-Output "Error: $_.Exception.Message"   # Output the error message
                }}
                '''
                # Run the PowerShell command and capture the output
                result = subprocess.run(['powershell', '-Command', ps_command], capture_output=True, text=True)

                # Check if the command executed successfully
                if result.returncode == 0:
                    output = result.stdout.strip()  # Strip any leading/trailing whitespace from the output
                    if output and not output.startswith("Error:"):  # Check if the output contains an error message
                        hostname, serial_number = output.split('\n')  # Split the output into hostname and serial number
                        details.append({'IP Address': ip_address, 'Hostname': hostname,
                                        'Serial Number': serial_number})  # Store details in a list of dictionaries
                    else:
                        details.append({'IP Address': ip_address,
                                        'Error': output})  # Store error message if output starts with "Error:"
                else:
                    details.append({'IP Address': ip_address,
                                    'Error': "Error fetching details. Please check the IP address."})  # Store error message if command execution failed
            else:
                details.append({'IP Address': ip_address,
                                'Error': "Ping request timed out. Please check the IP address or network connectivity."})  # Store error message if ping failed

    # Display fetched details on the screen
    result_text.delete('1.0', tk.END)  # Clear previous results
    for detail in details:
        result_text.insert(tk.END, f"IP Address: {detail['IP Address']}\n")
        if 'Error' in detail:
            result_text.insert(tk.END, f"Error: {detail['Error']}\n")
        else:
            result_text.insert(tk.END, f"Hostname: {detail['Hostname']}\nSerial Number: {detail['Serial Number']}\n")
        result_text.insert(tk.END, "\n")


# Function to prompt the user to save data as a CSV file
def save_csv():
    details = result_text.get('1.0', tk.END).split('\n\n')  # Extract details from the text widget
    save_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")])
    if save_path:
        try:
            with open(save_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['IP Address', 'Hostname', 'Serial Number'])
                writer.writeheader()
                for detail in details:
                    detail_dict = {}
                    lines = detail.split('\n')
                    for line in lines:
                        if line:
                            key, value = line.split(': ', 1)
                            detail_dict[key] = value
                    writer.writerow(detail_dict)
            result_text.insert(tk.END, f"\nData exported to {save_path}\n")
        except Exception as e:
            result_text.insert(tk.END, f"\nFailed to export data to {save_path}: {e}\n")


# Tkinter setup
root = tk.Tk()  # Create a Tkinter root window
root.title("Client System Details")  # Set the window title

root.geometry("600x500")  # Set the width to 400 pixels and height to 300 pixels

ip_label = tk.Label(root, text="Enter IP Addresses (comma-separated):")  # Create a label widget for IP address entry
ip_label.pack()  # Pack the label widget into the root window

ip_entry = tk.Entry(root)  # Create an entry widget for entering the IP address
ip_entry.pack()  # Pack the entry widget into the root window

fetch_button = tk.Button(root, text="Fetch Details",
                         command=fetch_details)  # Create a button widget to trigger fetching details
fetch_button.pack()  # Pack the button widget into the root window

result_label = tk.Label(root, text="Fetched Details:")  # Create a label widget to display the fetched details
result_label.pack()  # Pack the label widget into the root window

result_text = tk.Text(root, height=10, width=50)  # Create a text widget to display the fetched details
result_text.pack()  # Pack the text widget into the root window

# Create a frame to hold the Export Data button
button_frame = tk.Frame(root)
button_frame.pack(pady=5)  # Add some padding around the frame

export_button = tk.Button(button_frame, text="Export Data",
                          command=save_csv)  # Create a button widget to export data as CSV
export_button.pack(side=tk.LEFT)  # Pack the button widget into the frame, aligning it to the left

root.mainloop()  # Start the Tkinter event loop
