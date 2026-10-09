import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

peliculas = [
    ("Titanic", "Romance", "James Cameron", "Twentieth Century Fox"),
    ("Avatar", "Science Fiction", "James Cameron", "Twentieth Century Fox"),
    ("Inception", "Science Fiction", "Christopher Nolan", "Warner Bros"),
    ("Interstellar", "Science Fiction", "Christopher Nolan", "Paramount Pictures"),
    ("The Dark Knight", "Action", "Christopher Nolan", "Warner Bros"),
    ("Jurassic Park", "Adventure", "Steven Spielberg", "Universal Pictures"),
    ("E.T.", "Science Fiction", "Steven Spielberg", "Universal Pictures"),
    ("Jaws", "Thriller", "Steven Spielberg", "Universal Pictures"),
    ("Forrest Gump", "Drama", "Robert Zemeckis", "Paramount Pictures"),
    ("Back to the Future", "Science Fiction", "Robert Zemeckis", "Universal Pictures"),
    ("The Godfather", "Crime", "Francis Ford Coppola", "Paramount Pictures"),
    ("Pulp Fiction", "Crime", "Quentin Tarantino", "Miramax"),
    ("Kill Bill", "Action", "Quentin Tarantino", "Miramax"),
    ("Django Unchained", "Western", "Quentin Tarantino", "Columbia Pictures"),
    ("The Matrix", "Science Fiction", "Lana and Lilly Wachowski", "Warner Bros"),
    ("Gladiator", "Action", "Ridley Scott", "DreamWorks Pictures"),
    ("Alien", "Horror", "Ridley Scott", "Twentieth Century Fox"),
    ("The Lion King", "Animation", "Roger Allers", "Walt Disney Pictures"),
    ("Toy Story", "Animation", "John Lasseter", "Pixar"),
    ("Finding Nemo", "Animation", "Andrew Stanton", "Pixar")
]

for name, genre, director, company in peliculas:

    pelicula = {
        "name": name,
        "genre": genre,
        "director": director,
        "company": company
    }

    documento_id = name.lower().replace(" ", "_")

    db.collection("movies").document(documento_id).set(pelicula)

    print("Película guardada:", name)

print("Las 20 películas se guardaron correctamente en la colección 'movies' de Firestore.")