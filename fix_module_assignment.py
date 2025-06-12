from pymongo import MongoClient
import os

# Database connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'test_database')
client = MongoClient(MONGO_URL)
db = client[DB_NAME]
courses_collection = db['courses']

def fix_module_assignment():
    """Move 'The Exit Plan' module from W-2 course to Business Owner course"""
    
    # Get W-2 course
    w2_course = courses_collection.find_one({"title": "W-2 Escape Plan"})
    if not w2_course:
        print("❌ W-2 Escape Plan course not found")
        return False
    
    # Get Business Owner course
    business_course = courses_collection.find_one({"title": "Business Owner Escape Plan"})
    if not business_course:
        print("❌ Business Owner Escape Plan course not found")
        return False
    
    # Find the Exit Plan module in W-2 course (the one with QSBS, QOF description)
    exit_plan_module = None
    exit_plan_index = None
    
    for i, lesson in enumerate(w2_course.get('lessons', [])):
        if ('Exit Plan' in lesson.get('title', '') and 
            'QSBS' in lesson.get('description', '')):
            exit_plan_module = lesson
            exit_plan_index = i
            break
    
    if not exit_plan_module:
        print("❌ Exit Plan module with QSBS description not found in W-2 course")
        return False
    
    print(f"📋 Found module to move: {exit_plan_module['title']}")
    print(f"   ID: {exit_plan_module['id']}")
    print(f"   Description: {exit_plan_module.get('description', '')}")
    
    # Remove from W-2 course
    w2_lessons = w2_course['lessons']
    w2_lessons.pop(exit_plan_index)
    
    # Update module to be Module 9 of Business Owner course (since it currently has 9, this will be 10th)
    exit_plan_module['order_index'] = 9  # 0-based indexing, so 9 = Module 10
    exit_plan_module['description'] = "Module 10 of 10 - Complete exit planning with QSBS, QOF, and trust strategies"
    
    # Add to Business Owner course
    business_lessons = business_course['lessons']
    business_lessons.append(exit_plan_module)
    
    # Update W-2 course (now has 9 modules)
    result1 = courses_collection.update_one(
        {"id": w2_course["id"]},
        {"$set": {"lessons": w2_lessons, "total_lessons": len(w2_lessons)}}
    )
    
    # Update Business Owner course (now has 10 modules)
    result2 = courses_collection.update_one(
        {"id": business_course["id"]},
        {"$set": {"lessons": business_lessons, "total_lessons": len(business_lessons)}}
    )
    
    if result1.modified_count > 0 and result2.modified_count > 0:
        print(f"✅ Successfully moved 'The Exit Plan' module to Business Owner course")
        print(f"   W-2 Escape Plan now has {len(w2_lessons)} modules")
        print(f"   Business Owner Escape Plan now has {len(business_lessons)} modules")
        return True
    else:
        print("❌ Failed to update courses")
        return False

def verify_fix():
    """Verify the module counts are correct after the fix"""
    courses = list(courses_collection.find({}))
    
    print("\n📊 Course Module Counts After Fix:")
    for course in courses:
        print(f"   {course['title']}: {len(course.get('lessons', []))} modules")
        
        # Check for Exit Plan modules
        for lesson in course.get('lessons', []):
            if 'Exit Plan' in lesson.get('title', ''):
                print(f"     - Exit Plan module: {lesson['title']} (ID: {lesson['id']})")

if __name__ == "__main__":
    print("🔧 Starting module assignment fix...")
    
    if fix_module_assignment():
        verify_fix()
        print("\n✅ Module assignment fix completed successfully!")
    else:
        print("\n❌ Module assignment fix failed!")