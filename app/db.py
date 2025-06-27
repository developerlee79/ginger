import os

from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def get_db():
    cnx = mysql.connector.connect(
            user=os.getenv("AZURE_DATABASE_USER"),
            password=os.getenv("AZURE_DATABASE_PASSWORD"),
            host=os.getenv("AZURE_DATABASE_HOST"),
            port=int(os.getenv("AZURE_DATABASE_PORT")),
            database=os.getenv("AZURE_DATABASE_DATABASE"),
            ssl_disabled=False
        )
    return cnx
