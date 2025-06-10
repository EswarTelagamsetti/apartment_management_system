from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'eswar_root',
    'password': 'root',  
    'database': 'apartment_management'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('tenants.html')

# Tenants Routes
@app.route('/tenants')
def tenants():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tenants')
    tenants = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('tenants.html', tenants=tenants)

@app.route('/add_tenant', methods=['GET', 'POST'])
def add_tenant():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        move_in_date = request.form['move_in_date']
        apartment_id = request.form['apartment_id']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO tenants (name, email, phone, move_in_date, apartment_id) VALUES (%s, %s, %s, %s, %s)',
                (name, email, phone, move_in_date, apartment_id)
            )
            conn.commit()
            flash('Tenant added successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('tenants'))
    
    # For GET request, show the form
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT apartment_id, unit_number FROM apartments WHERE status = "vacant"')
    apartments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('add_tenant.html', apartments=apartments)

# Apartments Routes
@app.route('/apartments')
def apartments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM apartments')
    apartments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('apartments.html', apartments=apartments)

@app.route('/add_apartment', methods=['GET', 'POST'])
def add_apartment():
    if request.method == 'POST':
        unit_number = request.form['unit_number']
        bedrooms = request.form['bedrooms']
        bathrooms = request.form['bathrooms']
        square_feet = request.form['square_feet']
        monthly_rent = request.form['monthly_rent']
        status = request.form['status']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO apartments (unit_number, bedrooms, bathrooms, square_feet, monthly_rent, status) VALUES (%s, %s, %s, %s, %s, %s)',
                (unit_number, bedrooms, bathrooms, square_feet, monthly_rent, status)
            )
            conn.commit()
            flash('Apartment added successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('apartments'))
    return render_template('add_apartment.html')

# Payments Routes
@app.route('/payments')
def payments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT p.*, t.name as tenant_name, a.unit_number 
        FROM payments p
        JOIN tenants t ON p.tenant_id = t.tenant_id
        JOIN apartments a ON p.apartment_id = a.apartment_id
    ''')
    payments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('payments.html', payments=payments)

@app.route('/add_payment', methods=['GET', 'POST'])
def add_payment():
    if request.method == 'POST':
        tenant_id = request.form['tenant_id']
        apartment_id = request.form['apartment_id']
        amount = request.form['amount']
        payment_date = request.form['payment_date']
        payment_method = request.form['payment_method']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO payments (tenant_id, apartment_id, amount, payment_date, payment_method) VALUES (%s, %s, %s, %s, %s)',
                (tenant_id, apartment_id, amount, payment_date, payment_method)
            )
            conn.commit()
            flash('Payment added successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('payments'))
    
    # For GET request, show the form with tenants and apartments
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT tenant_id, name FROM tenants')
    tenants = cursor.fetchall()
    cursor.execute('SELECT apartment_id, unit_number FROM apartments')
    apartments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('add_payment.html', tenants=tenants, apartments=apartments)

# Maintenance Routes
@app.route('/maintenance')
def maintenance():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT m.*, t.name as tenant_name, a.unit_number 
        FROM maintenance m
        JOIN tenants t ON m.tenant_id = t.tenant_id
        JOIN apartments a ON m.apartment_id = a.apartment_id
    ''')
    maintenance_requests = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('maintenance.html', maintenance_requests=maintenance_requests)

@app.route('/add_maintenance', methods=['GET', 'POST'])
def add_maintenance():
    if request.method == 'POST':
        apartment_id = request.form['apartment_id']
        tenant_id = request.form['tenant_id']
        description = request.form['description']
        request_date = request.form['request_date']
        status = request.form['status']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO maintenance (apartment_id, tenant_id, description, request_date, status) VALUES (%s, %s, %s, %s, %s)',
                (apartment_id, tenant_id, description, request_date, status)
            )
            conn.commit()
            flash('Maintenance request added successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('maintenance'))
    
    # For GET request, show the form with tenants and apartments
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT tenant_id, name FROM tenants')
    tenants = cursor.fetchall()
    cursor.execute('SELECT apartment_id, unit_number FROM apartments')
    apartments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('add_maintenance.html', tenants=tenants, apartments=apartments)

# Employees Routes
@app.route('/employees')
def employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('employees.html', employees=employees)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        email = request.form['email']
        phone = request.form['phone']
        hire_date = request.form['hire_date']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO employees (name, position, email, phone, hire_date) VALUES (%s, %s, %s, %s, %s)',
                (name, position, email, phone, hire_date)
            )
            conn.commit()
            flash('Employee added successfully!', 'success')
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('employees'))
    return render_template('add_employee.html')

if __name__ == '__main__':
    app.run(debug=True)