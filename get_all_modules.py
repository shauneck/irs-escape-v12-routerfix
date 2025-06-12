import requests
import json
from pprint import pprint

def get_all_courses():
    response = requests.get("http://localhost:8001/api/courses")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching courses: {response.status_code}")
        return []

def get_course_details(course_id):
    response = requests.get(f"http://localhost:8001/api/courses/{course_id}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching course {course_id}: {response.status_code}")
        return None

def get_course_lessons(course_id):
    response = requests.get(f"http://localhost:8001/api/courses/{course_id}/lessons")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching lessons for course {course_id}: {response.status_code}")
        return []

def main():
    courses = get_all_courses()
    
    # Print the structure of the first course to understand the data
    if courses:
        print("First course structure:")
        pprint(courses[0])
    
    all_modules = []
    
    for course in courses:
        course_id = course["id"]
        course_name = course.get("title", "Unknown")  # Using title instead of name
        course_type = course["type"]
        
        print(f"\n{'='*80}")
        print(f"COURSE: {course_name} (Type: {course_type})")
        print(f"{'='*80}")
        
        lessons = get_course_lessons(course_id)
        
        for lesson in lessons:
            module_info = {
                "course_id": course_id,
                "course_name": course_name,
                "course_type": course_type,
                "module_id": lesson.get("id"),
                "title": lesson.get("title"),
                "order_index": lesson.get("order_index"),
                "content_preview": lesson.get("content", "")[:200] + "..." if lesson.get("content") else ""
            }
            
            all_modules.append(module_info)
            
            print(f"\nMODULE ID: {lesson.get('id')}")
            print(f"TITLE: {lesson.get('title')}")
            print(f"ORDER INDEX: {lesson.get('order_index')}")
            print(f"CONTENT PREVIEW: {module_info['content_preview']}")
    
    # Save all modules to a JSON file for reference
    with open("all_modules.json", "w") as f:
        json.dump(all_modules, f, indent=2)
    
    print(f"\nTotal modules found: {len(all_modules)}")
    print("Full module details saved to all_modules.json")

if __name__ == "__main__":
    main()