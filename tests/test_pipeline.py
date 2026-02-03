import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents import GeneratorAgent, ReviewerAgent, Pipeline
from utils.llm_client import LLMClient

@pytest.fixture
def mock_llm():
    return LLMClient(model='mock')

@pytest.fixture
def pipeline(mock_llm):
    generator = GeneratorAgent(mock_llm)
    reviewer = ReviewerAgent(mock_llm)
    return Pipeline(generator, reviewer, max_refinements=1)

def test_pipeline_execution(pipeline):
    """Test complete pipeline execution."""
    result = pipeline.run(grade=4, topic="Types of angles")
    
    assert "generated_content" in result
    assert "review_status" in result
    assert "review_feedback" in result
    assert "refined_content" in result
    assert "refinement_applied" in result

def test_pipeline_refinement_flag(pipeline):
    """Test that refinement_applied flag is set correctly."""
    result = pipeline.run(grade=4, topic="Types of angles")
    
    assert isinstance(result["refinement_applied"], bool)
    
    if result["review_status"] == "pass":
        assert result["refinement_applied"] == False
    # If fail, refinement_applied may be True if refinement runs

def test_pipeline_output_structure(pipeline):
    """Test that pipeline output has required structure."""
    result = pipeline.run(grade=4, topic="Types of angles")
    
    generated = result["generated_content"]
    assert "explanation" in generated
    assert "mcqs" in generated
    
    if result["refined_content"]:
        refined = result["refined_content"]
        assert "explanation" in refined
        assert "mcqs" in refined
