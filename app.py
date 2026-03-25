from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///cyberwatch.db")

app = Flask(__name__)

engine = create_engine('sqlite:///.database/cyberwatch.db') #link to the cyberwatch database here

@app.route('/dashboard')
def dashbord():
    with engine.connect() as connection:
        query = text("SELECT * FROM incidents")
        result = connection.execute(query)
        all_incidents = result.fetchall()
    return render_template('dashboard.html')


#route for index.html
@app.route('/')
def home():
    
    with engine.connect() as connection:
        # This way of connecting to the database 
        # ensures that the connection is automatically closed as soon as the function finishes
        query = text('SELECT * FROM vulnerabilities ORDER BY owasp_rank;')
        result = connection.execute(query).fetchall()

    print('Loading homepage...')
    return render_template('index.html', vulnerabilities=result)

@app.route('/incidents/<vul_id>')
def incident_page(vul_id):
    # TASK 1: Connect to the database
    with engine.connect() as connection:
        query = text('SELECT * FROM incidents WHERE vul_id = {};'.format(vul_id))
        result = connection.execute(query).fetchall()
        print(result)
    # TASK 2: Fetch the Vulnerability Name for the heading (JOIN or separate query)
        new_query = text('SELECT vul_name FROM vulnerabilities WHERE id = {};'.format(vul_id))
        new_result = connection.execute(new_query).fetchall()


    # TASK 3: Fetch all Incidents linked to this vul_id, return incidents list
    

    print(vul_id) #this is a print statement to help you understand what data is being returned
    return render_template('incidents.html', vulnerability = new_result[0][0], incidents = result)



app.run(debug=True, reloader_type='stat', port=3000)