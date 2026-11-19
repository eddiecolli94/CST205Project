from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home_page():
    return render_template("home.html")

@app.route("/create", methods=["GET", "POST"])
def create_deck():
    if request.method == "POST":
        deck_title = request.form.get("deck-title")
        question = request.form.get("question")
        answer = request.form.get("answer")

        print("Deck: ", deck_title)
        print("Question: ", question)
        print("Answer: ", answer)

    return render_template("create_deck.html")

if __name__ == "__main__":
    app.run(debug=True)
