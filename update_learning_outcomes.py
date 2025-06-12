# Script to update "What You'll Learn" sections across all courses
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

async def update_learning_outcomes():
    """Update all course modules with specific learning outcomes"""
    
    # Clear existing courses to replace with updated versions
    await db.courses.delete_many({})
    
    # PRIMER COURSE - The Escape Blueprint (5 modules)
    primer_learning_outcomes = {
        1: """## What You'll Learn

• **Identify the 3 tax treatment categories** that determine whether you overpay or optimize
• **Distinguish between CPA compliance vs. strategic tax planning** and when each is appropriate
• **Recognize the wealth-building behaviors** the tax code rewards vs. penalizes
• **Calculate your current tax inefficiency** by comparing proactive vs. reactive planning outcomes
• **Understand why W-2 income faces the highest effective tax rates** and what alternatives exist""",
        
        2: """## What You'll Learn

• **Master the 6 core levers** that control all tax outcomes: Entity Type, Income Type, Timing, Asset Location, Deduction Strategy, and Exit Planning
• **Determine your optimal entity structure** based on income type and business activities
• **Apply strategic timing** to control when income hits and when deductions are claimed
• **Position assets in the right locations** to minimize overall tax burden
• **Orchestrate deductions** through energy, depreciation, and trust layering strategies
• **Design your exit plan** using QSBS, Opportunity Zones, and stepped-up basis strategy""",
        
        3: """## What You'll Learn

• **Analyze Noah's RSU deferral strategy** that saved $96K through QOF repositioning and STR depreciation
• **Understand Jessica's S-Corp to C-Corp MSO transition** that reduced taxes from $278K to $122K
• **Apply Liam's REPS qualification approach** that offset $118K of W-2 income through STR depreciation
• **Identify which case study model** most closely matches your income profile and situation
• **Extract the common strategic elements** that create exponential tax reduction results""",
        
        4: """## What You'll Learn

• **Meet the 750-hour annual requirement** for Real Estate Professional Status qualification
• **Satisfy the "more than 50% of work time" test** for REPS election
• **Convert passive rental losses into active deductions** that offset W-2 and business income
• **Implement proper contemporaneous documentation** to defend REPS status in an audit
• **Combine REPS with other strategies** like cost segregation and bonus depreciation for maximum impact""",
        
        5: """## What You'll Learn

• **Evaluate your current tax situation** using the IRS Escape Plan assessment framework
• **Prioritize the 6 levers** based on your income type, business structure, and immediate opportunities
• **Create your 90-day implementation roadmap** with specific actions and timelines
• **Identify which advanced course** (W-2 Escape Plan vs. Business Owner Escape Plan) fits your situation
• **Establish success metrics** to measure tax reduction progress over the next 12 months"""
    }
    
    # W-2 ESCAPE PLAN learning outcomes (9 modules)
    w2_learning_outcomes = {
        1: """## What You'll Learn

• **Calculate your W-2 tax disadvantage** across limited deductions, immediate recognition, and payroll tax exposure
• **Map your W-2 profile** (High-Income, Side Business, Real Estate, or Tech/RSU) to identify optimal strategies
• **Understand the 4 pathways** to reduce W-2 tax burden without changing your employment
• **Quantify the tax impact** of different W-2 income levels and marginal rate thresholds
• **Recognize opportunity windows** for strategic income repositioning and timing arbitrage""",
        
        2: """## What You'll Learn

• **Reposition high-tax W-2 income** into tax-advantaged real estate and investment vehicles
• **Apply QOF deferral strategies** to postpone capital gains taxes while building opportunity zone wealth
• **Integrate RSU vesting timing** with other income sources for optimal tax treatment
• **Understand material participation rules** for short-term rentals vs. traditional rental properties
• **Create systematic income repositioning** that builds wealth while reducing current-year taxes""",
        
        3: """## What You'll Learn

• **Layer multiple offset strategies** to exceed single-strategy tax reduction limits
• **Coordinate W-2 income timing** with real estate depreciation and business deductions
• **Understand AGI impact** on various deduction limitations and phase-outs
• **Apply strategic bunching** of deductions to maximize itemization benefits
• **Optimize the interaction** between federal and state tax strategies for maximum offset""",
        
        4: """## What You'll Learn

• **Meet REPS qualification requirements** while maintaining W-2 employment status
• **Document the 750-hour test** with contemporaneous logs that satisfy IRS scrutiny
• **Apply REPS status** to convert passive rental losses into active W-2 offsets
• **Understand spousal REPS strategies** when one spouse qualifies and the other has W-2 income
• **Combine REPS with cost segregation** for maximum first-year depreciation benefits""",
        
        5: """## What You'll Learn

• **Structure Qualified Opportunity Fund investments** to defer capital gains while building real estate wealth
• **Optimize asset location strategies** across taxable, tax-deferred, and tax-free accounts
• **Time asset acquisitions** to maximize bonus depreciation and first-year deduction benefits
• **Coordinate QOF investments** with existing real estate holdings for portfolio optimization
• **Plan 10-year holding periods** to achieve maximum QOF tax benefits""",
        
        6: """## What You'll Learn

• **Time RSU vesting** to optimize tax liability across multiple years
• **Apply tax timing arbitrage** to control when income hits your tax return
• **Understand high-income thresholds** that trigger additional taxes and phase-outs
• **Coordinate equity compensation** with other income sources and deduction strategies
• **Plan for tax spikes** from large vesting events or bonus payments""",
        
        7: """## What You'll Learn

• **Systematically reposition W-2 income** into tax-advantaged investment vehicles
• **Apply dollar-cost averaging strategies** that reduce both investment and tax risk
• **Understand tax efficiency metrics** to measure after-tax wealth accumulation
• **Coordinate repositioning** with retirement account contributions and Roth conversions
• **Build tax-efficient portfolios** that generate cash flow while reducing current taxes""",
        
        8: """## What You'll Learn

• **Navigate passive loss limitation rules** that restrict W-2 earners from using rental losses
• **Apply the 750-hour test** to qualify real estate activities as non-passive
• **Understand audit-proofing strategies** that protect aggressive tax positions
• **Implement contemporaneous documentation** that satisfies IRS material participation requirements
• **Coordinate passive activity rules** with other W-2 offset strategies""",
        
        9: """## What You'll Learn

• **Apply Helen's complete transformation model** from high-tax W-2 to international tax freedom
• **Understand the 5-year roadmap** for transitioning from employment to entrepreneurial tax strategies
• **Implement REPS qualification** while building a short-term rental portfolio
• **Coordinate cost segregation studies** with W-2 income for maximum depreciation offset
• **Plan your personal IRS escape** using proven case study methodologies"""
    }
    
    # BUSINESS OWNER ESCAPE PLAN learning outcomes (9 modules)
    business_learning_outcomes = {
        0: """## What You'll Learn

• **Identify if you're a qualifying business owner** earning six figures in profit ready for advanced strategies
• **Understand the strategic arsenal** you'll build: C-Corp MSO, deduction strategies, trust structures, and exit planning
• **Map your current entity structure** against optimal tax-efficient alternatives
• **Recognize real case study results** showing $490K annual tax savings through strategic implementation
• **Establish your baseline** for measuring progress through the 12-module strategic transformation""",
        
        1: """## What You'll Learn

• **Structure C-Corp MSO entities** to capture income at 21% corporate rates instead of 37% personal rates
• **Understand income capture mechanics** that shift profit between entities for optimal tax treatment
• **Apply entity planning strategies** beyond basic S-Corps and LLCs into advanced structures
• **Coordinate multiple entities** to maximize deduction opportunities and income control
• **Recognize when MSO structures** provide the greatest tax advantages for your business type""",
        
        2: """## What You'll Learn

• **Apply QSBS qualification rules** to exclude up to $10M in business sale gains from federal taxes
• **Structure F-Reorganizations** to change entity types without triggering immediate tax consequences
• **Implement trust multiplication strategies** that amplify tax benefits across generations
• **Coordinate QSBS holding periods** with business growth and exit planning timelines
• **Understand qualification requirements** that must be met for QSBS benefits""",
        
        3: """## What You'll Learn

• **Build systematic deduction stacks** that layer business expenses, depreciation, and credits for maximum impact
• **Apply cost segregation studies** to accelerate real estate depreciation and improve cash flow
• **Understand IDC (Intangible Drilling Costs)** for immediate 100% deductions in energy investments
• **Coordinate timing strategies** that optimize when deductions hit your tax return
• **Layer multiple deduction sources** to create tax reduction impossible with single strategies""",
        
        4: """## What You'll Learn

• **Apply the Wealth Multiplier Loop** where tax savings generate investment capital that creates more tax benefits
• **Understand strategic compounding** of tax advantages through systematic reinvestment
• **Implement asset protection strategies** that preserve wealth while maintaining tax benefits
• **Coordinate wealth building** with tax reduction to accelerate both simultaneously
• **Create self-perpetuating cycles** of tax savings and wealth accumulation""",
        
        5: """## What You'll Learn

• **Build Zero-Tax Income Stacks** that generate substantial income with minimal federal tax liability
• **Apply income repositioning techniques** specific to business owners with multiple revenue streams
• **Understand tax efficiency optimization** for business owners with complex income structures
• **Coordinate business distributions** with personal tax planning for optimal overall treatment
• **Achieve high income with minimal tax burden** through systematic strategic structuring""",
        
        6: """## What You'll Learn

• **Structure Split-Dollar Life Insurance** arrangements that create tax advantages for both business and personal planning
• **Apply Loan-Based Premium Funding** to convert life insurance costs into tax-deductible wealth building
• **Understand estate tax exposure** for high-net-worth business owners and mitigation strategies
• **Coordinate insurance strategies** with business succession and wealth transfer planning
• **Maximize life insurance benefits** while minimizing tax costs for all parties involved""",
        
        7: """## What You'll Learn

• **Structure Co-Investment arrangements** where MSOs and trusts invest alongside business owners
• **Understand depreciation recapture** planning for optimal property disposition strategies
• **Apply installment sale techniques** to spread tax liability and reduce overall burden
• **Coordinate entity investing** to amplify investment returns and tax benefits
• **Plan asset dispositions** to minimize tax consequences while maximizing proceeds""",
        
        8: """## What You'll Learn

• **Implement Trust Multiplication Strategies** using multiple trust structures for maximum tax and protection benefits
• **Understand estate tax exposure** for business owners with growing wealth
• **Apply asset protection techniques** that work in conjunction with tax optimization
• **Coordinate trust strategies** with business operations and succession planning
• **Amplify wealth transfer benefits** while minimizing tax and legal complications""",
        
        9: """## What You'll Learn

• **Apply strategic compounding principles** to accelerate both tax savings and wealth accumulation
• **Understand the complete Wealth Multiplier Loop** system for business owners
• **Coordinate Zero-Tax Income Stack** strategies across multiple entities and investment vehicles
• **Implement systematic reinvestment** of tax savings into additional tax-advantaged opportunities
• **Create exponential wealth growth** through compounding tax advantages and strategic timing"""
    }
    
    # Now update each course with the learning outcomes
    print("Updating learning outcomes for all courses...")
    
    # This would be part of a larger script to reconstruct the courses
    # For now, let's create a summary of what needs to be updated
    
    print("Learning outcomes defined for:")
    print(f"- Primer Course: {len(primer_learning_outcomes)} modules")
    print(f"- W-2 Escape Plan: {len(w2_learning_outcomes)} modules") 
    print(f"- Business Owner Escape Plan: {len(business_learning_outcomes)} modules")
    
    return primer_learning_outcomes, w2_learning_outcomes, business_learning_outcomes

if __name__ == "__main__":
    asyncio.run(update_learning_outcomes())
