import requests
import json

def get_module_content(course_id, module_id):
    """Get the full content of a specific module"""
    # Get the course lessons
    response = requests.get(f"http://localhost:8001/api/courses/{course_id}/lessons")
    if response.status_code != 200:
        print(f"Error fetching lessons for course {course_id}: {response.status_code}")
        return None
    
    lessons = response.json()
    
    # Find the specific module
    module_content = None
    for lesson in lessons:
        if lesson["id"] == module_id:
            module_content = lesson
            break
    
    if not module_content:
        print(f"Module ID {module_id} not found in course {course_id}")
        return None
    
    return module_content

def verify_formatting():
    """Verify that the module formatting has been applied"""
    # Sample modules to check (one from each course)
    modules_to_check = [
        {
            "course_id": "a09bef85-39e5-4950-8cd3-0df6a44bfbc9",  # The Escape Blueprint
            "module_id": "af9ec455-9299-490e-943b-42e98b2d43f4",  # First module
            "course_name": "The Escape Blueprint"
        },
        {
            "course_id": "2d0238fd-a2be-4446-a2f0-377b5ac75e31",  # W-2 Escape Plan
            "module_id": "e057e456-40fc-448e-841b-bc292ded7154",  # First module
            "course_name": "W-2 Escape Plan"
        },
        {
            "course_id": "b3b18fd1-d549-4e4d-ab71-c280a9ab2670",  # Business Owner Escape Plan
            "module_id": "4e672ed4-dd6c-4373-aa8b-2c9ae6aa6bfe",  # First module
            "course_name": "Business Owner Escape Plan"
        }
    ]
    
    for module_info in modules_to_check:
        print(f"\nChecking module from {module_info['course_name']}...")
        
        module = get_module_content(module_info["course_id"], module_info["module_id"])
        
        if module:
            # Check if the content has been formatted
            content = module["content"]
            
            # Check for proper HTML formatting in the "What You'll Learn" section
            if "## What You'll Learn" in content and "<ul>" in content and "</ul>" in content:
                print(f"✅ Module {module_info['module_id']} has proper HTML formatting")
                
                # Print a snippet of the formatted content
                start_index = content.find("## What You'll Learn")
                end_index = content.find("##", start_index + 1) if content.find("##", start_index + 1) > 0 else len(content)
                snippet = content[start_index:end_index].strip()
                
                print("\nFormatted content snippet:")
                print("-" * 80)
                print(snippet)
                print("-" * 80)
            else:
                print(f"❌ Module {module_info['module_id']} does not have proper HTML formatting")
        else:
            print(f"❌ Could not retrieve module {module_info['module_id']}")

if __name__ == "__main__":
    verify_formatting()