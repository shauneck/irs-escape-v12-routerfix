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

# Clean module summaries for all 25 modules
MODULE_SUMMARIES = {
    # Primer Modules (6 modules)
    'af9ec455-9299-490e-943b-42e98b2d43f4': {  # Why You're Overpaying the IRS
        'summary': '''Module 1 establishes the fundamental tax mindset shift from reactive compliance to proactive strategy. You'll understand why the IRS system rewards investment and business ownership while penalizing passive employment. This foundation module shows you how CPAs file returns while strategists build wealth-preserving infrastructure that works within the tax code's incentive structure.'''
    },
    'fe110ef3-0fb1-428d-bf7a-587a9ef2fd5d': {  # The 6 Levers
        'summary': '''Module 2 introduces the core framework that controls all tax outcomes: entity type, income type, timing, asset location, deduction strategy, and exit planning. Every tax strategy moving forward pulls on one or more of these levers. This systematic approach replaces the confusion of hundreds of scattered tactics with six strategic categories that actually move the needle on your effective tax rate.'''
    },
    '648215b5-c355-4f69-95e4-f20fc63c777f': {  # Real Tax Case Studies
        'summary': '''Module 3 demonstrates the 6-lever framework in action through real client transformations. You'll see how RSU timing saved a tech executive $91K, how STR depreciation created six-figure deductions, and how entity restructuring eliminated $156K in annual taxes. These case studies show the practical application of strategic tax planning beyond theoretical concepts.'''
    },
    'a155c3a6-ecc6-40c4-9d3d-3d0af178308e': {  # The Tax Status That Changes Everything
        'summary': '''Module 4 focuses on Real Estate Professional Status (REPS) - the designation that transforms passive real estate losses into unlimited deductions against W-2 income. You'll understand the 750-hour test, material participation requirements, and documentation strategies that unlock this powerful tax status for high-income earners seeking aggressive but legal deduction opportunities.'''
    },
    '5a575f62-fa56-40bd-a889-a928a8d0a4cb': {  # Mapping Your Tax Exposure
        'summary': '''Module 5 guides you through a systematic self-assessment of your current tax situation using the 6-lever framework. You'll identify your income types, entity structure gaps, deduction bandwidth, and risk exposure. This mapping process reveals which levers offer the highest impact for your specific situation and creates your personalized optimization roadmap.'''
    },
    'a4123154-2f9a-4915-9ec6-ddd53006f28b': {  # Building Your Custom Escape Plan
        'summary': '''Module 6 synthesizes everything into your personalized implementation timeline. You'll combine the 6 levers, case study insights, and your exposure map into a systematic approach for reducing your effective tax rate by 20-50%+. This module provides the bridge from course completion to real-world execution with clear next steps and advisor integration strategies.'''
    },
    
    # W-2 Modules (10 modules)
    'e057e456-40fc-448e-841b-bc292ded7154': {  # The Real Problem with W-2 Income
        'summary': '''Module 1 exposes why W-2 income faces the highest effective tax rates in the U.S. system. You'll understand how employee compensation structure eliminates deduction opportunities that business owners enjoy daily. This module breaks down the psychological and financial "W-2 trap" that keeps high earners overpaying taxes and shows the strategic pathway to income repositioning.'''
    },
    '71635aae-3e88-4f22-9770-7e0c44493dff': {  # Repositioning W-2 Income
        'summary': '''Module 2 introduces strategic repositioning of already-taxed W-2 income into tax-advantaged investments. You'll master QOF (Qualified Opportunity Fund) strategies to defer capital gains, learn asset location optimization, and discover timing arbitrage techniques. This module shows how to create immediate tax benefits from income you've already earned through strategic reinvestment.'''
    },
    'ae5700a4-bdac-497f-9e86-492a4a47d579': {  # Stacking Offsets
        'summary': '''Module 3 reveals the "offset stacking" methodology that combines multiple tax strategies for maximum W-2 income reduction. You'll see how Helen generated $443K in deductions against $370K of income through strategic coordination of depreciation, energy investments, and cost segregation. This advanced approach creates compounding tax benefits rather than isolated savings.'''
    },
    '81dad385-c1a2-4e23-b1fd-2130400bd7f6': {  # Qualifying for REPS
        'summary': '''Module 4 provides the complete roadmap to qualifying for Real Estate Professional Status and eliminating passive loss limitations. You'll master the 750-hour requirement, majority time test, and systematic documentation strategies. This module shows Helen's Year 3 implementation generating 2,200+ qualifying hours and unlocking unlimited deduction potential against W-2 income.'''
    },
    '5818e570-1985-433f-973c-7879849ac317': {  # Real Estate Professional Status
        'summary': '''Module 5 explores advanced REPS optimization techniques for multi-property portfolios and complex investment structures. You'll understand material participation tests for individual properties, long-term planning strategies, and systematic REPS management. This module transforms REPS from a one-time qualification into a sustainable wealth-building system.'''
    },
    '0356b0af-ac2f-4836-84ab-667a37541a5e': {  # Short-Term Rentals
        'summary': '''Module 6 unlocks Short-Term Rental (STR) strategies for immediate depreciation benefits without REPS qualification. You'll master the 7-day average stay test, cost segregation applications, and material participation requirements specific to STRs. This module provides an accessible entry point for W-2 earners to generate substantial depreciation offsets.'''
    },
    '3a2c36b7-c454-4254-845f-45ae5155cd2f': {  # Oil & Gas Deductions
        'summary': '''Module 7 introduces aggressive yet IRS-sanctioned oil & gas investment strategies. You'll understand Intangible Drilling Costs (IDC) for immediate 100% deductions, depletion allowances for ongoing benefits, and proper investment structure evaluation. This module provides sophisticated deduction opportunities for high-income W-2 earners seeking maximum tax optimization.'''
    },
    'a97a81df-4dd9-445d-a6ec-f05664b60547': {  # The Wealth Multiplier Loop
        'summary': '''Module 8 establishes the systematic wealth-building framework that transforms annual tax savings into long-term passive income. You'll learn strategic compounding techniques, automated reinvestment systems, and the methodology for creating self-reinforcing wealth acceleration. This module shows how tax planning becomes a profit center rather than an expense.'''
    },
    '2aa16f6c-c98e-4184-a49e-e4c967296967': {  # The IRS Escape Plan
        'summary': '''Module 9 integrates all W-2 escape strategies into Helen's complete transformation from $0 tax optimization to $325K+ annual savings. You'll see the systematic implementation sequence, coordination of multiple strategies, and lifestyle design integration. This capstone module provides your blueprint for replicating Helen's success in your own situation.'''
    },
    'e2bb063a-22ea-4b73-b1d7-d6a3b9e3e784': {  # The Exit Plan (W-2)
        'summary': '''Module 10 presents the ultimate integration of sophisticated tax optimization and lifestyle design strategies. You'll review Helen's complete 5-year journey and understand how to build systematic escape timelines for different income and life situations. This module transforms tactical knowledge into strategic implementation.'''
    },
    
    # Business Owner Modules (9 modules)
    '4e672ed4-dd6c-4373-aa8b-2c9ae6aa6bfe': {  # Who This Is For
        'summary': '''Module 0 sets expectations and infrastructure requirements for six-figure+ business owners ready for advanced tax optimization. You'll understand what separates sophisticated strategies from basic compliance, see real examples of $100K+ annual savings, and map your current situation against the optimization opportunities ahead.'''
    },
    'a3860186-ae20-4c10-b904-e84488802329': {  # Entity Structuring & Income Capture
        'summary': '''Module 1 introduces C-Corp MSO (Management Services Organization) structures for optimal income capture and tax rate arbitrage. You'll learn how to transition from S-Corp or LLC structures, understand 21% corporate rates vs. 37%+ personal rates, and see Dr. Ben's implementation generating $320K+ in annual tax savings through strategic entity optimization.'''
    },
    '2c64dc93-9bb2-4f40-b206-7464c3554718': {  # Strategic Deductions & Asset Repositioning
        'summary': '''Module 2 transforms captured business income into tax-advantaged assets through the "deduction stack" methodology. You'll master cost segregation coordination, bonus depreciation rules, and IDC applications. This module shows Lauren's systematic approach generating $1.1M in accelerated deductions through strategic asset repositioning and timing optimization.'''
    },
    '37647570-1c7b-42fd-b942-ec4473d2ba04': {  # Long-Term Wealth Creation
        'summary': '''Module 3 builds protected, transferable wealth systems through QSBS qualification and trust multiplication strategies. You'll understand F-Reorg techniques for restructuring existing businesses, $10M+ gain exclusions, and systematic legacy planning. This module shows David's tech startup restructuring for $30M in excluded gains at exit.'''
    },
    'e5acbff1-60f7-4c31-89cd-cc10e0485ac4': {  # Business Structure Tax Implications  
        'summary': '''Module 4 demonstrates systematic income elimination through the Wealth Multiplier Loop for business owners. You'll see how David implemented $300K recurring income with $0 tax through strategic structuring, advanced timing strategies, and coordinated deduction management across multiple entities and investment vehicles.'''
    },
    'fe912e77-f0b8-4a06-bc0f-a207bad34884': {  # Business Deduction Strategies
        'summary': '''Module 5 converts tax planning from a cost center into a profit-generating strategy through the "Zero-Tax Income Stack." You'll learn systematic income and deduction coordination, advanced entity layering, and Sarah's achievement of $0 federal tax on $300K income through strategic repositioning and optimization.'''
    },
    '6153b599-2f1c-498e-9d6a-8cd341a5f7a7': {  # Capital Gains Repositioning
        'summary': '''Module 6 introduces advanced wealth protection through split-dollar life insurance and sophisticated financial planning. You'll understand loan-based premium funding, estate tax exposure mitigation, and Michael's $2.5M estate protection strategy using advanced insurance planning coordinated with business and tax optimization.'''
    },
    '37cbe8d5-7a88-453b-998c-98a2a917a508': {  # Protecting Wealth While You Grow It
        'summary': '''Module 7 explores co-investment MSO structures for family office coordination and sophisticated investor strategies. You'll learn depreciation recapture avoidance, advanced entity coordination for multi-generational planning, and Lisa's $450K depreciation capture through co-investment MSO structures and strategic asset coordination.'''
    },
    '2633803b-7881-436a-a25e-3de986cc4b8c': {  # The Exit Plan (Business)
        'summary': '''Module 8 presents ultimate wealth multiplication through trust strategies and comprehensive exit planning. You'll master multi-generational wealth transfer, advanced estate tax planning, and Robert's $3.5M wealth transfer optimization using sophisticated trust and entity structures for business succession and wealth preservation.'''
    }
}

def update_module_with_clean_summary(module_id, summary_text):
    """Update a module's content with clean summary structure while preserving What You'll Learn"""
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
        
        # Extract the What You'll Learn section to preserve it
        wyl_match = re.search(r'## What You\'ll Learn\s*<ul>.*?</ul>', current_content, re.DOTALL)
        
        if wyl_match:
            # Keep the What You'll Learn section and replace everything else with clean summary
            wyl_section = wyl_match.group(0)
            
            # Create the new clean content structure
            new_content = f'''{wyl_section}

<section class="module-summary">
  <h2>Summary</h2>
  <p>
    {summary_text}
  </p>
</section>'''
        else:
            # If no What You'll Learn section, just add the summary
            new_content = f'''<section class="module-summary">
  <h2>Summary</h2>
  <p>
    {summary_text}
  </p>
</section>'''
        
        # Update the specific lesson in the course
        result = courses_collection.update_one(
            {"id": course["id"]},
            {"$set": {f"lessons.{lesson_index}.content": new_content}}
        )
        
        if result.modified_count > 0:
            print(f"✅ Updated module {module_id}: {module.get('title', 'Unknown')}")
            return True
        else:
            print(f"❌ Failed to update module {module_id}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating module {module_id}: {str(e)}")
        return False

def main():
    """Update all modules with clean summary structure"""
    print("🧹 Starting module body structure cleanup...")
    print("Replacing module content with clean summaries while preserving What You'll Learn sections\n")
    
    updated_count = 0
    total_count = len(MODULE_SUMMARIES)
    
    print(f"Processing {total_count} modules...\n")
    
    for module_id, module_data in MODULE_SUMMARIES.items():
        if update_module_with_clean_summary(module_id, module_data['summary']):
            updated_count += 1
    
    print(f"\n🎯 Module structure cleanup complete: {updated_count}/{total_count} modules updated successfully")
    
    # Create summary report
    with open('module_structure_cleanup_summary.md', 'w') as f:
        f.write("# Module Body Structure Cleanup Summary\n\n")
        f.write(f"Updated {updated_count} out of {total_count} modules with clean summary structure.\n\n")
        f.write("## Changes Made:\n")
        f.write("- Replaced module body content with clean, focused summaries\n")
        f.write("- Used proper <h2> and <p> HTML structure\n")
        f.write("- Matched tone and clarity of 'Escape IRS Problems Forever' copy\n")
        f.write("- Ensured visual alignment across all modules\n\n")
        f.write("## Content Preserved:\n")
        f.write("- 'What You'll Learn' sections with bullet points (above video)\n")
        f.write("- Video components with duration and thumbnails\n")
        f.write("- Case Study sidebar sections\n")
        f.write("- Key Terms with +10 XP logic and links\n")
        f.write("- All quiz, XP, and glossary functionality\n\n")
        f.write("## Structure Applied:\n")
        f.write("- <section class=\"module-summary\">\n")
        f.write("- <h2>Summary</h2>\n") 
        f.write("- <p>1-2 paragraph high-level strategy framework summary</p>\n")
        f.write("- </section>\n")
    
    print(f"📄 Summary report saved to module_structure_cleanup_summary.md")

if __name__ == "__main__":
    main()