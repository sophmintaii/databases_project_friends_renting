import psycopg2
from datetime import datetime

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
        print("Performing: ", query)
        cur.execute(query)
        db_response = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        return db_response, colnames

    except psycopg2.DatabaseError:

        print("Error triggered on query")


def get_unreturned_gifts():

    query = """
    select given_id, t2.name, 
    t.name as from_name, 
    t.surname as from_surname, 
    t1.name as to_name, 
    t1.surname as to_surname
    from present_given as s
    JOIN user_ t on t.id = s.user_id
    JOIN friend t1 on t1.id = s.friend_id
    JOIN present t2 on t2.present_id = s.present_id
    where is_returned = false;
    """

    response, cols = db_perform_query(query)
    return response

def perform_db_action(form_post_data):
    cur_date = datetime.today().strftime('%Y-%m-%d')

    if 'rent_friend' in form_post_data:

        rented_friends = form_post_data.getlist("rented_friend")
        #

        cur_max_id, _ = db_perform_query("""
                                    SELECT * 
                            FROM rent 
                            WHERE rent_id = (SELECT MAX(rent_id) FROM rent)""")
        max_id = cur_max_id[0][0] + 1

        # Modify rent table
        query = f"""INSERT INTO rent(rent_id, user_id, date, party_id) VALUES
                            ({max_id}, {form_post_data["client_id"]}, '{cur_date}', {form_post_data["celebration_id"]})
                            """

        cur.execute(query)

        # Modify rent table
        query = "INSERT INTO rent_friends(rent_id, friend_id) VALUES "
        rented_friends_ids = []
        for rented_friend_id in rented_friends :
            rented_friends_ids.append(f"({max_id}, {rented_friend_id})\n")
        query = query + ", ".join(rented_friends_ids) + ";"
        print(query)
        cur.execute(query)


    elif 'add_client' in form_post_data:

        query = f"""
                INSERT INTO user_ (id, phone_number, name, surname) VALUES (11, '{form_post_data["phone"]}', '{form_post_data["name"]}', '{form_post_data["surname"]}');
                """
        cur.execute(query)

    elif 'add_friend' in form_post_data:

        gender = '0' if form_post_data["gender"] == "male" else "1"
        query = f"""
                INSERT INTO friend (phone_number, name, surname, description, age, gender) 
                VALUES ('{form_post_data["phone"]}', '{form_post_data["name"]}', '{form_post_data["surname"]}', '{form_post_data["description"]}', {form_post_data["age"]}, '{gender}');
                """
        cur.execute(query)

    elif 'gift_something' in form_post_data:



        given_present_query = f"""
                                INSERT INTO present_given(present_id, user_id, friend_id, date, is_returned) VALUES
                                ({form_post_data["gift_id"]}, {form_post_data["client_id"]}, {form_post_data["friend_id"]}, '{cur_date}', false)
                                """

        cur.execute(given_present_query)


    elif 'return_gift' in form_post_data:

        print("from return gift", form_post_data)


        query = f"""
                UPDATE present_given
                SET is_returned = true WHERE given_id = {form_post_data["given_id"]};
                """

        cur.execute(query)

    elif 'file_complaint' in form_post_data:


        cur_max_id, _ = db_perform_query("""
                            SELECT * 
                    FROM complaint 
                    WHERE complaint_id = (SELECT MAX(complaint_id) FROM complaint)""")
        max_id = cur_max_id[0][0] + 1
        complaining_clients_ids = form_post_data.getlist("complaining_client")

        # Modify complaint table
        query = f"""INSERT INTO complaint(complaint_id, text, friend_id, date) VALUES
                    ({max_id}, {form_post_data["complaint_descr"]}, {form_post_data["friend_id"]}, '{cur_date}')
                    """

        cur.execute(query)

        # Modify user_complaint table
        query = "INSERT INTO user_complaint(user_id, complaint_id) VALUES "
        complaint_list = []
        for complaining_client_id in complaining_clients_ids:
            complaint_list.append(f"({complaining_client_id}, {max_id})\n")
        query = query + ", ".join(complaint_list) + ";"
        print(query)
        cur.execute(query)

    elif 'take_holiday' in form_post_data:

        query = f"""INSERT INTO dayoffs(friend_id, date) VALUES
                            ({form_post_data["friend_id"]}, '{cur_date}')
                            """

        cur.execute(query)

    conn.commit()


def parse_user_select_form(form_post_data):

    cols_to_be_selected = form_post_data.getlist("column_name")
    from_table = form_post_data["table_name"]

    query = "select " + ",".join([col for col in cols_to_be_selected]) + " from " + from_table
    #print(query)
    response, cols = db_perform_query(query)
    return response, cols


def parse_custom_select_form(form_post_data):

    #form_post_data = {'client_id' : '6', 'N' : '2', 'start_date': '2021-04-28', 'end_date' : '2020-09-02', 'customselect1' : ''}
    if 'customselect1' in form_post_data:
        query = f"""SELECT friend_id, name FROM rent 
                    JOIN rent_friends AS rf ON rent.rent_id = rf.rent_id 
                    JOIN friend ON rf.friend_id = friend.id 
                    WHERE user_id = {form_post_data["client_id"]} and date('{form_post_data["end_date"]}') > date and date > date('{form_post_data["start_date"]}') 
                    GROUP BY friend_id, name HAVING COUNT(friend_id) >= {form_post_data["N"]}"""

    elif 'customselect2' in form_post_data:
        query = f"""
                SELECT user_id, name FROM rent JOIN rent_friends ON rent.rent_id = rent_friends.rent_id JOIN user_ ON rent.user_id = user_.id
                WHERE friend_id = {form_post_data["friend_id"]} and date('{form_post_data["end_date"]}') > date and date > date('{form_post_data["start_date"]}')
                GROUP BY user_id, name
                HAVING COUNT(user_id) >= {form_post_data["N"]};
                """

    elif 'customselect3' in form_post_data:
        query = f"""
                SELECT party.party_id, name AS party_name FROM rent JOIN rent_friends ON rent.rent_id = rent_friends.rent_id JOIN party ON rent.party_id = party.party_id
                WHERE friend_id = {form_post_data["friend_id"]} and date('{form_post_data["end_date"]}') > date and date > date('{form_post_data["start_date"]}')
                GROUP BY party.party_id, name
                HAVING COUNT(party.party_id) >= {form_post_data["N"]};
                """

    elif 'customselect4' in form_post_data:
        query = f"""
                SELECT user_id, COUNT( DISTINCT friend_id) FROM rent JOIN rent_friends ON rent.rent_id = rent_friends.rent_id JOIN user_ ON rent.user_id = user_.id
                WHERE date('{form_post_data["end_date"]}') > date and date > date('{form_post_data["start_date"]}')
                GROUP BY user_id
                HAVING COUNT( DISTINCT friend_id) >= {form_post_data["N"]};
                """

    elif 'customselect5' in form_post_data:
        query = f"""
                SELECT friend_id, COUNT(rent.rent_id) FROM rent JOIN rent_friends on rent.rent_id = rent_friends.rent_id
                WHERE date('{form_post_data["end_date"]}') > date and date > date('{form_post_data["start_date"]}')
                GROUP BY friend_id
                HAVING COUNT(rent.rent_id) > {form_post_data["N"]};
                """

    elif 'customselect6' in form_post_data:
        query = f"""
                SELECT EXTRACT(MONTH FROM date), COUNT(rent_id) as dates_for_months
                FROM rent
                GROUP BY EXTRACT(MONTH FROM date);
                """

    elif 'customselect7' in form_post_data:
        query = f"""
                SELECT COUNT(*) FROM (
                    SELECT DISTINCT rent_id FROM (
                        SELECT rent_id, friend_id AS x_id FROM friend 
                        JOIN rent_friends ON friend.id = rent_friends.friend_id
                        JOIN rent USING (rent_id)
                        WHERE friend_id = {form_post_data["friend_id"]} AND party_id IS NOT NULL AND date BETWEEN date('{form_post_data["start_date"]}') AND date('{form_post_data["end_date"]}')
                    ) AS filtered_parties
                    JOIN rent_friends USING (rent_id)
                    GROUP BY rent_id
                    HAVING COUNT(rent_id) >= {form_post_data["N"]}
                ) AS groups;
                """

    elif 'customselect8' in form_post_data:
        query = f"""
                SELECT present_id FROM present_given
                LEFT JOIN dayoffs USING (friend_id)
                WHERE user_id = {form_post_data["client_id"]} AND present_given.date BETWEEN date('{form_post_data["start_date"]}') AND date('{form_post_data["end_date"]}')
                GROUP BY present_id
                ORDER BY COUNT(DISTINCT dayoffs.date) DESC;
                """

    elif 'customselect9' in form_post_data:
        query = f"""
                SELECT friend_id FROM complaint 
                JOIN (
                    SELECT complaint_id FROM user_complaint
                    GROUP BY complaint_id
                    HAVING COUNT(complaint_id) > 0
                ) AS special_complaints
                USING (complaint_id)
                WHERE complaint.date BETWEEN date('{form_post_data["start_date"]}') AND date('{form_post_data["end_date"]}')
                GROUP BY friend_id
                ORDER BY COUNT(complaint_id) DESC;
                """

    elif 'customselect10' in form_post_data:
        query = f"""
                SELECT rent_id FROM rent 
                JOIN rent_friends USING (rent_id)
                WHERE user_id = {form_post_data["client_id"]} AND friend_id = {form_post_data["friend_id"]} AND date BETWEEN date('{form_post_data["start_date"]}') AND date('{form_post_data["end_date"]}')
                """

    elif 'customselect11' in form_post_data:
        query = f"""
                SELECT date FROM dayoffs
                GROUP BY date
                HAVING COUNT(date) BETWEEN {form_post_data["A"]} AND {form_post_data["B"]};
                """

    elif 'customselect12' in form_post_data:
        query = f"""
                SELECT EXTRACT(MONTH FROM date) AS month, AVG(group_size) AS average FROM complaint 
                JOIN (
                    SELECT complaint_id, COUNT(complaint_id) AS group_size FROM user_complaint
                    GROUP BY complaint_id
                ) AS special_complaints
                USING (complaint_id)
                WHERE friend_id = {form_post_data["friend_id"]}
                GROUP BY EXTRACT(MONTH FROM date);
                """
    else:
        query = ""

    if not query:
        return []

    try:
        response, cols = db_perform_query(query)
        # print(response)
        return response, cols
    except psycopg2.DatabaseError:
        return []



# print(db_perform_query("select id, name, surname from user_"))
# qr = input("query -> ")
# print(db_perform_query(qr))


