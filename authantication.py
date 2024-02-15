from flask import Flask, request, jsonify
import pyodbc
import pandas as pd

app = Flask(__name__)

# Replace this with your actual database connection logic
# For simplicity, we'll use an in-memory dictionary as a mock database
DB_Server = '90.0.0.110'  # DB Server
DB_Name = 'MyBotTest'  # DB Name
DB_UserName = 'developer'  # DB UserName
DB_Password = 'd123'  # DB Password


connection = pyodbc.connect('Driver={SQL Server};'f'Server={DB_Server};'f'Database={DB_Name};'\
		                        f'UID={DB_UserName};'f'PWD={DB_Password};')



user_info_query = pd.read_sql_query(f'''SELECT UserName, [Password] FROM dbo.[User]''', connection)


user_info = pd.DataFrame(user_info_query, columns=['UserName', 'Password'])


@app.route('/validate', methods=['POST'])
def validate_credentials():
    data = request.get_json()

    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid request format"}), 400

    username = data['username']
    password = data['password']

    # Check if the username exists in the database
    if username in user_info['UserName'].values and user_info.loc[user_info['UserName'] == username, 'Password'].values[0] == password:
        return jsonify({"message": "Credentials are valid"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='90.0.1.198', port=5000,)
