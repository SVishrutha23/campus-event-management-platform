-- Campus Event Management Platform - Reporting Queries

-- 1. Event Popularity Report (sorted by registrations)
SELECT e.id, e.title, e.event_type, c.name as college_name,
       COUNT(er.id) as total_registrations,
       e.max_capacity,
       ROUND(COUNT(er.id) * 100.0 / e.max_capacity, 2) as capacity_percentage
FROM events e
JOIN colleges c ON e.college_id = c.id
LEFT JOIN event_registrations er ON e.id = er.event_id AND er.status = 'registered'
GROUP BY e.id, e.title, e.event_type, c.name, e.max_capacity
ORDER BY total_registrations DESC;

-- 2. Attendance Percentage Report
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
GROUP BY e.id, e.title, e.event_type, c.name
ORDER BY attendance_percentage DESC;

-- 3. Average Feedback Score Report
SELECT e.id, e.title, e.event_type, c.name as college_name,
       COUNT(f.id) as feedback_count,
       ROUND(AVG(f.rating), 2) as average_rating
FROM events e
JOIN colleges c ON e.college_id = c.id
LEFT JOIN event_registrations er ON e.id = er.event_id
LEFT JOIN feedback f ON er.id = f.registration_id
GROUP BY e.id, e.title, e.event_type, c.name
HAVING COUNT(f.id) > 0
ORDER BY average_rating DESC;

-- 4. Student Participation Report
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
GROUP BY s.id, s.name, s.student_id, c.name
ORDER BY events_attended DESC, events_registered DESC;

-- 5. Top 3 Most Active Students (Bonus)
SELECT s.id, s.name, s.student_id, c.name as college_name,
       COUNT(a.id) as events_attended,
       COUNT(er.id) as events_registered
FROM students s
JOIN colleges c ON s.college_id = c.id
LEFT JOIN event_registrations er ON s.id = er.student_id AND er.status = 'registered'
LEFT JOIN attendance a ON er.id = a.registration_id AND a.attended = 1
GROUP BY s.id, s.name, s.student_id, c.name
ORDER BY events_attended DESC, events_registered DESC
LIMIT 3;

-- 6. Event Type Analysis
SELECT event_type,
       COUNT(*) as total_events,
       COUNT(er.id) as total_registrations,
       COUNT(a.id) as total_attended,
       ROUND(AVG(f.rating), 2) as avg_feedback_rating
FROM events e
LEFT JOIN event_registrations er ON e.id = er.event_id AND er.status = 'registered'
LEFT JOIN attendance a ON er.id = a.registration_id AND a.attended = 1
LEFT JOIN feedback f ON er.id = f.registration_id
GROUP BY event_type
ORDER BY total_registrations DESC;

-- 7. College-wise Event Statistics
SELECT c.name as college_name,
       COUNT(DISTINCT e.id) as total_events,
       COUNT(DISTINCT s.id) as total_students,
       COUNT(er.id) as total_registrations,
       COUNT(a.id) as total_attended
FROM colleges c
LEFT JOIN events e ON c.id = e.college_id
LEFT JOIN students s ON c.id = s.college_id
LEFT JOIN event_registrations er ON e.id = er.event_id AND er.status = 'registered'
LEFT JOIN attendance a ON er.id = a.registration_id AND a.attended = 1
GROUP BY c.id, c.name
ORDER BY total_events DESC;

-- 8. Monthly Event Trends (assuming current year)
SELECT strftime('%Y-%m', start_date) as month,
       COUNT(*) as events_count,
       COUNT(er.id) as total_registrations
FROM events e
LEFT JOIN event_registrations er ON e.id = er.event_id AND er.status = 'registered'
WHERE start_date >= date('now', 'start of year')
GROUP BY strftime('%Y-%m', start_date)
ORDER BY month;
