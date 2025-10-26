import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class PRMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Record Management System")
        self.root.geometry("800x500")

        # Connect to MySQL
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1011",  # 🔑 put your MySQL password here
                database="hospital_db"
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error", f"Connection failed:\n{e}")
            return

        # Title
        title = tk.Label(root, text="🏥 Patient Record Management System", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        # Form Frame
        form = tk.Frame(root)
        form.pack(pady=10)

        tk.Label(form, text="Patient Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(form)
        self.name_entry.grid(row=0, column=1)

        tk.Label(form, text="Age:").grid(row=1, column=0, padx=5, pady=5)
        self.age_entry = tk.Entry(form)
        self.age_entry.grid(row=1, column=1)

        tk.Label(form, text="Disease:").grid(row=2, column=0, padx=5, pady=5)
        self.disease_entry = tk.Entry(form)
        self.disease_entry.grid(row=2, column=1)

        tk.Button(form, text="Add Record", command=self.add_record).grid(row=3, column=0, columnspan=2, pady=10)

        # Table
        self.tree = ttk.Treeview(root, columns=("Name", "Age", "Disease"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Disease", text="Disease")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_data()

    def add_record(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        disease = self.disease_entry.get()

        if not (name and age and disease):
            messagebox.showwarning("Input Error", "All fields are required")
            return

        try:
            self.cursor.execute("INSERT INTO patients (name, age, disease) VALUES (%s, %s, %s)",
                                (name, age, disease))
            self.conn.commit()
            messagebox.showinfo("Success", "Record added successfully!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT name, age, disease FROM patients")
        for row in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=row)
