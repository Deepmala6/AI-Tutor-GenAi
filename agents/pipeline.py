from typing import Dict, Any
from .generator import GeneratorAgent
from .reviewer import ReviewerAgent

class Pipeline:
    """
    Orchestrates the Generator -> Reviewer -> (Optional) Refinement pipeline.
    """
    
    def __init__(self, generator: GeneratorAgent, reviewer: ReviewerAgent, max_refinements: int = 1):
        self.generator = generator
        self.reviewer = reviewer
        self.max_refinements = max_refinements
    
    def run(self, grade: int, topic: str, is_refinement: bool = False) -> Dict[str, Any]:
        """
        Run the complete pipeline: Generate -> Review -> Refine (if needed).
        
        Args:
            grade: Grade level
            topic: Topic for content generation
            is_refinement: If True, generate advanced/refined content
        
        Returns:
            Dictionary with:
            - generated_content: Initial output
            - review_status: Pass/Fail
            - review_feedback: Feedback list
            - refined_content: Refined output (if applicable)
            - refinement_applied: Boolean
        """
        
        # Step 1: Generate
        if is_refinement:
            # Generate advanced-level content with refinement flag
            generated_content = self.generator.generate(grade, topic, is_advanced=True)
        else:
            generated_content = self.generator.generate(grade, topic)
        
        # Step 2: Review
        review_result = self.reviewer.review(generated_content, grade, topic)
        
        result = {
            "generated_content": generated_content,
            "review_status": review_result["status"],
            "review_feedback": review_result["feedback"],
            "refined_content": None,
            "refinement_applied": False
        }
        
        # Step 3: Refine if needed (only when not already in refinement mode)
        if not is_refinement and review_result["status"] == "fail" and self.max_refinements > 0:
            feedback_text = "\n".join(review_result["feedback"])
            refined_content = self.generator.generate(grade, topic, feedback=feedback_text)
            
            result["refined_content"] = refined_content
            result["refinement_applied"] = True
        
        return result
