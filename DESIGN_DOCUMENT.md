# Campus Event Management Platform - Design Document

## Project Overview
A basic event reporting system for managing campus events across multiple colleges, supporting event creation, student registration, attendance tracking, and feedback collection.

## Data to Track
- **Event Creation**: Event details, scheduling, venue, capacity
- **Student Registration**: Registration records with status tracking
- **Attendance**: Check-in/check-out times with attendance status
- **Feedback**: Ratings (1-5) and optional comments

## Database Schema

### Tables Structure
```
colleges
├── id (PK)
├── name
├── code (UNIQUE)
├── address
└── created_at

events
├── id (PK)
├── college_id (FK → colleges.id)
├── title
├── description
├── event_type (hackathon, workshop, tech_talk, fest, seminar)
├── start_date, end_date
├── start_time, end_time
├── venue
├── max_capacity
├── is_active
└── created_at

students
├── id (PK)
├── college_id (FK → colleges.id)
├── student_id (college-specific)
├── name, email, phone
├── year_of_study, department
└── created_at
└── UNIQUE(college_id, student_id)

event_registrations
├── id (PK)
├── event_id (FK → events.id)
├── student_id (FK → students.id)
├── registration_date
├── status (registered, cancelled)
└── UNIQUE(event_id, student_id)

attendance
├── id (PK)
├── registration_id (FK → event_registrations.id)
├── check_in_time, check_out_time
├── attended (BOOLEAN)
└── created_at

feedback
├── id (PK)
├── registration_id (FK → event_registrations.id)
├── rating (1-5, CHECK constraint)
├── comments
└── submitted_at
```

### Performance Indexes
- `idx_events_college_id` on events(college_id)
- `idx_events_date` on events(start_date)
- `idx_students_college_id` on students(college_id)
- `idx_registrations_event_id` on event_registrations(event_id)
- `idx_registrations_student_id` on event_registrations(student_id)
- `idx_attendance_registration_id` on attendance(registration_id)
- `idx_feedback_registration_id` on feedback(registration_id)

## API Design

### Core Operations
```
GET    /api/colleges           # List all colleges
GET    /api/events             # List all events
GET    /api/students           # List students (filtered by college)
POST   /api/events             # Create new event
POST   /api/register           # Register student for event
POST   /api/attendance         # Mark attendance
POST   /api/feedback           # Submit feedback
```

### Reporting Endpoints
```
GET    /api/reports/event-popularity        # Events by registration count
GET    /api/reports/attendance-percentage   # Attendance rates by event
GET    /api/reports/average-feedback        # Average ratings by event
GET    /api/reports/student-participation   # Student activity by college
GET    /api/reports/top-active-students     # Most active students overall
```

### Request/Response Format
- **Content-Type**: application/json
- **Status Codes**: 200 (success), 201 (created), 400 (bad request), 404 (not found), 500 (server error)
- **Error Format**: `{"error": "Description of error"}`

## Workflows

### 1. Event Registration Flow
```
Student → Browse Events → Select Event → Register → Confirmation
                                      ↓
                              Check Capacity → Reject if Full
```

### 2. Attendance Flow
```
Event Day → Student Check-in → Mark Attendance → Optional Check-out
                            ↓
                    Update attendance record
```

### 3. Feedback Flow
```
Post-Event → Student Submits Rating (1-5) → Optional Comments → Store Feedback
```

### 4. Reporting Flow
```
Admin Request → Query Database → Aggregate Data → Return JSON Response
```

## Assumptions & Design Decisions

### Assumptions
1. **Event Uniqueness**: Events are unique per college (same event can exist in multiple colleges)
2. **Student Uniqueness**: Students have unique IDs within their college
3. **Feedback Optional**: Students can attend without providing feedback
4. **Single Registration**: One student can register only once per event
5. **Data Integrity**: Foreign key constraints ensure referential integrity

### Edge Cases Handled
1. **Duplicate Registrations**: UNIQUE constraint prevents duplicate registrations
2. **Capacity Management**: Registration checks available capacity before allowing registration
3. **Invalid Feedback**: CHECK constraint ensures ratings are between 1-5
4. **Missing Data**: API validates required fields before processing
5. **Cancelled Events**: Events have `is_active` flag for soft deletion

### Scale Considerations
- **Target Scale**: 50 colleges × 500 students × 20 events per semester
- **Database**: SQLite for development, PostgreSQL recommended for production
- **Indexing**: Strategic indexes on foreign keys and frequently queried fields
- **Caching**: Consider Redis for frequently accessed data in production

## Technology Stack
- **Backend**: Python Flask (lightweight, rapid development)
- **Database**: SQLite (easy setup, file-based)
- **API**: REST with JSON (standard, widely supported)
- **Testing**: Python requests library for API testing

## Security Considerations
- Input validation on all API endpoints
- SQL injection prevention through parameterized queries
- Rate limiting recommended for production
- Authentication/authorization not implemented (prototype scope)

## Future Enhancements
- Web UI for admin portal and student app
- Real-time notifications for event updates
- QR code generation for easy check-in
- Email notifications for registrations
- Advanced reporting with charts and graphs
- Mobile app for students
- Authentication and role-based access control
