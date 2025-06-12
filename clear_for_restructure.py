import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def clear_glossary_for_restructure():
    client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
    db = client[os.getenv('DB_NAME', 'test_database')]
    
    # Clear all glossary entries
    result = await db.glossary.delete_many({})
    print(f"✅ Cleared {result.deleted_count} glossary entries")
    
    # Verify empty
    remaining = await db.glossary.find({}).to_list(1000)
    print(f"Remaining entries: {len(remaining)}")
    
    if len(remaining) == 0:
        print("✅ Glossary is now empty and ready for structured format entries")
        print("✅ Updated schema supports: term, definition, category, tags, plain_english, case_study, key_benefit, client_name, structure, implementation, results")
    
    client.close()

asyncio.run(clear_glossary_for_restructure())