from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ai.services import generate_ai_response

def index_view(request):
    """Render the AI Roadmap page."""
    return render(request, 'roadmap/index.html')

class RoadmapGenerateView(APIView):
    def post(self, request):
        career_goal = request.data.get('career_goal', '')
        timeframe = request.data.get('timeframe', '6 months')
        
        system_prompt = (
            "You are an expert AI Career Planner for women. Create a structured roadmap for the given "
            "career goal and timeframe. Return JSON containing 'milestones' (list of dicts with 'title' and 'description'). "
            "Output ONLY valid JSON."
        )
        
        user_prompt = f"Goal: {career_goal}\nTimeframe: {timeframe}"
        
        result = generate_ai_response(system_prompt, user_prompt)
        
        if not result.get('success', True):
            return Response(result, status=503)
            
        return Response({
            "success": True,
            "data": result
        })
