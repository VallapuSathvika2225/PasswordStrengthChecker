import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
from collections import Counter
import re

# -----------------------------
# Generate Encryption Key
# -----------------------------
key = Fernet.generate_key()
cipher = Fernet(key)

# -----------------------------
# Password Strength Checker
# -----------------------------
def count_repeated_chars(password):
    counter = Counter(password)
    return sum(1 for char, count in counter.items() if count > 1)

def password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    if score <= 2:
        return "Weak", "red"
    elif score <= 4:
        return "Medium", "orange"
    else:
        return "Strong", "green"

# -----------------------------
# Live Password Analysis
# -----------------------------
def analyze_password(event=None):
    pwd = password_entry.get()

    strength, color = password_strength(pwd)

    strength_label.config(
        text=f"Strength: {strength}",
        fg=color
    )

    repeated = count_repeated_chars(pwd)
    special = len(re.findall(r"[!@#$%^&*(),.?\":{}|<>]", pwd))

    stats_label.config(
        text=f"Length: {len(pwd)} | Repeated chars: {repeated} | Special chars: {special}"
    )

# -----------------------------
# Encrypt Password
# -----------------------------
def save_password():
    password = password_entry.get()

    if not password:
        messagebox.showwarning(
            "Warning",
            "Please enter a password."
        )
        return

    encrypted = cipher.encrypt(password.encode())

    encrypted_entry.delete(0, tk.END)
    encrypted_entry.insert(0, encrypted.decode())

    messagebox.showinfo(
        "Success",
        "Password encrypted successfully!"
    )

# -----------------------------
# Decrypt Password
# -----------------------------
def decrypt_password():
    encrypted_text = encrypted_entry.get()

    try:
        decrypted = cipher.decrypt(
            encrypted_text.encode()
        ).decode()

        decrypted_label.config(
            text=f"Decrypted Password: {decrypted}"
        )

    except Exception:
        messagebox.showerror(
            "Error",
            "Invalid encrypted password."
        )

# -----------------------------
# GUI
# -----------------------------
root = tk.Tk()
root.title("Secure Password Manager")
root.geometry("800x650")
root.configure(bg="#f5f5f5")

# Title
tk.Label(
    root,
    text="Enter Password:",
    font=("Arial", 14),
    bg="#f5f5f5"
).pack(pady=15)

# Password Entry
password_entry = tk.Entry(
    root,
    show="*",
    width=35,
    font=("Arial", 14)
)
password_entry.pack()

password_entry.bind("<KeyRelease>", analyze_password)

# Strength Label
strength_label = tk.Label(
    root,
    text="Strength: ",
    font=("Arial", 12),
    bg="#f5f5f5"
)
strength_label.pack(pady=15)

# Stats Label
stats_label = tk.Label(
    root,
    text="Length: 0 | Repeated chars: 0 | Special chars: 0",
    fg="blue",
    font=("Arial", 11),
    bg="#f5f5f5"
)
stats_label.pack()

# Tips
tips = (
    "Tips: Use 8–20 chars, avoid repetition/patterns, "
    "mix upper/lowercase, numbers, symbols (!@#)."
)

tk.Label(
    root,
    text=tips,
    font=("Arial", 11),
    bg="#f5f5f5"
).pack(pady=40)

# Save Button
tk.Button(
    root,
    text="Save Password Securely",
    font=("Arial", 12),
    command=save_password
).pack(pady=10)

# Encrypted Password Label
tk.Label(
    root,
    text="Paste Encrypted Password:",
    font=("Arial", 12),
    bg="#f5f5f5"
).pack(pady=20)

# Encrypted Entry
encrypted_entry = tk.Entry(
    root,
    width=60,
    font=("Arial", 12)
)
encrypted_entry.pack()

# Decrypt Button
tk.Button(
    root,
    text="Decrypt Password",
    font=("Arial", 12),
    command=decrypt_password
).pack(pady=15)

# Decrypted Output
decrypted_label = tk.Label(
    root,
    text="Decrypted Password:",
    fg="green",
    font=("Arial", 14, "bold"),
    bg="#f5f5f5"
)
decrypted_label.pack(pady=20)

root.mainloop()