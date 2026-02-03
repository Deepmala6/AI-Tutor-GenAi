import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents import ReviewerAgent
from utils.llm_client import LLMClient

@pytest.fixture
def mock_llm():
    return LLMClient(model='mock')

@pytest.fixture
def reviewer(mock_llm):
    return ReviewerAgent(mock_llm)

def test_reviewer_output_structure(reviewer):
    """Test that reviewer output has correct structure."""
    content = {
        "explanation": "An angle is formed by two rays.",
        "mcqs": [
            {
                "question": "What is an angle?",
                "options": ["A shape", "A measure of rotation", "A line", "A point"],
                "answer": "A measure of rotation"
            }
        ]
    }
    
    result = reviewer.review(content, grade=4, topic="Types of angles")
    
    assert isinstance(result, dict)
    assert "status" in result
    assert "feedback" in result
    assert result["status"] in ["pass", "fail"]
    assert isinstance(result["feedback"], list)

def test_reviewer_feedback_format(reviewer):
    """Test that feedback is properly formatted."""
    content = {
        "explanation": "X" * 1000,  # Very long explanation
        "mcqs": []
    }
    
    result = reviewer.review(content, grade=4, topic="Types of angles")
    
    assert isinstance(result["feedback"], list)
    for feedback in result["feedback"]:
        assert isinstance(feedback, str)
