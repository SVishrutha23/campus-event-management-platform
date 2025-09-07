from flask import Flask, request, jsonify, g
import sqlite3
import os
from datetime import datetime
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Database configuration
DATABASE = 'database/campus_events.db'

def get_db():
    """Get database connection"""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.teardown_appcontext
def close_db_context(error):
    close_db()

def init_db():
    """Initialize database with schema and sample data"""
    if not os.path.exists('database'):
        os.makedirs('database')
    
    with app.app_context():
        db = get_db()
        
        # Check if tables already exist
        cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='colleges'")
        if cursor.fetchone() is None:
            # Tables don't exist, create them
            with open('database/schema.sql', 'r') as f:
                db.executescript(f.read())
            
            # Insert sample data
            with open('database/sample_data.sql', 'r') as f:
                db.executescript(f.read())
            
            db.commit()
            print("Database initialized with sample data")
        else:
            print("Database already exists, skipping initialization")

# API Endpoints

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events or filter by college_id"""
    college_id = request.args.get('college_id')
    db = get_db()
    
    if college_id:
        events = db.execute('''
            SELECT e.*, c.name as college_name 
            FROM events e 
            JOIN colleges c ON e.college_id = c.id 
            WHERE e.college_id = ? AND e.is_active = 1
            ORDER BY e.start_date
        ''', (college_id,)).fetchall()
    else:
        events = db.execute('''
            SELECT e.*, c.name as college_name 
            FROM events e 
            JOIN colleges c ON e.college_id = c.id 
            WHERE e.is_active = 1
            ORDER BY e.start_date
        ''').fetchall()
    
    return jsonify([dict(event) for event in events])

@app.route('/api/events', methods=['POST'])
def create_event():
    """Create a new event"""
    data = request.get_json()
    
    required_fields = ['college_id', 'title', 'event_type', 'start_date', 'end_date', 'start_time', 'end_time']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    db = get_db()
    cursor = db.execute('''
        INSERT INTO events (college_id, title, description, event_type, start_date, end_date, 
                           start_time, end_time, venue, max_capacity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['college_id'], data['title'], data.get('description', ''),
        data['event_type'], data['start_date'], data['end_date'],
        data['start_time'], data['end_time'], data.get('venue', ''),
        data.get('max_capacity', 100)
    ))
    
    db.commit()
    
    return jsonify({'message': 'Event created successfully', 'event_id': cursor.lastrowid}), 201

@app.route('/api/register', methods=['POST'])
def register_student():
    """Register a student for an event"""
    data = request.get_json()
    
    if 'event_id' not in data or 'student_id' not in data:
        return jsonify({'error': 'Missing event_id or student_id'}), 400
    
    db = get_db()
    
    # Check if already registered
    existing = db.execute('''
        SELECT id FROM event_registrations 
        WHERE event_id = ? AND student_id = ?
    ''', (data['event_id'], data['student_id'])).fetchone()
    
    if existing:
        return jsonify({'error': 'Student already registered for this event'}), 400
    
    # Check event capacity
    event_info = db.execute('''
        SELECT max_capacity, 
               (SELECT COUNT(*) FROM event_registrations WHERE event_id = ? AND status = 'registered') as current_registrations
        FROM events WHERE id = ?
    ''', (data['event_id'], data['event_id'])).fetchone()
    
    if event_info and event_info['current_registrations'] >= event_info['max_capacity']:
        return jsonify({'error': 'Event is full'}), 400
    
    cursor = db.execute('''
        INSERT INTO event_registrations (event_id, student_id)
        VALUES (?, ?)
    ''', (data['event_id'], data['student_id']))
    
    db.commit()
    
    return jsonify({'message': 'Registration successful', 'registration_id': cursor.lastrowid}), 201

@app.route('/api/attendance', methods=['POST'])
def mark_attendance():
    """Mark attendance for a student"""
    data = request.get_json()
    
    if 'registration_id' not in data:
        return jsonify({'error': 'Missing registration_id'}), 400
    
    db = get_db()
    
    # Check if attendance record exists
    existing = db.execute('''
        SELECT id FROM attendance WHERE registration_id = ?
    ''', (data['registration_id'],)).fetchone()
    
    if existing:
        # Update existing record
        db.execute('''
            UPDATE attendance 
            SET check_in_time = COALESCE(check_in_time, ?),
                check_out_time = ?,
                attended = 1
            WHERE registration_id = ?
        ''', (datetime.now().isoformat(), data.get('check_out_time'), data['registration_id']))
    else:
        # Create new attendance record
        db.execute('''
            INSERT INTO attendance (registration_id, check_in_time, check_out_time, attended)
            VALUES (?, ?, ?, 1)
        ''', (data['registration_id'], datetime.now().isoformat(), data.get('check_out_time')))
    
    db.commit()
    
    return jsonify({'message': 'Attendance marked successfully'}), 200

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit feedback for an event"""
    data = request.get_json()
    
    required_fields = ['registration_id', 'rating']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    if not (1 <= data['rating'] <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    db = get_db()
    
    # Check if feedback already exists
    existing = db.execute('''
        SELECT id FROM feedback WHERE registration_id = ?
    ''', (data['registration_id'],)).fetchone()
    
    if existing:
        return jsonify({'error': 'Feedback already submitted for this registration'}), 400
    
    cursor = db.execute('''
        INSERT INTO feedback (registration_id, rating, comments)
        VALUES (?, ?, ?)
    ''', (data['registration_id'], data['rating'], data.get('comments', '')))
    
    db.commit()
    
    return jsonify({'message': 'Feedback submitted successfully', 'feedback_id': cursor.lastrowid}), 201

# Reporting Endpoints

@app.route('/api/reports/event-popularity', methods=['GET'])
def event_popularity_report():
    """Get event popularity report sorted by registrations"""
    college_id = request.args.get('college_id')
    db = get_db()
    
    query = '''
        SELECT e.id, e.title, e.event_type, c.name as college_name,
               COUNT(er.id) as total_registrations,
               e.max_capacity,
               ROUND(COUNT(er.id) * 100.0 / e.max_capacity, 2) as capacity_percentage
        FROM events e
        JOIN colleges c ON e.college_id = c.id
        LEFT JOIN event_registrations er ON e.id = er.event_id AND er.status = 'registered'
    '''
    
    params = []
    if college_id:
        query += ' WHERE e.college_id = ?'
        params.append(college_id)
    
    query += '''
        GROUP BY e.id, e.title, e.event_type, c.name, e.max_capacity
        ORDER BY total_registrations DESC
    '''
    
    results = db.execute(query, params).fetchall()
    
    return jsonify([dict(row) for row in results])

@app.route('/api/reports/attendance-percentage', methods=['GET'])
def attendance_percentage_report():
    """Get attendance percentage for events"""
    college_id = request.args.get('college_id')
    db = get_db()
    
    query = '''
        SELECT e.id, e.title, e.event_type, c.name as college_name,
               COUNT(er.id) as total_registrations,
               COUNT(a.id) as total_attended,
               CASE 
                   WHEN COUNT(er.id) > 0 THEN ROUND(COUNT(a.id) * 100.0 / COUNT(er.id), 2)
                   ELSE 0
               END as attendance_percentage
        FROM events e
        JOIN colleges c ON e.college_id = c.id
        LEFT JOIN event_registrations er ON e.id = er.event_id AND er.status = 'registered'
        LEFT JOIN attendance a ON er.id = a.registration_id AND a.attended = 1
    '''
    
    params = []
    if college_id:
        query += ' WHERE e.college_id = ?'
        params.append(college_id)
    
    query += '''
        GROUP BY e.id, e.title, e.event_type, c.name
        ORDER BY attendance_percentage DESC
    '''
    
    results = db.execute(query, params).fetchall()
    
    return jsonify([dict(row) for row in results])

@app.route('/api/reports/average-feedback', methods=['GET'])
def average_feedback_report():
    """Get average feedback scores for events"""
    college_id = request.args.get('college_id')
    db = get_db()
    
    query = '''
        SELECT e.id, e.title, e.event_type, c.name as college_name,
               COUNT(f.id) as feedback_count,
               ROUND(AVG(f.rating), 2) as average_rating
        FROM events e
        JOIN colleges c ON e.college_id = c.id
        LEFT JOIN event_registrations er ON e.id = er.event_id
        LEFT JOIN feedback f ON er.id = f.registration_id
    '''
    
    params = []
    if college_id:
        query += ' WHERE e.college_id = ?'
        params.append(college_id)
    
    query += '''
        GROUP BY e.id, e.title, e.event_type, c.name
        HAVING COUNT(f.id) > 0
        ORDER BY average_rating DESC
    '''
    
    results = db.execute(query, params).fetchall()
    
    return jsonify([dict(row) for row in results])

@app.route('/api/reports/student-participation', methods=['GET'])
def student_participation_report():
    """Get student participation report"""
    college_id = request.args.get('college_id')
    db = get_db()
    
    query = '''
        SELECT s.id, s.name, s.student_id, c.name as college_name,
               COUNT(er.id) as events_registered,
               COUNT(a.id) as events_attended,
               CASE 
                   WHEN COUNT(er.id) > 0 THEN ROUND(COUNT(a.id) * 100.0 / COUNT(er.id), 2)
                   ELSE 0
               END as attendance_rate
        FROM students s
        JOIN colleges c ON s.college_id = c.id
        LEFT JOIN event_registrations er ON s.id = er.student_id AND er.status = 'registered'
        LEFT JOIN attendance a ON er.id = a.registration_id AND a.attended = 1
    '''
    
    params = []
    if college_id:
        query += ' WHERE s.college_id = ?'
        params.append(college_id)
    
    query += '''
        GROUP BY s.id, s.name, s.student_id, c.name
        ORDER BY events_attended DESC, events_registered DESC
    '''
    
    results = db.execute(query, params).fetchall()
    
    return jsonify([dict(row) for row in results])

@app.route('/api/reports/top-active-students', methods=['GET'])
def top_active_students():
    """Get top 3 most active students"""
    college_id = request.args.get('college_id')
    limit = request.args.get('limit', 3)
    db = get_db()
    
    query = '''
        SELECT s.id, s.name, s.student_id, c.name as college_name,
               COUNT(a.id) as events_attended,
               COUNT(er.id) as events_registered
        FROM students s
        JOIN colleges c ON s.college_id = c.id
        LEFT JOIN event_registrations er ON s.id = er.student_id AND er.status = 'registered'
        LEFT JOIN attendance a ON er.id = a.registration_id AND a.attended = 1
    '''
    
    params = []
    if college_id:
        query += ' WHERE s.college_id = ?'
        params.append(college_id)
    
    query += '''
        GROUP BY s.id, s.name, s.student_id, c.name
        ORDER BY events_attended DESC, events_registered DESC
        LIMIT ?
    '''
    params.append(limit)
    
    results = db.execute(query, params).fetchall()
    
    return jsonify([dict(row) for row in results])

@app.route('/api/colleges', methods=['GET'])
def get_colleges():
    """Get all colleges"""
    db = get_db()
    colleges = db.execute('SELECT * FROM colleges ORDER BY name').fetchall()
    return jsonify([dict(college) for college in colleges])

@app.route('/api/students', methods=['GET'])
def get_students():
    """Get students, optionally filtered by college"""
    college_id = request.args.get('college_id')
    db = get_db()
    
    if college_id:
        students = db.execute('''
            SELECT s.*, c.name as college_name 
            FROM students s 
            JOIN colleges c ON s.college_id = c.id 
            WHERE s.college_id = ?
            ORDER BY s.name
        ''', (college_id,)).fetchall()
    else:
        students = db.execute('''
            SELECT s.*, c.name as college_name 
            FROM students s 
            JOIN colleges c ON s.college_id = c.id 
            ORDER BY s.name
        ''').fetchall()
    
    return jsonify([dict(student) for student in students])

@app.route('/')
def index():
    """Basic API info"""
    return jsonify({
        'message': 'Campus Event Management Platform API',
        'version': '1.0',
        'endpoints': {
            'events': '/api/events',
            'register': '/api/register',
            'attendance': '/api/attendance',
            'feedback': '/api/feedback',
            'reports': {
                'event_popularity': '/api/reports/event-popularity',
                'attendance_percentage': '/api/reports/attendance-percentage',
                'average_feedback': '/api/reports/average-feedback',
                'student_participation': '/api/reports/student-participation',
                'top_active_students': '/api/reports/top-active-students'
            }
        }
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
