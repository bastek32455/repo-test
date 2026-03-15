from flask import Flask, render_template, request, redirect, url_for, flash, session
import database
import sqlite3

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-demo'

# Initialize database
database.init_db()



@app.route('/')
def index():
    if 'user_id' not in session:
        # For demo purposes, we automatically "log in" the demo user
        session['user_id'] = 1
        session['username'] = 'demo'
    
    conn = database.get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    transactions = conn.execute('SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC LIMIT 5', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('index.html', user=user, transactions=transactions)

@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'user_id' not in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        recipient = request.form['recipient']
        amount = float(request.form['amount'])
        description = request.form['description']
        
        conn = database.get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        
        if user['balance'] < amount:
            flash('Niewystarczające środki na koncie!', 'error')
        else:
            try:
                # Deduct from sender
                conn.execute('UPDATE users SET balance = balance - ? WHERE id = ?', (amount, session['user_id']))
                # Log transaction
                conn.execute('INSERT INTO transactions (user_id, type, amount, description) VALUES (?, ?, ?, ?)',
                            (session['user_id'], 'OUTGOING', amount, f"Przelew do: {recipient} - {description}"))
                conn.commit()
                flash('Przelew wykonany pomyślnie!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                conn.rollback()
                flash(f'Błąd podczas wykonywania przelewu: {str(e)}', 'error')
            finally:
                conn.close()
                
    return render_template('transfer.html')

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('index'))
        
    conn = database.get_db_connection()
    transactions = conn.execute('SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('history.html', transactions=transactions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
