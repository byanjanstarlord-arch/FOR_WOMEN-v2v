from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from ai.services import generate_ai_response

def index_view(request):
    """Render the AI Mentor Chat page."""
    return render(request, 'ai_mentor/index.html')

class MentorChatView(APIView):
    def post(self, request):
        user_message = request.data.get('message', '')
        
        system_prompt = (
            "You are Sakhi, an AI Mentor for women in technology. You provide empowering, "
            "actionable, and deeply empathetic career advice. Return a JSON response containing "
            "'reply' (the actual string response) and 'suggested_actions' (list of strings). "
            "Output ONLY valid JSON."
        )
        
        user_prompt = f"User: {user_message}"
        
        result = generate_ai_response(system_prompt, user_prompt)
        
        if not result.get('success', True):
            return Response(result, status=503)
            
        return Response({
            "success": True,
            "data": result
        })
