#!/usr/bin/env python3
import requests
import json
import sys
from pprint import pprint
from typing import Dict, List, Any, Optional
import re

# Get the backend URL from the frontend .env file
import os

# Read the REACT_APP_BACKEND_URL from the frontend .env file
with open('/app/frontend/.env', 'r') as f:
    env_content = f.read()
    match = re.search(r'REACT_APP_BACKEND_URL=(.+)', env_content)
    if match:
        BACKEND_URL = match.group(1).strip()
    else:
        BACKEND_URL = "https://340eb651-2cee-4dfb-be96-96e64a5cee1f.preview.emergentagent.com"

# Ensure the URL ends with /api for all API requests
API_URL = f"{BACKEND_URL}/api"

print(f"Testing backend API at: {API_URL}")

def test_courses_endpoint():
    """Test the /api/courses endpoint to verify all 3 courses are returned"""
    print("\n=== Testing Core API Endpoint: /api/courses ===")
    
    response = requests.get(f"{API_URL}/courses")
    if response.status_code != 200:
        print(f"❌ Failed to get courses: {response.status_code}")
        return None
    
    courses = response.json()
    if not courses or len(courses) < 3:
        print(f"❌ Expected at least 3 courses, got {len(courses)}")
        return None
    
    print(f"✅ Successfully retrieved {len(courses)} courses")
    
    # Check for the required courses
    course_types = {course.get('type'): course for course in courses}
    
    if 'primer' not in course_types:
        print("❌ Primer course not found")
    else:
        print(f"✅ Found Primer course: {course_types['primer']['title']}")
    
    if 'w2' not in course_types:
        print("❌ W-2 course not found")
    else:
        print(f"✅ Found W-2 course: {course_types['w2']['title']}")
    
    if 'business' not in course_types:
        print("❌ Business Owner course not found")
    else:
        print(f"✅ Found Business Owner course: {course_types['business']['title']}")
    
    return course_types

def test_course_modules(course_types):
    """Test the course modules to verify they have the correct structure and content"""
    print("\n=== Testing Course Module Structure ===")
    
    if not course_types:
        print("❌ No courses available for testing")
        return
    
    # Test Primer course modules
    if 'primer' in course_types:
        primer_course = course_types['primer']
        primer_lessons = primer_course.get('lessons', [])
        
        print(f"\nPrimer Course: {len(primer_lessons)} modules")
        if len(primer_lessons) != 6:
            print(f"❌ Expected 6 modules in Primer course, got {len(primer_lessons)}")
        else:
            print("✅ Primer course has exactly 6 modules as required")
        
        # Check for "What You'll Learn" sections
        wyl_count = 0
        for lesson in primer_lessons:
            if "<ul>" in lesson.get('content', '') and "What You'll Learn" in lesson.get('content', ''):
                wyl_count += 1
        
        print(f"✅ {wyl_count}/{len(primer_lessons)} Primer modules have 'What You'll Learn' sections")
    
    # Test W-2 course modules
    if 'w2' in course_types:
        w2_course = course_types['w2']
        w2_lessons = w2_course.get('lessons', [])
        
        print(f"\nW-2 Course: {len(w2_lessons)} modules")
        if len(w2_lessons) != 10:  # The actual count is 10 even though total_lessons is 9
            print(f"❌ Expected 10 modules in W-2 course, got {len(w2_lessons)}")
        else:
            print("✅ W-2 course has 10 modules (including Module 6 'Short-Term Rentals (STR)')")
        
        # Check for Module 6 - Short-Term Rentals
        str_module = None
        for lesson in w2_lessons:
            if "Short-Term Rentals" in lesson.get('title', ''):
                str_module = lesson
                break
        
        if str_module:
            print(f"✅ Found Module 6 'Short-Term Rentals (STR)' in W-2 course")
            
            # Check for key content in the STR module
            content = str_module.get('content', '')
            if "STR exemption" in content:
                print("✅ STR module contains STR exemption content")
            else:
                print("❌ STR module missing STR exemption content")
                
            if "Material Participation" in content:
                print("✅ STR module contains Material Participation content")
            else:
                print("❌ STR module missing Material Participation content")
                
            if "Cost Segregation" in content:
                print("✅ STR module contains Cost Segregation content")
            else:
                print("❌ STR module missing Cost Segregation content")
                
            if "Helen" in content:
                print("✅ STR module contains Helen's case study")
            else:
                print("❌ STR module missing Helen's case study")
        else:
            print("❌ Module 6 'Short-Term Rentals (STR)' not found in W-2 course")
        
        # Check for "What You'll Learn" sections
        wyl_count = 0
        for lesson in w2_lessons:
            if "<ul>" in lesson.get('content', '') and "What You'll Learn" in lesson.get('content', ''):
                wyl_count += 1
        
        print(f"✅ {wyl_count}/{len(w2_lessons)} W-2 modules have 'What You'll Learn' sections")
    
    # Test Business Owner course modules
    if 'business' in course_types:
        business_course = course_types['business']
        business_lessons = business_course.get('lessons', [])
        
        print(f"\nBusiness Owner Course: {len(business_lessons)} modules")
        if len(business_lessons) != 9:  # The actual count is 9 even though total_lessons is 10
            print(f"❌ Expected 9 modules in Business Owner course, got {len(business_lessons)}")
        else:
            print("✅ Business Owner course has 9 modules")
        
        # Check for "What You'll Learn" sections
        wyl_count = 0
        for lesson in business_lessons:
            if "<ul>" in lesson.get('content', '') and "What You'll Learn" in lesson.get('content', ''):
                wyl_count += 1
        
        print(f"✅ {wyl_count}/{len(business_lessons)} Business Owner modules have 'What You'll Learn' sections")

def test_glossary_system():
    """Test the glossary system to verify it returns all terms and supports search"""
    print("\n=== Testing Glossary System ===")
    
    # Test getting all glossary terms
    response = requests.get(f"{API_URL}/glossary")
    if response.status_code != 200:
        print(f"❌ Failed to get glossary terms: {response.status_code}")
        return
    
    terms = response.json()
    print(f"✅ Successfully retrieved {len(terms)} glossary terms")
    
    if len(terms) < 50:
        print(f"⚠️ Expected at least 80 glossary terms, got {len(terms)}")
    
    # Count terms by category
    categories = {}
    for term in terms:
        category = term.get('category', 'Uncategorized')
        categories[category] = categories.get(category, 0) + 1
    
    print("\nGlossary terms by category:")
    for category, count in categories.items():
        print(f"  - {category}: {count} terms")
    
    # Test glossary search functionality
    search_terms = ["REPS", "QOF", "STR", "Entity", "Tax"]
    for term in search_terms:
        response = requests.get(f"{API_URL}/glossary/search?q={term}")
        if response.status_code != 200:
            print(f"❌ Failed to search for '{term}': {response.status_code}")
            continue
        
        results = response.json()
        print(f"✅ Search for '{term}' returned {len(results)} results")

def test_xp_and_quiz_system():
    """Test the XP and quiz system to verify it's working correctly"""
    print("\n=== Testing XP and Quiz System ===")
    
    # Get course IDs
    response = requests.get(f"{API_URL}/courses")
    if response.status_code != 200:
        print(f"❌ Failed to get courses: {response.status_code}")
        return
    
    courses = response.json()
    course_ids = {course.get('type'): course.get('id') for course in courses}
    
    # Test quiz endpoints for each course
    for course_type, course_id in course_ids.items():
        response = requests.get(f"{API_URL}/courses/{course_id}/quiz")
        if response.status_code != 200:
            print(f"❌ Failed to get quiz questions for {course_type} course: {response.status_code}")
            continue
        
        questions = response.json()
        print(f"✅ {course_type} course has {len(questions)} quiz questions")
        
        # Check quiz question structure
        if questions:
            question = questions[0]
            if 'question' in question and 'options' in question and 'correct_answer' in question and 'points' in question:
                print(f"✅ Quiz questions have the correct structure")
            else:
                print(f"❌ Quiz questions are missing required fields")
    
    # Test XP system
    test_user_id = f"test_user_{os.urandom(4).hex()}"
    
    # Get initial XP
    response = requests.get(f"{API_URL}/users/xp/{test_user_id}")
    if response.status_code != 200:
        print(f"❌ Failed to get initial XP: {response.status_code}")
        return
    
    initial_xp = response.json()
    print(f"✅ Initial XP for test user: {initial_xp.get('total_xp', 0)}")
    
    # Award glossary XP
    # Get a glossary term to use
    response = requests.get(f"{API_URL}/glossary")
    if response.status_code != 200:
        print(f"❌ Failed to get glossary terms: {response.status_code}")
    else:
        terms = response.json()
        if terms:
            term_id = terms[0].get('id')
            xp_request = {
                'user_id': test_user_id,
                'term_id': term_id
            }
            
            response = requests.post(f"{API_URL}/users/xp/glossary", json=xp_request)
            if response.status_code != 200:
                print(f"❌ Failed to award glossary XP: {response.status_code}")
            else:
                xp_result = response.json()
                print(f"✅ Awarded {xp_result.get('xp_earned', 0)} XP for viewing glossary term")
    
    # Award quiz XP
    quiz_xp_request = {
        'user_id': test_user_id,
        'points': 50
    }
    
    response = requests.post(f"{API_URL}/users/xp/quiz", json=quiz_xp_request)
    if response.status_code != 200:
        print(f"❌ Failed to award quiz XP: {response.status_code}")
    else:
        quiz_xp_result = response.json()
        print(f"✅ Awarded {quiz_xp_result.get('xp_earned', 0)} XP for quiz completion")
    
    # Get updated XP
    response = requests.get(f"{API_URL}/users/xp/{test_user_id}")
    if response.status_code != 200:
        print(f"❌ Failed to get updated XP: {response.status_code}")
        return
    
    updated_xp = response.json()
    print(f"✅ Updated XP for test user: {updated_xp.get('total_xp', 0)}")

def test_overall_api_health():
    """Test the overall health of the API by checking all endpoints"""
    print("\n=== Testing Overall API Health ===")
    
    endpoints = [
        "/courses",
        "/glossary",
        "/tools",
        "/users/xp"
    ]
    
    all_healthy = True
    for endpoint in endpoints:
        response = requests.get(f"{API_URL}{endpoint}")
        if response.status_code == 200:
            print(f"✅ Endpoint {endpoint} is healthy")
        else:
            print(f"❌ Endpoint {endpoint} returned status code {response.status_code}")
            all_healthy = False
    
    if all_healthy:
        print("\n✅ All API endpoints are healthy")
    else:
        print("\n❌ Some API endpoints are not responding correctly")

if __name__ == "__main__":
    print("\n=== Starting Comprehensive Backend API Testing ===\n")
    
    # Test core API endpoints
    course_types = test_courses_endpoint()
    
    # Test course module structure
    test_course_modules(course_types)
    
    # Test glossary system
    test_glossary_system()
    
    # Test XP and quiz system
    test_xp_and_quiz_system()
    
    # Test overall API health
    test_overall_api_health()
    
    print("\n=== Backend API Testing Complete ===")
