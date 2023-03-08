import mysql.connector
import creds
from mysql.connector import Error
from sql import create_con
from sql import execute_query
from sql import execute_read_query
import flask
from flask import jsonify
from flask import request

# finished, need to test and write notes
@app.route('/api/captain', methods=["GET"])
def view_all_captains():
    myCreds = creds.Creds()
    conn = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql ="select * from captain"
    users = execute_read_query(conn, sql)
    return jsonify(users)

# finished, need to test and write notes
@app.route('/api/captain', methods=["POST"])
def add_captain():
    request_data = request.get_json()
    firstname = request_data['firstname']
    lastname = request_data['lastname']
    rank = request_data['rank']
    homeplanet = request_data['homeplanet']

    myCreds = creds.Creds()
    connection = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql = "insert into captain(firstname, lastname, rank, homeplanet) values ('%s','%s','%s', '%s')" % (firstname, lastname, rank, homeplanet)
    execute_query(connection, sql)

    return 'New Captain Added!'

# finished, need to test and write notes
@app.route('/api/captain', methods=["PUT"])
def update_captain():
    request_data = request.get_json()
    id = request_data['id']
    firstname = request_data['firstname']
    lastname = request_data['lastname']
    rank = request_data['rank']
    homeplanet = request_data['homeplanet']

    myCreds = creds.Creds()
    connection = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql = "UPDATE captain SET firstname = '%s', lastname = '%s', rank = '%s', homeplanet = '%s' WHERE id = '%s'" % (firstname, lastname, rank, homeplanet, id)
    execute_query(connection, sql)

    return f'Captain {firstname} Updated!'

# finished, need to test and write notes
@app.route('/api/captain', methods=['DELETE'])
def delete_captain():
    request_data = request.get_json()
    delete = request_data['id']
    
    myCreds = creds.Creds()
    connection = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql = "delete from captain where id = %s" % (delete)
    execute_query(connection, sql)
        
    return f"Captain {delete} Deleted!"

# finished, add notes and test
@app.route('/api/cargo', methods=["GET"])
def view_all_cargo():
    myCreds = creds.Creds()
    conn = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql ="select * from cargo"
    users = execute_read_query(conn, sql)
    return jsonify(users)

# need to add code to ensure there's enough room on ship for cargo
@app.route('/api/cargo', methods=["POST"])
def add_cargo():
    request_data = request.get_json()
    weight = request_data['weight']
    cargotype = request_data['cargotype']
    shipid = request_data['shipid']

    myCreds = creds.Creds()
    connection = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql = "insert into cargo(weight, cargotype, shipid) values ('%s','%s','%s')" % (weight, cargotype, shipid)
    execute_query(connection, sql)

    return 'New Cargo Added!'

# need to copy code that verifies maximum cargo weight hasn't been reached here
@app.route('/api/cardo', methods=["PUT"])
def update_cargo():
    request_data = request.get_json()
    id = request_data['id']
    cargotype = ['cargotype']
    weight = request_data['weight']
    departure = request_data['departure']
    arrival = request_data['arrival']
    shipid = request_data['shipid']

    myCreds = creds.Creds()
    connection = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql = "UPDATE cargo SET weight = '%s', cargotype = '%s', departure = '%s', arrival = '%s', shipid = '%s' WHERE id = '%s'" % (weight, cargotype, departure, arrival, shipid, id)
    execute_query(connection, sql)

    return f'Cargo {id} Updated!'

# finished, need to test and write notes
@app.route('/api/cargo', methods=['DELETE'])
def delete_cargo():
    request_data = request.get_json()
    delete = request_data['id']
    
    myCreds = creds.Creds()
    connection = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql = "delete from cargo where id = %s" % (delete)
    execute_query(connection, sql)
        
    return f"Cargo {delete} Deleted!"

app.run()