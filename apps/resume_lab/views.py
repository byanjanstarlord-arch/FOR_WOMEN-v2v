from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ai.services import generate_ai_response

def index_view(request):
    """Render the main Resume Lab page."""
    return render(request, 'resume_lab/index.html')

class ResumeAnalyzeView(APIView):
    def post(self, request):
        resume_text = request.data.get('resume_text', '')
        
        system_prompt = (
            "You are an expert AI Resume Analyst for women. Analyze the following resume text "
            "and provide a structured JSON response containing an 'ats_score' (0-100), "
            "'improvements' (list of strings), and 'action_verbs_used' (list of strings). "
            "Output ONLY valid JSON."
        )
        
        user_prompt = f"Resume Text: {resume_text}"
        
        result = generate_ai_response(system_prompt, user_prompt)
        
        if not result.get('success', True):
            return Response(result, status=503)
            
        return Response({
            "success": True,
            "data": result
        })
