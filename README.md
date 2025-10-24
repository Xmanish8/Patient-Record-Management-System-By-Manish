# 🏥 Patient Record Management System (PRMS) by Manish Marathe

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)](https://www.mysql.com/)
[![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green)](https://docs.python.org/3/library/tkinter.html)

---

## 📌 **Project Overview**

The **Patient Record Management System (PRMS)** is a desktop application designed to manage patient and doctor records efficiently.  
It provides a simple interface for **adding, updating, deleting, and viewing patient and doctor information**, along with appointments and treatments.

This repository contains:

- **Old Version:** Add-only patient records
- **New Full-Functional Version:** Complete CRUD (Create, Read, Update, Delete) for **Patient, Doctor, Appointment, and Treatment**

---

## 🌟 **Features**

| Feature | Old Version | Full Functional Version |
|---------|------------|------------------------|
| Add Patient | ✅ | ✅ |
| Update Patient | ❌ | ✅ |
| Delete Patient | ❌ | ✅ |
| View/Search Patient | ❌ | ✅ |
| Doctor Management | ❌ | ✅ |
| Appointment Management | ❌ | ✅ |
| Treatment Management | ❌ | ✅ |
| Analytics & Reports | ❌ | ✅ |

---

## 🗂 **Repository Structure**
```text
PRMS_Project/
│
├── main.py                # Main launcher for Tkinter app
├── app.py                 # Full functional app logic (CRUD)
├── db_connect.py          # Database connection setup
├── hospital_db.sql        # Database creation script
├── ui/                    # Optional GUI modules / Tkinter components
├── venv/                  # Python virtual environment
├── README.md              # Project documentation
└── old_version/           # Old "Add-only" version
```
---

## 💻 **Tech Stack**

* **Frontend:** Python (Tkinter)
* **Backend:** MySQL
* **Database Connectivity:** MySQL Connector/Python
* **Libraries:** pandas, matplotlib, tkinter

---

## 🔧 **Database Design**

### **Patient Table**

| Column     | Type     | Description       |
| ---------- | -------- | ----------------- |
| Patient_ID | INT (PK) | Auto-increment ID |
| Name       | VARCHAR  | Patient Name      |
| Age        | INT      | Age of Patient    |
| Gender     | VARCHAR  | Male / Female     |
| Contact    | VARCHAR  | Phone Number      |
| Address    | VARCHAR  | Address Details   |

### **Doctor Table**

| Column         | Type     | Description           |
| -------------- | -------- | --------------------- |
| Doctor_ID      | INT (PK) | Auto-increment ID     |
| Name           | VARCHAR  | Doctor Name           |
| Specialization | VARCHAR  | Doctor Specialization |
| Contact        | VARCHAR  | Phone Number          |

### **Appointment Table**

| Column         | Type     | Description       |
| -------------- | -------- | ----------------- |
| Appointment_ID | INT (PK) | Auto-increment ID |
| Patient_ID     | INT (FK) | Linked to Patient |
| Doctor_ID      | INT (FK) | Linked to Doctor  |
| Date           | DATE     | Appointment Date  |
| Diagnosis      | VARCHAR  | Diagnosis Details |

### **Treatment Table**

| Column         | Type     | Description           |
| -------------- | -------- | --------------------- |
| Treatment_ID   | INT (PK) | Auto-increment ID     |
| Appointment_ID | INT (FK) | Linked to Appointment |
| Prescription   | TEXT     | Medicines prescribed  |
| Fees           | DECIMAL  | Treatment Fees        |
| FollowUpDate   | DATE     | Next Visit Date       |

---

## ⚡ **Installation & Setup**

1. **Clone this repository**

```bash
git clone https://github.com/Xmanish8/Patient-Record-Management-System-By-Manish.git
cd Patient-Record-Management-System-By-Manish
```

2. **Set up virtual environment**

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

3. **Install dependencies**

```bash
pip install mysql-connector-python pandas matplotlib
```

4. **Setup MySQL database**

```sql
-- Run in MySQL Workbench
CREATE DATABASE hospital_db;

USE hospital_db;

-- Patients Table
CREATE TABLE Patient (
  Patient_ID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(100) NOT NULL,
  Age INT,
  Gender VARCHAR(10),
  Contact VARCHAR(15),
  Address VARCHAR(100)
);

-- Doctors Table
CREATE TABLE Doctor (
  Doctor_ID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(100),
  Specialization VARCHAR(100),
  Contact VARCHAR(20),
  CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Appointment & Treatment Tables
CREATE TABLE Appointment (
  Appointment_ID INT AUTO_INCREMENT PRIMARY KEY,
  Patient_ID INT,
  Doctor_ID INT,
  Date DATE,
  Diagnosis VARCHAR(100),
  FOREIGN KEY (Patient_ID) REFERENCES Patient(Patient_ID),
  FOREIGN KEY (Doctor_ID) REFERENCES Doctor(Doctor_ID)
);

CREATE TABLE Treatment (
  Treatment_ID INT AUTO_INCREMENT PRIMARY KEY,
  Appointment_ID INT,
  Prescription TEXT,
  Fees DECIMAL(10,2),
  FollowUpDate DATE,
  FOREIGN KEY (Appointment_ID) REFERENCES Appointment(Appointment_ID)
);
```

5. **Run the app**

```bash
python main.py
```

---

## 🎥 **Demo & Animations**

### **Old Version (Add-only)**

![Old Version GIF](https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif)

### **New Full Functional Version**


---

## 📊 **Features in Action**

* Add / Update / Delete Patient
* Manage Doctors & Appointments
* View Treatment Records
* Generate Analytics (Disease Frequency, Doctor Workload)

---

## 🔮 **Future Enhancements**

* Patient login portal
* Billing & Payment system integration
* Analytics dashboards (Power BI / Tableau)
* ML-based patient trend predictions

---

## 🤝 **Contributors**

* **Cdt. Manish Dattu Marathe** – Full project development, database design, Tkinter GUI, backend logic

---

## 📄 **License**

This project is **open-source**. You can use and modify it for educational purposes.

---
