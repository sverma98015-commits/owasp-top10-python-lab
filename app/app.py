from flask import Flask, request, render_template_string, render_template, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "super-secret-key"

def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT,
            secret_token TEXT
        )
    """)
    cursor.execute("INSERT INTO users (username, password, role, secret_token) VALUES ('admin', 'Password123!', 'Administrator', 'FLAG{SQLi_SUCCESS}')")
    cursor.execute("INSERT INTO users (username, password, role, secret_token) VALUES ('alice', 'alicepass', 'User', 'FLAG{IDOR_ALICE_TOKEN}')")
    cursor.execute("INSERT INTO users (username, password, role, secret_token) VALUES ('bob', 'bobpass', 'User', 'FLAG{IDOR_BOB_TOKEN}')")
    conn.commit()
    return conn

db_conn = init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vulnerable/sqli', methods=['POST'])
def sqli_vulnerable():
    username = request.form.get('username')
    password = request.form.get('password')
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor = db_conn.cursor()
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        if user:
            return f"<h3>Logged in successfully as: {user[1]} (Role: {user[3]})</h3><p>Secret Flag: {user[4]}</p>"
        else:
            return "<h3>Login Failed!</h3>"
    except Exception as e:
        return f"<h3>Database Error:</h3> <pre>{str(e)}</pre>"

@app.route('/vulnerable/xss', methods=['GET'])
def xss_vulnerable():
    search_query = request.args.get('search', '')
    html_template = f"""
    <h3>Search Results for: {search_query}</h3>
    <p>0 results found.</p>
    <a href="/">Go Back</a>
    """
    return render_template_string(html_template)

@app.route('/vulnerable/idor')
def idor_vulnerable():
    user_id = request.args.get('id')
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT id, username, role, secret_token FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        return render_template('profile.html', user=user)
    return "User not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
