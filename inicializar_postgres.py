import streamlit as st
import psycopg2

# Conectar con PostgreSQL
conexion = psycopg2.connect(
    host=st.secrets["postgres"]["host"],
    port=st.secrets["postgres"]["port"],
    database=st.secrets["postgres"]["database"],
    user=st.secrets["postgres"]["user"],
    password=st.secrets["postgres"]["password"],
    sslmode=st.secrets["postgres"]["sslmode"]
)

cursor = conexion.cursor()

cursor.execute("SELECT current_database()")
print("Base de datos conectada:", cursor.fetchone()[0])

cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
        email VARCHAR(255) NOT NULL,
        comment TEXT NOT NULL
    )
""")

conexion.commit()

cursor.close()
conexion.close()

print("Tabla people creada correctamente")