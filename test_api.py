import requests
import json
from datetime import datetime

# Base URL for the API
BASE_URL = 'http://localhost:5000'

def test_api_endpoints():
    """Test all API endpoints with sample data"""
    
    print("=" * 60)
    print("Campus Event Management Platform - API Testing")
    print("=" * 60)
    
    # Test 1: Get all colleges
    print("\n1. Testing GET /api/colleges")
    response = requests.get(f'{BASE_URL}/api/colleges')
    if response.status_code == 200:
        colleges = response.json()
        print(f"✓ Found {len(colleges)} colleges")
        for college in colleges[:2]:  # Show first 2
            print(f"  - {college['name']} ({college['code']})")
    else:
        print(f"✗ Error: {response.status_code}")
    
    # Test 2: Get all events
    print("\n2. Testing GET /api/events")
    response = requests.get(f'{BASE_URL}/api/events')
    if response.status_code == 200:
        events = response.json()
        print(f"✓ Found {len(events)} events")
        for event in events[:3]:  # Show first 3
            print(f"  - {event['title']} ({event['event_type']}) at {event['college_name']}")
    else:
        print(f"✗ Error: {response.status_code}")
    
    # Test 3: Get students
    print("\n3. Testing GET /api/students")
    response = requests.get(f'{BASE_URL}/api/students?college_id=1')
    if response.status_code == 200:
        students = response.json()
        print(f"✓ Found {len(students)} students from IITD")
        for student in students[:3]:  # Show first 3
            print(f"  - {student['name']} ({student['student_id']}) - {student['department']}")
    else:
        print(f"✗ Error: {response.status_code}")
    
    # Test 4: Create a new event
    print("\n4. Testing POST /api/events (Create Event)")
    new_event = {
        "college_id": 1,
        "title": "Test Workshop - API Demo",
        "description": "A test workshop created via API",
        "event_type": "workshop",
        "start_date": "2024-04-15",
        "end_date": "2024-04-15",
        "start_time": "14:00:00",
        "end_time": "17:00:00",
        "venue": "Test Lab",
        "max_capacity": 30
    }
    
    response = requests.post(f'{BASE_URL}/api/events', json=new_event)
    if response.status_code == 201:
        result = response.json()
        new_event_id = result['event_id']
        print(f"✓ Event created successfully with ID: {new_event_id}")
    else:
        print(f"✗ Error creating event: {response.status_code}")
        new_event_id = 1  # Fallback for testing
    
    # Test 5: Register student for event
    print("\n5. Testing POST /api/register (Student Registration)")
    registration_data = {
        "event_id": new_event_id,
        "student_id": 1
    }
    
    response = requests.post(f'{BASE_URL}/api/register', json=registration_data)
    if response.status_code == 201:
        result = response.json()
        registration_id = result['registration_id']
        print(f"✓ Student registered successfully with Registration ID: {registration_id}")
    else:
        print(f"✗ Error registering student: {response.status_code}")
        registration_id = 1  # Fallback for testing
    
    # Test 6: Mark attendance
    print("\n6. Testing POST /api/attendance (Mark Attendance)")
    attendance_data = {
        "registration_id": registration_id
    }
    
    response = requests.post(f'{BASE_URL}/api/attendance', json=attendance_data)
    if response.status_code == 200:
        print("✓ Attendance marked successfully")
    else:
        print(f"✗ Error marking attendance: {response.status_code}")
    
    # Test 7: Submit feedback
    print("\n7. Testing POST /api/feedback (Submit Feedback)")
    feedback_data = {
        "registration_id": registration_id,
        "rating": 4,
        "comments": "Great workshop! Very informative and well-organized."
    }
    
    response = requests.post(f'{BASE_URL}/api/feedback', json=feedback_data)
    if response.status_code == 201:
        print("✓ Feedback submitted successfully")
    else:
        print(f"✗ Error submitting feedback: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("REPORTING ENDPOINTS")
    print("=" * 60)
    
    # Test 8: Event Popularity Report
    print("\n8. Testing GET /api/reports/event-popularity")
    response = requests.get(f'{BASE_URL}/api/reports/event-popularity')
    if response.status_code == 200:
        report = response.json()
        print(f"✓ Event Popularity Report - {len(report)} events")
        print("Top 3 Most Popular Events:")
        for i, event in enumerate(report[:3], 1):
            print(f"  {i}. {event['title']} - {event['total_registrations']} registrations ({event['capacity_percentage']}% capacity)")
    else:
        print(f"✗ Error: {response.status_code}")
    
    # Test 9: Attendance Percentage Report
    print("\n9. Testing GET /api/reports/attendance-percentage")
    response = requests.get(f'{BASE_URL}/api/reports/attendance-percentage')
    if response.status_code == 200:
        report = response.json()
        print(f"✓ Attendance Report - {len(report)} events")
        print("Top 3 Events by Attendance:")
        for i, event in enumerate(report[:3], 1):
            print(f"  {i}. {event['title']} - {event['attendance_percentage']}% attendance ({event['total_attended']}/{event['total_registrations']})")
    else:
        print(f"✗ Error: {response.status_code}")
    
    # Test 10: Average Feedback Report
    print("\n10. Testing GET /api/reports/average-feedback")
    response = requests.get(f'{BASE_URL}/api/reports/average-feedback')
    if response.status_code == 200:
        report = response.json()
        print(f"✓ Feedback Report - {len(report)} events with feedback")
        print("Top 3 Events by Rating:")
        for i, event in enumerate(report[:3], 1):
            print(f"  {i}. {event['title']} - {event['average_rating']}/5.0 ({event['feedback_count']} reviews)")
    else:
        print(f"✗ Error: {response.status_code}")
    
    # Test 11: Student Participation Report
    print("\n11. Testing GET /api/reports/student-participation")
    response = requests.get(f'{BASE_URL}/api/reports/student-participation?college_id=1')
    if response.status_code == 200:
        report = response.json()
        print(f"✓ Student Participation Report - {len(report)} students from IITD")
        print("Top 3 Most Active Students:")
        for i, student in enumerate(report[:3], 1):
            print(f"  {i}. {student['name']} - {student['events_attended']} attended, {student['events_registered']} registered ({student['attendance_rate']}% rate)")
    else:
        print(f"✗ Error: {response.status_code}")
    
    # Test 12: Top Active Students (Bonus)
    print("\n12. Testing GET /api/reports/top-active-students")
    response = requests.get(f'{BASE_URL}/api/reports/top-active-students')
    if response.status_code == 200:
        report = response.json()
        print("✓ Top 3 Most Active Students Across All Colleges:")
        for i, student in enumerate(report, 1):
            print(f"  {i}. {student['name']} ({student['college_name']}) - {student['events_attended']} events attended")
    else:
        print(f"✗ Error: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("API Testing Complete!")
    print("=" * 60)

def test_error_cases():
    """Test error handling"""
    print("\n" + "=" * 60)
    print("TESTING ERROR CASES")
    print("=" * 60)
    
    # Test duplicate registration
    print("\n1. Testing duplicate registration")
    registration_data = {
        "event_id": 1,
        "student_id": 1
    }
    response = requests.post(f'{BASE_URL}/api/register', json=registration_data)
    if response.status_code == 400:
        print("✓ Correctly rejected duplicate registration")
    else:
        print(f"✗ Unexpected response: {response.status_code}")
    
    # Test invalid feedback rating
    print("\n2. Testing invalid feedback rating")
    feedback_data = {
        "registration_id": 1,
        "rating": 6,  # Invalid rating > 5
        "comments": "Test feedback"
    }
    response = requests.post(f'{BASE_URL}/api/feedback', json=feedback_data)
    if response.status_code == 400:
        print("✓ Correctly rejected invalid rating")
    else:
        print(f"✗ Unexpected response: {response.status_code}")
    
    # Test missing required fields
    print("\n3. Testing missing required fields")
    incomplete_event = {
        "title": "Incomplete Event"
        # Missing required fields
    }
    response = requests.post(f'{BASE_URL}/api/events', json=incomplete_event)
    if response.status_code == 400:
        print("✓ Correctly rejected incomplete event data")
    else:
        print(f"✗ Unexpected response: {response.status_code}")

if __name__ == '__main__':
    try:
        # Test basic connectivity
        response = requests.get(f'{BASE_URL}/')
        if response.status_code == 200:
            print("✓ API server is running")
            test_api_endpoints()
            test_error_cases()
        else:
            print("✗ API server not responding")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to API server. Make sure it's running on http://localhost:5000")
        print("Run: python app.py")
