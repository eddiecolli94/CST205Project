from flask import Flask, render_template, request
import sqlite3
import os
import uuid

decks_db = "decks.db"
connection = sqlite3.connect(decks_db)
connection.execute("PRAGMA foreign_keys = ON")
cursor = connection.cursor()

os.makedirs("static/uploads", exist_ok=True)

cursor.execute("""CREATE TABLE IF NOT EXISTS Decks(
                    deck_id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL UNIQUE
                );
""")

cursor.execute("""
            CREATE TABLE IF NOT EXISTS Flashcards(
            flashcard_id INTEGER PRIMARY KEY,
            deck_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            image TEXT,

            FOREIGN KEY(deck_id) REFERENCES Decks (deck_id)
        );
""")

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table';
""")

print(cursor.fetchall())

connection.commit()
connection.close()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home_page():
    return render_template("home.html")

@app.route("/create", methods=["GET", "POST"])
def create_deck():
    if request.method == "POST":
        # connect to database
        connection = sqlite3.connect(decks_db)
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        # get info from form in create_deck.html
        deck_title = request.form.get("deck-title")
        question = request.form.get("question")
        answer = request.form.get("answer")
        uploaded_image = request.files.get("image")

        image = None

        if uploaded_image and uploaded_image.filename:
            folder = "static/uploads"
            filename = uploaded_image.filename
            
            path = os.path.join(folder, filename)

            uploaded_image.save(path)

            print("Image saved to: ", path)
        else:
            print("No image uploaded")

        cursor.execute("""
                INSERT INTO Decks (title)
                VALUES (?)
        """, (deck_title,))

        # gives us id of last row inserted
        new_deck_id = cursor.lastrowid

        print("Image value:", image)
        print("Image type:", type(image))

        cursor.execute("""
                INSERT INTO Flashcards (deck_id, question, answer, image)
                VALUES(?,?,?,?)
        """, (new_deck_id, question, answer, image))

        connection.commit()

        # SEE ALL TABLES
        print("DECKS table:")
        cursor.execute("SELECT * FROM Decks")
        for deck in cursor.fetchall():
            print(deck)

        # print  flashcards table
        print("FLASHCARD table:")
        cursor.execute("Select * FROM Flashcards")
        for card in cursor.fetchall():
            print(card)

        connection.close()

        

    return render_template("create_deck.html")

if __name__ == "__main__":
    app.run(debug=True)
