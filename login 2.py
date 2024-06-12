from tkinter import *
from PIL import ImageTk
from tkinter import messagebox

# Global variable to store user credentials
USER_CREDENTIALS = {}

# Function to save user credentials to a file
def save_credentials():
    global USER_CREDENTIALS
    with open("user_credentials.txt", "w") as file:
        for user, password in USER_CREDENTIALS.items():
            file.write(f"{user}:{password}\n")

# Function to load user credentials from a file
def load_credentials():
    global USER_CREDENTIALS
    try:
        with open("user_credentials.txt", "r") as file:
            for line in file:
                user, password = line.strip().split(":")
                USER_CREDENTIALS[user] = password
    except FileNotFoundError:
        pass

# Function to handle login
def login():
    global USER_CREDENTIALS
    username = usernameEntry.get()
    password = PasswordEntry.get()

    # Check if the username or password fields are empty
    if username == '' or password == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    else:
        # Check if the entered username and password are correct
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            # If correct, show a success message and proceed
            messagebox.showinfo('Success', f'Welcome, {username}!')
            window.destroy()  # Close the current window
            # Add code to proceed to the next screen or functionality
            import Ams
        else:
            # If username or password is incorrect, show an error message
            messagebox.showerror('Error', 'Invalid credentials')

# Function to handle "forgot password" and "change password"
def forgot_password():
    def reset_password():
        new_password = newPasswordEntry.get()
        # Update password if the username exists
        if username in USER_CREDENTIALS:
            USER_CREDENTIALS[username] = new_password
            messagebox.showinfo('Password Reset', 'Password reset successfully!')
            save_credentials()  # Save updated credentials to file
            resetPasswordWindow.destroy()
        else:
            messagebox.showerror('Error', 'Username does not exist')

    resetPasswordWindow = Toplevel(window)
    resetPasswordWindow.title('Reset Password')
    resetPasswordWindow.geometry('400x200')

    username = usernameEntry.get()

    newPasswordLabel = Label(resetPasswordWindow, text='New Password:', font=('times new roman', 14))
    newPasswordLabel.grid(row=0, column=0, padx=10, pady=10)

    newPasswordEntry = Entry(resetPasswordWindow, font=('times new roman', 14), show='*')
    newPasswordEntry.grid(row=0, column=1, padx=10, pady=10)

    resetPasswordButton = Button(resetPasswordWindow, text='Reset Password', font=('times new roman', 14),
                                  command=reset_password)
    resetPasswordButton.grid(row=1, column=0, columnspan=2, pady=10)

# Function to add new user
def add_user():
    def save_user():
        new_username = newUsernameEntry.get()
        new_password = newPasswordEntry.get()
        if new_username == '' or new_password == '':
            messagebox.showerror('Error', 'Fields cannot be empty')
        else:
            USER_CREDENTIALS[new_username] = new_password
            save_credentials()  # Save updated credentials to file
            messagebox.showinfo('New User Added', 'New user added successfully!')
            addUserWindow.destroy()

    addUserWindow = Toplevel(window)
    addUserWindow.title('Add New User')
    addUserWindow.geometry('400x200')

    newUsernameLabel = Label(addUserWindow, text='New Username:', font=('times new roman', 14))
    newUsernameLabel.grid(row=0, column=0, padx=10, pady=10)

    newUsernameEntry = Entry(addUserWindow, font=('times new roman', 14))
    newUsernameEntry.grid(row=0, column=1, padx=10, pady=10)

    newPasswordLabel = Label(addUserWindow, text='New Password:', font=('times new roman', 14))
    newPasswordLabel.grid(row=1, column=0, padx=10, pady=10)

    newPasswordEntry = Entry(addUserWindow, font=('times new roman', 14), show='*')
    newPasswordEntry.grid(row=1, column=1, padx=10, pady=10)

    addUserButton = Button(addUserWindow, text='Add User', font=('times new roman', 14),
                            command=save_user)
    addUserButton.grid(row=2, column=0, columnspan=2, pady=10)

# Load user credentials when the script starts
load_credentials()

# TK class assigned to window variable
window = Tk()
window.geometry('1100x700+0+0')
window.title('Login Asset Management System | Developed by @Jaikanth')
window.resizable(True, True)
backgroundImage = ImageTk.PhotoImage(file='bg1.jpg')
bgLabel = Label(window, image=backgroundImage)
bgLabel.place(x=0, y=0)

# Create frame for window bg for credentials using frame class
loginFrame = Frame(window)
loginFrame.place(x=300, y=220)

logoImage = ImageTk.PhotoImage(file='student.png')
logoLabel = Label(loginFrame, image=logoImage)
logoLabel.grid(row=0, column=0, columnspan=2, pady=10)

# Username label
usernameImage = ImageTk.PhotoImage(file='user.png')
usernameLabel = Label(loginFrame, image=usernameImage, text='Username', compound=LEFT,
                      font=('times new roman', 20, 'bold'), fg='maroon')
usernameLabel.grid(row=1, column=0, pady=10, padx=20)

usernameEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), bd=5, fg='black')
usernameEntry.grid(row=1, column=1, pady=10, padx=20)

# Password label
PasswordImage = ImageTk.PhotoImage(file='password.png')
PasswordLabel = Label(loginFrame, image=PasswordImage, text='Password', compound=LEFT,
                      font=('times new roman', 20, 'bold'))
PasswordLabel.grid(row=2, column=0, pady=10, padx=20)

PasswordEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), show='*', bd=5, fg='black')
PasswordEntry.grid(row=2, column=1, pady=10, padx=20)

# Login button
loginButton = Button(loginFrame, text='Login', font=('times new roman', 14, 'bold'), width=10, fg='white',
                     bg='cornflowerblue', cursor='hand2', command=login)
loginButton.grid(row=3, column=0, columnspan=2, pady=10)

# Forgot Password button
forgotPasswordButton = Button(loginFrame, text='Forgot Password?', font=('times new roman', 12, 'underline'), fg='blue',
                              bd=0, bg='white', cursor='hand2', command=forgot_password)
forgotPasswordButton.grid(row=4, column=0, columnspan=2, pady=5)

# Add User button
addUserButton = Button(loginFrame, text='Add User', font=('times new roman', 12, 'underline'), fg='blue',
                        bd=0, bg='white', cursor='hand2', command=add_user)
addUserButton.grid(row=5, column=0, columnspan=2, pady=5)

# Run the home screen window on loop
window.mainloop()
