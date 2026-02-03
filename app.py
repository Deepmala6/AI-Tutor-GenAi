from flask import Flask, render_template, request, jsonify
from agents import GeneratorAgent, ReviewerAgent, Pipeline
from utils.llm_client import LLMClient
from utils.validators import ValidateInput
from utils.logger import setup_logger
from config import get_config
import json

# Setup
app = Flask(__name__)
config = get_config()
app.config.from_object(config)
logger = setup_logger('app')

# Initialize agents
llm_client = LLMClient()
generator = GeneratorAgent(llm_client)
reviewer = ReviewerAgent(llm_client)
pipeline = Pipeline(generator, reviewer, max_refinements=1)

@app.route('/')
def index():
    """Render the main UI."""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """
    API endpoint to trigger the agent pipeline.
    
    Request JSON:
    {
        "grade": 4,
        "topic": "Types of angles"
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        is_valid, error, cleaned_data = ValidateInput.validate_request(data)
        if not is_valid:
            return jsonify({"error": error}), 400
        
        logger.info(f"Processing request: grade={cleaned_data['grade']}, topic={cleaned_data['topic']}")
        
        # Run pipeline
        result = pipeline.run(
            grade=cleaned_data['grade'],
            topic=cleaned_data['topic']
        )
        
        logger.info(f"Pipeline completed. Status: {result['review_status']}")
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in /api/generate: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/refine', methods=['POST'])
def api_refine():
    """
    API endpoint to generate advanced-level content (refinement).
    
    Request JSON:
    {
        "grade": 10,
        "topic": "Machine learning",
        "previous_content": "..."
    }
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data.get('grade') or not data.get('topic'):
            return jsonify({"error": "Grade and topic are required"}), 400
        
        # Increase grade level for advanced content (max 12)
        advanced_grade = min(int(data['grade']) + 2, 12)
        
        logger.info(f"Refining content: topic={data['topic']}, original_grade={data['grade']}, advanced_grade={advanced_grade}")
        
        # Run pipeline with advanced settings
        result = pipeline.run(
            grade=advanced_grade,
            topic=data['topic'],
            is_refinement=True
        )
        
        logger.info(f"Refinement completed. Status: {result['review_status']}")
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in /api/refine: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    logger.info("Starting AI Tutor Generator")
    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)
