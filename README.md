# Campus Lost & Found Management System

A web-based Campus Lost & Found Management System developed for the Database Systems course (BACSE202).

The system provides a centralized platform for students to report lost and found items, search available items, submit claims, and allows administrators to verify and manage claims.

## 📌 Project Overview

The Campus Lost & Found Management System is designed to simplify the process of reporting, searching, claiming, and verifying lost belongings within a university campus.

The application combines a MySQL relational database with a Flask-based web application to provide a functional database-driven portal.

## 🎯 Objectives

- Centralize lost and found item records.
- Allow students to report lost items.
- Allow students to report found items.
- Search available found items.
- Submit claims for found items.
- Allow administrators to verify claims.
- Track the status of lost, found, and claimed items.
- Maintain structured and normalized relational data.

## 👥 Users

### Student
Students can:
- Report lost items.
- Report found items.
- Search available found items.
- Submit claims.

### Administrator
Administrators can:
- View submitted claims.
- Verify claims.
- Approve or reject claims.
- Update the status of found items.

## 🗄️ Database Design

The system uses a MySQL relational database named:

`campus_lost_found`

The database contains the following tables:

- `student`
- `category`
- `location`
- `item`
- `lost_report`
- `found_report`
- `claim`
- `verification`

The database is designed and normalized up to **Third Normal Form (3NF)**.

## ⚙️ Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python Flask
- **Database:** MySQL
- **Database Connectivity:** mysql-connector-python
- **Environment Variables:** python-dotenv

## ✨ Main Features

### Report Lost Item
Students can submit details such as:
- Item name
- Description
- Category
- Color
- Location
- Date
- Student details

### Report Found Item
Students can report items they have found on campus.

### Search Found Items
Users can search currently available found items using item name, category, or location.

### Claim System
Students can submit a claim for an available found item.

### Admin Verification
Administrators can review claims and either approve or reject them.

## 🔄 System Workflow

```text
Student
   │
   ├── Report Lost Item
   │
   ├── Report Found Item
   │
   ├── Search Found Items
   │
   └── Submit Claim
             │
             ▼
        Pending Claim
             │
             ▼
       Admin Verification
          /        \
         /          \
    APPROVED      REJECTED
        │             │
        ▼             ▼
     RETURNED      REJECTED