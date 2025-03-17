"""
Question generator for the Quiz Generator package.

This module contains the AnthropicQuestionGenerator class for generating questions.
"""

import json
import logging
from typing import Dict, Any, List, Optional, Union

from ..models.question_models import (
    BaseQuestion,
    MultipleChoiceQuestion,
    TrueFalseQuestion,
    ClozeQuestion
)
from ..prompts.multiple_choice_prompts import get_multiple_choice_prompt
from ..prompts.true_false_prompts import get_true_false_prompt
from ..prompts.cloze_prompts import get_cloze_prompt
from ..utils.host_agent import get_host_agent_response, clean_json_response

# Get the logger
logger = logging.getLogger("quiz_generator")


class AnthropicQuestionGenerator:
    """
    A class that generates questions using Anthropic's API.
    
    This class creates prompts for the Anthropic model to generate questions based on the provided parameters.
    """
    
    def __init__(self, client=None):
        """
        Initialize the AnthropicQuestionGenerator.
        
        Args:
            client: An optional Anthropic client instance
        """
        # Store the client
        self.client = client
    
    def generate_multiple_choice_question(
        self,
        topic: str,
        subtopic: Optional[str] = None,
        focus: str = "text",
        difficulty: str = "challenging",
        question_number: int = 1
    ) -> str:
        """
        Generate a prompt for the Anthropic model to create a multiple-choice question.
        
        Args:
            topic: The main topic for the question
            subtopic: Optional subtopic for more specific questions
            focus: Whether the question should focus on code or text
            difficulty: The difficulty level of the question (e.g., "easy", "medium", "challenging", "hard")
            question_number: The number of the question in the series
            
        Returns:
            A prompt for the Anthropic model
        """
        prompt = get_multiple_choice_prompt(
            topic=topic,
            subtopic=subtopic,
            focus=focus,
            difficulty=difficulty,
            question_number=question_number
        )
        
        return self._generate_question(prompt)
    
    def generate_true_false_question(
        self,
        topic: str,
        subtopic: Optional[str] = None,
        focus: str = "text",
        difficulty: str = "challenging",
        question_number: int = 1
    ) -> str:
        """
        Generate a prompt for the Anthropic model to create a true/false question.
        
        Args:
            topic: The main topic for the question
            subtopic: Optional subtopic for more specific questions
            focus: Whether the question should focus on code or text
            difficulty: The difficulty level of the question (e.g., "easy", "medium", "challenging", "hard")
            question_number: The number of the question in the series
            
        Returns:
            A prompt for the Anthropic model
        """
        prompt = get_true_false_prompt(
            topic=topic,
            subtopic=subtopic,
            focus=focus,
            difficulty=difficulty,
            question_number=question_number
        )
        
        return self._generate_question(prompt)
    
    def generate_cloze_question(
        self,
        topic: str,
        subtopic: Optional[str] = None,
        focus: str = "text",
        difficulty: str = "challenging",
        question_number: int = 1
    ) -> str:
        """
        Generate a prompt for the Anthropic model to create a cloze (fill-in-the-blank) question.
        
        Args:
            topic: The main topic for the question
            subtopic: Optional subtopic for more specific questions
            focus: Whether the question should focus on code or text
            difficulty: The difficulty level of the question (e.g., "easy", "medium", "challenging", "hard")
            question_number: The number of the question in the series
            
        Returns:
            A prompt for the Anthropic model
        """
        prompt = get_cloze_prompt(
            topic=topic,
            subtopic=subtopic,
            focus=focus,
            difficulty=difficulty,
            question_number=question_number
        )
        
        return self._generate_question(prompt)
    
    def _generate_question(self, prompt: str) -> str:
        """
        Generate a question using the Anthropic model.
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            The model's response as a string
        """
        return get_host_agent_response(prompt, self.client)
    
    def parse_question_response(
        self,
        response: str,
        question_type: str,
        topic: str,
        subtopic: Optional[str] = None,
        focus: str = "text"
    ) -> Union[MultipleChoiceQuestion, TrueFalseQuestion, ClozeQuestion]:
        """
        Parse the Anthropic model's response into a Question object.
        
        Args:
            response: The response from the model
            question_type: The type of question to parse
            topic: The main topic of the question
            subtopic: Optional subtopic of the question
            focus: Whether the question focuses on code or text
            
        Returns:
            A Question object
        """
        try:
            # Try to parse the JSON response
            # First, clean up the response to handle potential formatting issues
            response = clean_json_response(response)
            logger.info(f"Attempting to parse JSON: {response}")
            data = json.loads(response)
            logger.info(f"Successfully parsed JSON: {data}")
            
            # Create the appropriate question object based on the question type
            if question_type == "multiple_choice":
                # Check if explanation is present, if not, provide a default explanation
                explanation = data.get("explanation", f"This is a question about {data.get('concept_phrase', topic)}.")
                return MultipleChoiceQuestion(
                    question=data["question"],
                    options=data["options"],
                    correct_answer=data["correct_answer"],
                    explanation=explanation,
                    topic=topic,
                    subtopic=subtopic,
                    focus=focus,
                    language=data.get("language"),
                    concept_phrase=data.get("concept_phrase", "")
                )
            elif question_type == "true_false":
                # Check if explanation is present, if not, provide a default explanation
                explanation = data.get("explanation", f"This is a question about {data.get('concept_phrase', topic)}.")
                return TrueFalseQuestion(
                    question=data["question"],
                    correct_answer=data["correct_answer"],
                    explanation=explanation,
                    topic=topic,
                    subtopic=subtopic,
                    focus=focus,
                    language=data.get("language"),
                    concept_phrase=data.get("concept_phrase", "")
                )
            else:  # cloze
                logger.info(f"Creating cloze question with data: {data}")
                # Check if explanation is present, if not, provide a default explanation
                explanation = data.get("explanation", f"This is a question about {data.get('concept_phrase', topic)}.")
                return ClozeQuestion(
                    question=data["question"],
                    correct_answer=data["correct_answer"],
                    explanation=explanation,
                    topic=topic,
                    subtopic=subtopic,
                    focus=focus,
                    language=data.get("language"),
                    concept_phrase=data.get("concept_phrase", "")
                )
        except (json.JSONDecodeError, KeyError) as e:
            # If there's an error parsing the response, create a default question
            error_message = f"Error parsing response: {str(e)}\nResponse: {response}"
            logger.error(error_message)
            
            if question_type == "multiple_choice":
                return MultipleChoiceQuestion(
                    question=f"Error generating question about {topic}. Please try again.",
                    options=[
                        "A. First option",
                        "B. Second option",
                        "C. Third option",
                        "D. Fourth option"
                    ],
                    correct_answer="A",
                    explanation="This is a placeholder explanation due to an error in question generation.",
                    topic=topic,
                    subtopic=subtopic,
                    focus=focus,
                    language=None,
                    concept_phrase=f"Error in {topic}"
                )
            elif question_type == "true_false":
                return TrueFalseQuestion(
                    question=f"Error generating question about {topic}. Please try again.",
                    correct_answer=True,
                    explanation="This is a placeholder explanation due to an error in question generation.",
                    topic=topic,
                    subtopic=subtopic,
                    focus=focus,
                    language=None,
                    concept_phrase=f"Error in {topic}"
                )
            else:  # cloze
                return ClozeQuestion(
                    question=f"Error generating question about {topic}. Please fill in the ___.",
                    correct_answer="blank",
                    explanation="This is a placeholder explanation due to an error in question generation.",
                    topic=topic,
                    subtopic=subtopic,
                    focus=focus,
                    language=None,
                    concept_phrase=f"Error in {topic}"
                )
