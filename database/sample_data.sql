-- Sample data for Campus Event Management Platform

-- Insert sample colleges
INSERT INTO colleges (name, code, address) VALUES
('Indian Institute of Technology Delhi', 'IITD', 'Hauz Khas, New Delhi, Delhi 110016'),
('Delhi Technological University', 'DTU', 'Shahbad Daulatpur, Main Bawana Road, Delhi 110042'),
('Netaji Subhas University of Technology', 'NSUT', 'Azad Hind Fauj Marg, Sector 3, Dwarka, Delhi 110078');

-- Insert sample students
INSERT INTO students (college_id, student_id, name, email, phone, year_of_study, department) VALUES
-- IITD Students
(1, '2021CS001', 'Arjun Sharma', 'arjun.sharma@iitd.ac.in', '9876543210', 3, 'Computer Science'),
(1, '2021EE002', 'Priya Patel', 'priya.patel@iitd.ac.in', '9876543211', 3, 'Electrical Engineering'),
(1, '2022ME003', 'Rahul Kumar', 'rahul.kumar@iitd.ac.in', '9876543212', 2, 'Mechanical Engineering'),
(1, '2020CS004', 'Sneha Gupta', 'sneha.gupta@iitd.ac.in', '9876543213', 4, 'Computer Science'),
(1, '2021EC005', 'Vikram Singh', 'vikram.singh@iitd.ac.in', '9876543214', 3, 'Electronics'),

-- DTU Students
(2, 'DTU2021001', 'Ananya Joshi', 'ananya.joshi@dtu.ac.in', '9876543215', 3, 'Information Technology'),
(2, 'DTU2022002', 'Karan Verma', 'karan.verma@dtu.ac.in', '9876543216', 2, 'Computer Science'),
(2, 'DTU2021003', 'Riya Agarwal', 'riya.agarwal@dtu.ac.in', '9876543217', 3, 'Electronics'),
(2, 'DTU2020004', 'Amit Yadav', 'amit.yadav@dtu.ac.in', '9876543218', 4, 'Mechanical Engineering'),
(2, 'DTU2022005', 'Pooja Mishra', 'pooja.mishra@dtu.ac.in', '9876543219', 2, 'Information Technology'),

-- NSUT Students
(3, 'NSUT21001', 'Rohit Bansal', 'rohit.bansal@nsut.ac.in', '9876543220', 3, 'Computer Science'),
(3, 'NSUT22002', 'Kavya Reddy', 'kavya.reddy@nsut.ac.in', '9876543221', 2, 'Electronics'),
(3, 'NSUT21003', 'Deepak Tiwari', 'deepak.tiwari@nsut.ac.in', '9876543222', 3, 'Information Technology'),
(3, 'NSUT20004', 'Nisha Choudhary', 'nisha.choudhary@nsut.ac.in', '9876543223', 4, 'Computer Science'),
(3, 'NSUT22005', 'Sanjay Mehra', 'sanjay.mehra@nsut.ac.in', '9876543224', 2, 'Mechanical Engineering');

-- Insert sample events
INSERT INTO events (college_id, title, description, event_type, start_date, end_date, start_time, end_time, venue, max_capacity) VALUES
-- IITD Events
(1, 'HackIITD 2024', 'Annual hackathon for innovative solutions', 'hackathon', '2024-03-15', '2024-03-17', '09:00:00', '18:00:00', 'Main Auditorium', 200),
(1, 'AI/ML Workshop', 'Introduction to Machine Learning concepts', 'workshop', '2024-02-20', '2024-02-20', '14:00:00', '17:00:00', 'Computer Lab 1', 50),
(1, 'Tech Talk: Future of Computing', 'Industry expert discussion on computing trends', 'tech_talk', '2024-02-25', '2024-02-25', '16:00:00', '18:00:00', 'Lecture Hall 101', 100),

-- DTU Events
(2, 'DTU TechFest 2024', 'Annual technical festival', 'fest', '2024-03-20', '2024-03-22', '10:00:00', '20:00:00', 'Campus Ground', 500),
(2, 'Web Development Bootcamp', 'Full-stack web development workshop', 'workshop', '2024-02-28', '2024-03-01', '10:00:00', '16:00:00', 'IT Lab', 40),
(2, 'Robotics Seminar', 'Latest trends in robotics and automation', 'seminar', '2024-03-05', '2024-03-05', '15:00:00', '17:00:00', 'Seminar Hall', 80),

-- NSUT Events
(3, 'CodeSprint NSUT', '48-hour coding competition', 'hackathon', '2024-03-10', '2024-03-12', '08:00:00', '20:00:00', 'CS Department', 150),
(3, 'Data Science Workshop', 'Hands-on data analysis and visualization', 'workshop', '2024-02-22', '2024-02-22', '13:00:00', '18:00:00', 'Lab 201', 35),
(3, 'Industry Connect', 'Tech leaders sharing career insights', 'tech_talk', '2024-03-01', '2024-03-01', '17:00:00', '19:00:00', 'Main Hall', 120);

-- Insert sample registrations
INSERT INTO event_registrations (event_id, student_id, registration_date, status) VALUES
-- HackIITD registrations
(1, 1, '2024-02-10 10:30:00', 'registered'),
(1, 2, '2024-02-10 11:15:00', 'registered'),
(1, 3, '2024-02-11 09:20:00', 'registered'),
(1, 4, '2024-02-11 14:45:00', 'registered'),

-- AI/ML Workshop registrations
(2, 1, '2024-02-15 16:30:00', 'registered'),
(2, 4, '2024-02-16 10:20:00', 'registered'),
(2, 5, '2024-02-16 12:15:00', 'registered'),

-- DTU TechFest registrations
(4, 6, '2024-02-12 09:30:00', 'registered'),
(4, 7, '2024-02-12 10:45:00', 'registered'),
(4, 8, '2024-02-13 11:20:00', 'registered'),
(4, 9, '2024-02-13 15:30:00', 'registered'),
(4, 10, '2024-02-14 08:45:00', 'registered'),

-- Web Development Bootcamp registrations
(5, 6, '2024-02-18 14:20:00', 'registered'),
(5, 7, '2024-02-18 16:30:00', 'registered'),
(5, 10, '2024-02-19 09:15:00', 'registered'),

-- CodeSprint NSUT registrations
(7, 11, '2024-02-08 12:30:00', 'registered'),
(7, 12, '2024-02-08 13:45:00', 'registered'),
(7, 13, '2024-02-09 10:20:00', 'registered'),
(7, 14, '2024-02-09 11:30:00', 'registered'),
(7, 15, '2024-02-10 09:45:00', 'registered');

-- Insert sample attendance records
INSERT INTO attendance (registration_id, check_in_time, check_out_time, attended) VALUES
-- HackIITD attendance (assuming event happened)
(1, '2024-03-15 09:15:00', '2024-03-17 17:45:00', TRUE),
(2, '2024-03-15 09:30:00', '2024-03-17 18:00:00', TRUE),
(3, '2024-03-15 10:00:00', '2024-03-16 15:30:00', TRUE), -- Left early
(4, NULL, NULL, FALSE), -- Registered but didn't attend

-- AI/ML Workshop attendance
(5, '2024-02-20 14:10:00', '2024-02-20 17:15:00', TRUE),
(6, '2024-02-20 14:05:00', '2024-02-20 17:00:00', TRUE),
(7, NULL, NULL, FALSE); -- Registered but didn't attend

-- Insert sample feedback
INSERT INTO feedback (registration_id, rating, comments, submitted_at) VALUES
-- HackIITD feedback
(1, 5, 'Excellent event! Great learning experience and networking opportunities.', '2024-03-17 19:30:00'),
(2, 4, 'Well organized hackathon. Could have better mentorship support.', '2024-03-17 20:15:00'),
(3, 3, 'Good event but had to leave early due to personal reasons.', '2024-03-16 16:00:00'),

-- AI/ML Workshop feedback
(5, 5, 'Very informative workshop. Practical examples were helpful.', '2024-02-20 17:30:00'),
(6, 4, 'Good content but could be more hands-on.', '2024-02-20 17:45:00');
