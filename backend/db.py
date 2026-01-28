import sqlite3

DB_FILE = "data.db" # keeping this so that its easier to change later 

#open connection
conn = sqlite3.connect(DB_FILE, check_same_thread=False)

#grab cursor
curr = conn.cursor()


#table that stores raw content
curr.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    content TEXT,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")


#storing chuked tex + embeddings
curr.execute("""
CREATE TABLE IF NOT EXISTS chunks(
    id INTEGER PRIMARY KEY,
    item_id INTEGER,
    chunk_text TEXT,
    embedding BLOB)""")


# commit table creation
conn.commit()

# keep connection open for app to use
