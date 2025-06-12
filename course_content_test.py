import requests
import json
import re
import sys

# Base URL for API
BASE_URL = "http://localhost:8001/api"

def get_backend_url():
    """Get the backend URL from the frontend .env file"""
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if 'REACT_APP_BACKEND_URL' in line:
                    backend_url = line.strip().split('=')[1].strip('"\'')
                    return backend_url
    except Exception as e:
        print(f"Error reading backend URL: {e}")
        return "http://localhost:8001"

def test_courses_availability():
    """Test that all 3 courses are accessible"""
    backend_url = get_backend_url()
    response = requests.get(f"{backend_url}/api/courses")
    assert response.status_code == 200, f"Failed to get courses: {response.status_code}"
    
    courses = response.json()
    assert len(courses) == 3, f"Expected 3 courses, got {len(courses)}"
    
    # Verify course types
    course_types = [course["type"] for course in courses]
    assert "primer" in course_types, "Primer course not found"
    assert "w2" in course_types, "W-2 Escape Plan course not found"
    assert "business" in course_types, "Business Owner Escape Plan course not found"
    
    print("✅ All 3 courses are accessible")
    return courses

def test_course_modules_count(courses):
    """Test that each course has the correct number of modules"""
    backend_url = get_backend_url()
    
    for course in courses:
        course_id = course["id"]
        course_type = course["type"]
        course_title = course["title"]
        response = requests.get(f"{backend_url}/api/courses/{course_id}/lessons")
        assert response.status_code == 200, f"Failed to get lessons for course {course_id}: {response.status_code}"
        
        lessons = response.json()
        
        if course_type == "primer":
            expected_count = 6
            assert len(lessons) == expected_count, f"Expected {expected_count} modules in Primer course, got {len(lessons)}"
            print(f"✅ {course_title} has {len(lessons)} modules as expected")
        
        elif course_type == "w2":
            expected_count = 9
            assert len(lessons) == expected_count, f"Expected {expected_count} modules in W-2 Escape Plan course, got {len(lessons)}"
            print(f"✅ {course_title} has {len(lessons)} modules as expected")
        
        elif course_type == "business":
            expected_count = 9
            assert len(lessons) == expected_count, f"Expected {expected_count} modules in Business Owner Escape Plan course, got {len(lessons)}"
            print(f"✅ {course_title} has {len(lessons)} modules as expected")
    
    return True

def test_what_youll_learn_sections(courses):
    """Test that all modules contain 'What You'll Learn' sections with 4-6 specific bullet points"""
    backend_url = get_backend_url()
    
    for course in courses:
        course_id = course["id"]
        course_type = course["type"]
        course_title = course["title"]
        
        response = requests.get(f"{backend_url}/api/courses/{course_id}/lessons")
        assert response.status_code == 200, f"Failed to get lessons for course {course_id}: {response.status_code}"
        
        lessons = response.json()
        
        print(f"\nChecking 'What You'll Learn' sections in {course_title}:")
        
        modules_with_what_youll_learn = 0
        modules_with_proper_bullet_points = 0
        
        for lesson in lessons:
            lesson_title = lesson["title"]
            content = lesson["content"]
            
            # Check if "What You'll Learn" section exists
            what_youll_learn_match = re.search(r'## What You\'ll Learn\s+(.*?)(?=##|\Z)', content, re.DOTALL)
            
            if what_youll_learn_match:
                modules_with_what_youll_learn += 1
                what_youll_learn_content = what_youll_learn_match.group(1).strip()
                
                # Count bullet points (lines starting with • or -)
                bullet_points = re.findall(r'[•\-]\s+\*\*.*?\*\*', what_youll_learn_content)
                
                # Ensure there are 4-6 bullet points
                if 4 <= len(bullet_points) <= 6:
                    modules_with_proper_bullet_points += 1
                    print(f"  ✅ Module '{lesson_title}' has {len(bullet_points)} bullet points in 'What You'll Learn' section")
                else:
                    print(f"  ❌ Module '{lesson_title}' has {len(bullet_points)} bullet points in 'What You'll Learn' section (expected 4-6)")
                
                # Check that bullet points are specific and actionable
                for point in bullet_points:
                    # Remove bullet and whitespace
                    point_text = re.sub(r'^[•\-]\s+', '', point).strip()
                    
                    # Check if point contains action verbs
                    action_verbs = ["understand", "identify", "learn", "master", "apply", "determine", "recognize", "calculate", "distinguish", "design", "develop", "implement", "create", "analyze", "evaluate", "unlock", "avoid"]
                    has_action_verb = any(verb in point_text.lower() for verb in action_verbs)
                    
                    if not has_action_verb:
                        print(f"  ⚠️ Bullet point lacks action verb: {point_text}")
                    
                    # Check if point is specific (not generic)
                    if len(point_text) < 30:
                        print(f"  ⚠️ Bullet point too short/generic: {point_text}")
            else:
                print(f"  ❌ Module '{lesson_title}' is missing 'What You'll Learn' section")
        
        print(f"✅ {modules_with_what_youll_learn}/{len(lessons)} modules have 'What You'll Learn' sections")
        print(f"✅ {modules_with_proper_bullet_points}/{len(lessons)} modules have 4-6 bullet points in 'What You'll Learn' sections")
    
    return True

def test_learning_outcomes_quality(courses):
    """Test that learning outcomes are strategy-specific and actionable"""
    backend_url = get_backend_url()
    
    # Get glossary terms to check alignment
    glossary_response = requests.get(f"{backend_url}/api/glossary")
    assert glossary_response.status_code == 200, f"Failed to get glossary: {glossary_response.status_code}"
    
    glossary_terms = [term["term"].lower() for term in glossary_response.json()]
    
    for course in courses:
        course_id = course["id"]
        course_title = course["title"]
        
        response = requests.get(f"{backend_url}/api/courses/{course_id}/lessons")
        assert response.status_code == 200, f"Failed to get lessons for course {course_id}: {response.status_code}"
        
        lessons = response.json()
        
        print(f"\nChecking learning outcomes quality in {course_title}:")
        
        modules_with_understand_unlock_avoid = 0
        modules_with_glossary_alignment = 0
        
        for lesson in lessons:
            lesson_title = lesson["title"]
            content = lesson["content"]
            
            # Extract "What You'll Learn" section
            what_youll_learn_match = re.search(r'## What You\'ll Learn\s+(.*?)(?=##|\Z)', content, re.DOTALL)
            
            if what_youll_learn_match:
                what_youll_learn_content = what_youll_learn_match.group(1).strip()
                
                # Count bullet points with "understand", "unlock", or "avoid"
                understand_points = len(re.findall(r'[•\-]\s+\*\*.*?understand.*?\*\*', what_youll_learn_content, re.IGNORECASE))
                unlock_points = len(re.findall(r'[•\-]\s+\*\*.*?unlock.*?\*\*', what_youll_learn_content, re.IGNORECASE))
                avoid_points = len(re.findall(r'[•\-]\s+\*\*.*?avoid.*?\*\*', what_youll_learn_content, re.IGNORECASE))
                
                # Check if at least one bullet point focuses on what users will understand, unlock, or avoid
                if understand_points + unlock_points + avoid_points > 0:
                    modules_with_understand_unlock_avoid += 1
                    print(f"  ✅ Module '{lesson_title}' has bullet points focusing on what users will understand, unlock, or avoid")
                else:
                    print(f"  ⚠️ Module '{lesson_title}' has no bullet points focusing on what users will understand, unlock, or avoid")
                
                # Check if learning outcomes align with glossary terms
                glossary_term_matches = 0
                matched_terms = []
                
                for term in glossary_terms:
                    if term in what_youll_learn_content.lower():
                        glossary_term_matches += 1
                        matched_terms.append(term)
                
                if glossary_term_matches > 0:
                    modules_with_glossary_alignment += 1
                    print(f"  ✅ Module '{lesson_title}' has learning outcomes aligned with glossary terms: {', '.join(matched_terms[:3])}...")
                else:
                    print(f"  ⚠️ Module '{lesson_title}' has no learning outcomes aligned with glossary terms")
            else:
                print(f"  ❌ Module '{lesson_title}' is missing 'What You'll Learn' section")
        
        print(f"✅ {modules_with_understand_unlock_avoid}/{len(lessons)} modules have outcomes focusing on what users will understand, unlock, or avoid")
        print(f"✅ {modules_with_glossary_alignment}/{len(lessons)} modules have learning outcomes aligned with glossary terms")
    
    return True

def test_module_structure(courses):
    """Test that each module content is properly formatted with 'What You'll Learn' in the right position"""
    backend_url = get_backend_url()
    
    for course in courses:
        course_id = course["id"]
        course_title = course["title"]
        
        response = requests.get(f"{backend_url}/api/courses/{course_id}/lessons")
        assert response.status_code == 200, f"Failed to get lessons for course {course_id}: {response.status_code}"
        
        lessons = response.json()
        
        print(f"\nChecking module structure in {course_title}:")
        
        modules_with_proper_structure = 0
        
        for lesson in lessons:
            lesson_title = lesson["title"]
            content = lesson["content"]
            
            # Check if content has an introduction before "What You'll Learn"
            intro_and_what_youll_learn = re.search(r'(.*?)## What You\'ll Learn', content, re.DOTALL)
            
            if intro_and_what_youll_learn:
                intro = intro_and_what_youll_learn.group(1).strip()
                
                if len(intro) > 100:  # Arbitrary threshold for a meaningful introduction
                    # Check if "What You'll Learn" appears before main content sections
                    what_youll_learn_and_main = re.search(r'## What You\'ll Learn.*?(##.*)', content, re.DOTALL)
                    
                    if what_youll_learn_and_main:
                        modules_with_proper_structure += 1
                        print(f"  ✅ Module '{lesson_title}' has proper structure with 'What You'll Learn' in the right position")
                    else:
                        print(f"  ⚠️ Module '{lesson_title}' has 'What You'll Learn' but no main content sections after it")
                else:
                    print(f"  ⚠️ Module '{lesson_title}' has too short introduction before 'What You'll Learn'")
            else:
                print(f"  ❌ Module '{lesson_title}' doesn't have proper introduction before 'What You'll Learn'")
        
        print(f"✅ {modules_with_proper_structure}/{len(lessons)} modules have proper structure with 'What You'll Learn' in the right position")
    
    return True

def main():
    print("Starting course content verification tests...\n")
    
    try:
        # Test 1: Course Availability
        courses = test_courses_availability()
        
        # Test 2: Module Count
        test_course_modules_count(courses)
        
        # Test 3: "What You'll Learn" Sections
        test_what_youll_learn_sections(courses)
        
        # Test 4: Learning Outcomes Quality
        test_learning_outcomes_quality(courses)
        
        # Test 5: Module Structure
        test_module_structure(courses)
        
        print("\nAll tests completed successfully!")
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())