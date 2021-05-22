import psycopg2

DB_NAME = "friends_rent"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"


try:
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    print("Connected")
    cur = conn.cursor()

except psycopg2.DatabaseError:

    print("error")


def db_perform_query(query):

    try:
        cur.execute(query)
        db_response = cur.fetchall()
        return db_response

    except psycopg2.DatabaseError:

        print("Error triggered on query")


def parse_custom_select_form(form_post_data):

    if 'customselect1' in form_post_data:
        print("received:", form_post_data)


# qr = input("query -> ")
# print(db_perform_query(qr))



