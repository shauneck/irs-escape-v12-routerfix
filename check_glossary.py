import requests

# Get glossary terms
response = requests.get('http://localhost:8001/api/glossary')
terms = response.json()

print(f'Total glossary terms: {len(terms)}')

# Count by category
categories = {}
for term in terms:
    category = term.get('category', 'Unknown')
    if category in categories:
        categories[category] += 1
    else:
        categories[category] = 1

print('\nGlossary terms by category:')
for category, count in sorted(categories.items()):
    print(f'- {category}: {count} terms')

# Print sample terms
print('\nSample terms:')
for i, term in enumerate(terms[:10]):
    print(f"{i+1}. {term.get('term')} ({term.get('category')})")

# Test search functionality
test_terms = ["REPS", "W-2", "QOF", "STR", "Cost Segregation"]
print('\nSearch results:')
for term in test_terms:
    search_response = requests.get(f'http://localhost:8001/api/glossary/search?q={term}')
    results = search_response.json()
    print(f"- '{term}': {len(results)} results found")
    if results:
        print(f"  First result: {results[0].get('term')}")