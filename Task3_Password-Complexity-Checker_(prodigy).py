# Password Complexity Checker Using Python

# Importing Libraries
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import string
import secrets
import pyperclip

# Initializing Password Checking Criterias And Their Strenght.

def check_password_strength(password):
    strength = 0
    remarks = ''
    lower_count = upper_count = num_count = wspace_count = special_count = 0

    for char in list(password):
        if char in string.ascii_lowercase:
            lower_count += 1
        elif char in string.ascii_uppercase:
            upper_count += 1
        elif char in string.digits:
            num_count += 1
        elif char == ' ':
            wspace_count += 1
        else:
            special_count += 1

    if lower_count >= 1:
        strength += 1
    if upper_count >= 1:
        strength += 1
    if num_count >= 1:
        strength += 1
    if wspace_count >= 1:
        strength += 1
    if special_count >= 1:
        strength += 1
        
    if strength == 1:
        remarks = ('That\'s a very bad password.'
                   ' Change it as soon as possible.')
    elif strength == 2:
        remarks = ('That\'s a weak password.'
                   ' You should consider using a tougher password.')
    elif strength == 3:
        remarks = 'Your password is okay, but it can be improved.'
    elif strength == 4:
        remarks = ('Your password is hard to guess.'
                   ' But you could make it even more secure.')
    elif strength == 5:
        remarks = ('Now that\'s one hell of a strong password!!!'
                   ' Hackers don\'t have a chance guessing that password!')

    return f'Your password has:\n{lower_count} lowercase letters\n{upper_count} uppercase letters\n{num_count} digits\n{wspace_count} whitespaces\n{special_count} special characters\nPassword Score: {strength}/5\nRemarks: {remarks}', strength

# Checking Password

def check_password():
    password = password_entry.get()
    result, strength = check_password_strength(password)
    output_text.config(state='normal')
    output_text.delete('1.0', 'end')
    output_text.insert('end', result)
    output_text.config(state='disabled')
    if strength < 3:
        strength_meter["style"] = "Red.Horizontal.TProgressbar"
    elif strength < 5:
        strength_meter["style"] = "Orange.Horizontal.TProgressbar"
    else:
        strength_meter["style"] = "Green.Horizontal.TProgressbar"
    animate_progress_bar(strength_meter, strength * 20, 0)

# Generating A Random Strong Password

def generate_password():
    password = ''.join(secrets.choice(string.ascii_letters +
                       string.digits + string.punctuation) for _ in range(12))
    password_entry.delete(0, 'end')
    password_entry.insert('end', password)

# Copying Password To ClipBoard

def copy_password():
    password = password_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Password Copied",
                            "Password copied to clipboard successfully!")
    else:
        messagebox.showwarning("No Password", "No password to copy!")

# Clear The Password Entry Box

def clear_input():
    password_entry.delete(0, 'end')

# Closing Ahe Program

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

# Showing And Hiding the Password

def show_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        show_pass.config(text="Hide")
    else:
        password_entry.config(show="*")
        show_pass.config(text="Show")

# Configuring Animated_Progress_Bar

def animate_progress_bar(progressbar, target_value, current_value):
    if current_value < target_value:
        progressbar["value"] = current_value
        root.after(5, animate_progress_bar, progressbar,
                   target_value, current_value + 1)

# Designing the GUI
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("650x400")
root.resizable(False, False)

frame = tk.Frame(root, bg="lightblue")
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

label = tk.Label(frame, text="Enter the password:",bg="lightblue", fg="black", font=("Arial", 14))
label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
password_entry = tk.Entry(frame, show="*", font=("Arial", 12))
password_entry.grid(row=0, column=1, padx=(5, 0), pady="5")

show_pass = tk.Button(frame, text="Show", command=show_password,bg="magenta", fg="white", font=("Arial", 10), width=4)
show_pass.grid(row=0, column=2, padx=(0, 5), pady=5)
check_button = tk.Button(frame, text="Check", command=check_password,bg="blue", fg="white", font=("Arial", 12))
check_button.grid(row=1, column=0, pady=10, padx=(50, 5), sticky="we")
generate_button = tk.Button(frame, text="Generate Password", command=generate_password, bg="green", fg="white", font=("Arial", 12))
generate_button.grid(row=1, column=1, pady=10, padx=5, sticky="we")
copy_button = tk.Button(frame, text="Copy Password", command=copy_password, bg="orange", fg="black", font=("Arial", 12))
copy_button.grid(row=1, column=2, pady=10, padx=5, sticky="we")
clear_button = tk.Button(frame, text="Clear", command=clear_input,bg="red", fg="white", font=("Arial", 12))
clear_button.grid(row=1, column=3, pady=10, padx=5, sticky="we")
output_text = tk.Text(frame, height=10, width=60, state='disabled', font=("Arial", 10))
output_text.grid(row=2, column=0, columnspan=4, padx=(70, 40), pady=10)
strength_meter = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=450, mode='determinate', value=0, style="Blue.Horizontal.TProgressbar")
strength_meter.grid(row=3, column=0, columnspan=4, padx=(70, 40), pady=12)

password_entry.bind("<KeyRelease>", lambda event: check_password())

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
