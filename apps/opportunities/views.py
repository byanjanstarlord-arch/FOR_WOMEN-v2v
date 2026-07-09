from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ai.services import generate_ai_response

def index_view(request):
    """Render the Opportunities Hub page."""
    return render(request, 'opportunities/index.html')

class OpportunityMatchView(APIView):
    def post(self, request):
        skills = request.data.get('skills', '')
        preferences = request.data.get('preferences', '')
        
        system_prompt = (
            "You are an expert AI Career Matchmaker for women in tech. Based on the skills "
            "and preferences provided, recommend 3 specific opportunity types (e.g., specific "
            "internships, remote roles, open source programs, or scholarships). "
            "Return JSON containing 'opportunities' (list of dicts with 'title', 'company_or_type', and 'why_it_fits'). "
            "Output ONLY valid JSON."
        )
        
        user_prompt = f"Skills: {skills}\nPreferences: {preferences}"
        
        result = generate_ai_response(system_prompt, user_prompt)
        
        if not result.get('success', True):
            return Response(result, status=503)
            
        return Response({
            "success": True,
            "data": result
        })
