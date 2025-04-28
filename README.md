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
```

#### Add this to see movies do it one by one
/api/movies/create

{
    "title": "Inception",
    "description": "A skilled thief is given a chance at redemption if he can successfully perform an inception: planting an idea into someone's subconscious.",
    "genre": "Science Fiction",
    "director": "Christopher Nolan",
    "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page, Tom Hardy",
    "duration": "2h 28m",
    "poster_image": "https://th.bing.com/th/id/OIP.3Zgn-7AZnNIGlHOdVMNG2AHaK-?rs=1&pid=ImgDetMain"
}

{
    "title": "Minecraft: The Movie",
    "description": "An action-packed adventure set in the blocky world of Minecraft, where heroes must unite to save their world from destruction.",
    "genre": "Action",
    "director": "Jared Hess",
    "cast": "Jason Momoa, Jack Black, Sebastian Hansen",
    "duration": "2h 15m",
    "poster_image": "https://image.tmdb.org/t/p/original/4ZKUsFohURy72tTaB4ahfly6RAY.jpg"
}
{
    "title": "Avengers: Endgame",
    "description": "After the devastating events of Avengers: Infinity War, the Avengers assemble once more to reverse Thanos' actions and restore balance to the universe.",
    "genre": "Action",
    "director": "Anthony Russo",
    "cast": "Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth, Scarlett Johansson",
    "duration": "3h 2m",
    "poster_image": "https://th.bing.com/th/id/R.28d7c8a9a0fdda3bde7296f1356590e3?rik=tHvapbeS5EO97Q&riu=http%3a%2f%2feclipsemagazine.com%2fwp-content%2fuploads%2f2019%2f07%2fAvengers-Endgame.jpg&ehk=TVBuXsRenZ0yaieUte6Aa%2fw%2fT6%2f4yrfBG%2bpik7BDwZY%3d&risl=&pid=ImgRaw&r=0"
}

{
    "title": "The Batman",
    "description": "In his second year of fighting crime, Batman uncovers corruption in Gotham City that connects to his own family while facing a serial killer known as the Riddler.",
    "genre": "Action",
    "director": "Matt Reeves",
    "cast": "Robert Pattinson, Zoë Kravitz, Paul Dano, Jeffrey Wright, Colin Farrell",
    "duration": "2h 56m",
    "poster_image": "https://st1.uvnimg.com/d2/a0/9547b92931cd5b8f925a43d01375/the-batman.jpg"
}

{
    "title": "Spider-Man: No Way Home",
    "description": "Peter Parker seeks Doctor Strange's help to restore his secret identity, but things go awry, unleashing multiverse chaos.",
    "genre": "Adventure",
    "director": "Jon Watts",
    "cast": "Tom Holland, Zendaya, Benedict Cumberbatch, Willem Dafoe",
    "duration": "2h 28m",
    "poster_image": "https://cdn.shopify.com/s/files/1/1057/4964/products/Spider-Man-No-Way-Home-Vintage-Movie-Poster-Original-1-Sheet-27x41_25b5dfd9-d4d0-45f1-ad92-c7a118525092.jpg?v=1652936730"
}

{
    "title": "The Lion King",
    "description": "After the murder of his father, a young lion prince flees his kingdom only to learn the true meaning of responsibility and bravery.",
    "genre": "Animation",
    "director": "Jon Favreau",
    "cast": "Donald Glover, Beyoncé, Seth Rogen, Chiwetel Ejiofor",
    "duration": "1h 58m",
    "poster_image": "https://th.bing.com/th/id/OIP.H4zDLGrmdKkU_lYHGf2HyAHaLH?rs=1&pid=ImgDetMain"
}

{
    "title": "Sinners",
    "description": "Trying to leave their troubled lives behind, twin brothers return to their hometown to start again, only to discover that an even greater evil is waiting to welcome them back.",
    "genre": "Drama, Thriller",
    "director": "Ryan Coogler",
    "cast": "Michael B. Jordan, Hailee Steinfeld, Miles Caton, Jack O'Connell, Wunmi Mosaku, Jayme Lawson, Omar Miller, Delroy Lindo",
    "duration": "2h 10m",
    "poster_image": "https://mx.web.img3.acsta.net/img/24/d8/24d84f8cb3d436e05de073e41d9bfbeb.jpg"
}

{
    "title": "The Matrix Resurrections",
    "description": "Neo must decide whether to follow the white rabbit once more as he re-enters the Matrix to confront a new enemy.",
    "genre": "Sci-Fi",
    "director": "Lana Wachowski",
    "cast": "Keanu Reeves, Carrie-Anne Moss, Yahya Abdul-Mateen II, Jessica Henwick",
    "duration": "2h 28m",
    "poster_image": "https://th.bing.com/th/id/OIP.WBzRAGO2yoSk4xh2Yd3IUgHaKb?rs=1&pid=ImgDetMain"
}

{
    "title": "Dune: Part Two",
    "description": "Paul Atreides unites with the Fremen to seek revenge against those who destroyed his family while trying to prevent a terrible future only he can foresee.",
    "genre": "Adventure",
    "director": "Denis Villeneuve",
    "cast": "Timothée Chalamet, Zendaya, Rebecca Ferguson, Javier Bardem, Florence Pugh",
    "duration": "2h 45m",
    "poster_image": "https://image.tmdb.org/t/p/original/5aUVLiqcW0kFTBfGsCWjvLas91w.jpg"
}

{
    "title": "Oppenheimer",
    "description": "The story of J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II.",
    "genre": "Biography, Drama, History",
    "director": "Christopher Nolan",
    "cast": "Cillian Murphy, Emily Blunt, Matt Damon, Robert Downey Jr., Florence Pugh",
    "duration": "3h 0m",
    "poster_image": "https://m.media-amazon.com/images/M/MV5BNDg1ZWE5MmYtZGU5YS00MzU2LThjMjktYThiNmVmMmZjMDkxXkEyXkFqcGdeQXVyMTU3ODE5NzYy._V1_.jpg"
}

{
    "title": "Guardians of the Galaxy Vol. 3",
    "description": "The Guardians embark on a mission to protect one of their own, leading to revelations about Rocket's past and the team's future.",
    "genre": "Action, Adventure, Comedy",
    "director": "James Gunn",
    "cast": "Chris Pratt, Zoe Saldana, Dave Bautista, Bradley Cooper, Karen Gillan",
    "duration": "2h 30m",
    "poster_image": "https://th.bing.com/th/id/OIP.GhMid31zZdMX15CPXo6ARgHaK9?rs=1&pid=ImgDetMain"
}

{
    "title": "Your Name",
    "description": "Two teenagers, living in different parts of Japan, discover they are mysteriously swapping bodies and must work together to uncover the truth behind their connection.",
    "genre": "Animation, Drama, Fantasy, Romance",
    "director": "Makoto Shinkai",
    "cast": "Ryunosuke Kamiki, Mone Kamishiraishi, Masami Nagasawa, Etsuko Ichihara",
    "duration": "1h 52m",
    "poster_image": "https://image.tmdb.org/t/p/original/pZ7qsb8kqYqQuFzjFeAQ2IlbiXW.jpg"
}
