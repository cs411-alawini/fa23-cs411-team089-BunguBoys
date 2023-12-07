from flask import Flask
from flask import request
from flask_cors import CORS
import pymysql.cursors
from flask import jsonify

import json

app = Flask(__name__)
CORS(app)

# Connect to the database
connection = pymysql.connect(host='34.69.173.235',
                             user='root',
                             password='CS411-89',
                             database='CS411_Group89_PT1',
                             cursorclass=pymysql.cursors.DictCursor)


def make_where_clause(param_map):
    params = []
    parce = []
    for key, value in param_map.items():
        if value is not None:
            csv = value.split(",")
            if key == 'start_date' or key == 'gte_mean' or key == 'gte_aqi' or key == 'gte_avg_mean' or key == 'gte_avg_aqi':
                if key == 'start_data':
                    other_key = "date"
                elif key == 'gte_mean':
                    other_key = "mean"
                elif key == 'gte_aqi':
                    other_key = "aqi"
                elif key == 'gte_avg_mean':
                    other_key = "avg_mean"
                elif key == 'gte_avg_aqi':
                    other_key = "avg_aqi"
                else:
                    other_key = "FAILURE"
                params.append(f"{other_key} >= '{value}'")
            elif key == 'end_date' or key == 'lte_mean' or key == 'lte_aqi' or key == 'lte_avg_mean' or key == 'lte_avg_aqi':
                if key == 'start_data':
                    other_key = "date"
                elif key == 'lte_mean':
                    other_key = "mean"
                elif key == 'lte_aqi':
                    other_key = "aqi"
                elif key == 'lte_avg_mean':
                    other_key = "avg_mean"
                elif key == 'lte_avg_aqi':
                    other_key = "avg_aqi"
                else:
                    other_key = "FAILURE"
                params.append(f"{other_key} <= '{value}'")
            else:
                if len(csv) == 1:
                    params.append(f"{key} = '{value}'")
                else:
                    for i in range(len(csv)):
                        if i == 0:
                            parce.append(f"({key} = '{csv[i]}'")
                        elif i == (len(csv) - 1):
                            parce.append(f" OR {key} = '{csv[i]}')")
                        else:
                            parce.append(f" OR {key} = '{csv[i]}'")
                    condition = ' '.join(parce)
                    params.append(condition)
    query_where = ' AND '.join(params)
    if len(query_where) > 0:
        return f"WHERE {query_where}"
    return ''


def make_patch_set(param_map):
    params = []
    for key, value in param_map.items():
        if value is not None:
            params.append(f"{key} = '{value}'")
    patch_keys = ' , '.join(params)
    if len(patch_keys) > 0:
        return f"{patch_keys}"


@app.route('/')
def backend_entry():
    return "This is one of the backends ever made."


# get single entries by ID

@app.route('/api/site/<int:site_id>')
def get_site(site_id):  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM Site WHERE id={site_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/city/<int:id>')
def get_city(id):  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM City WHERE id={id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/county/<int:id>')
def get_county(id):  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM County WHERE id={id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/state/<int:id>')
def get_state(id):  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM State WHERE id={id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/region/<int:id>')
def get_region(id):  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM Region WHERE id={id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/measurement/<int:id>')
def get_measurement(id):  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM Measurement WHERE id={id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/compound/<int:id>')
def get_compound(id):  # put application's code here
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM Compound WHERE id={id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


# get multiple results with filters (or all entries without filters)


@app.route('/api/site/')  # @app.route(GET/api/states)
def get_sites():  # put application's code here
    param_map = {
        'id': request.args.get('id', None),
        'city_id': request.args.get('city_id', None),
        'address': request.args.get('address', None),
    }
    query_where = make_where_clause(param_map)
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM Site {query_where}"
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/city/')  # @app.route(GET/api/states)
def get_cities():  # put application's code here
    param_map = {
        'id': request.args.get('id', None),
        'county_id': request.args.get('county_id', None),
        'name': request.args.get('name', None),
    }
    query_where = make_where_clause(param_map)
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM City {query_where}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/county/')  # @app.route(GET/api/states)
def get_counties():  # put application's code here
    param_map = {
        'id': request.args.get('id', None),
        'state_id': request.args.get('state_id', None),
        'name': request.args.get('name', None),
    }
    query_where = make_where_clause(param_map)
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM County {query_where}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/state/')  # @app.route(GET/api/states)
def get_states():  # put application's code here
    with connection.cursor() as cursor:
        param_map = {
            'id': request.args.get('id', None),
            'name': request.args.get('name', None),
        }
        query_where = make_where_clause(param_map)
        # Read a single record
        sql = f"SELECT * FROM State {query_where}"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/region/')  # @app.route(GET/api/states)
def get_regions():  # put application's code here
    param_map = {
        'id': request.args.get('id', None),
        'name': request.args.get('name', None),
    }
    query_where = make_where_clause(param_map)
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM Region {query_where}"
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/site_region/')  # @app.route(GET/api/states)
def get_site_regions():  # put application's code here
    param_map = {
        'site_id': request.args.get('site_id', None),
        'region_id': request.args.get('region_id', None),
    }
    query_where = make_where_clause(param_map)
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM Site_Region {query_where}"
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/getdata/')
def get_data():  # put application's code here
    param_map = {
        'compound_id': request.args.get('compound_id', None),
        'site_id': request.args.get('site_id', None),  # return measurements taken at a given site
        'date': request.args.get('date', None),  # return measurements taken on a singular date
        'start_date': request.args.get('start_date', None),
        'end_date': request.args.get('end_date', None),  # return all or only measurements before this given date
        'mean': request.args.get('mean', None),
        'gte_mean': request.args.get('gte_mean', None),
        'lte_mean': request.args.get('lte_mean', None),
        'aqi': request.args.get('mean', None),
        'gte_aqi': request.args.get('gte_aqi', None),
        'lte_aqi': request.args.get('lte_aqi', None),
    }
    query_where = make_where_clause(param_map)
    # print(query_where)
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM Measurement {query_where}"
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


@app.route('/api/compound/')  # @app.route(GET/api/states)
def get_compounds():  # put application's code here
    param_map = {
        'id': request.args.get('id', None),
        'name': request.args.get('name', None),
    }
    query_where = make_where_clause(param_map)
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM Compound {query_where}"
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result

@app.route('/api/site_average/')  # @app.route(GET/api/states)
def get_site_avg():  # put application's code here
    param_map = {
        'site_id': request.args.get('site_id', None),
        'avg_mean': request.args.get('avg_mean', None),
        'avg_aqi': request.args.get('avg_aqi', None),
        'gte_avg_mean': request.args.get('gte_avg_mean', None),
        'lte_avg_mean': request.args.get('lte_avg_mean', None),
        'gte_avg_aqi': request.args.get('gte_avg_aqi', None),
        'lte_avg_aqi': request.args.get('lte_avg_aqi', None),
    }

    query_where = make_where_clause(param_map)
    with connection.cursor() as cursor:
        # Read a single record
        sql = f"SELECT * FROM Site_Avg {query_where}"
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
    return result


# add an entry


@app.route('/api/site/', methods=['POST'])
def add_site():
    address = request.form.get("address", None)
    city_id = request.form.get("city_id", None)
    if address is None or city_id is None:
        return "Bad request", 400
    with connection.cursor() as cursor:
        # verify site does not already exist
        sql = f"SELECT * FROM Site WHERE city_id = {city_id} and address = '{address}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) > 0:
            # return site_id
            return "A site in that city with that address already exists with ID ___", 200
        else:
            # verify the target city exists
            sql = f"SELECT * FROM City WHERE id = {city_id}"
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) == 0:
                return "Bad request, invalid city_id"
            else:
                sql = f"INSERT INTO Site(city_id, address) VALUES({city_id}, '{address}')"
                cursor.execute(sql)
                sql = f"SELECT * FROM Site WHERE city_id = city_id and address = '{address}'"
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
                return result, 201


@app.route('/api/city/', methods=['POST'])
def add_city():
    name = request.form.get("name", None)
    county_id = request.form.get("county_id", None)
    if name is None or county_id is None:
        return "Bad request", 400
    with connection.cursor() as cursor:
        # verify the city does not exist already
        sql = f"SELECT * FROM City WHERE county_id = {county_id} and name = '{name}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) > 0:
            # return site_id
            return "A city in that county with that address already exists with ID ___", 200
        else:
            # verify the county is valid
            sql = f"SELECT * FROM County WHERE id = {county_id}"
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) == 0:
                return "Bad request, invalid county_id"
            else:
                # preform the add
                sql = f"INSERT INTO City(county_id, name) VALUES({county_id}, '{name}')"
                cursor.execute(sql)
                sql = f"SELECT * FROM City WHERE county_id = county_id and name = '{name}'"
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
                return result, 201


@app.route('/api/county/', methods=['POST'])
def add_county():
    name = request.form.get("name", None)
    state_id = request.form.get("state_id", None)
    if name is None or state_id is None:
        return "Bad request", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM County WHERE state_id = {state_id} and name = '{name}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) > 0:
            # return site_id
            "A county in that state with that name already exists with ID ___", 200
        else:
            sql = f"SELECT * FROM State WHERE id = {state_id}"
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) == 0:
                return "Bad request, invalid state_id"
            else:
                sql = f"INSERT INTO County(state_id, name) VALUES({state_id}, '{name}')"
                cursor.execute(sql)
                sql = f"SELECT * FROM County WHERE state_id = state_id and name = '{name}'"
                cursor.execute(sql)
                result = cursor.fetchall()
                connection.commit()
                return result, 201


@app.route('/api/state/', methods=['POST'])
def add_state():
    name = request.form.get("name", None)
    if name is None:
        return "Bad request", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM State WHERE name = '{name}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            sql = f"INSERT INTO State(name) VALUES ('{name}')"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            sql = f"SELECT * FROM State WHERE name = '{name}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            connection.commit()
            return result, 201
        else:
            return "State already exists", 400


@app.route('/api/region/', methods=['POST'])
def add_region():
    name = request.form.get("name", None)
    if name is None:
        return "Bad request", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM Region WHERE name = '{name}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            sql = f"INSERT INTO Region(name) VALUES ('{name}')"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            sql = f"SELECT * FROM Region WHERE name = '{name}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            connection.commit()
            return result, 201
        else:
            return "Region already exists", 400


@app.route('/api/site_region/', methods=['POST'])
def add_site_region():
    site_id = request.form.get("site_id", None)
    region_id = request.form.get("region_id", None)
    if site_id is None:
        return "Bad request, no site", 400
    if region_id is None:
        return "Bad request, no region", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM Site_Region WHERE site_id = {site_id} AND region_id = {region_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            sql = f"INSERT INTO Site_Region(site_id, region_id) VALUES ({site_id}, {region_id})"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            sql = f"SELECT * FROM Site_Region WHERE site_id = {site_id} AND region_id = {region_id}"
            cursor.execute(sql)
            result = cursor.fetchall()
            connection.commit()
            return result, 201
        else:
            return "Relationship already exists", 200


@app.route('/api/measurement/', methods=['POST'])
def add_measurement():
    data = request.get_json()
    site_id = data.get("site_id", None)
    compound_id = data.get("compound_id", None)
    date = data.get("date", None)
    parts_per = data.get("parts_per", None)
    mean = data.get("mean", None)
    max_value = data.get("max_value", None)
    max_hour = data.get("max_hour", None)
    aqi = data.get("aqi", None)
    print(site_id, compound_id, date, parts_per, mean, max_value, max_hour, aqi)
    if site_id is None:
        return "Bad request: site id none", 401
    if compound_id is None or date is None:
        return "Bad request: compound id none", 401
    if date is None:
        return "Bad request: date none", 401
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM Site WHERE id = {site_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Invalid site", 402
        sql = f"SELECT * FROM Compound WHERE id = {compound_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Invalid compound", 403
        sql = (f"INSERT INTO Measurement(site_id, compound_id, date, parts_per, mean, max_value, max_hour, aqi) VALUES ({site_id}, {compound_id}, '{date}', {parts_per}, {mean}, {max_value}, {max_hour}, {aqi})")
        print(sql)
        cursor.execute(sql)
        # sql = f"SELECT * FROM Measurement WHERE name = '{name}'"
        # cursor.execute(sql)
        # result = cursor.fetchall()
        # print(result)
        connection.commit()
        return jsonify({"message": "Entry added"}), 200


@app.route('/api/compound/', methods=['POST'])
def add_compound():
    name = request.form.get("name", None)
    if name is None:
        return "Bad request", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM Compound WHERE name = '{name}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            sql = f"INSERT INTO Compound(name) VALUES ('{name}')"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            sql = f"SELECT * FROM Compound WHERE name = '{name}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            connection.commit()
            return result, 201
        else:
            return "Compound already exists", 400


# delete an entry


@app.route('/api/site/<int:site_id>', methods=['DELETE'])
def delete_site(site_id):
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM Site WHERE id = {site_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Entry did not exist", 200
        else:
            sql = f"DELETE FROM Site WHERE id = {site_id}"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            connection.commit()
            return result[0], 200


@app.route('/api/city/<int:city_id>', methods=['DELETE'])
def delete_city(city_id):
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM City WHERE id = {city_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Entry did not exist", 200
        else:
            sql = f"DELETE FROM City WHERE id = {city_id}"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            connection.commit()
            return result[0], 200


@app.route('/api/county/<int:county_id>', methods=['DELETE'])
def delete_county(county_id):
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM County WHERE id = {county_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Entry did not exist", 200
        else:
            sql = f"DELETE FROM County WHERE id = {county_id}"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            connection.commit()
            return result[0], 200


@app.route('/api/state/<int:state_id>', methods=['DELETE'])
def delete_state(state_id):
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM State WHERE id = {state_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Entry did not exist", 200
        else:
            sql = f"DELETE FROM State WHERE id = {state_id}"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            connection.commit()
            return result[0], 200


@app.route('/api/region/<int:region_id>', methods=['DELETE'])
def delete_region(region_id):
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM Region WHERE id = {region_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Entry did not exist", 200
        else:
            sql = f"DELETE FROM Region WHERE id = {region_id}"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            connection.commit()
            return result[0], 200


@app.route('/api/measurement/<int:measurement_id>', methods=['DELETE'])
def delete_measurement(measurement_id):
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM Measurement WHERE id = {measurement_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Entry did not exist", 200
        else:
            sql = f"DELETE FROM Measurement WHERE id = {measurement_id}"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            connection.commit()
            return result[0], 200


@app.route('/api/compound/<int:compound_id>', methods=['DELETE'])
def delete_compound(compound_id):
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM Compound WHERE id = {compound_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result) == 0:
            return "Entry did not exist", 200
        else:
            sql = f"DELETE FROM Compound WHERE id = {compound_id}"
            # request reutrns a dictionary, similar logic to above to parce an insert statement
            cursor.execute(sql)
            connection.commit()
            return result[0], 200


# patch an ID


@app.route('/api/site/<int:id>', methods=['PATCH'])
def patch_site(id):
    param_map = {
        'address': request.form.get('address', None),
        'city_id': request.form.get('city_id', None),
    }
    patch_params = make_patch_set(param_map)
    where_params = make_where_clause(param_map)
    if len(patch_params) == 0:
        return "Bad request", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM Site WHERE id = {id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result.__len__() == 0:
            return "Entry did not exist", 400
        else:
            sql = f"UPDATE Site SET {patch_params} WHERE id = {id}"
            print(sql)
            cursor.execute(sql)
            sql = f"SELECT * FROM Site {where_params}"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            connection.commit()
            return result, 201


@app.route('/api/city/<int:id>', methods=['PATCH'])
def patch_city(id):
    param_map = {
        'name': request.form.get('name', None),
        'county_id': request.form.get('city_id', None),
    }
    patch_params = make_patch_set(param_map)
    where_params = make_where_clause(param_map)
    if len(patch_params) == 0:
        return "Bad request", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM City WHERE id = {id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result.__len__() == 0:
            return "Entry did not exist", 400
        else:
            sql = f"UPDATE City SET {patch_params} WHERE id = {id}"
            print(sql)
            cursor.execute(sql)
            sql = f"SELECT * FROM City {where_params}"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            connection.commit()
            return result, 201


@app.route('/api/county/<int:id>', methods=['PATCH'])
def patch_county(id):
    param_map = {
        'name': request.form.get('name', None),
        'state_id': request.form.get('state_id', None),
    }
    patch_params = make_patch_set(param_map)
    where_params = make_where_clause(param_map)
    if len(patch_params) == 0:
        return "Bad request", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM County WHERE id = {id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result.__len__() == 0:
            return "Entry did not exist", 400
        else:
            sql = f"UPDATE County SET {patch_params} WHERE id = {id}"
            print(sql)
            cursor.execute(sql)
            sql = f"SELECT * FROM County {where_params}"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            connection.commit()
            return result, 201


@app.route('/api/state/<int:state_id>', methods=['PATCH'])
def patch_state(state_id):
    param_map = {
        'name': request.form.get('name', None),
    }
    patch_params = make_patch_set(param_map)
    where_params = make_where_clause(param_map)
    if len(patch_params) == 0:
        return "Bad request", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM State WHERE id = {state_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result.__len__() == 0:
            return "Entry did not exist", 400
        else:
            sql = f"UPDATE State SET {patch_params} WHERE id = {state_id}"
            print(sql)
            cursor.execute(sql)
            sql = f"SELECT * FROM State {where_params}"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            connection.commit()
            return result, 201


@app.route('/api/region/<int:region_id>', methods=['PATCH'])
def patch_region(region_id):
    name = request.form.get("name", None)
    if name is None:
        return "Bad request", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM Region WHERE id = {region_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result.__len__() == 0:
            return "Entry did not exist", 400
        else:
            sql = f"UPDATE Region SET name = '{name}' WHERE id = {region_id}"
            cursor.execute(sql)
            sql = f"SELECT * FROM Region WHERE name = '{name}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            connection.commit()
            return result, 201


@app.route('/api/measurement/<int:data_id>', methods=['PATCH'])
def patch_measurement(data_id):
    data = request.get_json()
    param_map = {
        'compound_id': data.get("compound_id", None),
        'date': data.get("date", None),
        'parts_per': data.get("parts_per", None),
        'mean': data.get("mean", None),
        'max_value': data.get("max_value", None),
        'max_hour': data.get("max_hour", None),
        'aqi': data.get("aqi", None)
    }
    print(param_map)
    patch_params = make_patch_set(param_map)
    print(patch_params)
    where_params = make_where_clause(param_map)
    if len(patch_params) == 0:
        return "Bad request", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM Measurement WHERE id = {data_id}"
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        if result.__len__() == 0:
            return "Entry did not exist", 400
        else:
            sql = f"UPDATE Measurement SET {patch_params} WHERE id = {data_id}"
            print(sql)
            cursor.execute(sql)
            sql = f"SELECT * FROM Measurement {where_params}"
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            connection.commit()
            # return jsonified result
            return jsonify({"message": "Entry updated"}), 200


@app.route('/api/compound/<int:compound_id>', methods=['PATCH'])
def patch_compound(compound_id):
    name = request.form.get("name", None)
    if name is None:
        return "Bad request", 400
    with connection.cursor() as cursor:
        sql = f"SELECT * FROM Compound WHERE id = {compound_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result.__len__() == 0:
            return "Entry did not exist", 400
        else:
            sql = f"UPDATE Compound SET name = '{name}' WHERE id = {compound_id}"
            cursor.execute(sql)
            sql = f"SELECT * FROM Compound WHERE name = '{name}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            connection.commit()
            return result, 201


if __name__ == '__main__':
    app.run(host="0.0.0.0")
