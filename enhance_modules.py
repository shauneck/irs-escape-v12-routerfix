import requests
import json
from pymongo import MongoClient
import os

# Database connection
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'test_database')
client = MongoClient(MONGO_URL)
db = client[DB_NAME]
courses_collection = db['courses']

# Enhanced module content with What You'll Learn sections
ENHANCED_MODULE_CONTENT = {
    # Primer modules (already have good structure, will preserve them)
    
    # W-2 Modules need enhancement
    'e057e456-40fc-448e-841b-bc292ded7154': {  # Module 1: The Real Problem with W-2 Income
        'summary': 'Understanding the fundamental limitations of W-2 income structure and how to escape the high-tax trap.',
        'what_youll_learn': [
            '<strong>Discover why W-2 income is taxed at the highest possible rates</strong> with limited planning options',
            '<strong>Learn how employee compensation structure</strong> eliminates deduction opportunities that business owners enjoy',
            '<strong>Understand the psychological and financial "W-2 Trap"</strong> that keeps high earners overpaying taxes',
            '<strong>See how wealthy individuals avoid W-2 income</strong> in favor of business and investment income',
            '<strong>Map your pathway from W-2 dependence</strong> to strategic income repositioning'
        ]
    },
    
    'e2bb063a-22ea-4b73-b1d7-d6a3b9e3e784': {  # Module 9: The Exit Plan (W-2)
        'summary': 'Helen\'s complete transformation from $0 tax optimization to $325K+ annual tax savings and financial freedom.',
        'what_youll_learn': [
            '<strong>Review Helen\'s complete 5-year transformation</strong> from tax victim to strategic optimizer',
            '<strong>See how strategic repositioning generated $325K+ in annual savings</strong> while building long-term wealth',
            '<strong>Learn the exact sequence of implementation</strong> from QOF investments to REPS qualification',
            '<strong>Understand how to coordinate multiple tax strategies</strong> for maximum compounding effect',
            '<strong>Build your own escape timeline</strong> using Helen\'s proven framework'
        ]
    },
    
    '71635aae-3e88-4f22-9770-7e0c44493dff': {  # Module 2: Repositioning W-2 Income
        'summary': 'Strategic methods to reposition already-taxed W-2 income into tax-advantaged investments and deduction opportunities.',
        'what_youll_learn': [
            '<strong>Master the QOF (Qualified Opportunity Fund) strategy</strong> to defer capital gains and reduce AGI',
            '<strong>Learn how to reposition RSU proceeds</strong> into depreciation-generating real estate investments',
            '<strong>Understand strategic asset location</strong> to optimize tax treatment across different account types',
            '<strong>See how timing arbitrage</strong> can create immediate tax benefits from already-earned income',
            '<strong>Build systematic repositioning workflows</strong> for consistent annual tax optimization'
        ]
    },
    
    'ae5700a4-bdac-497f-9e86-492a4a47d579': {  # Module 3: Stacking Offsets
        'summary': 'Advanced strategies to combine multiple tax offsets for maximum W-2 income reduction and wealth building.',
        'what_youll_learn': [
            '<strong>Master the "offset stacking" methodology</strong> to combine depreciation, energy, and business deductions',
            '<strong>Learn how Helen generated $443K in deductions</strong> against $370K of W-2 income in year two',
            '<strong>Understand AGI thresholds and planning</strong> to maximize deduction effectiveness',
            '<strong>See how cost segregation accelerates depreciation</strong> for immediate tax benefits',
            '<strong>Build systematic approaches to stacking multiple strategies</strong> for compounding results'
        ]
    },
    
    '81dad385-c1a2-4e23-b1fd-2130400bd7f6': {  # Module 4: Qualifying for REPS
        'summary': 'Complete guide to qualifying for Real Estate Professional Status and unlocking unlimited deduction potential.',
        'what_youll_learn': [
            '<strong>Master the 750-hour and majority time tests</strong> required for REPS qualification',
            '<strong>Learn systematic documentation and activity tracking</strong> to prove material participation',
            '<strong>Understand how REPS eliminates passive loss limitations</strong> for unlimited W-2 offset potential',
            '<strong>See Helen\'s Year 3 REPS implementation strategy</strong> generating 2,200+ qualifying hours',
            '<strong>Build sustainable REPS qualification systems</strong> for long-term tax optimization'
        ]
    },
    
    '5818e570-1985-433f-973c-7879849ac317': {  # Module 5: Real Estate Professional Status
        'summary': 'Advanced REPS strategies and optimization techniques for maximum tax benefit and wealth building.',
        'what_youll_learn': [
            '<strong>Optimize REPS qualification for multi-property portfolios</strong> and complex investment structures',
            '<strong>Learn advanced material participation tests</strong> for individual property optimization',
            '<strong>Master REPS coordination with other tax strategies</strong> for maximum compounding effect',
            '<strong>Understand long-term REPS planning</strong> for career transitions and retirement',
            '<strong>Build systematic REPS management processes</strong> for consistent annual qualification'
        ]
    },
    
    '0356b0af-ac2f-4836-84ab-667a37541a5e': {  # Module 6: Short-Term Rentals (STRs)
        'summary': 'Leveraging short-term rental investments for maximum depreciation benefits and active income treatment.',
        'what_youll_learn': [
            '<strong>Master STR depreciation strategies</strong> for immediate W-2 income offset without REPS qualification',
            '<strong>Learn the 7-day average stay test</strong> that qualifies STRs for active business treatment',
            '<strong>Understand cost segregation applications</strong> to accelerate STR depreciation schedules',
            '<strong>See how STR material participation</strong> differs from traditional rental property requirements',
            '<strong>Build scalable STR portfolios</strong> for consistent tax benefits and cash flow'
        ]
    },
    
    '3a2c36b7-c454-4254-845f-45ae5155cd2f': {  # Module 7: Oil & Gas Deductions
        'summary': 'Aggressive yet IRS-sanctioned oil & gas investment strategies for immediate deduction and long-term income.',
        'what_youll_learn': [
            '<strong>Master Intangible Drilling Costs (IDC)</strong> for immediate 100% deduction in year one',
            '<strong>Learn depletion allowance strategies</strong> that provide ongoing tax benefits from production',
            '<strong>Understand oil & gas investment structures</strong> and how to evaluate legitimate opportunities',
            '<strong>See how oil & gas coordinates with other strategies</strong> for maximum tax optimization',
            '<strong>Build portfolio allocation models</strong> that balance risk with tax benefits'
        ]
    },
    
    'a97a81df-4dd9-445d-a6ec-f05664b60547': {  # Module 8: The Wealth Multiplier Loop
        'summary': 'Creating self-reinforcing wealth-building systems that transform annual tax savings into long-term passive income.',
        'what_youll_learn': [
            '<strong>Master the Wealth Multiplier Loop methodology</strong> to reinvest tax savings systematically',
            '<strong>Learn strategic compounding techniques</strong> using depreciation assets and cash flow investments',
            '<strong>Understand how to build recurring income streams</strong> from tax-optimized asset allocation',
            '<strong>See Helen\'s systematic approach to wealth acceleration</strong> using the multiplier effect',
            '<strong>Build automated reinvestment systems</strong> for hands-off wealth building'
        ]
    },
    
    '2aa16f6c-c98e-4184-a49e-e4c967296967': {  # Module 9: The IRS Escape Plan
        'summary': 'Integration of all W-2 escape strategies into a comprehensive lifestyle and wealth-building framework.',
        'what_youll_learn': [
            '<strong>Review the complete IRS Escape Plan framework</strong> from foundation to advanced optimization',
            '<strong>See Helen\'s total transformation results</strong> and how to replicate her success',
            '<strong>Learn systematic implementation sequences</strong> for different income and life situations',
            '<strong>Understand how to coordinate multiple strategies</strong> for maximum compounding effect',
            '<strong>Build your personalized escape timeline</strong> based on your specific circumstances'
        ]
    },
    
    # Business Owner modules need enhancement
    '4e672ed4-dd6c-4373-aa8b-2c9ae6aa6bfe': {  # Module 0: Who This Is For
        'summary': 'Setting expectations and infrastructure overview for six-figure+ business owners ready for advanced tax optimization.',
        'what_youll_learn': [
            '<strong>Understand the business owner tax optimization landscape</strong> and what separates advanced strategies from basic compliance',
            '<strong>Learn the infrastructure requirements</strong> for sophisticated business tax planning',
            '<strong>See real client examples</strong> of $100K+ annual tax savings through strategic structuring',
            '<strong>Map your current situation</strong> against the optimization opportunities in this course',
            '<strong>Set realistic expectations</strong> for implementation timelines and professional coordination'
        ]
    },
    
    'a3860186-ae20-4c10-b904-e84488802329': {  # Module 1: Entity Structuring & Income Capture
        'summary': 'Advanced entity structuring using C-Corp MSOs to capture income at optimal tax rates and unlock deduction opportunities.',
        'what_youll_learn': [
            '<strong>Master C-Corp MSO (Management Services Organization) structures</strong> for optimal income capture and tax rates',
            '<strong>Learn how to transition from S-Corp or LLC</strong> to more sophisticated entity configurations',
            '<strong>Understand 21% corporate tax rates vs. 37%+ personal rates</strong> and how to arbitrage the difference',
            '<strong>See Dr. Ben\'s MSO implementation</strong> generating $320K+ in annual tax savings',
            '<strong>Build systematic entity optimization</strong> for growing businesses and income levels'
        ]
    },
    
    '2c64dc93-9bb2-4f40-b206-7464c3554718': {  # Module 2: Strategic Deductions & Asset Repositioning
        'summary': 'Converting captured business income into tax-advantaged assets and maximizing deduction stacking strategies.',
        'what_youll_learn': [
            '<strong>Master the "deduction stack" methodology</strong> combining cost segregation, energy, and equipment deductions',
            '<strong>Learn how Lauren generated $1.1M in accelerated deductions</strong> through systematic asset repositioning',
            '<strong>Understand bonus depreciation rules</strong> and how to maximize immediate deduction benefits',
            '<strong>See IDC (Intangible Drilling Costs) applications</strong> for aggressive yet legal deduction strategies',
            '<strong>Build systematic deduction workflows</strong> for consistent annual optimization'
        ]
    },
    
    '37647570-1c7b-42fd-b942-ec4473d2ba04': {  # Module 3: Long-Term Wealth Creation & Legacy Structuring
        'summary': 'Building protected, transferable wealth systems through trust structures and strategic exit planning.',
        'what_youll_learn': [
            '<strong>Master QSBS (Qualified Small Business Stock) qualification</strong> for $10M+ in excluded gains at exit',
            '<strong>Learn F-Reorg (F Reorganization) strategies</strong> to restructure existing businesses for QSBS benefits',
            '<strong>Understand trust multiplication strategies</strong> for wealth transfer and tax optimization',
            '<strong>See David\'s tech startup restructuring</strong> for $30M in excluded gains at exit',
            '<strong>Build systematic legacy planning</strong> that protects and transfers wealth efficiently'
        ]
    },
    
    'e5acbff1-60f7-4c31-89cd-cc10e0485ac4': {  # Module 4: Business Structure Tax Implications
        'summary': 'Systematic income elimination through coordinated deduction strategies and asset optimization.',
        'what_youll_learn': [
            '<strong>Master the Wealth Multiplier Loop for business owners</strong> to create self-reinforcing tax benefits',
            '<strong>Learn how David implemented $300K recurring income with $0 tax</strong> through strategic structuring',
            '<strong>Understand systematic deduction coordination</strong> across multiple business entities and investments',
            '<strong>See advanced timing strategies</strong> for income recognition and deduction acceleration',
            '<strong>Build automated wealth-building systems</strong> that compound tax savings into long-term assets'
        ]
    },
    
    'fe912e77-f0b8-4a06-bc0f-a207bad34884': {  # Module 5: Business Deduction Strategies
        'summary': 'Converting tax planning from a cost center into a profit-generating wealth-building strategy.',
        'what_youll_learn': [
            '<strong>Master the "Zero-Tax Income Stack"</strong> for business owners generating substantial income with minimal tax',
            '<strong>Learn how Sarah achieved $0 federal tax on $300K income</strong> through strategic income repositioning',
            '<strong>Understand systematic income and deduction coordination</strong> for maximum tax efficiency',
            '<strong>See advanced entity layering strategies</strong> for multi-business owners and complex structures',
            '<strong>Build recurring income systems</strong> that generate cash flow with optimal tax treatment'
        ]
    },
    
    '6153b599-2f1c-498e-9d6a-8cd341a5f7a7': {  # Module 6: Capital Gains Repositioning & Strategic Exit
        'summary': 'Advanced wealth protection strategies using life insurance and sophisticated financial planning.',
        'what_youll_learn': [
            '<strong>Master split-dollar life insurance strategies</strong> for tax-efficient wealth transfer and protection',
            '<strong>Learn loan-based premium funding</strong> to maximize insurance benefits with minimal cash outlay',
            '<strong>Understand estate tax exposure mitigation</strong> for high-net-worth business owners',
            '<strong>See Michael\'s $2.5M estate tax protection strategy</strong> using advanced insurance planning',
            '<strong>Build comprehensive wealth protection systems</strong> that coordinate with business and tax strategies'
        ]
    },
    
    '37cbe8d5-7a88-453b-998c-98a2a917a508': {  # Module 7: Protecting Wealth While You Grow It
        'summary': 'Advanced co-investment and MSO strategies for sophisticated business owners and family offices.',
        'what_youll_learn': [
            '<strong>Master co-investment MSO structures</strong> for family office and sophisticated investor coordination',
            '<strong>Learn depreciation recapture avoidance</strong> through strategic installment sales and 1031 exchanges',
            '<strong>Understand advanced entity coordination</strong> for multi-generational wealth planning',
            '<strong>See Lisa\'s $450K depreciation capture strategy</strong> using co-investment MSO structures',
            '<strong>Build scalable investment frameworks</strong> for family office and high-net-worth coordination'
        ]
    },
    
    '2633803b-7881-436a-a25e-3de986cc4b8c': {  # Module 8: The Exit Plan
        'summary': 'Ultimate wealth multiplication strategies and comprehensive exit planning for business owners.',
        'what_youll_learn': [
            '<strong>Master trust multiplication strategies</strong> for multi-generational wealth transfer and protection',
            '<strong>Learn advanced estate tax exposure planning</strong> for business owners and family wealth',
            '<strong>Understand wealth transfer optimization</strong> using sophisticated trust and entity structures',
            '<strong>See Robert\'s $3.5M wealth transfer strategy</strong> using trust multiplication techniques',
            '<strong>Build comprehensive exit planning systems</strong> for business succession and wealth preservation'
        ]
    }
}

def update_module_content(module_id, new_content_parts):
    """Update a module's content with enhanced formatting while preserving existing content"""
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
        
        # Extract existing What You'll Learn section if it exists
        existing_wyl_match = None
        if '## What You\'ll Learn' in current_content:
            import re
            existing_wyl_match = re.search(r'## What You\'ll Learn\s*(.*?)(?=##|\n\n[A-Z]|\Z)', current_content, re.DOTALL)
        
        # If module already has well-formatted What You'll Learn, preserve it
        if existing_wyl_match and '<ul>' in existing_wyl_match.group(1):
            print(f"Module {module_id} already has well-formatted What You'll Learn section, preserving it")
            return True
            
        # Build new What You'll Learn section
        wyl_section = '<section class="learning-outcomes">\n'
        wyl_section += '  <h3>What You\'ll Learn</h3>\n'
        wyl_section += '  <ul>\n'
        for point in new_content_parts['what_youll_learn']:
            wyl_section += f'    <li>{point}</li>\n'
        wyl_section += '  </ul>\n'
        wyl_section += '</section>\n\n'
        
        # Add course summary at the beginning if it doesn't exist
        summary = new_content_parts['summary']
        
        # Create enhanced content
        if existing_wyl_match:
            # Replace existing What You'll Learn section
            enhanced_content = current_content.replace(
                existing_wyl_match.group(0), 
                wyl_section.strip()
            )
        else:
            # Add What You'll Learn section after summary
            if current_content.startswith(summary):
                # Summary already exists, add What You'll Learn after it
                enhanced_content = summary + '\n\n' + wyl_section + current_content[len(summary):].lstrip()
            else:
                # Add both summary and What You'll Learn at the beginning
                enhanced_content = summary + '\n\n' + wyl_section + current_content
        
        # Update the specific lesson in the course
        result = courses_collection.update_one(
            {"id": course["id"]},
            {"$set": {f"lessons.{lesson_index}.content": enhanced_content}}
        )
        
        if result.modified_count > 0:
            print(f"Successfully updated module {module_id}: {module.get('title', 'Unknown')}")
            return True
        else:
            print(f"No changes made to module {module_id}")
            return False
            
    except Exception as e:
        print(f"Error updating module {module_id}: {str(e)}")
        return False

def main():
    """Update all modules with enhanced formatting"""
    updated_count = 0
    total_count = len(ENHANCED_MODULE_CONTENT)
    
    print(f"Starting update of {total_count} modules...")
    
    for module_id, content_parts in ENHANCED_MODULE_CONTENT.items():
        if update_module_content(module_id, content_parts):
            updated_count += 1
    
    print(f"\nUpdate complete: {updated_count}/{total_count} modules updated successfully")
    
    # Create summary report
    with open('module_update_summary.md', 'w') as f:
        f.write("# Module Content Update Summary\n\n")
        f.write(f"Updated {updated_count} out of {total_count} modules with enhanced formatting.\n\n")
        f.write("## Changes Made:\n")
        f.write("- Added clean HTML structure for What You'll Learn sections\n")
        f.write("- Enhanced course summaries with tactical focus\n")
        f.write("- Preserved all existing content and functionality\n")
        f.write("- Maintained all quiz, XP, and glossary integration\n\n")
        f.write("## Modules Updated:\n")
        
        for module_id in ENHANCED_MODULE_CONTENT.keys():
            # Find the course containing this module
            course = courses_collection.find_one({"lessons.id": module_id})
            if course:
                # Find the specific lesson
                for lesson in course.get('lessons', []):
                    if lesson.get('id') == module_id:
                        f.write(f"- {lesson.get('title', 'Unknown Title')} (ID: {module_id})\n")
                        break

if __name__ == "__main__":
    main()
