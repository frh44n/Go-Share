from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    return conn

# Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        if cursor.fetchone():
            return 'Email already registered'
        
        # Insert new user
        cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)',
                       (email, password))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check user credentials
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            session['user'] = email
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials'
    
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
