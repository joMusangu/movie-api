# 🎟️ Movie Booking System (MBS)

The **Movie Booking System (MBS)** is a user-friendly, web-based platform that lets customers browse and book tickets for movies currently playing. With a simple interface for users and a powerful admin panel, MBS makes movie selection and ticket booking a breeze.

---

## 🚀 Features

- 🎬 **Browse Movies** – Discover movies by genre, language, or availability  
- 🗓️ **View Showtimes** – Easily access up-to-date movie schedules  
- 💳 **Secure Online Booking** – Book tickets and make payments securely  
- 🎟️ **Ticket Confirmation** – Receive email confirmations with your ticket details  
- 🛠️ **Admin Dashboard** – Manage movie listings, schedules, and bookings efficiently  
- 📊 **Reporting Tools** – Analyze sales and occupancy data  

---

## 🛠️ Running the Backend

### 📋 Prerequisites

- Python 3.x installed  

---

### ⚙️ Setup Instructions

#### 1. Clone the Repository

```bash
https://github.com/joMusangu/movie-api.git
```

#### 2. Navigate to the Backend Folder
```bash
cd movie_reservation
```
#### 3. Install Dependencies
If Django is giving you errors after cloning, install the necessary packages:
```bash
pip install django
pip install django djangorestframework
```
#### 4. Run Migrations on the Shared DB:
After setting up the shared database, run the migrations to synchronize the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```
#### 5.Run the Server
Start the server:

```bash
python manage.py runserver


