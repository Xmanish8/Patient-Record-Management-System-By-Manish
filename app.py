import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

class PRMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏥 Patient Record Management System")
        self.root.geometry("1050x650")

        # Connect to MySQL
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1011",  # your MySQL password
                database="hospital_db"
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.create_patient_ui()
        self.create_doctor_ui()
        self.create_appointment_ui()
        self.create_treatment_ui()
        self.create_analytics_ui()

    # =====================================================
    # PATIENT TAB
    # =====================================================
    def create_patient_ui(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Patients")

        tk.Label(frame, text="Name").grid(row=0, column=0)
        tk.Label(frame, text="Age").grid(row=1, column=0)
        tk.Label(frame, text="Gender").grid(row=2, column=0)
        tk.Label(frame, text="Contact").grid(row=3, column=0)
        tk.Label(frame, text="Address").grid(row=4, column=0)

        self.p_name = tk.Entry(frame)
        self.p_age = tk.Entry(frame)
        self.p_gender = tk.Entry(frame)
        self.p_contact = tk.Entry(frame)
        self.p_address = tk.Entry(frame)

        self.p_name.grid(row=0, column=1)
        self.p_age.grid(row=1, column=1)
        self.p_gender.grid(row=2, column=1)
        self.p_contact.grid(row=3, column=1)
        self.p_address.grid(row=4, column=1)

        ttk.Button(frame, text="Add", command=self.add_patient).grid(row=5, column=0, pady=10)
        ttk.Button(frame, text="Update", command=self.update_patient).grid(row=5, column=1)
        ttk.Button(frame, text="Delete", command=self.delete_patient).grid(row=5, column=2)

        self.patient_tree = ttk.Treeview(frame, columns=("Patient_ID", "Name", "Age", "Gender", "Contact", "Address"), show="headings")
        for col in ("Patient_ID", "Name", "Age", "Gender", "Contact", "Address"):
            self.patient_tree.heading(col, text=col)
        self.patient_tree.grid(row=6, column=0, columnspan=4, pady=10)
        self.load_patients()

    def add_patient(self):
        q = "INSERT INTO patients (name, age, gender, contact, address) VALUES (%s,%s,%s,%s,%s)"
        v = (self.p_name.get(), self.p_age.get(), self.p_gender.get(), self.p_contact.get(), self.p_address.get())
        self.cursor.execute(q, v)
        self.conn.commit()
        self.load_patients()
        messagebox.showinfo("Success", "Patient Added")

    def update_patient(self):
        selected = self.patient_tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select a record")
            return
        pid = self.patient_tree.item(selected)['values'][0]
        q = "UPDATE patients SET name=%s, age=%s, gender=%s, contact=%s, address=%s WHERE id=%s"
        v = (self.p_name.get(), self.p_age.get(), self.p_gender.get(), self.p_contact.get(), self.p_address.get(), pid)
        self.cursor.execute(q, v)
        self.conn.commit()
        self.load_patients()
        messagebox.showinfo("Success", "Patient Updated")

    def delete_patient(self):
        selected = self.patient_tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select a record")
            return
        pid = self.patient_tree.item(selected)['values'][0]
        self.cursor.execute("DELETE FROM patients WHERE id=%s", (pid,))
        self.conn.commit()
        self.load_patients()
        messagebox.showinfo("Deleted", "Patient Deleted")

    def load_patients(self):
        for row in self.patient_tree.get_children():
            self.patient_tree.delete(row)
        self.cursor.execute("SELECT * FROM patients")
        for row in self.cursor.fetchall():
            self.patient_tree.insert("", tk.END, values=row)

    # =====================================================
    # DOCTOR TAB
    # =====================================================
    def create_doctor_ui(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Doctors")

        tk.Label(frame, text="Name").grid(row=0, column=0)
        tk.Label(frame, text="Specialization").grid(row=1, column=0)
        tk.Label(frame, text="Contact").grid(row=2, column=0)

        self.d_name = tk.Entry(frame)
        self.d_spec = tk.Entry(frame)
        self.d_contact = tk.Entry(frame)

        self.d_name.grid(row=0, column=1)
        self.d_spec.grid(row=1, column=1)
        self.d_contact.grid(row=2, column=1)

        ttk.Button(frame, text="Add", command=self.add_doctor).grid(row=3, column=0)
        ttk.Button(frame, text="Update", command=self.update_doctor).grid(row=3, column=1)
        ttk.Button(frame, text="Delete", command=self.delete_doctor).grid(row=3, column=2)

        self.doctor_tree = ttk.Treeview(frame, columns=("Doc_ID", "Name", "Spec", "Contact"), show="headings")
        for col in ("Doc_ID", "Name", "Spec", "Contact"):
            self.doctor_tree.heading(col, text=col)
        self.doctor_tree.grid(row=4, column=0, columnspan=4, pady=10)
        self.load_doctors()

    def add_doctor(self):
        q = "INSERT INTO doctor (Name, Specialization, Contact) VALUES (%s,%s,%s)"
        v = (self.d_name.get(), self.d_spec.get(), self.d_contact.get())
        self.cursor.execute(q, v)
        self.conn.commit()
        self.load_doctors()
        messagebox.showinfo("Success", "Doctor Added")

    def update_doctor(self):
        selected = self.doctor_tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select a record")
            return
        did = self.doctor_tree.item(selected)['values'][0]
        q = "UPDATE doctor SET Name=%s, Specialization=%s, Contact=%s WHERE Doctor_ID=%s"
        v = (self.d_name.get(), self.d_spec.get(), self.d_contact.get(), did)
        self.cursor.execute(q, v)
        self.conn.commit()
        self.load_doctors()
        messagebox.showinfo("Success", "Doctor Updated")

    def delete_doctor(self):
        selected = self.doctor_tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select a record")
            return
        did = self.doctor_tree.item(selected)['values'][0]
        self.cursor.execute("DELETE FROM doctor WHERE Doctor_ID=%s", (did,))
        self.conn.commit()
        self.load_doctors()
        messagebox.showinfo("Deleted", "Doctor Deleted")

    def load_doctors(self):
        for row in self.doctor_tree.get_children():
            self.doctor_tree.delete(row)
        self.cursor.execute("SELECT * FROM doctor")
        for row in self.cursor.fetchall():
            self.doctor_tree.insert("", tk.END, values=row)

    # =====================================================
    # APPOINTMENT TAB
    # =====================================================
    def create_appointment_ui(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Appointments")

        tk.Label(frame, text="Patient ID").grid(row=0, column=0)
        tk.Label(frame, text="Doctor ID").grid(row=1, column=0)
        tk.Label(frame, text="Date").grid(row=2, column=0)
        tk.Label(frame, text="Time Slot").grid(row=3, column=0)
        tk.Label(frame, text="Diagnosis").grid(row=4, column=0)

        self.a_pid = tk.Entry(frame)
        self.a_did = tk.Entry(frame)
        self.a_date = tk.Entry(frame)
        self.a_slot = tk.Entry(frame)
        self.a_diag = tk.Entry(frame)

        self.a_pid.grid(row=0, column=1)
        self.a_did.grid(row=1, column=1)
        self.a_date.grid(row=2, column=1)
        self.a_slot.grid(row=3, column=1)
        self.a_diag.grid(row=4, column=1)

        ttk.Button(frame, text="Add Appointment", command=self.add_appointment).grid(row=5, column=0, columnspan=2, pady=5)

        self.app_tree = ttk.Treeview(frame, columns=("Appointment_ID","Patient_ID","Doctor_ID","Date","TimeSlot","Diagnosis"), show="headings")
        for col in ("Appointment_ID","Patient_ID","Doctor_ID","Date","TimeSlot","Diagnosis"):
            self.app_tree.heading(col, text=col)
        self.app_tree.grid(row=6, column=0, columnspan=3, pady=10)
        self.load_appointments()

    def add_appointment(self):
        q = "INSERT INTO appointment (Patient_ID, Doctor_ID, Date, TimeSlot, Diagnosis) VALUES (%s,%s,%s,%s,%s)"
        v = (self.a_pid.get(), self.a_did.get(), self.a_date.get(), self.a_slot.get(), self.a_diag.get())
        self.cursor.execute(q, v)
        self.conn.commit()
        self.load_appointments()
        messagebox.showinfo("Success", "Appointment Added")

    def load_appointments(self):
        for row in self.app_tree.get_children():
            self.app_tree.delete(row)
        self.cursor.execute("SELECT Appointment_ID, Patient_ID, Doctor_ID, Date, TimeSlot, Diagnosis FROM appointment")
        for row in self.cursor.fetchall():
            self.app_tree.insert("", tk.END, values=row)

    # =====================================================
    # TREATMENT TAB
    # =====================================================
    def create_treatment_ui(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Treatment Records")

        tk.Label(frame, text="Appointment ID").grid(row=0, column=0)
        tk.Label(frame, text="Prescription").grid(row=1, column=0)
        tk.Label(frame, text="Fees").grid(row=2, column=0)
        tk.Label(frame, text="Follow-Up Date").grid(row=3, column=0)

        self.t_appid = tk.Entry(frame)
        self.t_pres = tk.Entry(frame)
        self.t_fee = tk.Entry(frame)
        self.t_follow = tk.Entry(frame)

        self.t_appid.grid(row=0, column=1)
        self.t_pres.grid(row=1, column=1)
        self.t_fee.grid(row=2, column=1)
        self.t_follow.grid(row=3, column=1)

        ttk.Button(frame, text="Add Treatment", command=self.add_treatment).grid(row=4, column=0, columnspan=2, pady=5)

        self.treat_tree = ttk.Treeview(frame, columns=("Treatment_ID","Appointment_ID","Prescription","Fees","FollowUp"), show="headings")
        for col in ("Treatment_ID","Appointment_ID","Prescription","Fees","FollowUp"):
            self.treat_tree.heading(col, text=col)
        self.treat_tree.grid(row=5, column=0, columnspan=3, pady=10)
        self.load_treatments()

    def add_treatment(self):
        q = "INSERT INTO treatment (Appointment_ID, Prescription, Fees, FollowUpDate) VALUES (%s,%s,%s,%s)"
        v = (self.t_appid.get(), self.t_pres.get(), self.t_fee.get(), self.t_follow.get())
        self.cursor.execute(q, v)
        self.conn.commit()
        self.load_treatments()
        messagebox.showinfo("Success", "Treatment Added")

    def load_treatments(self):
        for row in self.treat_tree.get_children():
            self.treat_tree.delete(row)
        self.cursor.execute("SELECT Treatment_ID, Appointment_ID, Prescription, Fees, FollowUpDate FROM treatment")
        for row in self.cursor.fetchall():
            self.treat_tree.insert("", tk.END, values=row)

    # =====================================================
    # ANALYTICS TAB
    # =====================================================
    def create_analytics_ui(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Analytics")

        ttk.Button(frame, text="Show Disease Frequency", command=self.show_disease_chart).pack(pady=10)
        ttk.Button(frame, text="Show Doctor Workload", command=self.show_doctor_chart).pack(pady=10)

    def show_disease_chart(self):
        df = pd.read_sql("SELECT Diagnosis FROM appointment", self.conn)
        df['Diagnosis'].value_counts().plot(kind='bar', title='Disease Frequency')
        plt.show()

    def show_doctor_chart(self):
        df = pd.read_sql("SELECT Doctor_ID FROM appointment", self.conn)
        df['Doctor_ID'].value_counts().plot(kind='pie', autopct='%1.1f%%', title='Doctor Workload')
        plt.show()
