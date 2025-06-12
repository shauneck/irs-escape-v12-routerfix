import json
import os
import requests
import re

def update_module_content(module_id, new_content):
    """Update the content of a specific module"""
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
        return False
    
    # Prepare the update data
    update_data = {
        "content": new_content
    }
    
    # Update the module
    response = requests.put(
        f"http://localhost:8001/api/courses/{course_id}/lessons/{module_id}",
        json=update_data
    )
    
    if response.status_code == 200:
        print(f"Successfully updated module {module_id}")
        return True
    else:
        print(f"Error updating module {module_id}: {response.status_code}")
        print(response.text)
        return False

def format_what_youll_learn_section(content):
    """Format the 'What You'll Learn' section with clean HTML"""
    # Check if the section exists
    if "## What You'll Learn" not in content:
        return content
    
    # Extract the section
    pattern = r"## What You'll Learn\s*\n(.*?)(?=\n##|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return content
    
    section_content = match.group(1).strip()
    
    # Check if it's already in <ul> format
    if "<ul>" in section_content and "</ul>" in section_content:
        # It's already formatted, just ensure consistent styling
        formatted_section = section_content
    else:
        # Convert bullet points or other formats to <ul> format
        items = []
        
        # Try to match different bullet point styles
        bullet_patterns = [
            r"[-•*]\s*(.*?)(?=\n[-•*]|\Z)",  # Markdown style bullets
            r"\d+\.\s*(.*?)(?=\n\d+\.|\Z)",  # Numbered lists
            r"✅\s*(.*?)(?=\n✅|\Z)",         # Checkmark bullets
        ]
        
        for pattern in bullet_patterns:
            matches = re.findall(pattern, section_content, re.DOTALL)
            if matches:
                items.extend(matches)
                break
        
        # If no bullet points found, split by newlines and filter empty lines
        if not items:
            items = [line.strip() for line in section_content.split('\n') if line.strip()]
        
        # Format as HTML list
        formatted_items = []
        for item in items:
            # If the item already has <strong> tags, keep them
            if "<strong>" in item and "</strong>" in item:
                formatted_items.append(f"  <li>{item.strip()}</li>")
            else:
                formatted_items.append(f"  <li><strong>{item.strip()}</strong></li>")
        
        formatted_section = "<ul>\n" + "\n".join(formatted_items) + "\n</ul>"
    
    # Replace the original section with the formatted one
    new_content = re.sub(
        r"## What You'll Learn\s*\n(.*?)(?=\n##|\Z)",
        f"## What You'll Learn\n\n{formatted_section}\n\n",
        content,
        flags=re.DOTALL
    )
    
    return new_content

def format_module_content(content):
    """Format the entire module content with clean HTML"""
    # Format the "What You'll Learn" section
    content = format_what_youll_learn_section(content)
    
    # Ensure proper spacing between sections
    content = re.sub(r'(##\s+[^\n]+)\n([^\n])', r'\1\n\n\2', content)
    
    # Ensure proper spacing after lists
    content = re.sub(r'(</ul>)\n([^\n])', r'\1\n\n\2', content)
    
    # Ensure proper spacing before lists
    content = re.sub(r'([^\n])\n(<ul>)', r'\1\n\n\2', content)
    
    # Format bullet points consistently
    content = re.sub(r'\n\s*[-•*]\s+', r'\n• ', content)
    
    # Ensure proper spacing for bullet points
    content = re.sub(r'(•\s+[^\n]+)\n([^\n•])', r'\1\n\n\2', content)
    
    return content

def process_all_modules():
    """Process and update all modules with improved formatting"""
    # Get all module files
    module_dir = "module_contents"
    module_files = [f for f in os.listdir(module_dir) if f.endswith(".json")]
    
    updated_count = 0
    
    for filename in module_files:
        filepath = os.path.join(module_dir, filename)
        
        # Load the module content
        with open(filepath, "r") as f:
            module_data = json.load(f)
        
        module_id = module_data["id"]
        original_content = module_data["content"]
        
        # Format the content
        formatted_content = format_module_content(original_content)
        
        # Save the formatted content to a new file for review
        formatted_filepath = os.path.join(module_dir, f"formatted_{filename}")
        with open(formatted_filepath, "w") as f:
            json.dump({"id": module_id, "content": formatted_content}, f, indent=2)
        
        print(f"Formatted content saved to {formatted_filepath} for review")
        
        # Update the module with the formatted content
        if update_module_content(module_id, formatted_content):
            updated_count += 1
    
    print(f"Updated {updated_count} out of {len(module_files)} modules")

if __name__ == "__main__":
    process_all_modules()