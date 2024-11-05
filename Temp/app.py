from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyodbc

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
username = 'manojsamala'
password = 'Amazon@123'
server = 'manojsamala.database.windows.net'
database = 'tempdatabase'
driver = 'ODBC Driver 17 for SQL Server'

# Connection string
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def get_db_connection():
    conn = pyodbc.connect(connection_string)
    return conn

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Query to check user credentials
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user[0]  # Assuming the first column is the user ID
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')
        
        cursor.close()
        conn.close()
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = (
            request.form['username'],
            request.form['password'],
            request.form['email'],
            request.form['first_name'],
            request.form['last_name'],
            request.form['phone'],
            request.form['address'],
            request.form['city'],
            request.form['state'],
            request.form['zip']
        )
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert new user into the database
        cursor.execute("""
            INSERT INTO users (username, password, email, first_name, last_name, phone, address, city, state, zip)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, new_user)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
