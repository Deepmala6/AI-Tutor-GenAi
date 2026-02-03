import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents import GeneratorAgent
from utils.llm_client import LLMClient

@pytest.fixture
def mock_llm():
    return LLMClient(model='mock')

@pytest.fixture
def generator(mock_llm):
    return GeneratorAgent(mock_llm)

def test_generator_output_structure(generator):
    """Test that generator output has correct structure."""
    result = generator.generate(grade=4, topic="Types of angles")
    
    assert isinstance(result, dict)
    assert "explanation" in result
    assert "mcqs" in result
    assert isinstance(result["explanation"], str)
    assert isinstance(result["mcqs"], list)

def test_generator_mcq_structure(generator):
    """Test that MCQs have correct structure."""
    result = generator.generate(grade=4, topic="Types of angles")
    
    if result["mcqs"]:
        mcq = result["mcqs"][0]
        assert "question" in mcq
        assert "options" in mcq
        assert "answer" in mcq
        assert len(mcq["options"]) >= 2
        assert mcq["answer"] in mcq["options"]

def test_generator_with_feedback(generator):
    """Test that generator accepts feedback for refinement."""
    feedback = "The explanation is too complex for Grade 4"
    result = generator.generate(
        grade=4, 
        topic="Types of angles",
        feedback=feedback
    )
    
    assert isinstance(result, dict)
    assert "explanation" in result
