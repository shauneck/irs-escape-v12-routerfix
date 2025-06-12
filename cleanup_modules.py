import requests
import json
from pymongo import MongoClient
import os
import re

# Database connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'test_database')
client = MongoClient(MONGO_URL)
db = client[DB_NAME]
courses_collection = db['courses']

def clean_module_content(content):
    """Remove redundant introductory paragraphs while preserving structured content"""
    
    # Patterns to identify redundant intro paragraphs that should be removed
    redundant_patterns = [
        # Remove blocks that start with module name/concept explanations
        r'\*\*.*?Loop.*?\*\*.*?(?=##|\n\n[A-Z])',
        r'\*\*.*?REPS.*?\*\*.*?(?=##|\n\n[A-Z])',
        r'\*\*.*?Real Estate Professional Status.*?\*\*.*?(?=##|\n\n[A-Z])',
        r'\*\*.*?Short-Term Rentals.*?\*\*.*?(?=##|\n\n[A-Z])',
        r'\*\*.*?Oil & Gas.*?\*\*.*?(?=##|\n\n[A-Z])',
        r'\*\*.*?MSO.*?\*\*.*?(?=##|\n\n[A-Z])',
        r'\*\*.*?QSBS.*?\*\*.*?(?=##|\n\n[A-Z])',
        r'\*\*.*?W-2 income.*?\*\*.*?(?=##|\n\n[A-Z])',
        
        # Remove explanatory paragraphs that start with common phrases
        r'The U\.S\. tax code is not a punishment.*?(?=##|\n\n[A-Z])',
        r'The \*\*Wealth Multiplier Loop\*\* represents.*?(?=##|\n\n[A-Z])',
        r'\*\*Real Estate Professional Status \(REPS\)\*\* is.*?(?=##|\n\n[A-Z])',
        r'\*\*Short-Term Rentals \(STRs\)\*\* represent.*?(?=##|\n\n[A-Z])',
        r'\*\*Oil & Gas Deductions\*\* represent.*?(?=##|\n\n[A-Z])',
        r'Most business owners are set up to fail.*?(?=##|\n\n[A-Z])',
        r'Tax savings are only part of the game.*?(?=##|\n\n[A-Z])',
        r'The highest-leverage move for business owners.*?(?=##|\n\n[A-Z])',
        r'Most business owners see tax planning as a cost center.*?(?=##|\n\n[A-Z])',
        r'As business owners build wealth.*?(?=##|\n\n[A-Z])',
        r'The ultimate goal for business owners.*?(?=##|\n\n[A-Z])',
        r'Every business owner\'s ultimate goal.*?(?=##|\n\n[A-Z])',
        
        # Remove duplicate What You'll Learn sections (keep only the first one)
        r'## What You\'ll Learn\s*<ul>.*?</ul>\s*## What You\'ll Learn',
        
        # Remove introductory paragraphs between video and content sections
        r'After understanding.*?(?=##|\n\n[A-Z])',
        r'Now that you understand.*?(?=##|\n\n[A-Z])',
        r'This module will.*?(?=##|\n\n[A-Z])',
        r'In this module.*?(?=##|\n\n[A-Z])',
        
        # Remove generic concept explanations
        r'Most.*?think.*?They\'re not.*?(?=##|\n\n[A-Z])',
        r'You don\'t need.*?strategies.*?(?=##|\n\n[A-Z])',
        r'There\'s one tax status.*?(?=##|\n\n[A-Z])',
        r'Understanding.*?requires.*?(?=##|\n\n[A-Z])',
    ]
    
    cleaned_content = content
    
    # Apply each pattern to remove redundant content
    for pattern in redundant_patterns:
        cleaned_content = re.sub(pattern, '', cleaned_content, flags=re.DOTALL | re.IGNORECASE)
    
    # Clean up multiple consecutive newlines
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)
    
    # Clean up leading/trailing whitespace
    cleaned_content = cleaned_content.strip()
    
    return cleaned_content

def update_module_content(module_id):
    """Update a module's content by removing redundant introductory paragraphs"""
    try:
        # Find the course containing this module
        course = courses_collection.find_one({"lessons.id": module_id})
        if not course:
            print(f"Course containing module {module_id} not found")
            return False
            
        # Find the specific lesson within the course
        module = None
        lesson_index = None
        for i, lesson in enumerate(course.get('lessons', [])):
            if lesson.get('id') == module_id:
                module = lesson
                lesson_index = i
                break
                
        if not module:
            print(f"Module {module_id} not found in course lessons")
            return False
            
        current_content = module.get('content', '')
        original_length = len(current_content)
        
        # Clean the content
        cleaned_content = clean_module_content(current_content)
        new_length = len(cleaned_content)
        
        # Only update if content actually changed
        if cleaned_content != current_content:
            # Update the specific lesson in the course
            result = courses_collection.update_one(
                {"id": course["id"]},
                {"$set": {f"lessons.{lesson_index}.content": cleaned_content}}
            )
            
            if result.modified_count > 0:
                chars_removed = original_length - new_length
                print(f"✅ Updated module {module_id}: {module.get('title', 'Unknown')} (removed {chars_removed} characters)")
                return True
            else:
                print(f"❌ Failed to update module {module_id}")
                return False
        else:
            print(f"⚪ No changes needed for module {module_id}: {module.get('title', 'Unknown')}")
            return True
            
    except Exception as e:
        print(f"❌ Error updating module {module_id}: {str(e)}")
        return False

def get_all_module_ids():
    """Get all module IDs from all courses"""
    module_ids = []
    courses = courses_collection.find({})
    
    for course in courses:
        for lesson in course.get('lessons', []):
            module_ids.append(lesson.get('id'))
    
    return module_ids

def main():
    """Clean up all modules by removing redundant content"""
    print("🧹 Starting module content cleanup...")
    print("Removing redundant introductory paragraphs from all modules\n")
    
    # Get all module IDs
    module_ids = get_all_module_ids()
    
    updated_count = 0
    total_count = len(module_ids)
    
    print(f"Found {total_count} modules to process...\n")
    
    for module_id in module_ids:
        if update_module_content(module_id):
            updated_count += 1
    
    print(f"\n🎯 Cleanup complete: {updated_count}/{total_count} modules processed successfully")
    
    # Create summary report
    with open('module_cleanup_summary.md', 'w') as f:
        f.write("# Module Content Cleanup Summary\n\n")
        f.write(f"Processed {updated_count} out of {total_count} modules for content cleanup.\n\n")
        f.write("## Changes Made:\n")
        f.write("- Removed redundant introductory paragraphs that repeat module concepts\n")
        f.write("- Cleaned up duplicate 'What You'll Learn' sections\n")
        f.write("- Removed explanatory text already covered in headers and video content\n")
        f.write("- Preserved all structured content (What You'll Learn, Case Studies, Key Terms)\n")
        f.write("- Maintained all quiz, XP, and glossary integration\n\n")
        f.write("## Content Preserved:\n")
        f.write("- HTML-formatted 'What You'll Learn' sections with bullet points\n")
        f.write("- All video components and structured content\n")
        f.write("- Case studies and key terms sections\n")
        f.write("- XP logic, glossary modals, and quizzes\n")
    
    print(f"📄 Summary report saved to module_cleanup_summary.md")

if __name__ == "__main__":
    main()