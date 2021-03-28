
from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import os
import numpy as np
import sys
import re
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET','POST'])
def submit_score():
    if request.method=='GET':
        filepath = '/home/pierret/helping_hand/ability.csv'
        data = pd.read_csv(filepath)
        return render_template('get_gamestats.html',id_info = data)
    else:
        p_id = (request.form['student_id_player'])
        ability = int(request.form['ability'])
        student_info = {'id': [p_id], 'ability' :[ability]}
        filepath = '/home/pierret/helping_hand/ability.csv'
        data = pd.read_csv(filepath)
        new_data = pd.DataFrame(student_info, columns= ['id', 'ability' ])
        data = data.append(new_data)
        data.to_csv(filepath, index = False, header=True)



        return render_template('get_gamestats.html',id_info = data)

@app.route('/exercise', methods=['GET','POST'])
def run_exercise():
    if request.method=='GET':
        return render_template('exercise.html')
    else:

        filepath = '/home/pierret/helping_hand/coordinates.csv'

        #Passing data from ajax:
        coordinates = request.get_data()
        #Converting it from a string:
        coordinates = str(coordinates)
        #Removing the css characters
        new_string = coordinates.replace("&xcoordinates%5B%5D=", ",")
        new_string = new_string.replace("&ycoordinates%5B%5D=", ",")
        new_string = new_string.replace("b'xcoordinates%5B%5D=", "")
        new_string = new_string.replace("'", "")
        #Find the id
        id_array = new_string.split("&id=", 1)
        id_name = id_array[1]
        #Removing the css characters
        new_string = re.sub('[a-z]', '', new_string)
        new_string = re.sub('[A-Z]', '', new_string)
        new_string = new_string.replace("&=", "")
        #Split a string into a list
        coordinate_list = new_string.split(',')
        #Convert into a np array
        numpy_array = np.array(coordinate_list)
        #Split the np array into x and y values
        numpy_array = np.split(numpy_array, 2)
        x_coordinates = numpy_array[0]
        y_coordinates = numpy_array[1]
        #Create a dictionary
        coordinates_dict = {'x_coordinates':x_coordinates,'y_coordinates':y_coordinates,'id_name':id_name}
        #Create a Pandas dataFrame
        new_data = pd.DataFrame(coordinates_dict, columns= ['x_coordinates','y_coordinates','id_name'])
        #Save it to a csv
        new_data = new_data.append(new_data)
        new_data.to_csv(filepath, index = False, header=True)
        return str(id_name)
        #return str(y_coordinates)