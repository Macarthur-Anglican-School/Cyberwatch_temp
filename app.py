from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///cyberwatch.db")

app = Flask(__name__)

engine = create_engine('sqlite:///.database/cyberwatch.db') #link to the cyberwatch database here


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

@app.route('/add-incident')
def add_incident_page():

    return render_template('add-incident.html')


# @app.route('/add-incident', methods=['GET'])
# def show_form():
#         return render_template('index.html', )

# @app.route('/add-incident', methods=['POST'])
# def add_incident():
#     Incident = request.form['Incident']
#     Vulnerability = request.form['Vulnerability']
#     Year = request.form['Year']

#     insert_statement = '''
#         INSERT INTO incidents (Incident, Vulnerability, URL, Year)
#         VALUES ('{}','{}', '{}', {});
#     '''.format(Incident, Vulnerability, URL, Year)

#     return redirect(url_for('base'))

@app.route('/add-incident/<vul_id>', methods=['GET', 'POST'])
def add_incident(vul_id):
    if request.method == 'GET':
        with engine.connect() as connection:
            vulname_query = text("SELECT vul_name FROM vulnerabilites WHERE id = {}".format(vul_id))
            vulname_result = connection.execute(vulname_query, {vul_id}).fetchall()
        return render_template("add-incident.html", vul_id=vul_id, vul_name=vulname_result[0])
    
    if request.method == 'POST':
        inc_name = request.form['inc_name']
        inc_url = request.form['inc_url']
        inc_year = request.form['inc_year']
        vul_id = request.form['vul_id']

        with engine.connect() as connection:
            form_query = text(f"INSERT INTO incidents (inc_name, inc_url, inc_year, vul_id)' "f"VALUES ('{inc_name}', '{inc_url}', '{inc_year}', '{vul_id}');")
            connection.execute(form_query)
            connection.commit()

        return redirect(url_for('incidents', vul_id = vul_id))

app.run(debug=True, reloader_type='stat', port=5000)