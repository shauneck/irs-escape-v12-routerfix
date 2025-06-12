# Script to systematically update all learning outcomes across all courses
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent / 'backend'
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# Define all specific learning outcomes based on actual module content
LEARNING_OUTCOMES = {
    # Primer Course - remaining modules
    "primer_module_5": """## What You'll Learn

• **Evaluate your current tax situation** using the IRS Escape Plan assessment framework to identify immediate opportunities
• **Prioritize the 6 levers** based on your income type, business structure, and highest-impact potential
• **Create your 90-day implementation roadmap** with specific actions, timelines, and professional resources needed
• **Choose your advanced specialization path** (W-2 Escape Plan vs. Business Owner Escape Plan) based on income profile
• **Establish success metrics** to measure tax reduction progress and ROI over the next 12 months""",
    
    # W-2 Escape Plan - all 9 modules  
    "w2_module_1": """## What You'll Learn

• **Calculate your W-2 tax disadvantage** across limited deductions, immediate recognition, and 15.3% payroll tax exposure
• **Map your W-2 profile** (High-Income, Side Business, Real Estate, or Tech/RSU) to optimal strategic pathways
• **Understand the 4 escape routes** that reduce W-2 tax burden without changing your employment status
• **Quantify marginal rate impact** at different W-2 income thresholds and phase-out ranges
• **Recognize timing windows** for strategic income repositioning and deduction coordination""",
    
    "w2_module_2": """## What You'll Learn

• **Reposition high-tax W-2 income** into QOF investments that defer capital gains while building opportunity zone wealth
• **Apply material participation rules** to qualify STR activities for active treatment without REPS
• **Integrate RSU vesting timing** with real estate depreciation for optimal tax coordination
• **Structure systematic dollar-cost averaging** that reduces both investment and tax risk
• **Create income repositioning workflows** that build wealth while reducing current-year tax liability""",
    
    "w2_module_3": """## What You'll Learn

• **Layer multiple offset strategies** to exceed individual strategy limitations and create compound tax reduction
• **Coordinate W-2 income timing** with bonus depreciation and cost segregation studies
• **Navigate AGI thresholds** that trigger deduction limitations, phase-outs, and additional taxes
• **Apply strategic deduction bunching** to maximize itemization benefits in alternating years
• **Optimize federal and state coordination** for maximum combined tax reduction""",
    
    "w2_module_4": """## What You'll Learn

• **Document the 750-hour REPS requirement** with contemporaneous logs that satisfy IRS audit standards
• **Qualify for REPS while maintaining W-2 employment** through strategic time allocation and activity tracking
• **Convert passive rental losses into active W-2 offsets** using material participation and REPS election
• **Implement spousal REPS strategies** when one spouse qualifies and the other has high W-2 income
• **Combine REPS with cost segregation** to maximize first-year depreciation benefits against current income""",
    
    "w2_module_5": """## What You'll Learn

• **Structure QOF investments** to defer capital gains taxes while building opportunity zone real estate wealth
• **Optimize asset location** across taxable, tax-deferred, and tax-free accounts for maximum efficiency
• **Time asset acquisitions** to maximize bonus depreciation and coordinate with income recognition
• **Plan 10-year QOF holding periods** to achieve maximum tax-free growth and basis step-up
• **Coordinate QOF strategy** with existing real estate holdings and REPS qualification""",
    
    "w2_module_6": """## What You'll Learn

• **Time RSU vesting events** to optimize tax liability across multiple years and avoid income spikes
• **Apply tax timing arbitrage** through strategic deferral, acceleration, and income smoothing techniques
• **Navigate high-income thresholds** that trigger NIIT, additional Medicare tax, and deduction phase-outs
• **Coordinate equity compensation** with real estate depreciation and other offset strategies
• **Plan for concentrated stock positions** and diversification strategies that minimize tax impact""",
    
    "w2_module_7": """## What You'll Learn

• **Build systematic income repositioning** that transforms W-2 wages into tax-advantaged investment cash flow
• **Apply tax-efficient investment strategies** that optimize after-tax returns through asset location and timing
• **Understand tax efficiency metrics** to measure and improve wealth accumulation rates
• **Coordinate retirement account strategies** with Roth conversions and backdoor contribution techniques
• **Create tax-efficient portfolios** that generate current income while building long-term wealth""",
    
    "w2_module_8": """## What You'll Learn

• **Navigate passive loss limitation rules** that restrict W-2 earners from using rental property losses
• **Apply material participation tests** to qualify real estate activities as active rather than passive
• **Implement audit-proof documentation** that protects aggressive positions and satisfies IRS requirements
• **Understand contemporaneous log requirements** for REPS and material participation claims
• **Coordinate passive activity rules** with grouping elections and other W-2 offset strategies""",
    
    "w2_module_9": """## What You'll Learn

• **Apply Helen's complete W-2 escape methodology** from high-tax employment to international tax optimization
• **Understand the 5-year transformation roadmap** for transitioning from W-2 dependency to entrepreneurial freedom
• **Implement REPS qualification** while building and scaling a profitable STR portfolio
• **Coordinate cost segregation studies** with W-2 income for maximum depreciation offset potential
• **Design your personal escape plan** using proven case study frameworks and implementation strategies""",
    
    # Business Owner Escape Plan - remaining 8 modules (Module 0 already done)
    "business_module_1": """## What You'll Learn

• **Structure C-Corp MSO entities** to capture business income at 21% corporate rates instead of 37% personal rates
• **Understand income shifting mechanics** that move profit between entities for optimal tax treatment
• **Apply advanced entity strategies** beyond basic S-Corps and LLCs to unlock deduction and timing control
• **Coordinate multiple entity structures** to maximize business deductions and minimize overall tax burden
• **Recognize optimal MSO opportunities** based on business type, income levels, and operational structure""",
    
    "business_module_2": """## What You'll Learn

• **Apply QSBS qualification rules** to exclude up to $10M in business sale gains from federal taxation
• **Structure F-Reorganizations** to change entity types without triggering immediate tax consequences
• **Implement trust multiplication strategies** that amplify tax benefits and wealth transfer across generations
• **Coordinate QSBS holding periods** with business growth and exit planning timelines
• **Understand Section 1202 requirements** that must be maintained for maximum QSBS benefits""",
    
    "business_module_3": """## What You'll Learn

• **Build systematic deduction stacks** that layer business expenses, depreciation, and energy credits for maximum impact
• **Apply cost segregation studies** to commercial and rental properties for accelerated depreciation benefits
• **Understand IDC deductions** for immediate 100% write-offs on oil and gas investment expenses
• **Coordinate deduction timing** to optimize when large deductions impact your tax liability
• **Layer energy, depreciation, and business strategies** to create tax reduction impossible with single approaches""",
    
    "business_module_4": """## What You'll Learn

• **Apply the Wealth Multiplier Loop** where tax savings generate investment capital that creates additional tax benefits
• **Understand strategic compounding** of tax advantages through systematic reinvestment of savings
• **Implement asset protection structures** that preserve wealth while maintaining tax optimization benefits
• **Coordinate wealth building** with tax reduction to accelerate both simultaneously through strategic timing
• **Create self-perpetuating systems** where each tax benefit funds additional tax-advantaged opportunities""",
    
    "business_module_5": """## What You'll Learn

• **Build Zero-Tax Income Stacks** that generate substantial business income with minimal federal tax liability
• **Apply income repositioning techniques** specific to business owners with multiple revenue streams and entities
• **Understand tax efficiency optimization** for complex business structures and multi-entity operations
• **Coordinate business distributions** with personal tax planning for optimal combined tax treatment
• **Achieve high income with minimal tax burden** through systematic strategic structuring and timing""",
    
    "business_module_6": """## What You'll Learn

• **Structure Split-Dollar Life Insurance** arrangements that create tax advantages for both business and personal wealth building
• **Apply Loan-Based Premium Funding** to convert life insurance costs into tax-deductible business strategies
• **Understand estate tax exposure** calculations for high-net-worth business owners and mitigation techniques
• **Coordinate insurance strategies** with business succession planning and wealth transfer optimization
• **Maximize life insurance benefits** while minimizing tax costs and maximizing business deduction opportunities""",
    
    "business_module_7": """## What You'll Learn

• **Structure Co-Investment arrangements** where MSOs and trusts invest alongside business owners for amplified benefits
• **Understand depreciation recapture planning** for optimal timing of property dispositions and tax consequences
• **Apply installment sale techniques** to spread business asset sale tax liability across multiple years
• **Coordinate entity investing strategies** to maximize investment returns while optimizing tax treatment
• **Plan asset disposition timing** to minimize tax consequences while maximizing after-tax proceeds""",
    
    "business_module_8": """## What You'll Learn

• **Implement Trust Multiplication Strategies** using coordinated trust structures for maximum tax and protection benefits
• **Understand estate tax exposure** calculations and mitigation strategies for growing business wealth
• **Apply advanced asset protection** techniques that work with tax optimization rather than against it
• **Coordinate trust strategies** with ongoing business operations and succession planning requirements
• **Amplify wealth transfer benefits** while minimizing tax complications and maintaining operational flexibility""",
    
    "business_module_9": """## What You'll Learn

• **Apply strategic compounding principles** to create exponential rather than linear tax savings and wealth growth
• **Master the complete Wealth Multiplier Loop** system for systematic tax reduction and wealth acceleration
• **Coordinate Zero-Tax Income Stack** strategies across multiple entities and investment vehicles
• **Implement systematic reinvestment** of tax savings into additional tax-advantaged wealth-building opportunities
• **Create exponential wealth growth** through compounding tax advantages, strategic timing, and systematic implementation"""
}

async def update_course_learning_outcomes():
    """Update all course modules with specific learning outcomes"""
    print("Updating learning outcomes for all course modules...")
    
    # Get all courses
    courses = await db.courses.find({}).to_list(length=None)
    
    for course in courses:
        course_type = course.get('type')
        print(f"\nUpdating {course_type} course: {course.get('title')}")
        
        # Update each lesson in the course
        for i, lesson in enumerate(course.get('lessons', [])):
            lesson_key = None
            
            # Determine the learning outcome key based on course and module
            if course_type == 'primer' and lesson.get('order_index') == 5:
                lesson_key = 'primer_module_5'
            elif course_type == 'w2':
                lesson_key = f'w2_module_{lesson.get("order_index")}'
            elif course_type == 'business' and lesson.get('order_index') > 0:
                lesson_key = f'business_module_{lesson.get("order_index")}'
            
            # Update lesson content if we have learning outcomes for it
            if lesson_key and lesson_key in LEARNING_OUTCOMES:
                current_content = lesson.get('content', '')
                
                # Check if learning outcomes already exist
                if "## What You'll Learn" not in current_content:
                    # Find where to insert the learning outcomes (after introduction, before first major section)
                    lines = current_content.split('\n')
                    insert_index = 0
                    
                    # Find the end of the introduction (first blank line or first ## section)
                    for j, line in enumerate(lines):
                        if j > 3 and (line.strip() == '' or line.startswith('## ')) and not line.startswith('## What You\'ll Learn'):
                            insert_index = j
                            break
                    
                    # Insert the learning outcomes
                    learning_outcome_lines = LEARNING_OUTCOMES[lesson_key].strip().split('\n')
                    lines[insert_index:insert_index] = [''] + learning_outcome_lines + ['']
                    
                    # Update the lesson content
                    updated_content = '\n'.join(lines)
                    lesson['content'] = updated_content
                    
                    print(f"  ✅ Updated {lesson.get('title')} (Module {lesson.get('order_index')})")
                else:
                    print(f"  ⏭️  {lesson.get('title')} already has learning outcomes")
        
        # Update the course in the database
        await db.courses.update_one(
            {'_id': course['_id']}, 
            {'$set': {'lessons': course['lessons']}}
        )
    
    print("\n✅ All learning outcomes updated successfully!")

if __name__ == "__main__":
    asyncio.run(update_course_learning_outcomes())
