from flask import Flask, render_template, request
from db_retrieval import db_perform_query
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello():

    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        query_text = request.form["query_text"]
        db_response_data = db_perform_query(query_text)
        #print(db_response_data)
        return render_template("index.html", db_response=db_response_data)


if __name__ == "__main__":

    app.run(debug=True)