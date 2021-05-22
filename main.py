from flask import Flask, render_template, request
from db_retrieval import db_perform_query, parse_custom_select_form
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


@app.route("/views", methods=["GET", "POST"])
def views():

    if request.method == "GET":
        client_data = db_perform_query("select id, name, surname from user_")
        print(client_data)
        return render_template("custom_selects.html", client_data=client_data)


@app.route("/custom_query_result", methods=["GET", "POST"])
def custom_query():

    if request.method == "POST":

        print(request.form)
        custom_select_output = parse_custom_select_form(request.form)
        if 'customselect1' in request.form:
            data = "Form 1 was selected"
        if 'customselect2' in request.form:
            data = "Form 2 was selected"
        if 'customselect3' in request.form:
            data = "Form 3 was selected"
        return render_template("resut.html", data=data)


if __name__ == "__main__":

    app.run(debug=True)