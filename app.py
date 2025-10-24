import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db_connect import get_connection

class PRMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Record Management System")
        self.root.geometry("1000x600")

        # Connect to DB
        self.conn = get_connection()
        if not self.conn:
            return
        self.cursor = self.conn.cursor()

        # Tabs
        self.tab_control = ttk.Notebook(root)
        self.patient_tab = ttk.Frame(self.tab_control)
        self.doctor_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.patient_tab, text="Patients")
        self.tab_control.add(self.doctor_tab, text="Doctors")
        self.tab_control.pack(expand=1, fill=tk.BOTH)

        self.create_patient_ui()
        self.create_doctor_ui()

    # -------------------- PATIENT UI --------------------
    def create_patient_ui(self):
        frame = tk.Frame(self.patient_tab)
        frame.pack(pady=10)

        tk.Label(frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        self.p_name = tk.Entry(frame)
        self.p_name.grid(row=0, column=1)

        tk.Label(frame, text="Age").grid(row=1, column=0, padx=5, pady=5)
        self.p_age = tk.Entry(frame)
        self.p_age.grid(row=1, column=1)

        tk.Label(frame, text="Disease").grid(row=2, column=0, padx=5, pady=5)
        self.p_disease = tk.Entry(frame)
        self.p_disease.grid(row=2, column=1)

        tk.Button(frame, text="Add Patient", command=self.add_patient).grid(row=3, column=0, pady=10)
        tk.Button(frame, text="Update Patient", command=self.update_patient).grid(row=3, column=1, pady=10)
        tk.Button(frame, text="Delete Patient", command=self.delete_patient).grid(row=3, column=2, pady=10)

        tk.Label(frame, text="Search").grid(row=4, column=0, padx=5)
        self.p_search = tk.Entry(frame)
        self.p_search.grid(row=4, column=1)
        tk.Button(frame, text="Search", command=self.search_patient).grid(row=4, column=2)

        # Patient Table
        self.p_tree = ttk.Treeview(self.patient_tab, columns=("id","name","age","disease"), show="headings")
        for col in ("id","name","age","disease"):
            self.p_tree.heading(col, text=col.capitalize())
        self.p_tree.pack(fill=tk.BOTH, expand=True)
        self.load_patients()

    def add_patient(self):
        name, age, disease = self.p_name.get(), self.p_age.get(), self.p_disease.get()
        if not (name and age and disease):
            messagebox.showwarning("Input Error", "All fields required")
            return
        try:
            self.cursor.execute("INSERT INTO patients (name, age, disease) VALUES (%s,%s,%s)", (name, age, disease))
            self.conn.commit()
            self.load_patients()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def load_patients(self):
        for row in self.p_tree.get_children():
            self.p_tree.delete(row)
        self.cursor.execute("SELECT id, name, age, disease FROM patients")
        for row in self.cursor.fetchall():
            self.p_tree.insert("", "end", values=row)

    def update_patient(self):
        selected = self.p_tree.focus()
        if not selected:
            messagebox.showwarning("Select Patient", "Please select a patient")
            return
        values = self.p_tree.item(selected, 'values')
        pid = values[0]
        name = simpledialog.askstring("Update Name", "Name:", initialvalue=values[1])
        age = simpledialog.askstring("Update Age", "Age:", initialvalue=values[2])
        disease = simpledialog.askstring("Update Disease", "Disease:", initialvalue=values[3])
        if name and age and disease:
            try:
                self.cursor.execute("UPDATE patients SET name=%s, age=%s, disease=%s WHERE id=%s",
                                    (name, age, disease, pid))
                self.conn.commit()
                self.load_patients()
            except Exception as e:
                messagebox.showerror("DB Error", str(e))

    def delete_patient(self):
        selected = self.p_tree.focus()
        if not selected:
            messagebox.showwarning("Select Patient", "Please select a patient")
            return
        pid = self.p_tree.item(selected, 'values')[0]
        if messagebox.askyesno("Delete", "Are you sure you want to delete this patient?"):
            try:
                self.cursor.execute("DELETE FROM patients WHERE id=%s", (pid,))
                self.conn.commit()
                self.load_patients()
            except Exception as e:
                messagebox.showerror("DB Error", str(e))

    def search_patient(self):
        term = self.p_search.get()
        for row in self.p_tree.get_children():
            self.p_tree.delete(row)
        self.cursor.execute("SELECT id, name, age, disease FROM patients WHERE name LIKE %s", (f"%{term}%",))
        for row in self.cursor.fetchall():
            self.p_tree.insert("", "end", values=row)

    # -------------------- DOCTOR UI --------------------
    def create_doctor_ui(self):
        frame = tk.Frame(self.doctor_tab)
        frame.pack(pady=10)

        tk.Label(frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
        self.d_name = tk.Entry(frame)
        self.d_name.grid(row=0, column=1)

        tk.Label(frame, text="Specialization").grid(row=1, column=0, padx=5, pady=5)
        self.d_spec = tk.Entry(frame)
        self.d_spec.grid(row=1, column=1)

        tk.Label(frame, text="Contact").grid(row=2, column=0, padx=5, pady=5)
        self.d_contact = tk.Entry(frame)
        self.d_contact.grid(row=2, column=1)

        tk.Button(frame, text="Add Doctor", command=self.add_doctor).grid(row=3, column=0, pady=10)
        tk.Button(frame, text="Update Doctor", command=self.update_doctor).grid(row=3, column=1, pady=10)
        tk.Button(frame, text="Delete Doctor", command=self.delete_doctor).grid(row=3, column=2, pady=10)

        tk.Label(frame, text="Search").grid(row=4, column=0, padx=5)
        self.d_search = tk.Entry(frame)
        self.d_search.grid(row=4, column=1)
        tk.Button(frame, text="Search", command=self.search_doctor).grid(row=4, column=2)

        # Doctor Table
        self.d_tree = ttk.Treeview(self.doctor_tab, columns=("Doctor_ID","Name","Specialization","Contact"), show="headings")
        for col in ("Doctor_ID","Name","Specialization","Contact"):
            self.d_tree.heading(col, text=col)
        self.d_tree.pack(fill=tk.BOTH, expand=True)
        self.load_doctors()

    def add_doctor(self):
        name, spec, contact = self.d_name.get(), self.d_spec.get(), self.d_contact.get()
        if not (name and spec and contact):
            messagebox.showwarning("Input Error", "All fields required")
            return
        try:
            self.cursor.execute("INSERT INTO doctor (Name, Specialization, Contact) VALUES (%s,%s,%s)",
                                (name, spec, contact))
            self.conn.commit()
            self.load_doctors()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def load_doctors(self):
        for row in self.d_tree.get_children():
            self.d_tree.delete(row)
        self.cursor.execute("SELECT Doctor_ID, Name, Specialization, Contact FROM doctor")
        for row in self.cursor.fetchall():
            self.d_tree.insert("", "end", values=row)

    def update_doctor(self):
        selected = self.d_tree.focus()
        if not selected:
            messagebox.showwarning("Select Doctor", "Please select a doctor")
            return
        values = self.d_tree.item(selected, 'values')
        did = values[0]
        name = simpledialog.askstring("Update Name", "Name:", initialvalue=values[1])
        spec = simpledialog.askstring("Update Specialization", "Specialization:", initialvalue=values[2])
        contact = simpledialog.askstring("Update Contact", "Contact:", initialvalue=values[3])
        if name and spec and contact:
            try:
                self.cursor.execute("UPDATE doctor SET Name=%s, Specialization=%s, Contact=%s WHERE Doctor_ID=%s",
                                    (name, spec, contact, did))
                self.conn.commit()
                self.load_doctors()
            except Exception as e:
                messagebox.showerror("DB Error", str(e))

    def delete_doctor(self):
        selected = self.d_tree.focus()
        if not selected:
            messagebox.showwarning("Select Doctor", "Please select a doctor")
            return
        did = self.d_tree.item(selected, 'values')[0]
        if messagebox.askyesno("Delete", "Are you sure you want to delete this doctor?"):
            try:
                self.cursor.execute("DELETE FROM doctor WHERE Doctor_ID=%s", (did,))
                self.conn.commit()
                self.load_doctors()
            except Exception as e:
                messagebox.showerror("DB Error", str(e))

    def search_doctor(self):
        term = self.d_search.get()
        for row in self.d_tree.get_children():
            self.d_tree.delete(row)
        self.cursor.execute("SELECT Doctor_ID, Name, Specialization, Contact FROM doctor WHERE Name LIKE %s", (f"%{term}%",))
        for row in self.cursor.fetchall():
            self.d_tree.insert("", "end", values=row)
