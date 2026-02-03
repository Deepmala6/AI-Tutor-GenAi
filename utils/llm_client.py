import openai
from config import get_config
from typing import Optional

class LLMClient:
    """
    Lightweight wrapper for LLM API calls.
    Supports OpenAI and can be extended for other providers.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        config = get_config()
        self.api_key = api_key or config.LLM_API_KEY
        self.model = model or config.LLM_MODEL
        
        if self.api_key:
            openai.api_key = self.api_key
    
    def call(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """
        Call the LLM with a prompt.
        
        Args:
            prompt: The prompt to send to the LLM
            temperature: Creativity level (0-1)
            max_tokens: Maximum response length
        
        Returns:
            LLM response text
        """
        
        if self.model == "mock":
            # For testing
            return self._mock_response(prompt)
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    def _mock_response(self, prompt: str) -> str:
        """Mock response for testing - generates varied content based on topic."""
        import random
        import json
        
        is_review = "review" in prompt.lower()
        is_refine = "refinement" in prompt.lower() or "address these issues" in prompt.lower()
        
        # Extract topic from prompt
        topic = self._extract_topic(prompt)
        
        if is_review:
            # 60% pass, 40% fail for variety
            status = "pass" if random.random() > 0.4 else "fail"
            feedback = []
            if status == "fail":
                feedback = [
                    "Could simplify language further",
                    "Add more real-world examples",
                    "Make it more engaging for the grade level"
                ]
            return json.dumps({
                "status": status,
                "feedback": feedback
            })
        
        # Generate dynamic content based on topic
        if is_refine:
            mcqs = self._generate_mcqs(topic, refined=True)
        else:
            mcqs = self._generate_mcqs(topic, refined=False)
        
        explanation = self._generate_explanation(topic, refined=is_refine)
        
        return json.dumps({
            "explanation": explanation,
            "mcqs": mcqs
        })
    
    def _extract_topic(self, prompt: str) -> str:
        """Extract topic from prompt."""
        if "Topic:" in prompt:
            parts = prompt.split("Topic:")
            if len(parts) > 1:
                topic = parts[1].split("\n")[0].strip()
                return topic
        return "general concept"
    
    def _generate_explanation(self, topic: str, refined: bool = False) -> str:
        """Generate explanation based on topic."""
        import random
        
        explanations = {
            "angle": {
                "basic": "An angle is formed when two rays meet at a point. You see angles everywhere - when you open a door, spread your legs, or turn your head.",
                "refined": "An angle is formed by two rays that share a common starting point called a vertex. Real-world examples include: the angle of an open door (between the door and frame), clock hands showing different times, and the corner where two walls meet. Angles are measured in degrees, where 360 degrees makes a complete rotation."
            },
            "types of angle": {
                "basic": "Angles can be acute (less than 90°), right (exactly 90°), obtuse (between 90° and 180°), or straight (exactly 180°).",
                "refined": "There are four main types of angles. An acute angle is smaller than a right angle (less than 90°) - like a slice of pizza. A right angle is exactly 90° - like a corner of a square. An obtuse angle is between 90° and 180° - wider than a right angle. A straight angle is exactly 180° - a straight line. You can recognize these angles in everyday objects."
            },
            "photosynthesis": {
                "basic": "Photosynthesis is the process where plants use sunlight, water, and carbon dioxide to make food and oxygen.",
                "refined": "Photosynthesis is how plants make their own food using sunlight. Here's the simple process: Plants take in water from soil through their roots and carbon dioxide from air through their leaves. When sunlight hits the leaves, it gives the plant energy to combine these two things into glucose (sugar) which the plant uses as food. As a byproduct, the plant releases oxygen which we breathe. This happens mainly in the leaves where green chlorophyll captures sunlight."
            },
            "fraction": {
                "basic": "A fraction is a part of a whole. It shows how many equal parts you have out of the total number of parts.",
                "refined": "A fraction represents a part of a whole divided into equal pieces. For example, if you cut a pizza into 8 equal slices and eat 3 slices, you've eaten 3/8 of the pizza. The bottom number (8) tells you how many equal parts the whole is divided into - this is called the denominator. The top number (3) tells you how many parts you have - this is called the numerator. Fractions help us measure, compare, and divide things fairly."
            },
            "machine learning": {
                "basic": "Machine learning is a type of artificial intelligence where computers learn from data and experience instead of being programmed for every task.",
                "refined": "Machine learning is a branch of artificial intelligence where computers can learn and improve from experience without being explicitly programmed for every situation. Here's how it works: You give the computer lots of examples (training data), the computer finds patterns in that data, and then it can make predictions or decisions about new data it hasn't seen before. For example, email programs use machine learning to learn which emails are spam by studying thousands of examples. Self-driving cars use machine learning to recognize stop signs, pedestrians, and other cars. Machine learning powers many things you use daily like voice assistants, recommendation systems, and face recognition."
            },
            "stock market": {
                "basic": "The stock market is a place where people buy and sell shares (small pieces) of companies. When you own a share, you own a tiny part of that company and can make money if the company does well.",
                "refined": "The stock market is a system where shares (also called stocks) of publicly-owned companies are traded between buyers and sellers. Here's how it works: A company divides itself into many equal parts called shares. When you buy a share, you become a partial owner of that company. If the company grows and becomes more valuable, your share becomes worth more money - you can sell it for a profit. The stock market helps companies raise money to expand, and it gives regular people a way to invest and build wealth. Stock prices go up and down based on supply and demand - when more people want to buy a stock, its price rises; when people want to sell, it falls. The most famous stock markets are the NYSE (New York Stock Exchange) and NASDAQ."
            },
            "democracy": {
                "basic": "Democracy is a form of government where power rests with the people. Citizens have a say in decisions through voting and participation.",
                "refined": "Democracy is a system of government where power ultimately rests with the people. In a democratic system, citizens have the right to vote in elections to choose their leaders and influence major decisions. There are different types of democracy: direct democracy (where citizens vote on every issue) and representative democracy (where citizens elect representatives to make decisions on their behalf). Key features include: free and fair elections, freedom of speech and press, rule of law, and protection of individual rights. Democracy encourages peaceful transfer of power and allows for change through elections rather than force."
            },
            "water cycle": {
                "basic": "The water cycle is how water moves around Earth. It evaporates from oceans and lakes, forms clouds, falls as rain, and returns to the ocean.",
                "refined": "The water cycle, also called the hydrological cycle, is the continuous movement of water around Earth. It has four main stages: Evaporation - Sun heats water in oceans and lakes, turning it into invisible water vapor. Condensation - As vapor rises and cools in the atmosphere, it turns back into liquid water droplets, forming clouds. Precipitation - Water falls from clouds as rain, snow, or hail. Collection - Water collects in oceans, lakes, and groundwater, and the cycle repeats. This cycle is essential for all life on Earth because it distributes fresh water across the planet and drives weather patterns."
            },
            "gravity": {
                "basic": "Gravity is a force that pulls objects toward each other. It's what keeps you on the ground and makes things fall down.",
                "refined": "Gravity is a fundamental force in the universe that attracts all objects with mass toward each other. Every object, from planets to people, has gravity - but larger objects have much stronger gravity. Earth's gravity is what pulls us toward the ground and keeps us from floating away. The strength of gravity depends on two things: how much mass an object has (more mass = stronger gravity) and the distance between objects (the farther apart they are, the weaker the pull). Gravity holds planets in orbit around stars and holds galaxies together. It's also the reason objects fall down when you drop them - you're not falling down, Earth is pulling you down."
            }
        }
        
        topic_lower = topic.lower()
        for key, explanation_dict in explanations.items():
            if key in topic_lower:
                if refined:
                    return explanation_dict["refined"]
                return explanation_dict["basic"]
        
        # Default for unknown topics
        if refined:
            return f"{topic.title()} is an important concept that helps us understand the world better. It has practical applications in many fields and real-world examples that demonstrate its value. Understanding {topic} involves both theory and practical experience."
        return f"Here is an explanation about {topic}. This concept is important to understand because it helps us learn and grow."
    
    def _generate_mcqs(self, topic: str, refined: bool = False) -> list:
        """Generate MCQs based on topic with randomized correct answers."""
        import random
        
        topic_lower = topic.lower()
        
        if "angle" in topic_lower:
            questions = [
                {
                    "question": "What is an angle?",
                    "base_options": ["A shape", "Two rays meeting at a point", "A line segment", "A circle"],
                    "answer_index": 1
                },
                {
                    "question": "What is the point where two rays meet called?",
                    "base_options": ["Edge", "Vertex", "Center", "Endpoint"],
                    "answer_index": 1
                },
                {
                    "question": "How many degrees is a right angle?",
                    "base_options": ["45", "90", "180", "360"],
                    "answer_index": 1
                }
            ]
        elif "photosynthesis" in topic_lower:
            questions = [
                {
                    "question": "What do plants use to make food?",
                    "base_options": ["Water only", "Sunlight, water, and carbon dioxide", "Soil only", "Air only"],
                    "answer_index": 1
                },
                {
                    "question": "What gas do plants release during photosynthesis?",
                    "base_options": ["Carbon dioxide", "Oxygen", "Nitrogen", "Hydrogen"],
                    "answer_index": 1
                },
                {
                    "question": "Where does photosynthesis happen?",
                    "base_options": ["Roots", "Stem", "Leaves", "Flowers"],
                    "answer_index": 2
                }
            ]
        elif "fraction" in topic_lower:
            questions = [
                {
                    "question": "What does the bottom number in a fraction mean?",
                    "base_options": ["Total parts", "Number of parts", "How many we have", "The answer"],
                    "answer_index": 0
                },
                {
                    "question": "What is 1/2 of 8?",
                    "base_options": ["4", "16", "8", "2"],
                    "answer_index": 0
                },
                {
                    "question": "Which fraction is the largest?",
                    "base_options": ["1/4", "1/2", "1/3", "1/5"],
                    "answer_index": 1
                }
            ]
        elif "machine learning" in topic_lower:
            questions = [
                {
                    "question": "What is machine learning?",
                    "base_options": ["A programming language", "Computers learning from data without explicit programming", "A type of robot", "A math formula"],
                    "answer_index": 1
                },
                {
                    "question": "Which is an example of machine learning?",
                    "base_options": ["A calculator", "Email spam detection", "A dictionary", "A clock"],
                    "answer_index": 1
                },
                {
                    "question": "What do machine learning algorithms need to work?",
                    "base_options": ["No data", "Only programming code", "Training data (examples)", "Only mathematical formulas"],
                    "answer_index": 2
                }
            ]
        elif "stock market" in topic_lower:
            questions = [
                {
                    "question": "What is the stock market?",
                    "base_options": ["A farmer's market selling vegetables", "A system where people buy and sell shares of companies", "A bank that lends money", "A place to exchange currency"],
                    "answer_index": 1
                },
                {
                    "question": "What do you own when you buy a share of stock?",
                    "base_options": ["A building", "A small piece of the company", "A job in the company", "The entire company"],
                    "answer_index": 1
                },
                {
                    "question": "What causes a stock price to go up?",
                    "base_options": ["Government decision", "More people wanting to buy it than sell it", "Always stays the same", "Only bad news"],
                    "answer_index": 1
                }
            ]
        elif "democracy" in topic_lower:
            questions = [
                {
                    "question": "What is democracy?",
                    "base_options": ["A type of currency", "A system where people have a say in government through voting", "A type of sport", "A mathematical equation"],
                    "answer_index": 1
                },
                {
                    "question": "What is one key feature of democracy?",
                    "base_options": ["One person makes all decisions", "Free and fair elections", "No one has rights", "People have no voice"],
                    "answer_index": 1
                },
                {
                    "question": "What does 'voting' mean in a democracy?",
                    "base_options": ["Staying silent", "Choosing leaders or decisions", "Arguing without voting", "Following without choice"],
                    "answer_index": 1
                }
            ]
        elif "water cycle" in topic_lower:
            questions = [
                {
                    "question": "What is the first stage of the water cycle?",
                    "base_options": ["Condensation", "Evaporation", "Precipitation", "Collection"],
                    "answer_index": 1
                },
                {
                    "question": "What happens during condensation?",
                    "base_options": ["Water is heated", "Water vapor turns into liquid water", "Water falls from sky", "Water freezes"],
                    "answer_index": 1
                },
                {
                    "question": "Which of these is an example of precipitation?",
                    "base_options": ["Evaporation", "Sunshine", "Rain or snow", "Wind"],
                    "answer_index": 2
                }
            ]
        elif "gravity" in topic_lower:
            questions = [
                {
                    "question": "What is gravity?",
                    "base_options": ["A type of color", "A force that pulls objects toward each other", "A type of weather", "A type of speed"],
                    "answer_index": 1
                },
                {
                    "question": "What causes objects to fall down?",
                    "base_options": ["Wind", "Gravity", "Friction", "Magnetism"],
                    "answer_index": 1
                },
                {
                    "question": "Why does the Moon orbit Earth?",
                    "base_options": ["The Moon is stuck", "Earth's gravity pulls it", "The Moon chooses to", "There's no reason"],
                    "answer_index": 1
                }
            ]
        else:
            # Generic questions
            questions = [
                {
                    "question": f"What is a {topic}?",
                    "base_options": ["A concept", "Not important", "Something to learn", "All of the above"],
                    "answer_index": 0
                },
                {
                    "question": f"Why do we study {topic}?",
                    "base_options": ["For fun", "To understand the world", "Because we must", "No reason"],
                    "answer_index": 1
                },
                {
                    "question": f"Can you explain {topic} simply?",
                    "base_options": ["No", "Yes, it's understandable", "Maybe", "Never"],
                    "answer_index": 1
                }
            ]
        
        # Build MCQs with randomized option positions
        mcqs = []
        for q in questions:
            options = q["base_options"].copy()
            answer = options[q["answer_index"]]
            random.shuffle(options)
            new_answer_index = options.index(answer)
            
            mcqs.append({
                "question": q["question"],
                "options": options,
                "answer": answer
            })
        
        return mcqs
