# Comprehensive script to add all missing "What You'll Learn" sections
import re

# Learning outcomes for all remaining modules
LEARNING_OUTCOMES = {
    # Primer Course - Module 5
    "primer_module_5": """## What You'll Learn

• **Evaluate your current tax situation** using the IRS Escape Plan assessment framework to identify immediate opportunities
• **Prioritize the 6 levers** based on your income type, business structure, and highest-impact potential
• **Create your 90-day implementation roadmap** with specific actions, timelines, and professional resources needed
• **Choose your advanced specialization path** (W-2 Escape Plan vs. Business Owner Escape Plan) based on income profile
• **Establish success metrics** to measure tax reduction progress and ROI over the next 12 months""",
    
    # W-2 Escape Plan - remaining modules
    "w2_module_4": """## What You'll Learn

• **Document the 750-hour REPS requirement** with contemporaneous logs that satisfy IRS audit standards
• **Qualify for REPS while maintaining W-2 employment** through strategic time allocation and activity tracking
• **Convert passive rental losses into active W-2 offsets** using material participation and REPS election
• **Implement spousal REPS strategies** when one spouse qualifies and the other has high W-2 income
• **Combine REPS with cost segregation** to maximize first-year depreciation benefits against current income""",
    
    "w2_module_5": """## What You'll Learn

• **Meet REPS qualification requirements** through documented 750+ hour real estate professional activities
• **Convert passive rental losses into active deductions** that offset W-2 income dollar-for-dollar
• **Apply material participation tests** to qualify real estate activities as business rather than investment
• **Coordinate REPS election timing** with property acquisitions and depreciation strategies
• **Implement audit-proof documentation** systems that satisfy IRS contemporaneous log requirements""",
    
    "w2_module_6": """## What You'll Learn

• **Structure STR properties** to qualify for material participation without REPS requirements
• **Apply the 7-day average test** to ensure short-term rental classification and benefits
• **Coordinate STR depreciation** with cost segregation studies for maximum first-year deductions
• **Navigate STR vs traditional rental** tax treatment differences and optimization opportunities
• **Scale STR portfolios** while maintaining material participation and maximizing depreciation benefits""",
    
    "w2_module_7": """## What You'll Learn

• **Structure IDC investments** to generate immediate 100% deductions on drilling and completion costs
• **Coordinate oil and gas timing** with W-2 income spikes and bonus payments for maximum offset
• **Understand depletion allowances** and ongoing tax benefits from energy investments
• **Apply energy investment strategies** specific to high-income W-2 earners without business ownership
• **Integrate energy deductions** with real estate and other offset strategies for comprehensive planning""",
    
    "w2_module_8": """## What You'll Learn

• **Apply the Wealth Multiplier Loop** where tax savings generate investment capital that creates additional tax benefits
• **Coordinate systematic reinvestment** of tax savings into additional tax-advantaged opportunities
• **Structure self-perpetuating cycles** where each tax benefit funds additional wealth-building investments
• **Scale wealth accumulation** through compounding tax advantages and strategic asset positioning
• **Integrate all W-2 strategies** into a comprehensive system for exponential rather than linear growth""",
    
    "w2_module_9": """## What You'll Learn

• **Apply Helen's complete W-2 transformation model** from high-tax employment to international tax optimization
• **Implement the 5-year roadmap** for transitioning from W-2 dependency to entrepreneurial tax strategies
• **Coordinate REPS qualification** with STR portfolio development and cost segregation timing
• **Scale multiple offset strategies** simultaneously while maintaining compliance and audit protection
• **Design your personal escape plan** using proven case study methodologies and implementation frameworks""",
    
    # Business Owner Escape Plan - remaining modules
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

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def write_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

def update_server_file():
    # Read the current server.py file
    server_content = read_file('/app/backend/server.py')
    
    # Define search patterns and replacements for each module
    updates = [
        # Primer Module 5
        {
            'search': r'(title="Building Your Custom Escape Plan".*?content="""[^"]*?)(## (?!What You\'ll Learn))',
            'replace': r'\1' + LEARNING_OUTCOMES['primer_module_5'] + '\n\n\2',
            'module': 'Primer Module 5'
        },
        
        # W-2 Module 4
        {
            'search': r'(title="Qualifying for REPS.*?content="""[^"]*?)(## (?!What You\'ll Learn))',
            'replace': r'\1' + LEARNING_OUTCOMES['w2_module_4'] + '\n\n\2',
            'module': 'W-2 Module 4'
        },
        
        # W-2 Module 5
        {
            'search': r'(title="Real Estate Professional Status \(REPS\)".*?content="""[^"]*?)(## (?!What You\'ll Learn))',
            'replace': r'\1' + LEARNING_OUTCOMES['w2_module_5'] + '\n\n\2',
            'module': 'W-2 Module 5'
        },
        
        # W-2 Module 6
        {
            'search': r'(title="Short-Term Rentals \(STRs\)".*?content="""[^"]*?)(## (?!What You\'ll Learn))',
            'replace': r'\1' + LEARNING_OUTCOMES['w2_module_6'] + '\n\n\2',
            'module': 'W-2 Module 6'
        },
        
        # W-2 Module 7
        {
            'search': r'(title="Oil & Gas Deductions".*?content="""[^"]*?)(## (?!What You\'ll Learn))',
            'replace': r'\1' + LEARNING_OUTCOMES['w2_module_7'] + '\n\n\2',
            'module': 'W-2 Module 7'
        },
        
        # W-2 Module 8
        {
            'search': r'(title="The Wealth Multiplier Loop".*?content="""[^"]*?)(## (?!What You\'ll Learn))',
            'replace': r'\1' + LEARNING_OUTCOMES['w2_module_8'] + '\n\n\2',
            'module': 'W-2 Module 8'
        },
        
        # W-2 Module 9
        {
            'search': r'(title="The IRS Escape Plan".*?content="""[^"]*?)(## (?!What You\'ll Learn))',
            'replace': r'\1' + LEARNING_OUTCOMES['w2_module_9'] + '\n\n\2',
            'module': 'W-2 Module 9'
        }
    ]
    
    # Apply updates
    updated_content = server_content
    for update in updates:
        if re.search(update['search'], updated_content, re.DOTALL):
            updated_content = re.sub(update['search'], update['replace'], updated_content, flags=re.DOTALL)
            print(f"✅ Updated {update['module']}")
        else:
            print(f"❌ Could not find pattern for {update['module']}")
    
    # Write the updated content back
    write_file('/app/backend/server.py', updated_content)
    print("\n✅ All learning outcomes updated in server.py")

if __name__ == "__main__":
    update_server_file()
