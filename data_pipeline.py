import sqlite3
import os

filenames = [filenames for filenames in os.walk("./assets/Cleaned/")][0][2]
filepaths = ["./assets/Cleaned/"+i for i in filenames]


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
conn = sqlite3.connect('books.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        content TEXT
    )
''')
conn.commit()

def insert_book(title, content):
    c.execute('INSERT INTO books (title, content) VALUES (?, ?)', (title, content))
    conn.commit()


for file_path in filepaths:
    book_title = os.path.basename(file_path).replace('_cleaned.txt', '')
    book_content = read_file(file_path)
    insert_book(book_title, book_content)

c.execute('SELECT * FROM books')
print(c.fetchall())

conn.close()