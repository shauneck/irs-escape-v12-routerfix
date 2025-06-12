import requests
import json

# Get courses
response = requests.get('http://localhost:8001/api/courses')
courses = response.json()

print("=== Course Module Details ===\n")

for course in courses:
    course_id = course.get('id')
    course_title = course.get('title')
    course_type = course.get('type')
    
    print(f"Course: {course_title} ({course_type})")
    print(f"Total Lessons: {course.get('total_lessons')}")
    print(f"Estimated Hours: {course.get('estimated_hours')}")
    
    # Get lessons
    lessons_response = requests.get(f'http://localhost:8001/api/courses/{course_id}/lessons')
    lessons = lessons_response.json()
    
    print(f"Actual Module Count: {len(lessons)}")
    print("\nModules:")
    
    # Sort by order_index
    for lesson in sorted(lessons, key=lambda x: x.get('order_index', 0)):
        print(f"  {lesson.get('order_index')}. {lesson.get('title')} ({lesson.get('duration_minutes')} minutes)")
    
    print("\n" + "-"*50 + "\n")