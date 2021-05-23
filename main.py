from flask import Flask, render_template, request
from db_retrieval import db_perform_query, parse_custom_select_form, parse_user_select_form
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


@app.route("/actions", methods=["GET", "POST"])
def actions():

    if request.method == "GET":
        return render_template("actions.html")


@app.route("/db_custom_views", methods=["GET", "POST"])
def custom_views():

    if request.method == "GET":
        client_data, cols = db_perform_query("select id, name, surname from user_")
        friend_data, cols = db_perform_query("select id, name, surname from friend")
        return render_template("custom_views.html", client_data=client_data, friend_data=friend_data)


@app.route("/db_user_views", methods=["GET", "POST"])
def user_views():

    if request.method == "GET":
        return render_template("user_views.html")


@app.route("/custom_query_result", methods=["GET", "POST"])
def custom_query():

    if request.method == "POST":

        custom_select_output, cols = parse_custom_select_form(request.form)
        return render_template("result.html", db_response=custom_select_output, db_response_cols=cols)


@app.route("/user_query_result", methods=["GET", "POST"])
def user_query():

    if request.method == "POST":

        user_select_output, cols = parse_user_select_form(request.form)
        return render_template("result.html", db_response=user_select_output, db_response_cols=cols)



if __name__ == "__main__":

    app.run(debug=True)