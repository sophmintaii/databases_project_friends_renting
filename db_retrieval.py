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
        colnames = [desc[0] for desc in cur.description]
        return db_response, colnames

    except psycopg2.DatabaseError:

        print("Error triggered on query")


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
                
                """
    else:
        query = ""

    # print(query)

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


