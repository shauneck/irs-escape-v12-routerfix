import json
import os
import re
from pymongo import MongoClient
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

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

async def update_module_in_db(mongo_url, module_id, new_content):
    """Update a module's content directly in the MongoDB database"""
    client = AsyncIOMotorClient(mongo_url)
    db = client.test_database
    
    # Find the course that contains this module
    courses = await db.courses.find().to_list(1000)
    
    for course in courses:
        for i, lesson in enumerate(course.get("lessons", [])):
            if lesson.get("id") == module_id:
                # Update the lesson content
                course["lessons"][i]["content"] = new_content
                
                # Update the course in the database
                result = await db.courses.update_one(
                    {"id": course["id"]},
                    {"$set": {"lessons": course["lessons"]}}
                )
                
                if result.modified_count > 0:
                    print(f"Successfully updated module {module_id} in course {course['title']}")
                    return True
                else:
                    print(f"Module {module_id} found but update failed")
                    return False
    
    print(f"Module {module_id} not found in any course")
    return False

async def process_all_modules():
    """Process and update all modules with improved formatting"""
    # MongoDB connection string from environment variable
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    
    # Get all module files
    module_dir = "module_contents"
    module_files = [f for f in os.listdir(module_dir) if f.endswith(".json") and not f.startswith("formatted_")]
    
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
        
        # Update the module in the database
        if await update_module_in_db(mongo_url, module_id, formatted_content):
            updated_count += 1
    
    print(f"Updated {updated_count} out of {len(module_files)} modules")

if __name__ == "__main__":
    asyncio.run(process_all_modules())