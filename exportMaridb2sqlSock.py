import os
import subprocess
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Imposta la connessione MariaDB/MySQL con SQLAlchemy, utilizzando il file socket
db_user = 'root'  # Inserisci il tuo utente MariaDB
db_password = 'rir38fe'  # Inserisci la tua password
db_socket = '/tmp/mysql.sock'  # Specifica il percorso del file socket
db_host = 'localhost'  # Host del database, localhost va bene poiché usiamo il socket

# Crea l'engine di SQLAlchemy specificando il socket
engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@localhost/?unix_socket={db_socket}")

def list_databases():
    """
    Funzione per ottenere l'elenco di tutti i database presenti in MariaDB.
    """
    try:
        # Connessione al motore di MariaDB
        with engine.connect() as connection:
            result = connection.execute("SHOW DATABASES;")
            databases = [row[0] for row in result]
            return databases
    except SQLAlchemyError as e:
        print(f"Errore durante il recupero dei database: {str(e)}")
        return []

def export_database_to_sql(db_name):
    """
    Funzione che esegue il dump di un database in un file .sql utilizzando mysqldump.
    """
    file_name = f"{db_name}.sql"
    try:
        # Comando mysqldump per esportare il database
        subprocess.run(
            ['mysqldump', '-u', db_user, f'-p{db_password}', '--socket', db_socket, db_name, '--result-file', file_name],
            check=True
        )
        print(f"Database '{db_name}' esportato con successo in '{file_name}'")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esportazione del database '{db_name}': {str(e)}")

def main():
    # Ottieni l'elenco di tutti i database esistenti
    databases = list_databases()

    # Escludi database di sistema che non desideri esportare (ad es. 'mysql', 'information_schema')
    exclude_databases = ['information_schema', 'performance_schema', 'mysql', 'sys']

    # Esegui l'export per ogni database
    for db_name in databases:
        if db_name not in exclude_databases:
            export_database_to_sql(db_name)

if __name__ == '__main__':
    main()
