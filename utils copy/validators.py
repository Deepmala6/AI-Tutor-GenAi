from typing import Dict, Any, List

class ValidateGeneratorOutput:
    """Validates and cleans Generator Agent output."""
    
    def validate(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure output has required structure and fields.
        
        Args:
            content: Raw content from Generator
        
        Returns:
            Validated content dictionary
        """
        
        # Ensure explanation exists
        explanation = content.get("explanation", "")
        if not isinstance(explanation, str):
            explanation = str(explanation)
        
        # Ensure MCQs list exists and is valid
        mcqs = content.get("mcqs", [])
        if not isinstance(mcqs, list):
            mcqs = []
        
        # Validate each MCQ
        validated_mcqs = []
        for mcq in mcqs:
            validated_mcq = self._validate_mcq(mcq)
            if validated_mcq:
                validated_mcqs.append(validated_mcq)
        
        return {
            "explanation": explanation,
            "mcqs": validated_mcqs
        }
    
    def _validate_mcq(self, mcq: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single MCQ."""
        
        if not isinstance(mcq, dict):
            return None
        
        question = mcq.get("question", "")
        options = mcq.get("options", [])
        answer = mcq.get("answer", "")
        
        # Validate required fields
        if not question or not options or not answer:
            return None
        
        # Ensure options is a list with 4 items
        if not isinstance(options, list) or len(options) < 2:
            return None
        
        options = options[:4]  # Limit to 4 options
        
        # Ensure answer is in options
        if answer not in options:
            answer = options[0]  # Fallback to first option
        
        return {
            "question": str(question),
            "options": [str(opt) for opt in options],
            "answer": str(answer)
        }


class ValidateInput:
    """Validates user input for the pipeline."""
    
    @staticmethod
    def validate_request(data: Dict[str, Any]) -> tuple[bool, str, Dict[str, Any]]:
        """
        Validate API request.
        
        Args:
            data: Request data
        
        Returns:
            (is_valid, error_message, cleaned_data)
        """
        
        # Check required fields
        if "grade" not in data or "topic" not in data:
            return False, "Missing required fields: grade, topic", {}
        
        grade = data.get("grade")
        topic = data.get("topic")
        
        # Validate grade
        if not isinstance(grade, int) or grade < 1 or grade > 12:
            return False, "Grade must be an integer between 1 and 12", {}
        
        # Validate topic
        if not isinstance(topic, str) or len(topic.strip()) < 3:
            return False, "Topic must be a non-empty string (min 3 characters)", {}
        
        return True, "", {
            "grade": grade,
            "topic": topic.strip()
        }
