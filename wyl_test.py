import requests
import re
import json
from pprint import pprint

# Base URL for API
BASE_URL = "http://localhost:8001/api"

def test_what_youll_learn_sections():
    """
    Test the 'What You'll Learn' sections across all courses to verify they meet requirements:
    1. Strategy-specific (not generic)
    2. Include action verbs
    3. Mention specific tax concepts and glossary terms
    4. Have 4-6 bullets per module
    """
    print("\n=== Testing 'What You'll Learn' Sections ===\n")
    
    # Get all courses
    response = requests.get(f"{BASE_URL}/courses")
    courses = response.json()
    
    # Track statistics
    stats = {
        "total_modules": 0,
        "modules_with_wyl": 0,
        "modules_with_proper_wyl": 0,
        "modules_missing_wyl": 0,
        "by_course": {}
    }
    
    action_verbs = [
        "calculate", "understand", "structure", "apply", "recognize", 
        "identify", "distinguish", "analyze", "verify", "determine", 
        "master", "design", "implement", "create", "develop", "evaluate",
        "extract", "meet", "satisfy", "convert", "combine"
    ]
    
    tax_concepts = [
        "tax treatment", "CPA", "strategist", "core levers", "W-2 profile", 
        "payroll tax", "corporate rates", "personal rates", "REPS", "QOF", 
        "STR", "C-Corp", "MSO", "Cost Segregation", "tax concepts", 
        "glossary terms", "tax strategy", "tax planning", "effective tax rate"
    ]
    
    # Process each course
    for course in courses:
        course_id = course["id"]
        course_title = course["title"]
        print(f"\nCourse: {course_title}")
        
        # Initialize course stats
        stats["by_course"][course_title] = {
            "total_modules": 0,
            "modules_with_wyl": 0,
            "modules_with_proper_wyl": 0,
            "modules_missing_wyl": 0,
            "modules": []
        }
        
        # Get course lessons
        response = requests.get(f"{BASE_URL}/courses/{course_id}/lessons")
        lessons = response.json()
        
        # Process each lesson/module
        for lesson in lessons:
            module_title = lesson["title"]
            module_content = lesson["content"]
            module_order = lesson["order_index"]
            
            stats["total_modules"] += 1
            stats["by_course"][course_title]["total_modules"] += 1
            
            # Check if module has "What You'll Learn" section
            wyl_match = re.search(r'## What You\'ll Learn\s+(.*?)(?=##|\Z)', module_content, re.DOTALL)
            
            if wyl_match:
                wyl_content = wyl_match.group(1).strip()
                bullet_points = [bp.strip() for bp in re.findall(r'•\s+(.*?)$', wyl_content, re.MULTILINE)]
                
                stats["modules_with_wyl"] += 1
                stats["by_course"][course_title]["modules_with_wyl"] += 1
                
                # Check bullet points count
                has_proper_count = 4 <= len(bullet_points) <= 6
                
                # Check for action verbs
                has_action_verbs = all(any(verb.lower() in bp.lower() for verb in action_verbs) for bp in bullet_points)
                
                # Check for tax concepts
                has_tax_concepts = any(any(concept.lower() in bp.lower() for concept in tax_concepts) for bp in bullet_points)
                
                # Check if content is strategy-specific (not generic)
                is_strategy_specific = not all(bp.startswith("Learn") or bp.startswith("Understand") for bp in bullet_points)
                
                # Determine if this is a proper WYL section
                is_proper_wyl = has_proper_count and has_action_verbs and has_tax_concepts and is_strategy_specific
                
                if is_proper_wyl:
                    stats["modules_with_proper_wyl"] += 1
                    stats["by_course"][course_title]["modules_with_proper_wyl"] += 1
                
                # Store module details
                module_info = {
                    "title": module_title,
                    "order_index": module_order,
                    "has_wyl": True,
                    "bullet_count": len(bullet_points),
                    "has_proper_count": has_proper_count,
                    "has_action_verbs": has_action_verbs,
                    "has_tax_concepts": has_tax_concepts,
                    "is_strategy_specific": is_strategy_specific,
                    "is_proper_wyl": is_proper_wyl,
                    "bullet_points": bullet_points
                }
                
                # Check for specific required content in certain modules
                if course_title == "The Escape Blueprint" and module_order == 1:
                    # Primer Module 1 should mention "3 tax treatment categories" and "CPA vs strategist"
                    has_tax_categories = any("3 tax treatment categories" in bp.lower() for bp in bullet_points)
                    has_cpa_vs_strategist = any("cpa" in bp.lower() and "strategist" in bp.lower() for bp in bullet_points)
                    module_info["has_required_content"] = has_tax_categories and has_cpa_vs_strategist
                    
                elif course_title == "The Escape Blueprint" and module_order == 2:
                    # Primer Module 2 should mention "6 core levers" and specific strategies
                    has_core_levers = any("6 core levers" in bp.lower() for bp in bullet_points)
                    has_specific_strategies = any("entity" in bp.lower() or "deduction" in bp.lower() or "exit" in bp.lower() for bp in bullet_points)
                    module_info["has_required_content"] = has_core_levers and has_specific_strategies
                    
                elif course_title == "W-2 Escape Plan" and module_order == 1:
                    # W-2 Module 1 should mention "15.3% payroll tax exposure" and "W-2 profile mapping"
                    has_payroll_tax = any("15.3%" in bp.lower() and "payroll tax" in bp.lower() for bp in bullet_points)
                    has_profile_mapping = any("w-2 profile" in bp.lower() for bp in bullet_points)
                    module_info["has_required_content"] = has_payroll_tax and has_profile_mapping
                    
                elif course_title == "Business Owner Escape Plan" and module_order == 1:
                    # Business Owner Module 1 should mention "21% corporate rates vs 37% personal rates"
                    has_rate_comparison = any("21%" in bp.lower() and "37%" in bp.lower() for bp in bullet_points)
                    module_info["has_required_content"] = has_rate_comparison
                
            else:
                stats["modules_missing_wyl"] += 1
                stats["by_course"][course_title]["modules_missing_wyl"] += 1
                
                # Store module details
                module_info = {
                    "title": module_title,
                    "order_index": module_order,
                    "has_wyl": False
                }
            
            stats["by_course"][course_title]["modules"].append(module_info)
            
            # Print module results
            print(f"  Module {module_order}: {module_title}")
            print(f"    Has 'What You'll Learn' section: {module_info.get('has_wyl', False)}")
            if module_info.get('has_wyl', False):
                print(f"    Bullet points: {module_info.get('bullet_count', 0)}")
                print(f"    Has proper count (4-6): {module_info.get('has_proper_count', False)}")
                print(f"    Has action verbs: {module_info.get('has_action_verbs', False)}")
                print(f"    Has tax concepts: {module_info.get('has_tax_concepts', False)}")
                print(f"    Is strategy-specific: {module_info.get('is_strategy_specific', False)}")
                print(f"    Is proper WYL section: {module_info.get('is_proper_wyl', False)}")
                if "has_required_content" in module_info:
                    print(f"    Has required specific content: {module_info.get('has_required_content', False)}")
                print(f"    Bullet points:")
                for bp in module_info.get('bullet_points', []):
                    print(f"      • {bp}")
    
    # Print summary statistics
    print("\n=== Summary Statistics ===")
    print(f"Total modules across all courses: {stats['total_modules']}")
    print(f"Modules with 'What You'll Learn' sections: {stats['modules_with_wyl']} ({stats['modules_with_wyl']/stats['total_modules']*100:.1f}%)")
    print(f"Modules with proper 'What You'll Learn' sections: {stats['modules_with_proper_wyl']} ({stats['modules_with_proper_wyl']/stats['total_modules']*100:.1f}%)")
    print(f"Modules missing 'What You'll Learn' sections: {stats['modules_missing_wyl']} ({stats['modules_missing_wyl']/stats['total_modules']*100:.1f}%)")
    
    print("\nBy Course:")
    for course_title, course_stats in stats["by_course"].items():
        print(f"\n{course_title}:")
        print(f"  Total modules: {course_stats['total_modules']}")
        print(f"  Modules with 'What You'll Learn' sections: {course_stats['modules_with_wyl']} ({course_stats['modules_with_wyl']/course_stats['total_modules']*100:.1f}%)")
        print(f"  Modules with proper 'What You'll Learn' sections: {course_stats['modules_with_proper_wyl']} ({course_stats['modules_with_proper_wyl']/course_stats['total_modules']*100:.1f}%)")
        print(f"  Modules missing 'What You'll Learn' sections: {course_stats['modules_missing_wyl']} ({course_stats['modules_missing_wyl']/course_stats['total_modules']*100:.1f}%)")
    
    # Check for glossary term integration
    print("\n=== Checking Glossary Term Integration ===")
    response = requests.get(f"{BASE_URL}/glossary")
    glossary_terms = response.json()
    
    # Extract term names
    term_names = [term["term"] for term in glossary_terms]
    
    # Check for specific required terms
    required_terms = ["REPS", "QOF", "STR", "C-Corp MSO", "Cost Segregation"]
    found_terms = [term for term in required_terms if term in term_names]
    missing_terms = [term for term in required_terms if term not in term_names]
    
    print(f"Required glossary terms found: {len(found_terms)}/{len(required_terms)}")
    print(f"Found terms: {', '.join(found_terms)}")
    if missing_terms:
        print(f"Missing terms: {', '.join(missing_terms)}")
    
    # Check for term integration in WYL sections
    modules_with_glossary_terms = 0
    for course_title, course_stats in stats["by_course"].items():
        for module in course_stats["modules"]:
            if module.get("has_wyl", False):
                has_glossary_term = False
                for bp in module.get("bullet_points", []):
                    for term in term_names:
                        if term.lower() in bp.lower():
                            has_glossary_term = True
                            break
                    if has_glossary_term:
                        break
                
                if has_glossary_term:
                    modules_with_glossary_terms += 1
    
    print(f"Modules with 'What You'll Learn' sections that include glossary terms: {modules_with_glossary_terms}/{stats['modules_with_wyl']} ({modules_with_glossary_terms/stats['modules_with_wyl']*100:.1f}%)")
    
    return stats

if __name__ == "__main__":
    test_what_youll_learn_sections()