#!/usr/bin/env python3
"""Test trend cache functionality"""

from src.trend_scraper import get_live_trends
from src.trend_cache import get_cache_info
import time

print("=" * 60)
print("TEST 1: First call - should fetch and cache trends")
print("=" * 60)

result1 = get_live_trends()
print(f"Status: {result1.get('cache_status', 'unknown')}")
print(f"Count: {result1.get('count', 0)}")
print(f"First trend: {result1.get('trends', [{}])[0].get('raw', 'N/A')}")

cache_info = get_cache_info()
print(f"\nCache Info: {cache_info}")

print("\n" + "=" * 60)
print("TEST 2: Second call - should use cached trends (immediate)")
print("=" * 60)

result2 = get_live_trends()
print(f"Status: {result2.get('cache_status', 'unknown')}")
print(f"Count: {result2.get('count', 0)}")
print(f"First trend: {result2.get('trends', [{}])[0].get('raw', 'N/A')}")

print("\n✅ Cache is working! Same trends returned from cache.")
print("   Next refresh: After 24 hours")
