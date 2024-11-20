from mysql import connector
import uuid
import ast

################################
connection = connector.connect(host ="...", user ="...", passwd="...", database="...")
################################

cursor = connection.cursor()

def make_new_poll(data):
    print(data)

    uid = uuid.uuid4()
    no_of_options = len(data["poll_options"])
    zeros = "0," * no_of_options

    query = f""" INSERT INTO polls VALUES ( '{uid}', '{data["poll_question"]}', "{list(data["poll_options"])}" , '[{zeros}]') """
    print(query)

    cursor.execute(query)
    connection.commit()

    return uid

def poll_data(id):

    query = f"SELECT question, options FROM polls WHERE poll_id='{id}'"

    cursor.execute(query)

    return cursor.fetchone()

def cast(id, option):

    query = f"SELECT votes FROM polls WHERE poll_id = '{id}'"
    cursor.execute(query)

    #('[0,0,0,]',)

    data = ast.literal_eval((cursor.fetchone())[0])

    data[option] += 1
    q2 = f"UPDATE polls SET votes = '{data}' WHERE poll_id = '{id}'"

    cursor.execute(q2)
    connection.commit()    

def ret_results(id):

    query = f"SELECT question, options, votes FROM polls WHERE poll_id = '{id}'"

    cursor.execute(query)

    data = cursor.fetchone()

    print(data)
    # ('Toppings?', "['Macaroni', 'Sausage', 'Shreads']", '[1, 3, 1]')

    # [
    #   { "option": "Cheese", "votes": 45 },
    #   { "option": "Pepperoni", "votes": 32 },
    #   { "option": "Mushroom", "votes": 23 }
    # ]

    results = []

    raw_res = zip(ast.literal_eval(data[1]), ast.literal_eval(data[2]))


    for opt in raw_res:
        results.append({'option': opt[0], 'votes': opt[1]})
    
    return results


ret_results('27434330-b927-4772-ac5d-dd0a5d169de8')

    


