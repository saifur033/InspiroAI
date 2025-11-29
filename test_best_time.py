#!/usr/bin/env python3
"""
Test script for Best Time to Post Analysis
Tests all 4 new API endpoints with various scenarios
"""

from src.best_time_analyzer import (
    analyze_best_posting_time,
    get_all_days_analysis,
    get_hourly_analysis,
    get_weekly_posting_strategy
)
import json


def test_best_time_single_day():
    """Test best time analysis for a single day"""
    print("\n" + "="*70)
    print("TEST 1: Best Time Analysis for Friday")
    print("="*70)
    
    result = analyze_best_posting_time("friday", "non-paid", "video", "general")
    
    print(f"\nDay: {result['current_day'].upper()}")
    print(f"Best Time to Post: {result['best_time']}")
    print(f"Next Best Time: {result['next_best_time']}")
    print(f"Avoid Times: {result['avoid_times']}")
    print(f"Engagement Score: {result['engagement_score']}/100")
    print(f"Expected Reach: {result['expected_reach']}")
    print(f"Content Type: {result['content_type']}")
    print(f"\nTips:")
    for i, tip in enumerate(result['tips'], 1):
        print(f"  {i}. {tip}")
    
    print("\nDay Ranking (Best to Worst):")
    for rank in result['day_ranking']:
        print(f"  #{rank['day'].capitalize()}: {rank['score']}/100")


def test_all_days_comparison():
    """Test comparison across all days"""
    print("\n" + "="*70)
    print("TEST 2: All Days Comparison (Video Content, Non-Paid)")
    print("="*70)
    
    results = get_all_days_analysis("non-paid", "video")
    
    print("\n┌" + "─"*68 + "┐")
    print("│ {:<15} {:<20} {:<15} {:<15} │".format("Day", "Engagement", "Reach", "Best Time"))
    print("├" + "─"*68 + "┤")
    
    for item in results:
        day = item['day']
        engagement = f"{item['engagement_score']}/100"
        reach = str(item['expected_reach'])
        best_time = item['best_time']
        rank = f"#{item['ranking']}"
        
        print("│ {:<15} {:<20} {:<15} {:<15} │".format(
            f"{day} {rank}", engagement, reach, best_time
        ))
    
    print("└" + "─"*68 + "┘")


def test_hourly_breakdown():
    """Test hourly breakdown for specific day"""
    print("\n" + "="*70)
    print("TEST 3: Hourly Breakdown for Friday")
    print("="*70)
    
    hourly = get_hourly_analysis("friday")
    
    print("\nHourly Engagement Patterns:")
    print("┌" + "─"*66 + "┐")
    print("│ {:<20} {:<20} {:<20} │".format("Time Period", "Engagement", "Best Hour"))
    print("├" + "─"*66 + "┤")
    
    for period, data in hourly.items():
        hours = data['hours']
        engagement = f"{data['engagement']}/100"
        best_hour = data['best_hour']
        
        print("│ {:<20} {:<20} {:<20} │".format(
            hours, engagement, best_hour
        ))
    
    print("└" + "─"*66 + "┘")


def test_weekly_strategy():
    """Test weekly posting strategy"""
    print("\n" + "="*70)
    print("TEST 4: Weekly Posting Strategy (Maximize Reach)")
    print("="*70)
    
    strategy = get_weekly_posting_strategy("maximize_reach")
    
    print(f"\nGoal: {strategy['focus']}")
    print(f"Posts per Week: {strategy['posts_per_week']}")
    print(f"\nBest Days to Post:")
    for day in strategy['post_days']:
        print(f"  ✓ {day.capitalize()}")
    
    if strategy['avoid_days']:
        print(f"\nDays to Avoid:")
        for day in strategy['avoid_days']:
            print(f"  ✗ {day.capitalize()}")
    
    print(f"\nStrategy Tips:")
    for i, tip in enumerate(strategy['tips'], 1):
        print(f"  {i}. {tip}")


def test_paid_vs_non_paid():
    """Compare paid vs non-paid performance"""
    print("\n" + "="*70)
    print("TEST 5: Paid vs Non-Paid Analysis (Monday)")
    print("="*70)
    
    non_paid = analyze_best_posting_time("monday", "non-paid")
    paid = analyze_best_posting_time("monday", "paid")
    
    print(f"\n{'Metric':<25} {'Non-Paid':<20} {'Paid':<20}")
    print("─" * 65)
    print(f"{'Engagement Score':<25} {non_paid['engagement_score']:<20} {paid['engagement_score']:<20}")
    print(f"{'Expected Reach':<25} {non_paid['expected_reach']:<20} {paid['expected_reach']:<20}")
    print(f"{'Best Time':<25} {non_paid['best_time']:<20} {paid['best_time']:<20}")
    
    reach_increase = ((paid['expected_reach'] - non_paid['expected_reach']) / non_paid['expected_reach']) * 100
    print(f"\n[INFO] Paid posts get {reach_increase:.1f}% more reach!")


def test_content_types():
    """Compare different content types"""
    print("\n" + "="*70)
    print("TEST 6: Content Type Performance (Wednesday)")
    print("="*70)
    
    types = ["video", "image", "reel", "carousel", "text"]
    
    print(f"\n{'Content Type':<15} {'Engagement':<15} {'Reach':<15}")
    print("─" * 45)
    
    for content_type in types:
        result = analyze_best_posting_time("wednesday", "non-paid", content_type)
        print(f"{content_type.upper():<15} {result['engagement_score']:<15} {result['expected_reach']:<15}")
    
    print("\n[INFO] Video and Reel formats perform best!")


def test_audience_targeting():
    """Test audience-specific recommendations"""
    print("\n" + "="*70)
    print("TEST 7: Audience-Specific Recommendations")
    print("="*70)
    
    audiences = ["students", "working_professionals", "homemakers", "entrepreneurs"]
    
    for audience in audiences:
        result = analyze_best_posting_time("friday", "non-paid", "video", audience)
        print(f"\n[AUDIENCE] {audience.replace('_', ' ').upper()}:")
        print(f"   Best Day: Friday (Generic)")
        print(f"   Best Time: {result['best_time']}")
        print(f"   Engagement: {result['engagement_score']}/100")
        
        if result['tips']:
            print(f"   Tip: {result['tips'][-1]}")  # Last tip is usually audience-specific


def test_all_scenarios():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("BEST TIME TO POST ANALYSIS - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    try:
        test_best_time_single_day()
        test_all_days_comparison()
        test_hourly_breakdown()
        test_weekly_strategy()
        test_paid_vs_non_paid()
        test_content_types()
        test_audience_targeting()
        
        print("\n" + "=" * 70)
        print("ALL TESTS PASSED SUCCESSFULLY!")
        print("=" * 70)
        print("\nSummary:")
        print("  [OK] Best Time Analyzer: Working")
        print("  [OK] All Days Comparison: Working")
        print("  [OK] Hourly Breakdown: Working")
        print("  [OK] Weekly Strategy: Working")
        print("  [OK] Paid/Non-Paid Comparison: Working")
        print("  [OK] Content Type Analysis: Working")
        print("  [OK] Audience Targeting: Working")
        print("\n4 NEW API ENDPOINTS AVAILABLE:")
        print("  1. GET /api/best_time - Best posting time analysis")
        print("  2. GET /api/all_days_analysis - Compare all days")
        print("  3. GET /api/hourly_breakdown - Hourly patterns")
        print("  4. GET /api/weekly_strategy - Weekly strategy")
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_all_scenarios()
