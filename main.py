from flask import Flask, render_template, request
from db_retrieval import db_perform_query, parse_custom_select_form, parse_user_select_form, perform_db_action, get_unreturned_gifts

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello():

    try:
        if request.method == "GET":
            return render_template("index.html")
    except:
        error_msg = "something went wrong"
        return render_template("error.html", error_msg=error_msg)


@app.route("/actions", methods=["GET", "POST"])
def actions():

    # try:
        celebrations_data, _ = db_perform_query("select * from party")
        rent_friends_data, _ = db_perform_query("select id, description, name, surname from friend")
        unreturned_gifts_data = get_unreturned_gifts()
        client_data, _ = db_perform_query("select id, name, surname from user_")
        friend_data, _ = db_perform_query("select id, name, surname from friend")
        # print(unreturned_gifts_data)
        if request.method == "GET":
            return render_template("actions.html", client_data=client_data,
                                   friend_data=friend_data,
                                   unreturned_gifts_data=unreturned_gifts_data,
                                   rent_friends_data=rent_friends_data,
                                   celebrations_data=celebrations_data)
    # except:
    #     error_msg = "something went wrong"
    #     return render_template("error.html", error_msg=error_msg)


@app.route("/db_custom_views", methods=["GET", "POST"])
def custom_views():

    # try:
        if request.method == "GET":
            client_data, cols = db_perform_query("select id, name, surname from user_")
            friend_data, cols = db_perform_query("select id, name, surname from friend")
            return render_template("custom_views.html", client_data=client_data, friend_data=friend_data)
    # except:
    #     error_msg = "something went wrong"
    #     return render_template("error.html", error_msg=error_msg)

@app.route("/db_user_views", methods=["GET", "POST"])
def user_views():

    # try:
        if request.method == "GET":
            return render_template("user_views.html")
    # except:
    #     error_msg = "Couldn't load user views page"
    #     return render_template("error.html", error_msg=error_msg)


@app.route("/custom_query_result", methods=["GET", "POST"])
def custom_query():

    try:
        if request.method == "POST":

            custom_select_output, cols = parse_custom_select_form(request.form)
            return render_template("result.html", db_response=custom_select_output, db_response_cols=cols)
    except:
        error_msg = "Couldn't load custom views page"
        return render_template("error.html", error_msg=error_msg)


@app.route("/user_query_result", methods=["GET", "POST"])
def user_query():

    # try:
        if request.method == "POST":

            user_select_output, cols = parse_user_select_form(request.form)
            return render_template("result.html", db_response=user_select_output, db_response_cols=cols)
    # except:
    #     error_msg = "Couldn't perform desired query"
    #     return render_template("error.html", error_msg=error_msg)


@app.route("/handle_action", methods=["GET", "POST"])
def handle_action():

    # try:
        if request.method == "POST":

            perform_db_action(request.form)
            msg = "Successfully performed desired action!"
            return render_template("result.html", msg=msg)
    # except:
    #     error_msg = "Couldn't load actions page"
    #     return render_template("error.html", error_msg=error_msg)




if __name__ == "__main__":

    app.run(debug=True)