from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ai.services import generate_ai_response

def index_view(request):
    """Render the Skill Gap Analysis page."""
    return render(request, 'skill_gap/index.html')

class SkillGapAnalyzeView(APIView):
    def post(self, request):
        current_skills = request.data.get('current_skills', '')
        target_role = request.data.get('target_role', '')
        
        system_prompt = (
            "You are an expert AI Career Strategist for women. Analyze the current skills vs "
            "target role and provide a structured JSON response containing 'missing_skills' (list of strings), "
            "'learning_resources' (list of dicts with 'skill' and 'resource_type'), and "
            "'readiness_percentage' (0-100). Output ONLY valid JSON."
        )
        
        user_prompt = f"Current Skills: {current_skills}\nTarget Role: {target_role}"
        
        result = generate_ai_response(system_prompt, user_prompt)
        
        if not result.get('success', True):
            return Response(result, status=503)
            
        return Response({
            "success": True,
            "data": result
        })
