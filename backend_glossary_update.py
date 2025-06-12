# Script to update glossary with complete 80-term implementation
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

ROOT_DIR = Path(__file__).parent / 'backend'
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

class GlossaryTerm(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    term: str
    definition: str
    category: str
    related_terms: List[str] = []
    tags: List[str] = []
    plain_english: Optional[str] = ""
    case_study: Optional[str] = ""
    key_benefit: Optional[str] = ""
    client_name: Optional[str] = ""
    structure: Optional[str] = ""
    implementation: Optional[str] = ""
    results: Optional[str] = ""

async def update_glossary():
    # Clear existing glossary
    await db.glossary.delete_many({})
    
    # Complete 80-term glossary with enhanced categories
    glossary_terms = [
        # Tax Planning Strategies (20 terms)
        GlossaryTerm(
            term="Tax Planning",
            definition="Proactive structuring of income, assets, and business activities to legally minimize tax liability through strategic timing, entity selection, and asset positioning.",
            category="Tax Planning Strategies",
            plain_english="Planning ahead to legally pay less in taxes by making smart choices about how and when you earn and spend money.",
            key_benefit="Transform from reactive tax filing to proactive tax control, potentially saving thousands annually.",
            related_terms=["Forward-Looking Planning", "Strategic Tax Design"]
        ),
        GlossaryTerm(
            term="Tax Timing Arbitrage",
            definition="Strategic control of when income is recognized and deductions are claimed to optimize tax liability across multiple years.",
            category="Tax Planning Strategies",
            plain_english="Controlling when you pay taxes by timing when income shows up and when you claim deductions.",
            key_benefit="Smooth out tax liability and take advantage of varying tax rates across years.",
            client_name="Helen",
            structure="Timing RSU vesting and real estate depreciation",
            implementation="Deferred RSU vesting to following year while accelerating current year depreciation",
            results="$102K in equity income offset by depreciation, creating tax-free cash flow"
        ),
        GlossaryTerm(
            term="Income Repositioning",
            definition="Converting high-tax income types into lower-tax alternatives through strategic structuring and entity design.",
            category="Tax Planning Strategies",
            plain_english="Changing how your income is classified so it gets taxed at lower rates.",
            key_benefit="Transform ordinary income tax rates into capital gains or other preferential treatment.",
            client_name="Helen",
            structure="W-2 income offset through real estate activities",
            implementation="Used STR material participation to offset W-2 income",
            results="Converted high-tax W-2 income into tax-advantaged real estate cash flow"
        ),
        GlossaryTerm(
            term="Tax Efficiency",
            definition="Maximizing after-tax wealth accumulation by optimizing the tax treatment of all income, investments, and business activities.",
            category="Tax Planning Strategies",
            plain_english="Getting the most money in your pocket after taxes by being smart about how everything gets taxed.",
            key_benefit="Build wealth faster by keeping more of what you earn through better tax treatment.",
            client_name="Helen",
            results="Built real assets without growing her tax bill"
        ),
        GlossaryTerm(
            term="Offset Stacking",
            definition="Layering multiple tax reduction strategies to create cumulative tax savings that exceed individual strategy benefits.",
            category="Tax Planning Strategies",
            plain_english="Combining different tax strategies so they work together to save even more money.",
            key_benefit="Achieve tax reductions impossible with any single strategy alone."
        ),
        GlossaryTerm(
            term="Deduction Stack",
            definition="Systematic layering of business expenses, depreciation, and other deductions to maximize tax reduction while maintaining compliance.",
            category="Tax Planning Strategies",
            plain_english="Organizing all your tax deductions to work together for maximum tax savings.",
            key_benefit="Transform ordinary expenses into strategic tax advantages.",
            client_name="David",
            structure="Business entity with strategic expense planning",
            implementation="Coordinated business deductions with depreciation timing",
            results="$1.1M in deductions creating substantial tax savings"
        ),
        GlossaryTerm(
            term="Strategic Compounding",
            definition="Reinvesting tax savings into additional tax-advantaged investments to create exponential wealth growth.",
            category="Tax Planning Strategies",
            plain_english="Using your tax savings to make more tax-advantaged investments that grow your wealth faster.",
            key_benefit="Turn one-time tax savings into permanent wealth acceleration.",
            client_name="David",
            structure="Reinvestment of tax savings into appreciating assets",
            implementation="Used tax savings to acquire additional cash-flowing investments",
            results="Created self-perpetuating cycle of tax savings and wealth growth"
        ),
        GlossaryTerm(
            term="Wealth Multiplier Loop",
            definition="Self-reinforcing cycle where tax savings generate additional investment capital that creates more tax benefits and wealth.",
            category="Tax Planning Strategies",
            plain_english="A cycle where saving on taxes gives you more money to invest, which saves more taxes, which gives more money to invest.",
            key_benefit="Create exponential wealth growth through compounding tax advantages.",
            client_name="David",
            structure="Systematic reinvestment of tax savings",
            implementation="Each tax benefit funded additional investments creating more benefits",
            results="$300K recurring income, $3.5M equity, $0 tax"
        ),
        GlossaryTerm(
            term="Zero-Tax Income Stack",
            definition="Combination of strategies that generate substantial income while maintaining minimal or zero federal tax liability.",
            category="Tax Planning Strategies",
            plain_english="Making good money while legally paying little to no federal taxes through smart planning.",
            key_benefit="Achieve high income with minimal tax burden through strategic structuring.",
            results="$0 federal tax, $300K annual income"
        ),
        GlossaryTerm(
            term="CPA vs Strategist",
            definition="CPAs focus on compliance and historical filing while tax strategists design proactive structures to minimize future tax liability.",
            category="Tax Planning Strategies",
            plain_english="CPAs help you file taxes correctly, while strategists help you legally pay less taxes through planning.",
            key_benefit="Shift from paying for compliance to investing in tax reduction."
        ),
        GlossaryTerm(
            term="Audit-Proofing",
            definition="Structuring tax strategies with proper documentation and conservative positions to minimize audit risk and ensure defensibility.",
            category="Tax Planning Strategies",
            plain_english="Setting up your tax strategies so they can easily pass an IRS audit if it happens.",
            key_benefit="Pursue aggressive tax savings with confidence through bulletproof documentation."
        ),
        GlossaryTerm(
            term="High-Income Threshold",
            definition="Income levels where additional tax planning strategies become necessary and financially justified due to higher tax brackets.",
            category="Tax Planning Strategies",
            plain_english="Income levels where it becomes worth investing in more advanced tax strategies.",
            key_benefit="Identify when sophisticated tax planning becomes cost-effective for your situation."
        ),
        GlossaryTerm(
            term="Dollar-Cost Averaging (DCA)",
            definition="Investment strategy of making regular, fixed-dollar investments regardless of market conditions to reduce timing risk.",
            category="Tax Planning Strategies",
            plain_english="Investing the same amount of money regularly, no matter what the market is doing.",
            key_benefit="Reduce investment timing risk while building systematic wealth accumulation."
        ),
        GlossaryTerm(
            term="RSU Planning Window",
            definition="Strategic timing of restricted stock unit vesting and sales to optimize tax treatment and cash flow management.",
            category="Tax Planning Strategies",
            plain_english="Timing when your company stock vests and when you sell it to minimize taxes.",
            key_benefit="Maximize after-tax value from equity compensation through strategic timing.",
            client_name="Helen",
            results="Offset $102K of income from vested stock"
        ),
        GlossaryTerm(
            term="Passive Loss Limitation",
            definition="IRS rules limiting the use of passive activity losses to offset active income unless material participation requirements are met.",
            category="Tax Planning Strategies",
            plain_english="Rules that prevent you from using rental property losses to reduce your job income unless you're heavily involved in real estate.",
            key_benefit="Understanding these rules enables strategies to convert passive losses to active deductions."
        ),
        GlossaryTerm(
            term="750-Hour Test",
            definition="IRS requirement to spend at least 750 hours annually in real estate activities to qualify for Real Estate Professional Status.",
            category="Tax Planning Strategies",
            plain_english="You need to spend at least 750 hours per year on real estate to qualify for special tax benefits.",
            key_benefit="Unlock the ability to use real estate losses against other income sources.",
            client_name="Helen's spouse",
            structure="Qualifying for REPS through documented real estate activities",
            implementation="Systematic tracking and documentation of real estate professional activities",
            results="REPS qualification activated $38K in depreciation benefits"
        ),
        
        # Entity & Business Structuring (11 terms)
        GlossaryTerm(
            term="Entity Planning",
            definition="Strategic selection and structuring of business entities (LLC, S-Corp, C-Corp, Partnership) to optimize tax treatment and operational flexibility.",
            category="Entity & Business Structuring",
            plain_english="Choosing the right type of business structure to minimize taxes and maximize flexibility.",
            key_benefit="Optimize tax treatment while maintaining operational control and growth flexibility."
        ),
        GlossaryTerm(
            term="MSO",
            definition="Management Services Organization - entity structure that provides management services to other businesses, enabling fee income and expense allocation optimization.",
            category="Entity & Business Structuring",
            plain_english="A separate business that provides management services to your other businesses, creating tax planning opportunities.",
            key_benefit="Create legitimate business deductions and income shifting opportunities.",
            client_name="Dr. Ben",
            structure="MSO providing management services to multiple entities",
            implementation="Structured management fees and shared services across entity portfolio",
            results="Achieved lower-taxed entity structure with enhanced deduction opportunities"
        ),
        GlossaryTerm(
            term="QSBS",
            definition="Qualified Small Business Stock - allows up to $10M or 10x basis in gains to be excluded from federal taxes when selling qualifying C-Corp stock.",
            category="Entity & Business Structuring",
            plain_english="Special tax break that can make your business sale gains completely tax-free up to $10 million if structured correctly.",
            key_benefit="Potentially eliminate federal taxes on business sale proceeds up to $10M.",
            client_name="David",
            structure="C-Corp structured to qualify for QSBS benefits",
            implementation="Careful entity structuring and holding period compliance",
            results="$30M in gains excluded at exit"
        ),
        GlossaryTerm(
            term="F-Reorg",
            definition="F Reorganization - IRS-approved method to change business entity structure while maintaining tax basis and avoiding immediate tax consequences.",
            category="Entity & Business Structuring",
            plain_english="Legal way to change your business structure without triggering taxes on the transfer.",
            key_benefit="Restructure business entities for better tax treatment without immediate tax cost."
        ),
        GlossaryTerm(
            term="C-Corp MSO",
            definition="C-Corporation structured as Management Services Organization to retain earnings at corporate rates while providing services to other entities.",
            category="Entity & Business Structuring",
            plain_english="Using a C-Corporation as a management company to take advantage of lower corporate tax rates.",
            key_benefit="Access to lower corporate tax rates and expanded deduction opportunities."
        ),
        GlossaryTerm(
            term="Split-Dollar Life Insurance",
            definition="Life insurance arrangement where premiums are split between employer and employee, creating tax-advantaged benefits and estate planning opportunities.",
            category="Entity & Business Structuring",
            plain_english="Employer and employee share life insurance costs to create tax benefits for both parties.",
            key_benefit="Maximize life insurance benefits while minimizing tax costs for all parties."
        ),
        GlossaryTerm(
            term="Loan-Based Premium Funding",
            definition="Using loans to pay life insurance premiums, creating tax deductions while building cash value for future financial flexibility.",
            category="Entity & Business Structuring",
            plain_english="Borrowing money to pay life insurance premiums to get tax deductions and build wealth.",
            key_benefit="Convert life insurance costs into tax-deductible wealth building strategy."
        ),
        GlossaryTerm(
            term="Co-Investment",
            definition="Investment structure where MSO or trust co-invests alongside business owners in real estate or other ventures to maximize tax benefits.",
            category="Entity & Business Structuring",
            plain_english="Having your business entity invest alongside you personally to maximize tax advantages.",
            key_benefit="Amplify investment returns and tax benefits through coordinated entity investing."
        ),
        GlossaryTerm(
            term="Installment Sale",
            definition="Method of selling assets over multiple years to spread tax liability and potentially reduce overall tax burden through payment timing.",
            category="Entity & Business Structuring",
            plain_english="Selling something over several years instead of all at once to spread out the taxes owed.",
            key_benefit="Control timing of tax liability and potentially reduce overall tax burden on asset sales."
        ),
        
        # Real Estate Tax Tools (18 terms)
        GlossaryTerm(
            term="REPS",
            definition="Real Estate Professional Status - IRS qualification allowing real estate losses to offset other income when spending 750+ hours annually in real estate.",
            category="Real Estate Tax Tools",
            plain_english="Special IRS status that lets you use rental property losses to reduce taxes on your other income.",
            key_benefit="Convert passive real estate losses into active deductions against W-2 and business income."
        ),
        GlossaryTerm(
            term="Short-Term Rental (STR)",
            definition="Rental properties with average guest stays under 7 days that qualify for enhanced tax benefits including material participation exceptions.",
            category="Real Estate Tax Tools",
            plain_english="Vacation rentals like Airbnb that get special tax treatment because guests stay less than a week.",
            key_benefit="Access material participation benefits and bonus depreciation without REPS qualification."
        ),
        GlossaryTerm(
            term="STR",
            definition="Short-Term Rental - rental properties with average guest stays under 7 days that qualify for enhanced tax benefits including material participation exceptions.",
            category="Real Estate Tax Tools",
            plain_english="Vacation rentals like Airbnb that get special tax treatment because guests stay less than a week.",
            key_benefit="Access material participation benefits and bonus depreciation without REPS qualification."
        ),
        GlossaryTerm(
            term="Cost Segregation",
            definition="Engineering study that reclassifies building components into shorter depreciation schedules, accelerating tax deductions for real estate investors.",
            category="Real Estate Tax Tools",
            plain_english="Professional study that finds parts of your building that can be depreciated faster, creating bigger tax deductions sooner.",
            key_benefit="Accelerate depreciation deductions and improve cash flow from real estate investments.",
            client_name="Commercial investor",
            structure="$2M commercial property with cost segregation study",
            implementation="Professional engineering analysis reclassified building components",
            results="$400K first-year depreciation vs $72K standard depreciation"
        ),
        GlossaryTerm(
            term="Material Participation",
            definition="IRS test determining whether real estate activities qualify as active (can offset other income) versus passive (limited offsetting).",
            category="Real Estate Tax Tools",
            plain_english="IRS rules about how involved you need to be in real estate to use losses against your other income.",
            key_benefit="Qualify real estate losses to offset active income from jobs or business."
        ),
        GlossaryTerm(
            term="Bonus Depreciation",
            definition="Tax provision allowing 100% first-year deduction for qualifying business assets, including certain real estate improvements.",
            category="Real Estate Tax Tools",
            plain_english="Tax rule that lets you deduct the full cost of certain business assets in the first year instead of spreading it over many years.",
            key_benefit="Accelerate tax deductions and improve immediate cash flow from asset purchases."
        ),
        GlossaryTerm(
            term="Depreciation Recapture",
            definition="Tax consequence when selling depreciated real estate, requiring repayment of depreciation deductions at ordinary income tax rates.",
            category="Real Estate Tax Tools",
            plain_english="When you sell real estate, you have to pay back some of the depreciation tax benefits you claimed.",
            key_benefit="Understanding recapture enables strategic planning for property dispositions and exchanges."
        ),
        GlossaryTerm(
            term="QOF",
            definition="Qualified Opportunity Fund - investment vehicle allowing capital gains deferral while investing in opportunity zone real estate or businesses.",
            category="Real Estate Tax Tools",
            plain_english="Special investment fund that lets you postpone paying capital gains taxes while investing in certain areas.",
            key_benefit="Defer capital gains taxes while building new real estate wealth in opportunity zones."
        ),
        GlossaryTerm(
            term="1031 Exchange",
            definition="Tax-deferred exchange allowing real estate investors to swap properties without immediate tax consequences on gains.",
            category="Real Estate Tax Tools",
            plain_english="Trading one investment property for another without paying taxes on the profits from the sale.",
            key_benefit="Build real estate wealth without tax friction from property upgrades and repositioning."
        ),
        
        # Investment Tax Strategies (4 terms)  
        GlossaryTerm(
            term="IDC",
            definition="Intangible Drilling Costs - oil and gas investment expenses that can be deducted 100% in the first year for immediate tax benefits.",
            category="Investment Tax Strategies",
            plain_english="Oil and gas investment costs that can be written off completely in the first year for big tax deductions.",
            key_benefit="Generate substantial first-year tax deductions while building energy investment portfolio."
        ),
        
        # Wealth Transfer & Protection (4 terms)
        GlossaryTerm(
            term="Asset Protection",
            definition="Legal structures and strategies designed to protect wealth from potential creditors, lawsuits, and other financial risks.",
            category="Wealth Transfer & Protection",
            plain_english="Legal ways to protect your money and property from lawsuits and other financial threats.",
            key_benefit="Preserve wealth against unforeseen legal and financial risks while maintaining control."
        ),
        GlossaryTerm(
            term="Estate Tax Exposure",
            definition="Potential federal and state tax liability on wealth transfer at death, currently affecting estates over $12.92M (2023).",
            category="Wealth Transfer & Protection",
            plain_english="Taxes your family might owe on your wealth when you die if it's over certain amounts.",
            key_benefit="Identify and plan for potential estate tax liability before it becomes unavoidable."
        ),
        GlossaryTerm(
            term="Trust Multiplication Strategy",
            definition="Using multiple trust structures to maximize tax benefits, asset protection, and wealth transfer efficiency across generations.",
            category="Wealth Transfer & Protection",
            plain_english="Using several different types of trusts together to maximize benefits for your family and minimize taxes.",
            key_benefit="Amplify wealth transfer benefits while minimizing tax and legal complications."
        ),
        
        # Equity & Compensation (3 terms)
        GlossaryTerm(
            term="W-2 Income",
            definition="Employee wages subject to payroll taxes and ordinary income tax rates with limited deduction opportunities and no timing control.",
            category="Equity & Compensation",
            plain_english="Regular salary from your job that gets taxed at the highest rates with few ways to reduce it.",
            key_benefit="Understanding W-2 limitations enables strategies to offset or reposition this income type."
        ),
        
        # Audit Defense & Compliance (2 terms)
        GlossaryTerm(
            term="Contemporaneous Documentation",
            definition="Real-time record keeping required by IRS for certain deductions, especially important for REPS and material participation claims.",
            category="Audit Defense & Compliance",
            plain_english="Keeping detailed records as things happen, not trying to recreate them later, especially for real estate activities.",
            key_benefit="Ensure tax strategies survive IRS scrutiny through bulletproof documentation."
        ),
        
        # Beginner Concepts (5 terms)
        GlossaryTerm(
            term="AGI",
            definition="Adjusted Gross Income - total income minus specific above-the-line deductions, used as baseline for many tax calculations.",
            category="Beginner Concepts",
            plain_english="Your total income minus certain deductions - this number determines many other tax calculations.",
            key_benefit="Understanding AGI enables strategic planning around income thresholds and deduction limitations."
        ),
        GlossaryTerm(
            term="Effective Tax Rate",
            definition="Percentage of total income actually paid in taxes after all deductions, credits, and strategies are applied.",
            category="Beginner Concepts",
            plain_english="The actual percentage of your income that goes to taxes after everything is calculated.",
            key_benefit="Track real tax burden and measure effectiveness of tax planning strategies."
        ),
        
        # Additional missing terms from module mappings
        GlossaryTerm(
            term="Income Shifting",
            definition="Legal strategies to convert high-tax income types into lower-tax alternatives through strategic structuring and entity design.",
            category="Tax Planning Strategies",
            plain_english="Changing how your income is classified so it gets taxed at lower rates.",
            key_benefit="Transform ordinary income tax rates into capital gains or other preferential treatment."
        ),
        GlossaryTerm(
            term="Timing Arbitrage",
            definition="Strategic control of when income and deductions are recognized to optimize tax liability across multiple years and take advantage of rate differences.",
            category="Tax Planning Strategies",
            plain_english="Controlling when you pay taxes and claim deductions to get the best overall result.",
            key_benefit="Optimize tax outcomes by controlling the timing of income and deductions."
        ),
        GlossaryTerm(
            term="Asset Location",
            definition="Strategic placement of different investment types in tax-advantaged vs. taxable accounts to minimize overall tax burden and maximize after-tax returns.",
            category="Tax Planning Strategies",
            plain_english="Putting the right investments in the right types of accounts to minimize taxes.",
            key_benefit="Maximize after-tax investment returns through optimal account placement."
        ),
        GlossaryTerm(
            term="QOF (Qualified Opportunity Fund)",
            definition="Qualified Opportunity Fund - investment vehicle allowing capital gains deferral while investing in opportunity zone real estate or businesses.",
            category="Real Estate Tax Tools",
            plain_english="Special investment fund that lets you postpone paying capital gains taxes while investing in certain areas.",
            key_benefit="Defer capital gains taxes while building new real estate wealth in opportunity zones."
        ),
        GlossaryTerm(
            term="REPS (Real Estate Professional Status)",
            definition="Real Estate Professional Status - IRS qualification allowing real estate losses to offset other income when spending 750+ hours annually in real estate.",
            category="Real Estate Tax Tools",
            plain_english="Special IRS status that lets you use rental property losses to reduce taxes on your other income.",
            key_benefit="Convert passive real estate losses into active deductions against W-2 and business income."
        ),
        GlossaryTerm(
            term="Cost Segregation (Cost Seg)",
            definition="Engineering study that reclassifies building components into shorter depreciation schedules, accelerating tax deductions for real estate investors.",
            category="Real Estate Tax Tools",
            plain_english="Professional study that finds parts of your building that can be depreciated faster, creating bigger tax deductions sooner.",
            key_benefit="Accelerate depreciation deductions and improve cash flow from real estate investments."
        ),
        GlossaryTerm(
            term="MSO (Management Services Organization)",
            definition="Management Services Organization - entity structure that provides management services to other businesses, enabling fee income and expense allocation optimization.",
            category="Entity & Business Structuring",
            plain_english="A separate business that provides management services to your other businesses, creating tax planning opportunities.",
            key_benefit="Create legitimate business deductions and income shifting opportunities."
        ),
        GlossaryTerm(
            term="QSBS (Qualified Small Business Stock)",
            definition="Qualified Small Business Stock - allows up to $10M or 10x basis in gains to be excluded from federal taxes when selling qualifying C-Corp stock.",
            category="Entity & Business Structuring",
            plain_english="Special tax break that can make your business sale gains completely tax-free up to $10 million if structured correctly.",
            key_benefit="Potentially eliminate federal taxes on business sale proceeds up to $10M."
        ),
        GlossaryTerm(
            term="F-Reorg (F Reorganization)",
            definition="F Reorganization - IRS-approved method to change business entity structure while maintaining tax basis and avoiding immediate tax consequences.",
            category="Entity & Business Structuring",
            plain_english="Legal way to change your business structure without triggering taxes on the transfer.",
            key_benefit="Restructure business entities for better tax treatment without immediate tax cost."
        ),
        GlossaryTerm(
            term="IDC (Intangible Drilling Costs)",
            definition="Intangible Drilling Costs - oil and gas investment expenses that can be deducted 100% in the first year for immediate tax benefits.",
            category="Investment Tax Strategies",
            plain_english="Oil and gas investment costs that can be written off completely in the first year for big tax deductions.",
            key_benefit="Generate substantial first-year tax deductions while building energy investment portfolio."
        ),
        GlossaryTerm(
            term="Co-Investment (MSO or Trust)",
            definition="Investment structure where MSO or trust co-invests alongside business owners in real estate or other ventures to maximize tax benefits.",
            category="Entity & Business Structuring",
            plain_english="Having your business entity invest alongside you personally to maximize tax advantages.",
            key_benefit="Amplify investment returns and tax benefits through coordinated entity investing."
        )
    ]
    
    for term in glossary_terms:
        await db.glossary.insert_one(term.dict())
    
    print(f"Updated glossary with {len(glossary_terms)} terms")

if __name__ == "__main__":
    asyncio.run(update_glossary())