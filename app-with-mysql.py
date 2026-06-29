import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv

# Carica le configurazioni dal file .env
load_dotenv()

app = Flask(__name__)

# --- CONFIGURAZIONE RDS MYSQL ---
DB_ENDPOINT = os.getenv("DB_ENDPOINT")
DB_USER = "admin"                                      # Username standard del corso
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = "flaskdb"                                    # Il database iniziale che hai creato su RDS

# Stringa di connessione che usa PyMySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_ENDPOINT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Popolamento iniziale del database con i dati di sample del corso
def insert_initial_data():
    data = text("""
    INSERT INTO users VALUES
        ('dora', 'dora@amazon.com'),
        ('cansın', 'cansın@google.com'),
        ('sencer', 'sencer@bmw.com'),
        ('uras', 'uras@mercedes.com'),
        ('ares', 'ares@porche.com');
    """)
    db.session.execute(data)
    db.session.commit()

# --- ROTTE DELL'APPLICAZIONE WEB ---

@app.route('/', methods=['GET', 'POST'])
def emails():
    if request.method == 'POST':
        # 'user_keyword' corrisponde esattamente al name dell'input nel tuo emails.html
        keyword = request.form['user_keyword']
        
        query = text(f"SELECT * FROM users WHERE email LIKE '%{keyword}%'")
        result = db.session.execute(query)
        # Passiamo 'keyword' all'HTML così viene renderizzato in <h1>Result for '{{ keyword }}'</h1>
        return render_template('emails.html', name_emails=result, keyword=keyword, show_result=True)
    
    return render_template('emails.html', show_result=False)

@app.route('/add', methods=['GET', 'POST'])
def add_email():
    if request.method == 'POST':
        username = request.form['username']
        user_email = request.form['useremail']
        
        if username and user_email:
            query = text(f"INSERT INTO users VALUES ('{username}', '{user_email}')")
            db.session.execute(query)
            db.session.commit()
            return render_template('add-email.html', show_progress=True, username=username)
            
    return render_template('add-email.html', show_progress=False)

# --- INIZIALIZZAZIONE DATABASE E AVVIO ---
if __name__ == '__main__':
    with app.app_context():
        # Forza la creazione della tabella via SQL per evitare conflitti con l'ORM
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL,
                PRIMARY KEY (username)
            );
        """))
        db.session.commit()
        
        # Inserisce i dati se il database RDS è vuoto
        check_empty = db.session.execute(text("SELECT COUNT(*) FROM users")).scalar()
        if check_empty == 0:
            insert_initial_data()
            
    # L'applicazione risponde sulla porta 8080 come richiesto dal README
    app.run(host='0.0.0.0', port=8080)