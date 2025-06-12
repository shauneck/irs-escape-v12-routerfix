import requests
import json

# Get courses
response = requests.get('http://localhost:8001/api/courses')
courses = response.json()

print("=== Quiz System Details ===\n")

total_questions = 0

for course in courses:
    course_id = course.get('id')
    course_title = course.get('title')
    course_type = course.get('type')
    
    print(f"Course: {course_title} ({course_type})")
    
    # Get quiz questions
    quiz_response = requests.get(f'http://localhost:8001/api/courses/{course_id}/quiz')
    questions = quiz_response.json()
    
    print(f"Total Quiz Questions: {len(questions)}")
    total_questions += len(questions)
    
    # Test randomization
    quiz_response2 = requests.get(f'http://localhost:8001/api/courses/{course_id}/quiz')
    questions2 = quiz_response2.json()
    
    # Check if options are randomized
    randomization_detected = False
    for i in range(min(len(questions), len(questions2))):
        q1 = questions[i]
        q2 = questions2[i]
        
        # Find a question with the same ID but different option order
        if q1.get("id") == q2.get("id") and q1.get("options") != q2.get("options"):
            randomization_detected = True
            print(f"Randomization detected: Yes")
            break
    
    if not randomization_detected:
        print(f"Randomization detected: No (may be coincidence)")
    
    # Print sample questions
    print("\nSample Questions:")
    for i, question in enumerate(questions[:3]):
        print(f"  {i+1}. {question.get('question')}")
        print(f"     Options: {', '.join(question.get('options', []))}")
        print(f"     Points: {question.get('points', 0)}")
    
    print("\n" + "-"*50 + "\n")

print(f"Total Quiz Questions Across All Courses: {total_questions}")