from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ai.services import generate_ai_response

def index_view(request):
    """Render the main Assessment page."""
    return render(request, 'assessment/index.html')

class AssessmentAnalyzeView(APIView):
    def post(self, request):
        user_data = request.data.get('answers', {})
        
        system_prompt = (
            "You are an expert AI Career Architect for women. Analyze the following assessment data "
            "and provide a structured JSON response containing a 'career_score' (0-100), "
            "'strengths' (list of strings), and 'areas_for_improvement' (list of strings). "
            "Output ONLY valid JSON."
        )
        
        user_prompt = f"Assessment data: {user_data}"
        
        result = generate_ai_response(system_prompt, user_prompt)
        
        if not result.get('success', True):
            # The AI service returns success: False on failure
            return Response(result, status=503)
            
        return Response({
            "success": True,
            "data": result
        })
