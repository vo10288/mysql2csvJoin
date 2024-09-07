import os
import csv
from sqlalchemy import create_engine, text
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
            # Usa 'text()' per eseguire una query SQL diretta
            result = connection.execute(text("SHOW DATABASES;"))
            databases = [row[0] for row in result]
            return databases
    except SQLAlchemyError as e:
        print(f"Errore durante il recupero dei database: {str(e)}")
        return []

def export_join_to_csv(db_name):
    """
    Funzione che esegue un JOIN tra le tabelle 'mov_dett' e 'articoli' tramite 'idarticolo' e
    salva il risultato in un file CSV nella directory che ha il nome del database.
    """
    # Crea la directory con il nome del database se non esiste
    dir_name = db_name
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    
    # Salva il file CSV all'interno della directory del database
    file_name = os.path.join(dir_name, f"{db_name}_mov_dett_articoli.csv")
    
    try:
        # Crea una connessione al database specifico
        db_engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@localhost/{db_name}?unix_socket={db_socket}")
        with db_engine.connect() as connection:
            # Esegui la query con il JOIN tra mov_dett e articoli
            query = """
            SELECT mov_dett.*, articoli.*
            FROM mov_dett
            JOIN articoli ON mov_dett.idarticolo = articoli.idarticolo;
            """
            result = connection.execute(text(query))
            
            # Esporta il risultato in un file CSV
            with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Scrivi l'intestazione (i nomi delle colonne)
                writer.writerow(result.keys())
                
                # Scrivi i dati riga per riga
                for row in result:
                    writer.writerow(row)
                
            print(f"Join esportato con successo in '{file_name}'")
    
    except SQLAlchemyError as e:
        print(f"Errore durante l'esecuzione della query per il database '{db_name}': {str(e)}")

def main():
    # Ottieni l'elenco di tutti i database esistenti
    databases = list_databases()

    # Escludi database di sistema e di prova che non desideri esportare (ad es. 'mysql', 'information_schema', 'test')
    exclude_databases = ['information_schema', 'performance_schema', 'mysql', 'sys', 'test']

    # Esegui l'export per ogni database
    for db_name in databases:
        if db_name not in exclude_databases:
            print(f"Esportazione per il database: {db_name}")
            export_join_to_csv(db_name)

if __name__ == '__main__':
    main()
