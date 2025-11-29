"""
Best Time to Post Analysis Module
Analyzes optimal posting times based on day, time, and post type
Provides detailed recommendations with engagement metrics
"""

from datetime import datetime, timedelta
import random


class BestTimeAnalyzer:
    """Analyzes and recommends best posting times for maximum engagement"""
    
    def __init__(self):
        # Engagement scores by day (0-100)
        self.day_scores = {
            "monday": 60,
            "tuesday": 65,
            "wednesday": 70,
            "thursday": 75,
            "friday": 85,
            "saturday": 90,
            "sunday": 80
        }
        
        # Reach base by day
        self.day_reach_base = {
            "monday": 2500,
            "tuesday": 3000,
            "wednesday": 3500,
            "thursday": 4000,
            "friday": 5000,
            "saturday": 6000,
            "sunday": 4500
        }
        
        # Best times by day
        self.best_times = {
            "monday": {"best": "9:00 AM", "next": "2:00 PM", "avoid": "12:00 AM - 7:00 AM"},
            "tuesday": {"best": "8:30 AM", "next": "3:00 PM", "avoid": "12:00 AM - 7:00 AM"},
            "wednesday": {"best": "10:00 AM", "next": "2:30 PM", "avoid": "12:00 AM - 7:00 AM"},
            "thursday": {"best": "9:30 AM", "next": "1:00 PM", "avoid": "12:00 AM - 7:00 AM"},
            "friday": {"best": "11:00 AM", "next": "4:00 PM", "avoid": "12:00 AM - 7:00 AM"},
            "saturday": {"best": "12:00 PM", "next": "7:00 PM", "avoid": "12:00 AM - 8:00 AM"},
            "sunday": {"best": "1:00 PM", "next": "6:00 PM", "avoid": "12:00 AM - 8:00 AM"}
        }
        
        # Content type optimization
        self.content_type_boost = {
            "video": 20,
            "image": 15,
            "carousel": 18,
            "text": 10,
            "link": 12,
            "reel": 25
        }
        
        # Audience type optimization
        self.audience_boost = {
            "students": {"best_day": "friday", "best_time": "8:00 PM"},
            "working_professionals": {"best_day": "monday", "best_time": "9:00 AM"},
            "homemakers": {"best_day": "tuesday", "best_time": "10:00 AM"},
            "entrepreneurs": {"best_day": "thursday", "best_time": "11:00 AM"},
            "general": {"best_day": "friday", "best_time": "11:00 AM"}
        }

    def analyze_best_times(self, day=None, post_type="non-paid", content_type=None, audience=None):
        """
        Comprehensive analysis of best posting times
        
        Args:
            day: Specific day (e.g., 'monday')
            post_type: 'paid' or 'non-paid'
            content_type: 'video', 'image', 'carousel', 'text', 'link', 'reel'
            audience: Target audience type
            
        Returns:
            Dictionary with detailed recommendations
        """
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        
        # Get current day if not specified
        if not day:
            day = datetime.now().strftime("%A").lower()
        
        if day not in days:
            day = "friday"  # Default to Friday if invalid
        
        # Calculate scores
        base_engagement = self.day_scores.get(day, 70)
        base_reach = self.day_reach_base.get(day, 3000)
        
        # Apply modifiers
        paid_boost = 15 if post_type == "paid" else 0
        content_boost = self.content_type_boost.get(content_type, 10) if content_type else 10
        
        engagement_score = min(100, base_engagement + paid_boost + (content_boost * 0.3))
        reach_variance = random.randint(-500, 1000)
        reach = base_reach + reach_variance + (3000 if post_type == "paid" else 500)
        reach = max(100, reach)
        
        times_data = self.best_times.get(day, self.best_times["friday"])
        
        # Rank all days for user
        day_ranking = sorted(self.day_scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "current_day": day,
            "best_time": times_data["best"],
            "next_best_time": times_data["next"],
            "avoid_times": times_data["avoid"],
            "engagement_score": round(engagement_score, 1),
            "expected_reach": reach,
            "post_type": post_type,
            "content_type": content_type or "general",
            "audience": audience or "general",
            "day_ranking": [{"day": d, "score": s} for d, s in day_ranking],
            "tips": self._generate_tips(day, post_type, content_type, audience)
        }
    
    def get_all_days_comparison(self, post_type="non-paid", content_type=None):
        """
        Compare posting performance across all days of the week
        
        Args:
            post_type: 'paid' or 'non-paid'
            content_type: Type of content
            
        Returns:
            List of all days with metrics sorted by engagement
        """
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        results = []
        
        for day in days:
            base_engagement = self.day_scores[day]
            paid_boost = 15 if post_type == "paid" else 0
            content_boost = self.content_type_boost.get(content_type, 10) if content_type else 10
            
            engagement = min(100, base_engagement + paid_boost + (content_boost * 0.3))
            reach = self.day_reach_base[day] + (3000 if post_type == "paid" else 500)
            
            times = self.best_times[day]
            
            results.append({
                "day": day.capitalize(),
                "engagement_score": round(engagement, 1),
                "expected_reach": reach,
                "best_time": times["best"],
                "next_best": times["next"],
                "avoid_times": times["avoid"],
                "ranking": None  # Will be set after sorting
            })
        
        # Sort by engagement score
        results.sort(key=lambda x: x["engagement_score"], reverse=True)
        
        # Add ranking
        for idx, result in enumerate(results, 1):
            result["ranking"] = idx
        
        return results
    
    def get_hourly_breakdown(self, day):
        """
        Get detailed hourly breakdown for a specific day
        Shows engagement levels for each hour
        """
        hours_pattern = {
            "monday": {
                "morning": {"hours": "6 AM - 12 PM", "engagement": 75, "best_hour": "9 AM"},
                "afternoon": {"hours": "12 PM - 5 PM", "engagement": 55, "best_hour": "2 PM"},
                "evening": {"hours": "5 PM - 10 PM", "engagement": 65, "best_hour": "7 PM"},
                "night": {"hours": "10 PM - 12 AM", "engagement": 40, "best_hour": "11 PM"}
            },
            "tuesday": {
                "morning": {"hours": "6 AM - 12 PM", "engagement": 80, "best_hour": "8:30 AM"},
                "afternoon": {"hours": "12 PM - 5 PM", "engagement": 60, "best_hour": "3 PM"},
                "evening": {"hours": "5 PM - 10 PM", "engagement": 70, "best_hour": "7 PM"},
                "night": {"hours": "10 PM - 12 AM", "engagement": 45, "best_hour": "11 PM"}
            },
            "wednesday": {
                "morning": {"hours": "6 AM - 12 PM", "engagement": 85, "best_hour": "10 AM"},
                "afternoon": {"hours": "12 PM - 5 PM", "engagement": 65, "best_hour": "2:30 PM"},
                "evening": {"hours": "5 PM - 10 PM", "engagement": 75, "best_hour": "8 PM"},
                "night": {"hours": "10 PM - 12 AM", "engagement": 50, "best_hour": "11 PM"}
            },
            "thursday": {
                "morning": {"hours": "6 AM - 12 PM", "engagement": 85, "best_hour": "9:30 AM"},
                "afternoon": {"hours": "12 PM - 5 PM", "engagement": 70, "best_hour": "1 PM"},
                "evening": {"hours": "5 PM - 10 PM", "engagement": 80, "best_hour": "7 PM"},
                "night": {"hours": "10 PM - 12 AM", "engagement": 55, "best_hour": "11 PM"}
            },
            "friday": {
                "morning": {"hours": "6 AM - 12 PM", "engagement": 90, "best_hour": "11 AM"},
                "afternoon": {"hours": "12 PM - 5 PM", "engagement": 85, "best_hour": "4 PM"},
                "evening": {"hours": "5 PM - 10 PM", "engagement": 88, "best_hour": "7 PM"},
                "night": {"hours": "10 PM - 12 AM", "engagement": 70, "best_hour": "11 PM"}
            },
            "saturday": {
                "morning": {"hours": "6 AM - 12 PM", "engagement": 85, "best_hour": "10 AM"},
                "afternoon": {"hours": "12 PM - 5 PM", "engagement": 90, "best_hour": "12 PM"},
                "evening": {"hours": "5 PM - 10 PM", "engagement": 95, "best_hour": "7 PM"},
                "night": {"hours": "10 PM - 12 AM", "engagement": 75, "best_hour": "11 PM"}
            },
            "sunday": {
                "morning": {"hours": "6 AM - 12 PM", "engagement": 80, "best_hour": "10 AM"},
                "afternoon": {"hours": "12 PM - 5 PM", "engagement": 85, "best_hour": "1 PM"},
                "evening": {"hours": "5 PM - 10 PM", "engagement": 92, "best_hour": "6 PM"},
                "night": {"hours": "10 PM - 12 AM", "engagement": 70, "best_hour": "11 PM"}
            }
        }
        
        day_lower = day.lower()
        return hours_pattern.get(day_lower, hours_pattern["friday"])
    
    def get_weekly_strategy(self, goal="maximize_reach"):
        """
        Get recommended posting strategy for entire week
        
        Args:
            goal: 'maximize_reach', 'maximize_engagement', 'balanced'
            
        Returns:
            Weekly strategy with recommendations
        """
        strategy = {
            "maximize_reach": {
                "post_days": ["friday", "saturday", "thursday"],
                "avoid_days": ["monday", "tuesday"],
                "posts_per_week": 3,
                "focus": "High-reach days with maximum visibility",
                "tips": [
                    "Post on Friday, Saturday, or Thursday",
                    "Use paid promotion on these days for 3x reach boost",
                    "Use video or reel format for extra engagement",
                    "Post at 11 AM on Friday for maximum reach"
                ]
            },
            "maximize_engagement": {
                "post_days": ["thursday", "friday", "wednesday"],
                "avoid_days": ["sunday", "monday"],
                "posts_per_week": 4,
                "focus": "High-engagement days with audience interaction",
                "tips": [
                    "Thursday, Friday, and Wednesday have highest engagement rates",
                    "Post during morning hours (8 AM - 11 AM)",
                    "Use interactive content (polls, questions, carousels)",
                    "Respond to comments within first hour for algorithm boost"
                ]
            },
            "balanced": {
                "post_days": ["monday", "wednesday", "friday", "sunday"],
                "avoid_days": [],
                "posts_per_week": 4,
                "focus": "Consistent presence with optimal timing",
                "tips": [
                    "Spread posts across week for consistent visibility",
                    "Vary content types throughout week",
                    "Use best times for each specific day",
                    "Mix organic and paid posts strategically"
                ]
            }
        }
        
        return strategy.get(goal, strategy["balanced"])
    
    def _generate_tips(self, day, post_type, content_type, audience):
        """Generate personalized posting tips"""
        tips = []
        
        # Day-specific tips
        day_tips = {
            "monday": "Start the week strong! Monday mornings are good for professional content",
            "tuesday": "Tuesday engagement peaks mid-morning. Great for educational content",
            "wednesday": "Mid-week energy is high! Perfect for interactive content",
            "thursday": "Thursday is one of the best days. Try promotional content",
            "friday": "PEAK DAY! Post during 11 AM slot for maximum reach",
            "saturday": "Weekend audience is active! Post entertainment or lifestyle content",
            "sunday": "Plan ahead for the week. Great for inspirational content"
        }
        
        tips.append(day_tips.get(day, "Post strategically for best results"))
        
        # Content type tips
        if content_type == "video":
            tips.append("Videos get 75% more engagement! Add captions for accessibility")
        elif content_type == "reel":
            tips.append("Reels dominate the algorithm! Post during peak hours")
        elif content_type == "image":
            tips.append("Use high-quality images with bright colors for better performance")
        elif content_type == "carousel":
            tips.append("Carousels get 3x more interactions! Use 3-5 slides")
        
        # Post type tips
        if post_type == "paid":
            tips.append("Paid promotion boosts reach by 3x. Perfect for important announcements")
        else:
            tips.append("Organic reach is good! Build community through consistent posting")
        
        # Audience tips
        if audience == "students":
            tips.append("Post during evening hours (7 PM - 10 PM) for student audience")
        elif audience == "working_professionals":
            tips.append("Early morning (8-9 AM) works best for professional audience")
        
        return tips


def analyze_best_posting_time(day=None, post_type="non-paid", content_type=None, audience=None):
    """
    Quick function to get best posting time recommendations
    
    Args:
        day: Day of week or None for today
        post_type: 'paid' or 'non-paid'
        content_type: Type of content
        audience: Target audience
        
    Returns:
        Dictionary with recommendations
    """
    analyzer = BestTimeAnalyzer()
    return analyzer.analyze_best_times(day, post_type, content_type, audience)


def get_all_days_analysis(post_type="non-paid", content_type=None):
    """Get comparison of all days"""
    analyzer = BestTimeAnalyzer()
    return analyzer.get_all_days_comparison(post_type, content_type)


def get_hourly_analysis(day):
    """Get hourly breakdown for specific day"""
    analyzer = BestTimeAnalyzer()
    return analyzer.get_hourly_breakdown(day)


def get_weekly_posting_strategy(goal="balanced"):
    """Get weekly posting strategy"""
    analyzer = BestTimeAnalyzer()
    return analyzer.get_weekly_strategy(goal)
