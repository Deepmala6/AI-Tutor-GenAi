import json
from typing import Dict, List, Any
from utils.llm_client import LLMClient
from utils.validators import ValidateGeneratorOutput

class GeneratorAgent:
    """
    Generates draft educational content for a given grade and topic.
    
    Input: {"grade": int, "topic": str, "feedback": str (optional)}
    Output: {"explanation": str, "mcqs": List[Dict]}
    """
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.validator = ValidateGeneratorOutput()
    
    def generate(self, grade: int, topic: str, feedback: str = None, is_advanced: bool = False) -> Dict[str, Any]:
        """
        Generate educational content.
        
        Args:
            grade: Grade level (e.g., 4, 8, 10)
            topic: Topic to generate content for
            feedback: Optional feedback from reviewer for refinement
            is_advanced: If True, generate advanced/detailed content
        
        Returns:
            Dictionary with 'explanation' and 'mcqs'
        """
        
        prompt = self._build_prompt(grade, topic, feedback, is_advanced)
        
        # Call LLM
        response = self.llm_client.call(prompt)
        
        # Parse and validate
        content = self._parse_response(response)
        
        # Ensure structured output
        validated = self.validator.validate(content)
        
        return validated
    
    def _build_prompt(self, grade: int, topic: str, feedback: str = None, is_advanced: bool = False) -> str:
        """Build the prompt for the LLM."""
        
        grade_description = {
            4: "Grade 4 (9-10 years old): Simple, concrete language. Short sentences. Familiar examples.",
            6: "Grade 6 (11-12 years old): Clear, age-appropriate. Some technical terms. Engaging examples.",
            8: "Grade 8 (13-14 years old): Moderate complexity. Technical terms with explanations. Real-world applications.",
            10: "Grade 10 (15-16 years old): Complex concepts. Technical language. Abstract reasoning.",
            12: "Grade 12 (17-18 years old): Advanced concepts. Deep technical analysis. Complex reasoning required."
        }
        
        base_prompt = f"""You are an expert educational content creator.

Grade Level: {grade_description.get(grade, 'Grade 4')}
Topic: {topic}
Content Type: {'ADVANCED/DETAILED' if is_advanced else 'STANDARD'}

Generate educational content with:
1. A clear, grade-appropriate explanation
2. 3 multiple-choice questions (MCQs) with 4 options each

Return ONLY valid JSON in this format:
{{
    "explanation": "Clear explanation suitable for the grade level",
    "mcqs": [
        {{
            "question": "Question text",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "answer": "Option A"
        }}
    ]
}}"""
        
        if feedback:
            base_prompt += f"\n\nRefinement feedback from reviewer:\n{feedback}\n\nPlease address these issues."
        
        return base_prompt
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response to JSON."""
        try:
            # Try to extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        # Fallback structure
        return {
            "explanation": response,
            "mcqs": []
        }
