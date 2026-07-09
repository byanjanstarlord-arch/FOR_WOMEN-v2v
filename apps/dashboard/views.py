from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserStat, RoadmapPhase, AIInsight, RecommendedOpportunity
from django.utils import timezone

def seed_initial_user_data(user):
    # Create Stats
    if not hasattr(user, 'dashboard_stat'):
        UserStat.objects.create(
            user=user,
            career_readiness=85,
            skills_strength=78,
            profile_progress=92,
            ai_score=88,
            day_streak=12
        )
    
    # Create Roadmap if empty
    if not user.roadmap_phases.exists():
        RoadmapPhase.objects.bulk_create([
            RoadmapPhase(user=user, title="Foundation", description="Build strong fundamentals", status="Completed", order=1),
            RoadmapPhase(user=user, title="Skill Building", description="Learn in-demand skills", status="In Progress", order=2),
            RoadmapPhase(user=user, title="Real World Projects", description="Apply your knowledge", status="Upcoming", order=3),
            RoadmapPhase(user=user, title="Career Launch", description="Get ready for opportunities", status="Upcoming", order=4),
        ])
    
    # Create Insights if empty
    if not user.ai_insights.exists():
        AIInsight.objects.bulk_create([
            AIInsight(user=user, title="Your communication skills are strong!", message="Boost them further for leadership roles.", time_ago="2h ago", icon_type="growth"),
            AIInsight(user=user, title="Data Analysis is a high growth skill for you.", message="Consider learning SQL and Python.", time_ago="1d ago", icon_type="trend"),
            AIInsight(user=user, title="You're consistent! 🔥", message="Keep up your daily learning streak.", time_ago="2d ago", icon_type="streak"),
        ])
    
    # Create Opportunities if empty
    if not user.opportunities.exists():
        RecommendedOpportunity.objects.bulk_create([
            RecommendedOpportunity(user=user, title="Data Analyst Intern", company="Microsoft", location="Bangalore, India", type="Internship", time_left="2d left", logo_url="https://logo.clearbit.com/microsoft.com"),
            RecommendedOpportunity(user=user, title="Product Management Intern", company="Google", location="Remote", type="Internship", time_left="5d left", logo_url="https://logo.clearbit.com/google.com"),
            RecommendedOpportunity(user=user, title="AI/ML Virtual Internship", company="SmartBridge", location="Remote", type="Virtual", time_left="7d left", logo_url="https://logo.clearbit.com/smartbridge.com"),
        ])

@login_required
def index_view(request):
    """Render the main dashboard."""
    seed_initial_user_data(request.user)
    
    context = {
        'stats': request.user.dashboard_stat,
        'roadmap_phases': request.user.roadmap_phases.all(),
        'ai_insights': request.user.ai_insights.all()[:3],
        'opportunities': request.user.opportunities.all()[:3]
    }
    
    return render(request, 'dashboard/index.html', context)
