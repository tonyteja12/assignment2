
from flask import *
import pymysql

app = Flask(__name__,template_folder="templates",static_folder="static")




connection = pymysql.connect(
    host='sql9.freesqldatabase.com',
    user='sql9599820',
    password='AwVn2gCwQh',
    db='sql9599820'

)



@app.route('/all')
def all():
    return render_template('all.html')



@app.route("/table")
def table():
    
   
    cursor = connection.cursor()
    sql = "SELECT * FROM theearthquakes"
    print(sql)
    cursor.execute(sql)
    output = cursor.fetchall()
    print(output)
    
    return render_template('table.html', received=output)






@app.route('/magnitude',methods=['GET', 'POST'])
def magnitude():
    if request.method == 'POST':
        magnitude=float(request.form['magnitude'])
        cursor = connection.cursor()
        sql = "SELECT COUNT(*) FROM theearthquakes WHERE mag > {}".format(magnitude)
        print(sql)
        cursor.execute(sql)
        output = cursor.fetchall()
        print(output)
       
        return render_template('magnitude.html', received=output)

@app.route('/earthquakes', methods=['GET'])
def get_earthquakes():
    # Parse user input from query parameters
    location = request.args.get('location')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    min_mag = request.args.get('min_mag')
    max_mag = request.args.get('max_mag')

    # Build SQL query based on user input
    query = 'SELECT * FROM earthquakes WHERE 1=1'
    if location:
        query += f" AND location='{location}'"
    if start_time:
        query += f" AND time>='{start_time}'"
    if end_time:
        query += f" AND time<='{end_time}'"
    if min_mag:
        query += f" AND mag>={min_mag}"
    if max_mag:
        query += f" AND mag<={max_mag}"

    # Perform database query
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    # Convert results to JSON and return to user
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
