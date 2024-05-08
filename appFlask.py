import json
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

command = "python app.py"
'''
@app.route('/signin', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Check if the username exists and the password matches
    if username in userTestingBD and userTestingBD[username]['password'] == password:
        # Return a JWT token with user's role
        return jsonify({'token': 'token', 'role': userTestingBD[username]['role']}), 200
    else:
        return 'Unauthorized', 401
'''
'''
@app.route('/testing',methods = ['GET'])
def testing_test():

    subprocess.run(command, shell=True)
    return jsonify("call")
'''

@app.route('/door', methods = ['GET'])
def door_called():
   

    
    return jsonify("Connection Established")

    #response = {'message': 'Data received successfully'}
    #return jsonify(response)
    
    

if __name__ == "__main__":
    app.run(host='192.168.56.1',port=3000,debug=True)

        

