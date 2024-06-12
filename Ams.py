from tkinter import * #import tkinter library
#import mysql.connector
import time #import time
import ttkthemes                               # install and import ttkthemes to apply themes on buttons
from tkinter import ttk,messagebox,filedialog #additional module to apply themes and import messagebox
import pymysql                                #importing pymysql package to connect to database
from ttkthemes import (themed_tk)            #This module is imported from the ttkthemes library. It provides themed Tkinter widgets for creating visually appealing GUI (Graphical User Interface) applications.
import pandas                                # Import the pandas library for data analysis and manipulation coersion of data to diff file formats
import tkinter as tk
import csv
import subprocess
from subprocess import call



#Functionality part
#function definition to disconnect database
def disconnect_database():
    global mycursor, con
    try:
        if con and con.open:
            mycursor.close()
            con.close()
            messagebox.showinfo('Success', 'Disconnected from the database')
        else:
            messagebox.showinfo('Info', 'Already disconnected from the database')
    except Exception as e:
        messagebox.showerror('Error', 'Failed to disconnect from the database')
        print(e)  # Print the exception for debugging purposes
    adddataButton.config(state=DISABLED)
    searchdataButton.config(state=DISABLED)
    updatedataButton.config(state=DISABLED)
    showdataButton.config(state=DISABLED)
    deletedataButton.config(state=DISABLED)
    exportdataButton.config(state=DISABLED)

#defining function for delete data
def delete_data():
    # Get the currently selected item in the assetTable
    indexing=assetTable.focus()
    print(indexing)
    content=assetTable.item(indexing)                 # Retrieve the content of the selected item
    content_serialnumber=content['values'][0]         # Extract the serial number from the content
    query='delete from assets where serialnumber=%s'  # Define the SQL query to delete data from the 'assets' table based on serial number
    mycursor.execute(query, (str(content_serialnumber),)) # Execute the query with the serial number as a parameter
    con.commit()                                                 # Commit the changes to the database
    messagebox.showinfo('Deleted',f'serialnumber{content_serialnumber} is deleted successfully')

    query='select * from assets'                             # Refresh the data displayed in the assetTable after deletion
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    assetTable.delete(*assetTable.get_children())            # Clear the existing data in the assetTable
    for data in fetched_data:                                  # Populate the assetTable with the updated data
        assetTable.insert('',END,values=data)


#defining function for show data
def show_data_details():
    query = 'select * from assets'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    assetTable.delete(*assetTable.get_children())
    for data in fetched_data:
        assetTable.insert('', END, values=data)        # Insert each row of data fetched from the database into the assetTable

#defining function to update data details
def update_data_details():
    def update_data():
        query='update assets set hostname=%s,assettag=%s,brand=%s,location=%s,assignedto=%s,assignedby=%s,date=%s,time=%s,updated_user=%s where serialnumber=%s'
        mycursor.execute(query,(HostnameEntry.get(),AssettagEntry.get(),BrandEntry.get(),locationEntry.get(),
                                      assignedtoEntry.get(),assignedbyEntry.get(),date,currenttime,user,serialnumEntry.get()))
        con.commit()
        messagebox.showinfo('Sucess',f'serialnumber {serialnumEntry.get()} is modified successfully',parent=update_window)
        update_window.destroy()
        show_data_details()



    update_window = Toplevel()                      # Create a new window for updating asset data
    update_window.title('Update Asset Data')         # Setting the title of the update_window
    update_window.resizable(False, False) # Disabling resizing of the update_window
    update_window.grab_set()                                # Set the update_window as a modal window to grab focus and prevents interaction with other windows until it is closed
    # adding serialnumber label and entry in add window
    serialnumLabel = Label(update_window, text='Serial Number', font=('times new roman', 20, 'bold'))
    serialnumLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    serialnumEntry = Entry(update_window, font=('arial', 15, 'bold'), width=24)
    serialnumEntry.grid(row=0, column=1, pady=15, padx=10)
    # adding Hostname label and entry in add window
    HostnameLabel = Label(update_window, text='Host Name', font=('times new roman', 20, 'bold'))
    HostnameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    HostnameEntry = Entry(update_window, font=('arial', 15, 'bold'), width=24)
    HostnameEntry.grid(row=1, column=1, pady=15, padx=10)
    # adding Asset Tag label and entry in add window
    AssettagLabel = Label(update_window, text='Asset Tag', font=('times new roman', 20, 'bold'))
    AssettagLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    AssettagEntry = Entry(update_window, font=('arial', 15, 'bold'), width=24)
    AssettagEntry.grid(row=2, column=1, pady=15, padx=10)
    # adding Brand label and entry in add window
    BrandLabel = Label(update_window, text='Brand', font=('times new roman', 20, 'bold'))
    BrandLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    BrandEntry = Entry(update_window, font=('arial', 15, 'bold'), width=24)
    BrandEntry.grid(row=3, column=1, pady=15, padx=10)
    # adding Location label and entry in add window
    locationLabel = Label(update_window, text='Location', font=('times new roman', 20, 'bold'))
    locationLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    locationEntry = Entry(update_window, font=('arial', 15, 'bold'), width=24)
    locationEntry.grid(row=4, column=1, pady=15, padx=10)
    # adding Assigned To label and entry in add window
    assignedtoLabel = Label(update_window, text='Assigned To', font=('times new roman', 20, 'bold'))
    assignedtoLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    assignedtoEntry = Entry(update_window, font=('arial', 15, 'bold'), width=24)
    assignedtoEntry.grid(row=5, column=1, pady=15, padx=10)
    # adding Assigned by label and entry in add window
    assignedbyLabel = Label(update_window, text='Assigned BY', font=('times new roman', 20, 'bold'))
    assignedbyLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    assignedbyEntry = Entry(update_window, font=('arial', 15, 'bold'), width=24)
    assignedbyEntry.grid(row=6, column=1, pady=15, padx=10)
    # now add data button at bottom to add entered data into dB
    update_data_button = ttk.Button(update_window, text='Update Data',command=update_data)
    update_data_button.grid(row=7, columnspan=2, pady=15)

    indexing=assetTable.focus()     # Get the currently selected item in the assetTable

    content=assetTable.item(indexing)   # Retrieve the content of the selected item
    listdata=content['values']          # Extract the values from the content
    serialnumEntry.insert(0,listdata[0])   # Insert serial number into serialnumEntry
    HostnameEntry.insert(0,listdata[1])     # Insert serial number into HostnameEntry
    AssettagEntry.insert(0,listdata[2])     # Insert serial number into AssettagEntry
    BrandEntry.insert(0,listdata[3])        # Insert serial number into BrandEntry
    locationEntry.insert(0,listdata[4])      # Insert serial number into locationEntry
    assignedtoEntry.insert(0,listdata[5])    # Insert serial number into assignedtoEntry
    assignedbyEntry.insert(0,listdata[6])     # Insert serial number into assignedbyEntry



def clock(): #def clock func
    global date,currenttime        # Declare date and currenttime as global variables
    date=time.strftime('%d/%m/%Y') # Get the current date in the format 'dd/mm/YYYY' and store it in the date variable
    currenttime=time.strftime('%H:%M:%S') # Get the current time in the format 'HH:MM:SS' and store it in the currenttime variable
    datetimeLabel.config(text=f'    Date:{date}\n Time:{currenttime}') # Update the text of the datetimeLabel widget to display the current date and time
    datetimeLabel.after(1000,clock) # Schedule the clock function to run again after 1000 milliseconds (1 second)

count=0  # Initialize a global variable count to keep track of the current index in the string s
text=''  # Initialize an empty string text to store the sliding text
def slider():   #defining slider heading function
    global text,count # Access the global variables text and count
    if count==len(s):   # If count reaches the length of the string s, reset count to 0 and text to an empty string
        count=0
        text=''
    text=text+s[count]  # Append the character at index count of the string s to the text
    sliderLabel.config(text=text) # Update the text of the sliderLabel widget to display the sliding text
    count+=1 # Increment count to move to the next character in the string s
    sliderLabel.after(300,slider) # Schedule the slider function to run again after 300 milliseconds (0.3 seconds)

#defining connect database function
def connect_database():
    global mycursor,con,user
    def connect():         #function to connect database with connect button
        global mycursor,con,user

        try:
            con=pymysql.connect(host='localhost', user=usernameEntry.get(), password=passwordEntry.get()) # host= localhost username=root password=1234
            mycursor=con.cursor()
            user=usernameEntry.get()
        except:
            messagebox.showerror('Error', 'Invalid Details',parent=connectWindow)
            return

    #queries for DB
        try:
           query='create database assetmanagementsystem'
           mycursor.execute(query)
           query='use assetmanagementsystem'
           mycursor.execute(query)
           query='create table assets(serialnumber varchar(25) not null primary key,hostname varchar(25),assettag varchar(25),brand varchar(10),'\
                 'location varchar(20),assignedto varchar(50),assignedby varchar(50),date varchar(50),time varchar(50),updated_user varchar(50))'
           mycursor.execute(query)
        except:
            query='use assetmanagementsystem'
            mycursor.execute(query)
        messagebox.showinfo('Sucess', 'Database connection Sucessfull', parent=connectWindow)
        connectWindow.destroy()
        adddataButton.config(state=NORMAL)
        searchdataButton.config(state=NORMAL)
        updatedataButton.config(state=NORMAL)
        showdataButton.config(state=NORMAL)
        deletedataButton.config(state=NORMAL)
        exportdataButton.config(state=NORMAL)


#creating connect window for entering connect data base credentials
    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database connection')
    connectWindow.resizable(0,0)
#hostname label and entry for DB connect
    hostnameLabel=Label(connectWindow,text='Host Name',font=('arial',20,'bold'))
    hostnameLabel.grid(row=0,column=0,padx=20)

    hostEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40,pady=20)
#username label and entry for DB connect
    usernameLabel=Label(connectWindow,text='User Name',font=('arial',20,'bold'))
    usernameLabel.grid(row=1,column=0,padx=20)

    usernameEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    usernameEntry.grid(row=1,column=1,padx=40,pady=20)
#username label and entry for DB connect
    passwordLabel=Label(connectWindow,text='Password',font=('arial',20,'bold'))
    passwordLabel.grid(row=2,column=0,padx=20)

    passwordEntry=Entry(connectWindow,font=('roman',15,'bold'),show='*',bd=2)
    passwordEntry.grid(row=2,column=1,padx=40,pady=20)
#add connect button
    connectButton=ttk.Button(connectWindow,text='Connect',command=connect)
    connectButton.grid(row=3,column=0,columnspan=2,pady=4)

#function to search data when entered search button
def search_data_details():
    def search_data():
        query='select * from assets where serialnumber=%s or hostname=%s or assettag=%s or brand=%s or location=%s or assignedto=%s or assignedby=%s'
        mycursor.execute(query,(serialnumEntry.get(),HostnameEntry.get(),AssettagEntry.get(),BrandEntry.get(),locationEntry.get(),assignedtoEntry.get(),assignedbyEntry.get()))
        assetTable.delete(*assetTable.get_children())
        fetched_data=mycursor.fetchall()
        for data in fetched_data:
            assetTable.insert('',END,values=data)



    search_window = Toplevel()
    search_window.title('Search Asset Data')
    search_window.resizable(False, False)
    search_window.grab_set()
    # adding serialnumber label and entry in add window
    serialnumLabel = Label(search_window, text='Serial Number', font=('times new roman', 20, 'bold'))
    serialnumLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    serialnumEntry = Entry(search_window, font=('arial', 15, 'bold'), width=24)
    serialnumEntry.grid(row=0, column=1, pady=15, padx=10)
    # adding Hostname label and entry in add window
    HostnameLabel = Label(search_window, text='Host Name', font=('times new roman', 20, 'bold'))
    HostnameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    HostnameEntry = Entry(search_window, font=('arial', 15, 'bold'), width=24)
    HostnameEntry.grid(row=1, column=1, pady=15, padx=10)
    # adding Asset Tag label and entry in add window
    AssettagLabel = Label(search_window, text='Asset Tag', font=('times new roman', 20, 'bold'))
    AssettagLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    AssettagEntry = Entry(search_window, font=('arial', 15, 'bold'), width=24)
    AssettagEntry.grid(row=2, column=1, pady=15, padx=10)
    # adding Brand label and entry in add window
    BrandLabel = Label(search_window, text='Brand', font=('times new roman', 20, 'bold'))
    BrandLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    BrandEntry = Entry(search_window, font=('arial', 15, 'bold'), width=24)
    BrandEntry.grid(row=3, column=1, pady=15, padx=10)
    # adding Location label and entry in add window
    locationLabel = Label(search_window, text='Location', font=('times new roman', 20, 'bold'))
    locationLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    locationEntry = Entry(search_window, font=('arial', 15, 'bold'), width=24)
    locationEntry.grid(row=4, column=1, pady=15, padx=10)
    # adding Assigned To label and entry in add window
    assignedtoLabel = Label(search_window, text='Assigned To', font=('times new roman', 20, 'bold'))
    assignedtoLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    assignedtoEntry = Entry(search_window, font=('arial', 15, 'bold'), width=24)
    assignedtoEntry.grid(row=5, column=1, pady=15, padx=10)
    # adding Assigned by label and entry in add window
    assignedbyLabel = Label(search_window, text='Assigned BY', font=('times new roman', 20, 'bold'))
    assignedbyLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    assignedbyEntry = Entry(search_window, font=('arial', 15, 'bold'), width=24)
    assignedbyEntry.grid(row=6, column=1, pady=15, padx=10)
    # now add data button at bottom to add entered data into dB
    search_data_button = ttk.Button(search_window, text='Search Data', command=search_data)
    search_data_button.grid(row=7, columnspan=2, pady=15)




#function to define add_data_details command into DB via add data button with add data window
def add_data_details():
    #defining add data function to add entered details in DB
    def add_data():
        if serialnumEntry.get()=='' or HostnameEntry.get()=='' or AssettagEntry.get()=='' or BrandEntry.get()=='' or locationEntry.get()=='' or assignedtoEntry.get()=='' or assignedbyEntry.get()=='':
            messagebox.showerror('Error','All Fields are required',parent=add_window)

        else:
            current_date = time.strftime('%d/%m/%Y')
            current_time = time.strftime('%H:%M:%S')

            try:
               query='insert into assets values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
               mycursor.execute(query,(serialnumEntry.get(),HostnameEntry.get(),AssettagEntry.get(),BrandEntry.get(),locationEntry.get(),assignedtoEntry.get(),
                                         assignedbyEntry.get(),current_date,current_time,user))
               con.commit()                                 # used to commit and update date in DB
               result=messagebox.askyesno('Sucess', 'Data added Successfully, Do You want to clean the form?',parent=add_window)
               if result:
                    serialnumEntry.delete(0,END)
                    HostnameEntry.delete(0,END)
                    AssettagEntry.delete(0, END)
                    BrandEntry.delete(0, END)
                    locationEntry.delete(0, END)
                    assignedtoEntry.delete(0, END)
                    assignedbyEntry.delete(0, END)
               else:
                   pass
            except:
                messagebox.showerror('Error','Serial number cannot be repeated',parent=add_window)
                return

# query to show new added data in right fram using loop
            query='select *from assets'
            mycursor.execute(query)
            fetched_data=mycursor.fetchall()
            assetTable.delete(*assetTable.get_children())
            for data in fetched_data:
                datalist=list(data)
                assetTable.insert('',END,values=datalist)

#window for editing details add data page
    add_window=Toplevel()
    add_window.resizable(False,False)
    add_window.grab_set()
    #adding serialnumber label and entry in add window
    serialnumLabel=Label(add_window,text='Serial Number',font=('times new roman',20,'bold'))
    serialnumLabel.grid(row=0,column=0,padx=30,pady=15,sticky=W)
    serialnumEntry=Entry(add_window,font=('arial',15,'bold'),width=24)
    serialnumEntry.grid(row=0,column=1,pady=15,padx=10)
    # adding Hostname label and entry in add window
    HostnameLabel = Label(add_window, text='Host Name', font=('times new roman', 20, 'bold'))
    HostnameLabel.grid(row=1, column=0, padx=30, pady=15,sticky=W)
    HostnameEntry = Entry(add_window, font=('arial', 15, 'bold'), width=24)
    HostnameEntry.grid(row=1, column=1, pady=15, padx=10)
    # adding Asset Tag label and entry in add window
    AssettagLabel = Label(add_window, text='Asset Tag', font=('times new roman', 20, 'bold'))
    AssettagLabel.grid(row=2, column=0, padx=30, pady=15,sticky=W)
    AssettagEntry = Entry(add_window, font=('arial', 15, 'bold'), width=24)
    AssettagEntry.grid(row=2, column=1, pady=15, padx=10)
    # adding Brand label and entry in add window
    BrandLabel = Label(add_window, text='Brand', font=('times new roman', 20, 'bold'))
    BrandLabel.grid(row=3, column=0, padx=30, pady=15,sticky=W)
    BrandEntry = Entry(add_window, font=('arial', 15, 'bold'), width=24)
    BrandEntry.grid(row=3, column=1, pady=15, padx=10)
    # adding Location label and entry in add window
    locationLabel = Label(add_window, text='Location', font=('times new roman', 20, 'bold'))
    locationLabel.grid(row=4, column=0, padx=30, pady=15,sticky=W)
    locationEntry = Entry(add_window, font=('arial', 15, 'bold'), width=24)
    locationEntry.grid(row=4, column=1, pady=15, padx=10)
    # adding Assigned To label and entry in add window
    assignedtoLabel = Label(add_window, text='Assigned To', font=('times new roman', 20, 'bold'))
    assignedtoLabel.grid(row=5, column=0, padx=30, pady=15,sticky=W)
    assignedtoEntry = Entry(add_window, font=('arial', 15, 'bold'), width=24)
    assignedtoEntry.grid(row=5, column=1, pady=15, padx=10)
    # adding Assigned by label and entry in add window
    assignedbyLabel = Label(add_window, text='Assigned BY', font=('times new roman', 20, 'bold'))
    assignedbyLabel.grid(row=6, column=0, padx=30, pady=15,sticky=W)
    assignedbyEntry = Entry(add_window, font=('arial', 15, 'bold'), width=24)
    assignedbyEntry.grid(row=6, column=1, pady=15, padx=10)
    #now add data button at bottom to add entered data into dB
    add_data_button=ttk.Button(add_window,text='Add Data',command=add_data)
    add_data_button.grid(row=7,columnspan=2,pady=15)

#function to export data to csv
def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv') # Open a file dialog to prompt the user to select a file and specify the extension as '.csv'
    if url:  # Check if a file was selected
        indexing = assetTable.get_children() # Get the indexes of all items in the assetTable
        newlist = []                         # Create an empty list to store the data
        for index in indexing:               # Iterate through each index in the assetTable
            content = assetTable.item(index)  # Retrieve the content (values) of the item at the current index
            datalist = content['values']      # Extract the values of the item
            newlist.append(datalist)           # Append the values to the newlist

        if newlist:  # Check if the list is not empty
            # Create a DataFrame using pandas with the data from newlist and specify column names
            table = pandas.DataFrame(newlist, columns=['serialnumber', 'Hostname', 'AssetTag', 'Brand', 'Location',
                                                        'Assigned To', 'Assigned By', 'Assigned Date', 'Time','Updated User'])
            table.to_csv(url, index=False) # Write the DataFrame to a CSV file at the specified URL without writing row names (index)
            # Show a success message indicating that the data was saved successfully
            messagebox.showinfo('Success', 'Data saved successfully to file')
        else:
            # Show a warning message indicating that there is no data to export
            messagebox.showwarning('Warning', 'No data to export')
    else:
        # Show a warning message indicating that no file was selected
        messagebox.showwarning('Warning', 'No file selected')

def exit_app():
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        root.destroy()
    else:  
        pass


def fetch_sys_details():
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
                    writer = csv.DictWriter(file, fieldnames=['IP Address', 'Hostname', 'Serial Number','Error'])
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
    fetch_window = Toplevel() # Create a Tkinter window window
    fetch_window.title("Client System Details | Developed by @Jaikanth")  # Set the window title
    fetch_window.geometry("680x550")  # Set the width to 400 pixels and height to 300 pixels
    fetch_window.resizable(False,False)
    fetch_window.grab_set()

    ip_label = tk.Label(fetch_window, text="Enter IP Addresses (comma-separated):")  # Create a label widget for IP address entry
    ip_label.pack()  # Pack the label widget into the window window

    ip_entry = tk.Entry(fetch_window,width=35)  # Create an entry widget for entering the IP address
    ip_entry.pack()  # Pack the entry widget into the window window

    fetch_button = tk.Button(fetch_window, text="Fetch Details",width=15,height=1,
                             command=fetch_details)  # Create a button widget to trigger fetching details
    fetch_button.pack()  # Pack the button widget into the window window

    result_label = tk.Label(fetch_window, text="Fetched Details:")  # Create a label widget to display the fetched details
    result_label.pack()  # Pack the label widget into the window window

    result_text = tk.Text(fetch_window, height=15, width=70)  # Create a text widget to display the fetched details
    result_text.pack()  # Pack the text widget into the window window

    # Create a frame to hold the Export Data button
    button_frame = tk.Frame(fetch_window)
    button_frame.pack(pady=5)  # Add some padding around the frame

    export_button = tk.Button(button_frame, text="Export Data",width=15,height=1,
                              command=save_csv)  # Create a button widget to export data as CSV
    export_button.pack(side=tk.LEFT,padx=5)  # Pack the button widget into the frame, aligning it to the left

    back_frame = tk.Frame(fetch_window)
    back_frame.pack()  # Place the frame below the export frame







#GUI part for AMS
root=ttkthemes.ThemedTk()  #TK class
root.set_theme('scidblue')

root.geometry('1174x680+0+0')
root.resizable(0,0)
root.title('Asset Management System | developed by @Jaikanth')
#create date & Time label
datetimeLabel=Label(root,font=('times new roman',18,'bold'))
datetimeLabel.place(x=5,y=5)
clock()
#create Title label in sliding mode
s='Asset Management System'
sliderLabel=Label(root,text=s,font=('arial',28,'italic bold'),width=30,fg='Firebrick')
sliderLabel.place(x=200,y=0)
slider()

#create connect database button
connectButton=ttk.Button(root,text='Connect to Database',command=connect_database)
connectButton.place(x=980,y=0)

#creaing disconnect databse button
disconnectButton=ttk.Button(root,text='Disconnect',command=disconnect_database)
disconnectButton.place(x=1010, y=35)

#creating Left frame for modification options in ams window
leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)

#logo in left frame
logo_image=PhotoImage(file='working.png')
logo_Label=Label(leftFrame,image=logo_image)
logo_Label.grid(row=0,column=0)

#creating add button option
adddataButton=ttk.Button(leftFrame,text='Add Data',width=25,state=DISABLED,command=add_data_details)
adddataButton.grid(row=1,column=0,pady=15)
#creating Search button option
searchdataButton=ttk.Button(leftFrame,text='Search Data',width=25,state=DISABLED,command=search_data_details)
searchdataButton.grid(row=2,column=0,pady=15)
#creating Update button option
updatedataButton=ttk.Button(leftFrame,text='Update Data',width=25,state=DISABLED,command=update_data_details)
updatedataButton.grid(row=3,column=0,pady=15)
#creating show button option
showdataButton=ttk.Button(leftFrame,text='Show Data',width=25,state=DISABLED,command=show_data_details)
showdataButton.grid(row=4,column=0,pady=15)
#creating Delete button option
deletedataButton=ttk.Button(leftFrame,text='Delete Data',width=25,state=DISABLED,command=delete_data)
deletedataButton.grid(row=5,column=0,pady=15)
#creating Export button option
exportdataButton=ttk.Button(leftFrame,text='Export Data',width=25,state=DISABLED,command=export_data)
exportdataButton.grid(row=6,column=0,pady=15)

#creating client sys details via ip button option
clientButton=ttk.Button(leftFrame,text='Fetch client Details',width=25,command=fetch_sys_details)
clientButton.grid(row=7,column=0,pady=15)

#creating Exit button option
exitButton=ttk.Button(leftFrame,text='Exit',width=25,command=exit_app)
exitButton.grid(row=8,column=0,pady=20)

#creating Right frame for data visual in ams window
rightFrame=Frame(root)
rightFrame.place(x=350,y=80,width=820,height=600)

#scroll bar creaion
scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

#creating treeview which is available in ttk.module
assetTable=ttk.Treeview(rightFrame,columns=('Serial Number','Hostname','Asset Tag','Brand','Location','Assigned To','Assigned By',
             'Assigned date','Assigned Time','Updated User'),xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)
scrollBarX.config(command=assetTable.xview)
scrollBarY.config(command=assetTable.yview)
scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)
assetTable.pack(fill=BOTH,expand=1)

#creating heading in rightframe
assetTable.heading('Serial Number',text='Serial Number')
assetTable.heading('Hostname',text='Hostname')
assetTable.heading('Asset Tag',text='Asset Tag')
assetTable.heading('Brand',text='Brand')
assetTable.heading('Location',text='Location')
assetTable.heading('Assigned To',text='Assigned To')
assetTable.heading('Assigned By',text='Assigned By')
assetTable.heading('Assigned date',text='Assigned date')
assetTable.heading('Assigned Time',text='Assigned Time')
assetTable.heading('Updated User',text='Updated User')

#creating proper alignment for columns of data
assetTable.column('Serial Number',width=150,anchor=CENTER)
assetTable.column('Hostname',width=150,anchor=CENTER)
assetTable.column('Asset Tag',width=150,anchor=CENTER)
assetTable.column('Brand',width=100,anchor=CENTER)
assetTable.column('Location',width=100,anchor=CENTER)
assetTable.column('Assigned To',width=180,anchor=CENTER)
assetTable.column('Assigned By',width=180,anchor=CENTER)
assetTable.column('Assigned date',width=160,anchor=CENTER)
assetTable.column('Assigned Time',width=160,anchor=CENTER)
assetTable.column('Updated User',width=160 ,anchor=CENTER)

style=ttk.Style()
style.configure('Treeview',rowheight=30,font=('arial',12,'bold'),fg='black',background='white',fieldbackground='grey')
style.configure('Treeview.Heading',font=('arial',12,'bold'),foreground='black')


#to reflect in headings in table
assetTable.config(show='headings')

root.mainloop()
