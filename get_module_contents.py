import requests
import json
import os

def get_module_content(module_id):
    """Get the full content of a specific module"""
    # First, find the module in our all_modules.json file
    with open("all_modules.json", "r") as f:
        all_modules = json.load(f)
    
    # Find the course that contains this module
    course_id = None
    for module in all_modules:
        if module["module_id"] == module_id:
            course_id = module["course_id"]
            break
    
    if not course_id:
        print(f"Module ID {module_id} not found in all_modules.json")
        return None
    
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

def get_module_details(module_id):
    """Get module details including course information"""
    with open("all_modules.json", "r") as f:
        all_modules = json.load(f)
    
    for module in all_modules:
        if module["module_id"] == module_id:
            return module
    
    return None

def save_module_content(module_id, output_dir="module_contents"):
    """Save the full content of a module to a file"""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get module details
    module_details = get_module_details(module_id)
    if not module_details:
        print(f"Module details not found for {module_id}")
        return
    
    # Get full module content
    module_content = get_module_content(module_id)
    if not module_content:
        print(f"Module content not found for {module_id}")
        return
    
    # Create a filename based on course type and module order
    filename = f"{module_details['course_type']}_{module_details['order_index']:02d}_{module_id}.json"
    filepath = os.path.join(output_dir, filename)
    
    # Save the full module content to a file
    with open(filepath, "w") as f:
        json.dump(module_content, f, indent=2)
    
    print(f"Saved module content to {filepath}")
    
    return filepath

def get_all_module_contents():
    """Get and save the content of all modules"""
    with open("all_modules.json", "r") as f:
        all_modules = json.load(f)
    
    # Create a directory to store all module contents
    output_dir = "module_contents"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save a summary file with basic module info
    summary_file = os.path.join(output_dir, "modules_summary.md")
    
    with open(summary_file, "w") as f:
        f.write("# IRS Escape Plan Modules Summary\n\n")
        
        # Group modules by course
        courses = {}
        for module in all_modules:
            course_id = module["course_id"]
            if course_id not in courses:
                courses[course_id] = {
                    "name": module["course_name"],
                    "type": module["course_type"],
                    "modules": []
                }
            courses[course_id]["modules"].append(module)
        
        # Sort modules by order_index within each course
        for course_id, course in courses.items():
            course["modules"].sort(key=lambda m: m["order_index"])
        
        # Write summary for each course
        for course_id, course in courses.items():
            f.write(f"## {course['name']} (Type: {course['type']})\n\n")
            f.write("| Module ID | Order | Title | Content Preview |\n")
            f.write("|-----------|-------|-------|----------------|\n")
            
            for module in course["modules"]:
                preview = module["content_preview"][:100] + "..." if len(module["content_preview"]) > 100 else module["content_preview"]
                f.write(f"| {module['module_id']} | {module['order_index']} | {module['title']} | {preview} |\n")
            
            f.write("\n")
    
    print(f"Created modules summary at {summary_file}")
    
    # Save each module's full content
    saved_files = []
    for module in all_modules:
        filepath = save_module_content(module["module_id"], output_dir)
        if filepath:
            saved_files.append(filepath)
    
    print(f"Saved {len(saved_files)} module content files to {output_dir}/")
    return saved_files

if __name__ == "__main__":
    get_all_module_contents()