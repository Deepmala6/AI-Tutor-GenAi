# AI Tutor Generator

A lightweight, AI-powered system for generating and reviewing educational content. The system uses two specialized agents to create quality educational materials.

## Features

✨ **Two-Agent Pipeline**
- **Generator Agent**: Creates educational content (explanations + MCQs) tailored to specific grades
- **Reviewer Agent**: Evaluates content for age-appropriateness, correctness, and clarity
- **Automatic Refinement**: Refines content based on reviewer feedback (one pass)

🎯 **Smart UI**
- Clean, intuitive interface
- Visual pipeline flow showing: Generate → Review → (Optional) Refine
- Real-time feedback and results display
- Mobile-responsive design

🚀 **Production-Ready**
- Modular, scalable architecture
- Structured input/output validation
- Error handling and logging
- Comprehensive test suite

## Project Structure

```
AI-Tutor-Generator/
├── app.py                          # Flask application
├── config.py                        # Configuration management
├── requirements.txt                 # Dependencies
├── README.md                        # This file
│
├── agents/                          # Agent implementations
│   ├── generator.py                 # Generator Agent
│   ├── reviewer.py                  # Reviewer Agent
│   └── pipeline.py                  # Pipeline orchestration
│
├── utils/                           # Utility modules
│   ├── llm_client.py               # LLM API wrapper
│   ├── validators.py               # Input/output validation
│   └── logger.py                    # Logging setup
│
├── static/                          # Frontend assets
│   ├── css/style.css               # Styling
│   └── js/script.js                # Client-side logic
│
├── templates/                       # HTML templates
│   └── index.html                  # Main UI
│
└── tests/                           # Test suite
    ├── test_generator.py           # Generator tests
    ├── test_reviewer.py            # Reviewer tests
    └── test_pipeline.py            # Pipeline tests
```

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key (or use mock for testing)

### Setup

1. **Clone the repository**
```bash
cd "AI Tutor Generator"
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=gpt-3.5-turbo
FLASK_ENV=development
```

## Usage

### Running the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

### API Endpoint

**POST /api/generate**

Request:
```json
{
    "grade": 4,
    "topic": "Types of angles"
}
```

Response:
```json
{
    "generated_content": {
        "explanation": "...",
        "mcqs": [...]
    },
    "review_status": "pass|fail",
    "review_feedback": ["feedback items"],
    "refined_content": null,
    "refinement_applied": false
}
```

### Running Tests

```bash
pytest tests/
```

With coverage:
```bash
pytest tests/ --cov=agents --cov=utils
```

## Agent Definitions

### Generator Agent

**Responsibility**: Generate draft educational content for a given grade and topic

**Input**:
```json
{
    "grade": 4,
    "topic": "Types of angles"
}
```

**Output**:
```json
{
    "explanation": "Clear, grade-appropriate explanation",
    "mcqs": [
        {
            "question": "Question text",
            "options": ["A", "B", "C", "D"],
            "answer": "B"
        }
    ]
}
```

**Key Features**:
- Grade-level language adaptation
- Conceptually correct content
- Deterministic output structure
- Support for refinement feedback

### Reviewer Agent

**Responsibility**: Evaluate content for quality and appropriateness

**Input**:
- Content JSON from Generator Agent
- Grade level and topic context

**Output**:
```json
{
    "status": "pass|fail",
    "feedback": [
        "Specific issue with location",
        "Another specific issue"
    ]
}
```

**Evaluation Criteria**:
- Age-appropriateness (language level, concepts)
- Conceptual correctness (no misinformation)
- Clarity (understandability, structure)

## Configuration

Edit `config.py` to customize:

```python
class DevelopmentConfig(Config):
    LLM_MODEL = 'gpt-3.5-turbo'        # LLM to use
    MAX_REFINEMENTS = 1                # Maximum refinement passes
```

## Supported Grade Levels

- Grade 4 (9-10 years): Simple, concrete language
- Grade 6 (11-12 years): Clear, age-appropriate
- Grade 8 (13-14 years): Moderate complexity
- Grade 10 (15-16 years): Complex concepts

## Error Handling

The system handles:
- Invalid input (missing fields, wrong types)
- LLM API failures
- Malformed responses
- Missing configuration

All errors are logged and returned with descriptive messages.

## Performance

- **Generator**: ~3-5 seconds (LLM dependent)
- **Reviewer**: ~2-3 seconds (LLM dependent)
- **Pipeline**: ~5-10 seconds including refinement
- **UI Response**: Instant with loading indicator

## Dependencies

- **Flask**: Web framework
- **OpenAI**: LLM API
- **python-dotenv**: Environment configuration
- **Pydantic**: Data validation
- **Pytest**: Testing

## Development

### Adding Custom LLM Provider

Extend `utils/llm_client.py`:
```python
def call(self, prompt: str) -> str:
    # Your custom LLM call
    pass
```

### Extending Agents

Create new agents by inheriting the base pattern:
```python
class CustomAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def process(self, input_data):
        # Process logic
        pass
```

## Future Enhancements

- [ ] Support for different content types (videos, exercises)
- [ ] Multi-language support
- [ ] User authentication
- [ ] Content history and analytics
- [ ] Advanced refinement with multiple iterations
- [ ] Integration with learning management systems

## Author

**Deepmala Bhakta**  
AI Engineer | Vadodara, Gujarat, India  
📧 deepmalab65@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/deepmala-bhakta-80267b2b8/)  
🔗 [GitHub](https://github.com/Deepmala6)

## License

MIT License - feel free to use this project!

## Support

For issues or suggestions, please reach out via email or create a GitHub issue.

---

**Created**: February 2026  
**Version**: 1.0.0
"# AI-Tutor-GenAi" 
