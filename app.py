from flask import Flask, render_template, request, redirect, url_for , flash
from flask_pymongo import PyMongo
from bson import ObjectId
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pymongo import MongoClient
from io import BytesIO
import base64
import pandas as pd


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/EmployeeDB'
mongo = PyMongo(app)
app.secret_key = "secret key test"

client = MongoClient('mongodb://localhost:27017/')
db = client['EmployeeDB']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Employees')
def Employees():
    employee_from_mongo = mongo.db.Employee.find()
    return render_template('Employees.html', Employee=employee_from_mongo)

@app.route('/Managers')
def Managers():
    manager_from_mongo = mongo.db.Manager.find()
    return render_template('Managers.html', Manager=manager_from_mongo)

@app.route('/Visualize')
def Visualize():
    employee_from_mongo = mongo.db.Employee.find()
    manager_from_mongo = mongo.db.Manager.find()
    project_from_mongo = mongo.db.Project.find()

    employee_data = list(employee_from_mongo)
    df_employee = pd.DataFrame(employee_data)

    # Count the number of employees in each department
    department_counts = df_employee['department'].value_counts()

    # Plot data
    department_counts.plot(kind='bar', xlabel='Department', ylabel='Number of Employees', title='Number of Employees in Each Department')
    plt.yticks(range(int(department_counts.max()) + 1))
    plt.tight_layout()
    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.read()).decode('utf-8')
    plt.close()

    return render_template('Visualize.html', Employee =employee_from_mongo, Manager = manager_from_mongo, Project = project_from_mongo,chart=img_base64)


@app.route('/Visualizeprojects')
def Visualizeprojects():
    employee_from_mongo = mongo.db.Employee.find()
    manager_from_mongo = mongo.db.Manager.find()
    project_from_mongo = mongo.db.Project.find()

    project_data = list(project_from_mongo)
    df_project = pd.DataFrame(project_data)

    # Count the number of employees in each department
    department_counts = df_project['department'].value_counts()

    # Plot data
    department_counts.plot(kind='bar', xlabel='Department', ylabel='Number of Projects', title='Number of projects in Each Department')
    plt.yticks(range(int(department_counts.max()) + 1))
    plt.tight_layout()
    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.read()).decode('utf-8')
    plt.close()

    return render_template('Visualizeprojects.html', Employee =employee_from_mongo, Manager = manager_from_mongo, Project = project_from_mongo,chart=img_base64)




@app.route('/Projects')
def Projects():
    employee_from_mongo = mongo.db.Employee.find()
    manager_from_mongo = mongo.db.Manager.find()
    project_from_mongo = mongo.db.Project.find()
    return render_template('Projects.html', Employee =employee_from_mongo, Manager = manager_from_mongo, Project = project_from_mongo)


@app.route('/Searches')
def Searches():
    employee_from_mongo = mongo.db.Employee.find()
    manager_from_mongo = mongo.db.Manager.find()
    project_from_mongo = mongo.db.Project.find()
    return render_template('Searches.html', Employee_result =employee_from_mongo, Manager_result = manager_from_mongo, Project_result = project_from_mongo)


@app.route('/Query1', methods=['POST'])
def Query1():
    employee_from_mongo = mongo.db.Employee.find()
    manager_from_mongo = mongo.db.Manager.find()
    project_from_mongo = mongo.db.Project.find()
    department_name = request.form['department']  

    pipeline1 = [
        {
            '$match': {
                'department': department_name
            }
        },
        {
            '$lookup': {
                'from': 'Employee',
                'localField': 'emp_id',
                'foreignField': 'emp_id',
                'as': 'employee_details'
            }
        },
        {
            '$project': {
                '_id':0,
                'name': 1,
                'position': 1,
                'emp_id': '$employee_details.emp_id'
            }
        }
    ]
    employees_in_department = list(mongo.db.Employee.aggregate(pipeline1))
    # print(employees_in_department)

    pipeline2 = [
        {
            '$match': {
                'department': department_name
            }
        },
        {
            '$lookup': {
                'from': 'Manager',
                'localField': 'man_id',
                'foreignField': 'man_id',
                'as': 'manager_details'
            }
        },
        {
            '$project': {
                '_id':0,
                'name': 1,
                'position': 1,
                'man_id': '$manager_details.man_id'
            }
        }
    ]
    managers_in_department = list(mongo.db.Manager.aggregate(pipeline2))
    # print(managers_in_department)

    pipeline3 = [
        {
            '$match': {
                'department': department_name
            }
        },
        {
            '$lookup': {
                'from': 'Project',
                'localField': 'pro_id',
                'foreignField': 'pro_id',
                'as': 'project_details'
            }
        },
        {
            '$project': {
                '_id':0,
                'name': 1,
                'position': 1,
                'pro_id': '$project_details.pro_id',
                'status':'$project_details.status',
                'emp_id':'$project_details.emp_id',
                'man_id':'$project_details.man_id',
                'pro_id': '$project_details.pro_id'
            }
        }
    ]
    projects_in_department = list(mongo.db.Project.aggregate(pipeline3))
    # print(projects_in_department)

    return render_template('Query1.html', Employee =employee_from_mongo, Manager = manager_from_mongo, Project = project_from_mongo,result=employees_in_department,result2=managers_in_department,result3=projects_in_department,department_name=department_name)

@app.route('/Query2', methods=['POST'])
def Query2():
    employee_from_mongo = mongo.db.Employee.find()
    manager_from_mongo = mongo.db.Manager.find()
    project_from_mongo = mongo.db.Project.find()
    employee_ID = request.form['employee']   
    employee_ID2 = employee_ID   
    employee_ID = int(employee_ID) 
    # print(employee_ID)
    # print(employee_ID2)

    pipeline1 = [
        {
            '$match': {
                'emp_id': employee_ID
            }
        },
        {
            '$lookup': {
                'from': 'Employee',
                'localField': 'emp_id',
                'foreignField': 'emp_id',
                'as': 'employee_details'
            }
        },
        {
            '$project': {
                '_id':0,
                'name': 1,
                'position': 1,
                'emp_id': '$employee_details.emp_id'
            }
        }
    ]
    employees_in_employees = list(mongo.db.Employee.aggregate(pipeline1))
    # print(employees_in_employees)

    pipeline2 = [
        {
            '$match': {
                'emp_id': employee_ID2
            }
        },
        {
            '$lookup': {
                'from': 'Project',
                'localField': 'pro_id',
                'foreignField': 'pro_id',
                'as': 'project_details'
            }
        },
        {
            '$project': {
                '_id':0,
                'name': 1,
                'position': 1,
                'pro_id': '$project_details.pro_id',
                'status':'$project_details.status',
                'emp_id':'$project_details.emp_id',
                'man_id':'$project_details.man_id',
                'pro_id': '$project_details.pro_id'
            }
        }
    ]
    projects_in_employees = list(mongo.db.Project.aggregate(pipeline2))
    # print(projects_in_employees)


    return render_template('Query2.html', Employee =employee_from_mongo, Manager = manager_from_mongo, Project = project_from_mongo,result=employees_in_employees,result3=projects_in_employees,employee_ID = employee_ID   )


@app.route('/Query3', methods=['POST'])
def Query3():
    employee_from_mongo = mongo.db.Employee.find()
    manager_from_mongo = mongo.db.Manager.find()
    project_from_mongo = mongo.db.Project.find()
    manager_ID = request.form['manager']   
    manager_ID2 = manager_ID   
    manager_ID = int(manager_ID) 
    # print(manager_ID)
    # print(manager_ID2)

    pipeline1 = [
        {
            '$match': {
                'man_id': manager_ID
            }
        },
        {
            '$lookup': {
                'from': 'Manager',
                'localField': 'man_id',
                'foreignField': 'man_id',
                'as': 'manager_details'
            }
        },
        {
            '$project': {
                '_id':0,
                'name': 1,
                'position': 1,
                'man_id': '$manager_details.man_id'
            }
        }
    ]
    managers_in_managers = list(mongo.db.Manager.aggregate(pipeline1))
    # print(managers_in_managers)

    pipeline2 = [
        {
            '$match': {
                'man_id': manager_ID2
            }
        },
        {
            '$lookup': {
                'from': 'Project',
                'localField': 'pro_id',
                'foreignField': 'pro_id',
                'as': 'project_details'
            }
        },
        {
            '$project': {
                '_id':0,
                'name': 1,
                'position': 1,
                'pro_id': '$project_details.pro_id',
                'status':'$project_details.status',
                'emp_id':'$project_details.emp_id',
                'man_id':'$project_details.man_id',
                'pro_id': '$project_details.pro_id'
            }
        }
    ]
    projects_in_managers = list(mongo.db.Project.aggregate(pipeline2))
    # print(projects_in_managers)
    return render_template('Query3.html', Employee =employee_from_mongo, Manager = manager_from_mongo, Project = project_from_mongo,result=managers_in_managers,result3=projects_in_managers,manager_ID = manager_ID )


@app.route('/add_employee', methods=['POST'])
def add_employee():
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        position = request.form['position']
        department = request.form['department']
        last_document_id = mongo.db.Employee.find_one(sort=[('_id', -1)])
        if last_document_id:
            last_emp_id = last_document_id.get('emp_id')
            last_emp_id = int(last_emp_id)
        else:
            last_emp_id = 0
        new_id = last_emp_id + 1

        # Create a dictionary with the data
        employee_data = {
            'emp_id': new_id,
            'name': name,
            'position': position,
            'department': department
        }

        # Insert data into the "employee" collection
        mongo.db.Employee.insert_one(employee_data)

        # # Redirect to the home page or any other page you want
        return redirect('/Employees')
    

@app.route('/add_manager', methods=['POST'])
def add_manager():
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        position = request.form['position']
        department = request.form['department']
        last_document_id = mongo.db.Manager.find_one(sort=[('_id', -1)])
        if last_document_id:
            last_man_id = last_document_id.get('man_id')
            last_man_id = int(last_man_id)
        else:
            last_man_id = 0
        new_id = last_man_id + 1

        # Create a dictionary with the data
        employee_data = {
            'man_id': new_id,
            'name': name,
            'position': position,
            'department': department
        }

        # Insert data into the "employee" collection
        mongo.db.Manager.insert_one(employee_data)

        # # Redirect to the home page or any other page you want
        return redirect('/Managers')
    
@app.route('/add_project', methods=['POST'])
def add_project():
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        status = request.form['status']
        department = request.form['department']
        emp_id = request.form['emp_id']
        man_id = request.form['man_id']
        last_document_id = mongo.db.Project.find_one(sort=[('_id', -1)])
        if last_document_id:
            last_pro_id = last_document_id.get('pro_id')
            last_pro_id = int(last_pro_id)
        else:
            last_pro_id = 0
        new_id = last_pro_id + 1

        # Create a dictionary with the data
        project_data = {
            'pro_id': new_id,
            'name': name,
            'status': status,
            'department': department,
            'emp_id':emp_id,
            'man_id':man_id
        }

        # Insert data into the "employee" collection
        mongo.db.Project.insert_one(project_data)

        # # Redirect to the home page or any other page you want
        return redirect('/Projects')

@app.route('/delete_employee/<int:emp_id>', methods=['POST'])
def delete_employee(emp_id):
    mongo.db.Employee.delete_one({'emp_id': emp_id})
    return redirect('/Employees')

@app.route('/delete_project/<int:pro_id>', methods=['POST'])
def delete_project(pro_id):
    mongo.db.Project.delete_one({'pro_id': pro_id})
    return redirect('/Projects')

@app.route('/delete_manager/<int:man_id>', methods=['POST'])
def delete_manager(man_id):
    mongo.db.Manager.delete_one({'man_id': man_id})
    return redirect('/Managers')



@app.route('/update_employee/<int:emp_id>', methods=['POST'])
def update_employee(emp_id):
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        position = request.form['position']
        department = request.form['department']

        # Create a dictionary with the data
        employee_data = {
            'emp_id': emp_id,
            'name': name,
            'position': position,
            'department': department
        }

        # Insert data into the "employee" collection
        mongo.db.Employee.update_one({'emp_id': emp_id},{'$set': employee_data})
        # # Redirect to the home page or any other page you want
        return redirect('/Employees')
    
@app.route('/update_manager/<int:man_id>', methods=['POST'])
def update_manager(man_id):
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        position = request.form['position']
        department = request.form['department']

        # Create a dictionary with the data
        manager_data = {
            'man_id': man_id,
            'name': name,
            'position': position,
            'department': department,
            
        }

        # Insert data into the "employee" collection
        mongo.db.Manager.update_one({'man_id': man_id},{'$set': manager_data})
        # # Redirect to the home page or any other page you want
        return redirect('/Managers')
    
@app.route('/update_project/<int:pro_id>', methods=['POST'])
def update_project(pro_id):
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        status = request.form['status']
        department = request.form['department']
        emp_id = request.form['emp_id']
        man_id = request.form['man_id']
        # Create a dictionary with the data
        project_data = {
            'pro_id': pro_id,
            'name': name,
            'status': status,
            'department': department,
            'emp_id':emp_id,
            'man_id':man_id
        }

        # Insert data into the "employee" collection
        mongo.db.Project.update_one({'pro_id': pro_id},{'$set': project_data})
        # # Redirect to the home page or any other page you want
        return redirect('/Projects')

if __name__ == '__main__':
    app.run(debug=True)
