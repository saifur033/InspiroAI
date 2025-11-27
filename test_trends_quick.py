from src.trend_scraper import get_live_trends

data = get_live_trends()
print(f"Trends count: {len(data.get('trends', []))}")
print(f"First 3 trends:")
for t in data.get('trends', [])[:3]:
    print(f"  - {t['raw']} ({t['category']}) - {t['momentum']}")
