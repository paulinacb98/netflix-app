import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import psycopg2

st.set_page_config(
    page_title="Netflix App",
    layout="wide"
)

if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

def obtener_peliculas():
    documentos = db.collection("movies").stream()

    peliculas = []

    for documento in documentos:
        pelicula = documento.to_dict()
        peliculas.append(pelicula)

    df = pd.DataFrame(
        peliculas,
        columns=["name", "genre", "director", "company"]
    )

    return df

df = obtener_peliculas()

st.title("Netflix App")

st.write("Dashboard interactivo de películas")

st.sidebar.header("Buscar películas")

mostrar_todas = st.sidebar.checkbox(
    "Mostrar todos los filmes", value=True
)

if mostrar_todas:
    st.subheader("Todos los filmes")
    st.write("Total de películas:", len(df))
    st.dataframe(df, use_container_width=True)

st.sidebar.subheader("Buscar por título")

titulo = st.sidebar.text_input("Título del filme:")

if st.sidebar.button("Buscar filmes"):

    if titulo.strip() != "":

        resultado = df[
            df["name"].str.contains(
                titulo,
                case=False,
                na=False,
                regex=False
            )
        ]

        st.subheader("Resultados de búsqueda")
        st.write("Total de películas encontradas:", len(resultado))
        st.dataframe(resultado, use_container_width=True)

    else:
        st.warning("Escribe un título para buscar.")

st.sidebar.subheader("Filtrar por director")

directores = sorted(df["director"].dropna().unique())

director = st.sidebar.selectbox(
    "Seleccionar director:",
    directores
)

if st.sidebar.button("Filtrar director"):

    resultado = df[df["director"] == director]

    st.subheader("Películas de " + director)
    st.write("Total de películas:", len(resultado))
    st.dataframe(resultado, use_container_width=True)

st.sidebar.divider()
st.sidebar.subheader("Nuevo filme")

with st.sidebar.form("formulario_pelicula"):

    nombre = st.text_input("Name:")

    companias = sorted(df["company"].dropna().unique())
    directores = sorted(df["director"].dropna().unique())
    generos = sorted(df["genre"].dropna().unique())

    compania = st.selectbox("Company:", companias)
    director_nuevo = st.selectbox("Director:", directores)
    genero = st.selectbox("Genre:", generos)

    guardar = st.form_submit_button("Crear nuevo filme")

    if guardar:

        if nombre.strip() != "":

            nueva_pelicula = {
                "name": nombre.strip(),
                "genre": genero,
                "director": director_nuevo,
                "company": compania
            }

            db.collection("movies").add(nueva_pelicula)

            st.success("Película agregada correctamente")
            st.rerun()

        else:
            st.warning("Debes escribir el nombre de la película.")

def conectar_postgres():
    conexion = psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        port=st.secrets["postgres"]["port"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        sslmode=st.secrets["postgres"]["sslmode"]
    )

    return conexion

st.sidebar.divider()
st.sidebar.header("Libro de visitas")

with st.sidebar.form("formulario_visitas"):

    email = st.text_input("Email:")
    comentario = st.text_area("Comentario:")

    registrar = st.form_submit_button("Registrar Visita")

    if registrar:

        if email.strip() != "" and comentario.strip() != "":

            try:
                conexion = conectar_postgres()

                with conexion:
                    with conexion.cursor() as cursor:
                        cursor.execute(
                            """
                            INSERT INTO people (email, comment)
                            VALUES (%s, %s)
                            """,
                            (email.strip(), comentario.strip())
                        )

                conexion.close()

                st.success("Visita registrada correctamente")

            except Exception as error:
                st.error("No se pudo registrar la visita.")
                st.exception(error)

        else:
            st.warning("Completa el email y el comentario.")

st.sidebar.divider()

if st.sidebar.button("Ver visitas"):

    try:
        conexion = conectar_postgres()

        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT email, comment
                FROM people
            """)

            visitas = cursor.fetchall()

        conexion.close()

        st.sidebar.subheader("Comentarios registrados")

        if len(visitas) == 0:
            st.sidebar.info("Todavía no hay comentarios.")

        else:
            for numero, visita in enumerate(visitas, start=1):

                st.sidebar.write(
                    str(numero) + ". " + visita[1]
                )

                st.sidebar.caption(visita[0])

    except Exception as error:
        st.sidebar.error("No se pudieron consultar las visitas.")
        st.sidebar.exception(error)