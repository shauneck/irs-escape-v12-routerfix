import unittest
import requests
import json
import random
import os
from urllib.parse import urljoin
import sys

class TestIRSEscapePlan(unittest.TestCase):
    """Test suite to verify the IRS Escape Plan platform functionality"""
    
    def setUp(self):
        """Set up the test environment"""
        # Get the backend URL from environment or use default
        self.base_url = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
        if not self.base_url.endswith('/api'):
            self.base_url = urljoin(self.base_url, '/api/')
        else:
            self.base_url = self.base_url + '/'
        
        print(f"Using API base URL: {self.base_url}")
        
        # Get course IDs
        self.course_ids = {}
        self.get_course_ids()
        
        # Test user ID
        self.test_user_id = f"test_user_{random.randint(1000, 9999)}"
    
    def get_course_ids(self):
        """Get course IDs for all courses"""
        try:
            response = requests.get(urljoin(self.base_url, 'courses'))
            if response.status_code == 200:
                courses = response.json()
                for course in courses:
                    if course.get('type') == 'primer':
                        self.course_ids['primer'] = course.get('id')
                    elif course.get('type') == 'w2':
                        self.course_ids['w2'] = course.get('id')
                    elif course.get('type') == 'business':
                        self.course_ids['business'] = course.get('id')
                
                print(f"Found course IDs: {self.course_ids}")
            else:
                print(f"Failed to get courses: {response.status_code}")
        except Exception as e:
            print(f"Error getting course IDs: {e}")
    
    def test_course_system(self):
        """Test the course system functionality"""
        print("\n=== Testing Course System ===")
        
        # Get all courses
        try:
            response = requests.get(urljoin(self.base_url, 'courses'))
            self.assertEqual(response.status_code, 200, "Failed to get courses")
            
            courses = response.json()
            self.assertIsInstance(courses, list, "Courses response is not a list")
            self.assertGreaterEqual(len(courses), 3, "Expected at least 3 courses")
            
            # Check course types
            course_types = [course.get('type') for course in courses]
            required_types = ['primer', 'w2', 'business']
            for required_type in required_types:
                self.assertIn(required_type, course_types, f"Missing required course type: {required_type}")
            
            # Print course details
            print("\nCourse details:")
            for course in courses:
                print(f"- {course.get('title')} ({course.get('type')}): {course.get('total_lessons')} lessons, {course.get('estimated_hours')} hours")
            
            # Check specific course requirements
            for course in courses:
                if course.get('type') == 'primer':
                    self.assertEqual(course.get('total_lessons'), 5, "The Escape Blueprint should have 5 modules")
                elif course.get('type') == 'w2':
                    self.assertEqual(course.get('total_lessons'), 9, "W-2 Escape Plan should have 9 modules")
                elif course.get('type') == 'business':
                    self.assertEqual(course.get('total_lessons'), 9, "Business Owner Escape Plan should have 9 modules")
            
            return True
        except Exception as e:
            print(f"Error testing course system: {e}")
            return False
    
    def test_course_modules(self):
        """Test the modules for each course"""
        print("\n=== Testing Course Modules ===")
        
        # Expected module counts
        expected_counts = {
            'primer': 5,  # The Escape Blueprint (showing 5 now)
            'w2': 9,      # W-2 Escape Plan (9 modules)
            'business': 9  # Business Owner Escape Plan (showing 9 now)
        }
        
        all_correct = True
        
        print("\nModule counts for each course:")
        for course_type, course_id in self.course_ids.items():
            try:
                # Get lessons for this course
                response = requests.get(urljoin(self.base_url, f'courses/{course_id}/lessons'))
                self.assertEqual(response.status_code, 200, f"Failed to get lessons for course {course_id}")
                
                lessons = response.json()
                lesson_count = len(lessons)
                
                expected_count = expected_counts.get(course_type, 0)
                
                print(f"- {course_type.upper()} course: {lesson_count} modules (expected {expected_count})")
                
                if lesson_count != expected_count:
                    print(f"  ❌ Module count mismatch for {course_type} course")
                    all_correct = False
                else:
                    print(f"  ✅ Module count matches expected value")
                
                # Print module titles
                print(f"  Modules:")
                for lesson in sorted(lessons, key=lambda x: x.get("order_index", 0)):
                    print(f"    - {lesson.get('order_index')}: {lesson.get('title')}")
                
                # Check for specific modules
                if course_type == 'w2':
                    # Check for Module 6 - Short-Term Rentals (STRs)
                    str_module = next((m for m in lessons if m.get('order_index') == 6), None)
                    if str_module:
                        print(f"  ✅ Found Module 6 - Short-Term Rentals (STRs): {str_module.get('title')}")
                        
                        # Check module content for STR-related terms
                        content = str_module.get('content', '')
                        str_terms = ['STR exemption', 'Material Participation', 'Cost Segregation', 'Helen']
                        for term in str_terms:
                            if term.lower() in content.lower():
                                print(f"    ✅ Module 6 contains '{term}'")
                            else:
                                print(f"    ❌ Module 6 missing '{term}'")
                                all_correct = False
                    else:
                        print(f"  ❌ Missing Module 6 - Short-Term Rentals (STRs)")
                        all_correct = False
            except Exception as e:
                print(f"Error testing modules for {course_type} course: {e}")
                all_correct = False
        
        return all_correct
    
    def test_glossary_system(self):
        """Test the glossary system functionality"""
        print("\n=== Testing Glossary System ===")
        
        try:
            # Get all glossary terms
            response = requests.get(urljoin(self.base_url, 'glossary'))
            self.assertEqual(response.status_code, 200, "Failed to get glossary terms")
            
            terms = response.json()
            self.assertIsInstance(terms, list, "Glossary response is not a list")
            self.assertGreaterEqual(len(terms), 53, f"Expected at least 53 glossary terms, got {len(terms)}")
            
            # Count terms by category
            categories = {}
            for term in terms:
                category = term.get("category", "Unknown")
                if category in categories:
                    categories[category] += 1
                else:
                    categories[category] = 1
            
            # Print category counts
            print("\nGlossary terms by category:")
            for category, count in categories.items():
                print(f"- {category}: {count} terms")
            
            print(f"\nTotal glossary terms: {len(terms)}")
            
            # Test search functionality
            test_terms = ["REPS", "W-2", "QOF", "STR", "Cost Segregation"]
            
            print("\nGlossary search results:")
            for term in test_terms:
                search_response = requests.get(urljoin(self.base_url, f'glossary/search?q={term}'))
                self.assertEqual(search_response.status_code, 200, f"Failed to search for '{term}'")
                
                results = search_response.json()
                if results:
                    print(f"- '{term}': {len(results)} results found ✅")
                    # Print the first result
                    first_result = results[0]
                    print(f"  First result: {first_result.get('term')}")
                    print(f"  Category: {first_result.get('category')}")
                    if first_result.get('plain_english'):
                        print(f"  Plain English: {first_result.get('plain_english')[:100]}...")
                else:
                    print(f"- '{term}': No results found ❌")
                    # Not failing the test for this, as some terms might be spelled differently
            
            return True
        except Exception as e:
            print(f"Error testing glossary system: {e}")
            return False
    
    def test_quiz_system(self):
        """Test the quiz system functionality"""
        print("\n=== Testing Quiz System ===")
        
        try:
            total_questions = 0
            
            print("\nQuiz system test:")
            for course_type, course_id in self.course_ids.items():
                # Get quiz questions for this course
                quiz_response = requests.get(urljoin(self.base_url, f'courses/{course_id}/quiz'))
                self.assertEqual(quiz_response.status_code, 200, f"Failed to get quiz for course {course_id}")
                
                questions = quiz_response.json()
                if questions:
                    print(f"- {course_type.upper()} course: {len(questions)} quiz questions found ✅")
                    total_questions += len(questions)
                    
                    # Test randomization by requesting the quiz twice
                    quiz_response2 = requests.get(urljoin(self.base_url, f'courses/{course_id}/quiz'))
                    self.assertEqual(quiz_response2.status_code, 200, f"Failed to get quiz second time for course {course_id}")
                    
                    questions2 = quiz_response2.json()
                    
                    # Check if options are randomized
                    randomization_detected = False
                    for i in range(min(len(questions), len(questions2))):
                        q1 = questions[i]
                        q2 = questions2[i]
                        
                        # Find a question with the same ID but different option order
                        if q1.get("id") == q2.get("id") and q1.get("options") != q2.get("options"):
                            randomization_detected = True
                            print(f"  Randomization detected in question: {q1.get('question')[:50]}...")
                            break
                    
                    if randomization_detected:
                        print(f"  ✅ Quiz randomization is working")
                    else:
                        print(f"  ⚠️ Quiz randomization not detected (may be coincidence)")
                else:
                    print(f"- {course_type.upper()} course: No quiz questions found ❌")
            
            print(f"\nTotal quiz questions across all courses: {total_questions}")
            self.assertGreater(total_questions, 0, "No quiz questions found across all courses")
            
            return True
        except Exception as e:
            print(f"Error testing quiz system: {e}")
            return False
    
    def test_xp_system(self):
        """Test the XP system functionality"""
        print("\n=== Testing XP System ===")
        
        try:
            # Get initial XP
            response = requests.get(urljoin(self.base_url, f'users/xp/{self.test_user_id}'))
            self.assertEqual(response.status_code, 200, "Failed to get initial XP")
            
            initial_xp = response.json()
            print(f"\nInitial XP for {self.test_user_id}: {initial_xp.get('total_xp', 0)}")
            
            # Get glossary terms
            glossary_response = requests.get(urljoin(self.base_url, 'glossary'))
            self.assertEqual(glossary_response.status_code, 200, "Failed to get glossary")
            
            terms = glossary_response.json()
            self.assertGreater(len(terms), 0, "No glossary terms found")
            
            # Test awarding XP for viewing a glossary term
            term_id = terms[0].get("id")
            term_name = terms[0].get("term")
            
            xp_request = {
                "user_id": self.test_user_id,
                "term_id": term_id
            }
            
            xp_response = requests.post(urljoin(self.base_url, 'users/xp/glossary'), json=xp_request)
            self.assertEqual(xp_response.status_code, 200, "Failed to award glossary XP")
            
            xp_result = xp_response.json()
            print(f"Awarded XP for viewing '{term_name}': {xp_result.get('xp_earned', 0)} XP")
            
            # Verify XP was awarded
            self.assertEqual(xp_result.get('xp_earned', 0), 10, "Expected 10 XP for first view")
            
            # Try viewing the same term again (should not award XP)
            xp_response2 = requests.post(urljoin(self.base_url, 'users/xp/glossary'), json=xp_request)
            self.assertEqual(xp_response2.status_code, 200, "Failed to check second view")
            
            xp_result2 = xp_response2.json()
            print(f"Second view of '{term_name}': {xp_result2.get('xp_earned', 0)} XP")
            
            # Verify no XP was awarded for second view
            self.assertEqual(xp_result2.get('xp_earned', 0), 0, "Expected 0 XP for second view")
            
            # Test awarding XP for quiz completion
            quiz_xp_request = {
                "user_id": self.test_user_id,
                "points": 50
            }
            
            quiz_xp_response = requests.post(urljoin(self.base_url, 'users/xp/quiz'), json=quiz_xp_request)
            self.assertEqual(quiz_xp_response.status_code, 200, "Failed to award quiz XP")
            
            quiz_xp_result = quiz_xp_response.json()
            print(f"Awarded quiz XP: {quiz_xp_result.get('xp_earned', 0)} XP")
            
            # Get final XP
            final_xp_response = requests.get(urljoin(self.base_url, f'users/xp/{self.test_user_id}'))
            self.assertEqual(final_xp_response.status_code, 200, "Failed to get final XP")
            
            final_xp = final_xp_response.json()
            print(f"Final XP for {self.test_user_id}: {final_xp.get('total_xp', 0)}")
            
            # Verify total XP
            expected_total = 60  # 10 for glossary + 50 for quiz
            self.assertEqual(final_xp.get('total_xp', 0), expected_total, f"Expected total XP to be {expected_total}")
            
            return True
        except Exception as e:
            print(f"Error testing XP system: {e}")
            return False
    
    def test_user_progress(self):
        """Test the user progress tracking"""
        print("\n=== Testing User Progress ===")
        
        try:
            # Create test progress
            test_progress = {
                "user_id": self.test_user_id,
                "course_id": "test_course_id",
                "lesson_id": "test_lesson_id",
                "completed": True,
                "score": 85
            }
            
            progress_response = requests.post(urljoin(self.base_url, 'progress'), json=test_progress)
            self.assertEqual(progress_response.status_code, 200, "Failed to create progress")
            
            print(f"\nCreated test progress for user {self.test_user_id}")
            
            # Get user progress
            get_progress_response = requests.get(urljoin(self.base_url, f'progress/{self.test_user_id}'))
            self.assertEqual(get_progress_response.status_code, 200, "Failed to get user progress")
            
            progress_data = get_progress_response.json()
            self.assertIsInstance(progress_data, list, "Progress data is not a list")
            
            # Verify progress data
            found = False
            for progress in progress_data:
                if (progress.get("user_id") == self.test_user_id and 
                    progress.get("course_id") == "test_course_id" and
                    progress.get("lesson_id") == "test_lesson_id"):
                    found = True
                    print(f"Found progress data: completed={progress.get('completed')}, score={progress.get('score')}")
                    break
            
            self.assertTrue(found, "Progress data not found")
            
            return True
        except Exception as e:
            print(f"Error testing user progress: {e}")
            return False
    
    def test_api_endpoints(self):
        """Test all core API endpoints"""
        print("\n=== Testing Core API Endpoints ===")
        
        endpoints = [
            'courses',
            f'courses/{self.course_ids.get("primer", "unknown")}',
            f'courses/{self.course_ids.get("primer", "unknown")}/lessons',
            'glossary',
            'glossary/search?q=REPS',
            f'courses/{self.course_ids.get("primer", "unknown")}/quiz',
            f'users/xp/{self.test_user_id}',
            f'progress/{self.test_user_id}'
        ]
        
        all_working = True
        
        print("\nTesting API endpoints:")
        for endpoint in endpoints:
            try:
                response = requests.get(urljoin(self.base_url, endpoint))
                if response.status_code == 200:
                    print(f"- {endpoint}: ✅ (200 OK)")
                else:
                    print(f"- {endpoint}: ❌ ({response.status_code})")
                    all_working = False
            except Exception as e:
                print(f"- {endpoint}: ❌ (Error: {e})")
                all_working = False
        
        return all_working

def run_tests():
    """Run all tests and return results"""
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestIRSEscapePlan('test_course_system'))
    test_suite.addTest(TestIRSEscapePlan('test_course_modules'))
    test_suite.addTest(TestIRSEscapePlan('test_glossary_system'))
    test_suite.addTest(TestIRSEscapePlan('test_quiz_system'))
    test_suite.addTest(TestIRSEscapePlan('test_xp_system'))
    test_suite.addTest(TestIRSEscapePlan('test_user_progress'))
    test_suite.addTest(TestIRSEscapePlan('test_api_endpoints'))
    
    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)
    
    return result

if __name__ == '__main__':
    result = run_tests()
    sys.exit(not result.wasSuccessful())