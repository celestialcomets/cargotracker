import hashlib
import datetime
import time

import flask
from flask import jsonify
from flask import request, make_response

from sql import create_con
from sql import execute_query
from sql import execute_read_query

import creds

app = flask.Flask(__name__)
app.config["DEBUG"] = True

masterPassword = "17caa840ab2c9794d76e1b4d4ab08bb983d626031e3699d5886b6f93bb187522"
masterUsername = 'admin'

# this api is handles the log in process. the username is "admin" and password is "CIS3368"
# to test, go to the authorization tab, select basic authorization under type, then input credentials.
@app.route('/authenticatedroute', methods=['GET'])
def auth_test():
    if request.authorization:
        encoded = request.authorization.password.encode() #unicode encoding
        hasedResult = hashlib.sha256(encoded) #hashing
        if request.authorization.username == masterUsername and hasedResult.hexdigest() == masterPassword:
            return '<h1> Authorized user access </h1>'
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

# CAPTAIN-RELATED APIS
# this code uses the 'get' method to allow users to retrieve all captains in the captain database
# along with all their information. no user input is needed.
@app.route('/api/captain', methods=["GET"])
def view_all_captains():
    myCreds = creds.Creds()
    connection = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql ="select * from captain"
    users = execute_read_query(connection, sql)
    return jsonify(users)

# this code uses the 'post' method to allow users to add a captain to the captain database.
# information for the new captain must be included in the body in this format:
#{
#    "firstname": "insert first name",
#    "lastname": "insert last name",
#    "rank": "insert ranking",
#    "homeplanet": "insert home planet"
# }
@app.route('/api/captain', methods=["POST"])
def add_captain():
    request_data = request.get_json()
    firstname = request_data['firstname']
    lastname = request_data['lastname']
    rank = request_data['rank']
    homeplanet = request_data['homeplanet']

    myCreds = creds.Creds()
    connection = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql = "insert into captain(firstname, lastname, `rank`, homeplanet) values ('%s','%s','%s', '%s')" % (firstname, lastname, rank, homeplanet)
    execute_query(connection, sql)

    return 'New Captain Added!'

# this code uses the 'put' method to allow users to update captains in the captain database by id.
# information for the captain to be updated must be included in the body in this format:
#{
#    "id": insert id, 
#    "firstname": "insert first name",
#    "lastname": "insert last name",
#    "rank": "insert ranking",
#    "homeplanet": "insert home planet"
# }
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
    sql = "UPDATE captain SET firstname = '%s', lastname = '%s', `rank` = '%s', homeplanet = '%s' WHERE id = '%s'" % (firstname, lastname, rank, homeplanet, id)
    execute_query(connection, sql)

    return f'Captain {firstname} Updated!'

# this code uses the 'delete' method to allow users to delete captains in the captain database by id.
# information for the captain to be deleted must be included in the body in this format:
#{
#    "id": insert id
# }
@app.route('/api/captain', methods=['DELETE'])
def delete_captain():
    request_data = request.get_json()
    delete = request_data['id']
    
    myCreds = creds.Creds()
    connection = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql = "delete from captain where id = %s" % (delete)
    execute_query(connection, sql)
        
    return f"Captain {delete} Deleted!"


# SPACESHIP-RELATED APIS
# this code uses the 'get' method to allow users to retrieve all spaceships in the spaceship database
# along with all their information. no user input is needed.
@app.route('/api/spaceship', methods=["GET"])
def view_all_spaceships():
    myCreds = creds.Creds()
    conn = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql ="select * from spaceship"
    users = execute_read_query(conn, sql)
    return jsonify(users)

# finished, need to test and write notes
# SOLUTION: captains was returning nested dictionaries inside a list, so indexing further allowed the ids to be added to a list for comparison
@app.route('/api/spaceship', methods=["POST"])
def add_spaceship():
    request_data = request.get_json()
    maxweight = request_data['maxweight'] #requests maxweight for new entry
    captainid = request_data['captainid'] #requests captainid for new entry
    captains_list = []

    myCreds = creds.Creds()
    connection = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql = "select * from captain"
    captains = execute_read_query(connection, sql)
    for i in range(len(captains)):
        captains_list.append(captains[i]["id"])
    
    if captainid in captains_list:
        sql = "insert into spaceship(maxweight, captainid) values ('%s','%s')" % (maxweight, captainid)
        execute_query(connection, sql)
        return 'New Spaceship Added!'
    else:
        return f'There is no captain number {captainid}!'
    

# finished, need to test and write notes
# SOLUTION: captains was returning nested dictionaries inside a list, so indexing further allowed the ids to be added to a list for comparison
@app.route('/api/spaceship', methods=["PUT"])
def update_spaceship():
    request_data = request.get_json()
    id = request_data['id']
    maxweight = request_data['maxweight']
    captainid = request_data['captainid']
    captains_list = []

    myCreds = creds.Creds()
    connection = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql = "select * from captain"
    captains = execute_read_query(connection, sql)
    for i in range(len(captains)):
        captains_list.append(captains[i]["id"])

    if captainid in captains_list:
        sql = "UPDATE spaceship SET maxweight = '%s', captainid = '%s' WHERE id = '%s'" % (maxweight, captainid, id)
        execute_query(connection, sql)
        return f'Spaceship {id} Updated!'
    else:
        return f'There is no captain number {captainid}!'

# this code uses the 'delete' method to allow users to delete spaceships in the spaceship database by id.
# information for the spaceship to be deleted must be included in the body in this format:
#{
#    "id": insert id
# }
@app.route('/api/spaceship', methods=['DELETE'])
def delete_spaceship():
    request_data = request.get_json()
    delete = request_data['id']
    
    myCreds = creds.Creds()
    connection = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql = "delete from spaceship where id = %s" % (delete)
    execute_query(connection, sql)
        
    return f"Spaceship {delete} Deleted!"



# CARGO-RELATED APIS
# this code uses the 'get' method to allow users to retrieve all cargo in the cargo database
# along with all their information. no user input is needed.
# as of right now, returning error "mktime argument is out of range"
# importing datetime & time module didn't seem to affect it
@app.route('/api/cargo', methods=["GET"])
def view_all_cargo():
    myCreds = creds.Creds()
    connection = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql ="select * from cargo"
    users = execute_read_query(connection, sql)
    return jsonify(users)

# need to add code to ensure there's enough room on ship for cargo
# as of right now, api is constantly returning "Spaceship does not exist!" error
# solutions attemped: adding ids to list to compare against user input, creating new dictionary and searching for values, selecting only ids from spaceship table
@app.route('/api/cargo', methods=["POST"])
def add_cargo():
    request_data = request.get_json()
    weight = request_data['weight']
    cargotype = request_data['cargotype']
    shipid = request_data['shipid']

    myCreds = creds.Creds()
    connection = create_con(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    
    sql = "select * from spaceship"
    ships = execute_read_query(connection, sql)
    if shipid in ships:
        sql = "select * from cargo"
        cargos = execute_read_query(connection, sql)
        current_weight = 0
        for cargo in cargos:
            if cargo['shipid'] == shipid:
                current_weight += cargo['weight']
        
        max_weight = 0
        for ship in ships:
            if ship['id'] == shipid:
                max_weight = ship['maxweight']
        
        if max_weight - current_weight > weight:
            sql = "insert into cargo(weight, cargotype, shipid) values ('%s','%s','%s')" % (weight, cargotype, shipid)
            execute_query(connection, sql)
            return 'New Cargo Added!'
        else:
            return f'Not enough cargo space on ship {shipid}'
    else:
        return f'Spaceship {shipid} does not exist!'
    

# need to copy code that verifies maximum cargo weight hasn't been reached here
# as of right now, api is constantly returning "Spaceship does not exist!" error
# solutions attemped: adding ids to list to compare against user input, creating new dictionary and searching for values, selecting only ids from spaceship table
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
    
    sql = "select * from spaceship"
    ships = execute_read_query(connection, sql)
    if shipid in ships:
        sql = "select * from cargo"
        cargos = execute_read_query(connection, sql)
        current_weight = 0
        for cargo in cargos:
            if cargo['shipid'] == shipid:
                current_weight += cargo['weight']
        
        max_weight = 0
        for ship in ships:
            if ship['id'] == shipid:
                max_weight = ship['maxweight']
        
        if max_weight - current_weight > weight:
            sql = "UPDATE cargo SET weight = '%s', cargotype = '%s', departure = '%s', arrival = '%s', shipid = '%s' WHERE id = '%s'" % (weight, cargotype, departure, arrival, shipid, id)
            execute_query(connection, sql)
            return f'Cargo {id} Updated!'
        else:
            return f'Not enough cargo space on ship {shipid}'
    else:
        return f'Spaceship {shipid} does not exist!'

# this code uses the 'delete' method to allow users to delete cargo in cargo database by id.
# information for the cargo to be deleted must be included in the body in this format:
#{
#    "id": insert id
# }
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
