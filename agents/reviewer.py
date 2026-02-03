from typing import Dict, List, Any
from utils.llm_client import LLMClient
import json

class ReviewerAgent:
    """
    Evaluates Generator output for:
    - Age appropriateness
    - Conceptual correctness
    - Clarity
    
    Input: {"explanation": str, "mcqs": List[Dict]}
    Output: {"status": "pass|fail", "feedback": List[str]}
    """
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
    
    def review(self, content: Dict[str, Any], grade: int, topic: str) -> Dict[str, Any]:
        """
        Review generated content.
        
        Args:
            content: Output from GeneratorAgent
            grade: Grade level
            topic: Topic being taught
        
        Returns:
            Dictionary with 'status' and 'feedback'
        """
        
        prompt = self._build_prompt(content, grade, topic)
        response = self.llm_client.call(prompt)
        
        review_result = self._parse_response(response)
        
        return review_result
    
    def _build_prompt(self, content: Dict[str, Any], grade: int, topic: str) -> str:
        """Build the review prompt."""
        
        content_str = json.dumps(content, indent=2)
        
        prompt = f"""You are an expert educational content reviewer.

Grade Level: {grade}
Topic: {topic}

Review this educational content for:
1. **Age Appropriateness**: Is language suitable for the grade?
2. **Conceptual Correctness**: Are the concepts accurate and well-explained?
3. **Clarity**: Is the content clear and understandable?

Content to Review:
{content_str}

Respond with ONLY this JSON format:
{{
    "status": "pass or fail",
    "feedback": [
        "Issue 1 with specific location",
        "Issue 2 with specific location"
    ]
}}

If all checks pass, set status to "pass" with empty feedback list.
If any issue found, set status to "fail" with specific feedback."""
        
        return prompt
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse reviewer response."""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                result = json.loads(json_str)
                
                # Ensure proper structure
                status = result.get("status", "pass").lower()
                feedback = result.get("feedback", [])
                
                # Ensure feedback is a list
                if not isinstance(feedback, list):
                    feedback = [str(feedback)] if feedback else []
                
                return {
                    "status": "pass" if status == "pass" else "fail",
                    "feedback": feedback
                }
        except (json.JSONDecodeError, KeyError):
            pass
        
        return {
            "status": "pass",
            "feedback": []
        }
