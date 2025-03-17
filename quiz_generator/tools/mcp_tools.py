"""
MCP tool functions for the Quiz Generator package.

This module contains functions that are exposed as MCP tools.
"""

import json
import logging
from typing import Dict, Any, List, Optional

import anthropic

from ..generators.question_generator import AnthropicQuestionGenerator
from ..utils.host_agent import get_host_agent_response
from ..utils.output_utils import create_bootable_quiz, create_html_quiz

# Get the logger
logger = logging.getLogger("quiz_generator")


def get_host_agent_response_tool(prompt: str, model: str = None, platform: str = None) -> str:
    """
    Send a prompt to the host agent (Anthropic, OpenAI, GROQ, OpenRouter, or Ollama) and get a response.
    
    This tool is used to communicate with the host agent to generate questions.
    
    Args:
        prompt: The prompt to send to the host agent
        model: The model to use (default: determined automatically based on available API keys)
               Can be:
               - Anthropic models like "claude-3-7-sonnet-20250219"
               - OpenAI models like "gpt-4o"
               - GROQ models like "llama3-70b-8192"
               - OpenRouter models like "qwen/qwen-2.5-72b-instruct:free"
               - Ollama models like "ollama:llama3" (format: "ollama:model_name")
        platform: The platform to use (anthropic, openai, groq, openrouter, ollama)
               If specified, will use the default model for that platform
    
    Returns:
        The host agent's response as a string
    """
    # Import directly to avoid circular imports
    from ..utils.host_agent import get_host_agent_response
    
    # Use the host_agent function to handle all the platform and model selection logic
    return get_host_agent_response(prompt, model=model, platform=platform)


def test_host_agent(prompt: str = None, model: str = None, platform: str = None) -> str:
    """
    Test the host agent response with a simple prompt.
    
    This tool is used to test the API connection and response parsing.
    
    Args:
        prompt: Optional custom prompt to send to the host agent. If not provided, a default prompt will be used.
        model: The model to use (default: determined automatically based on available API keys)
               Can be:
               - Anthropic models like "claude-3-7-sonnet-20250219"
               - OpenAI models like "gpt-4o"
               - GROQ models like "llama3-70b-8192"
               - OpenRouter models like "qwen/qwen-2.5-72b-instruct:free"
               - Ollama models like "ollama:llama3" (format: "ollama:model_name")
        platform: The platform to use (anthropic, openai, groq, openrouter, ollama)
               If specified, will use the default model for that platform
    
    Returns:
        The host agent's response as a string
    """
    if not prompt:
        # Default prompt for a multiple-choice question about Python data structures
        prompt = """
        Create a challenging multiple-choice question about Python Programming (subtopic: Data Structures).
        
        This should be a text-focused question about concepts. Do not include code snippets.
          
        IMPORTANT: DO NOT wrap your JSON response in ```json code blocks. Return the raw JSON object only.
        
        Return ONLY a JSON object with the following structure:
        {
            "question": "The question text",
            "options": ["A. Option text", "B. Option text", "C. Option text", "D. Option text"],
            "correct_answer": "The correct option (exactly as it appears in options)",
            "type": "multiple_choice",
            "concept_phrase": "A short 4-5 word phrase describing what this question is about",
            "explanation": "A detailed explanation of why the correct answer is right and why the other options are wrong"
        }
        """
    
    # Get the response using the direct implementation to avoid circular references
    response = get_host_agent_response_tool(prompt, model, platform)
    
    # Try to parse the JSON response
    try:
        data = json.loads(response)
        logger.info(f"Successfully parsed JSON response: {data}")
        return json.dumps({
            "raw_response": response,
            "parsed_json": data,
            "is_valid_json": True
        }, indent=2)
    except json.JSONDecodeError as e:
        error_message = f"Error parsing JSON: {str(e)}"
        logger.error(error_message)
        return json.dumps({
            "raw_response": response,
            "error": error_message,
            "is_valid_json": False
        }, indent=2)


def generate_quiz(
    topic: str,
    subtopic: str = None,
    question_focus: str = "text",
    question_type: str = "multiple_choice",
    difficulty: str = "challenging",
    num_questions: int = 5,
    output_format: str = "html",
    model: str = None,
    platform: str = None
) -> Dict[str, Any]:
    """
    Generate a quiz based on the provided parameters.
    
    This tool creates a quiz with the specified number of questions about the given topic.
    The quiz can be generated in two formats:
    - .bquiz: A bootable quiz file that can be opened directly in MagicTutor
    - .html: A self-contained HTML file that can be opened in any web browser
    
    Args:
        topic: The main topic for the quiz
        subtopic: Optional subtopic for more specific questions
        question_focus: Whether questions should focus on code or text
        question_type: The type of questions to generate (multiple_choice, true_false, cloze)
        difficulty: The difficulty level of the questions (e.g., "easy", "medium", "challenging", "hard")
        num_questions: Number of questions to generate (1-20)
        output_format: Output format ('bquiz' for MagicTutor bootable quiz or 'html' for self-contained HTML)
        model: The model to use (default: determined automatically based on available API keys)
               Can be:
               - Anthropic models like "claude-3-7-sonnet-20250219"
               - OpenAI models like "gpt-4o"
               - GROQ models like "llama3-70b-8192"
               - OpenRouter models like "qwen/qwen-2.5-72b-instruct:free"
               - Ollama models like "ollama:llama3" (format: "ollama:model_name")
        platform: The platform to use (anthropic, openai, groq, openrouter, ollama)
               If specified, will use the default model for that platform
    
    Returns:
        A dictionary containing information about the generated quiz
    """
    # Create a question generator
    question_generator = AnthropicQuestionGenerator()
    
    # Generate questions
    questions = []
    for i in range(num_questions):
        # Generate a prompt based on the question type
        if question_type == "multiple_choice":
            prompt = question_generator.generate_multiple_choice_question(
                topic=topic,
                subtopic=subtopic,
                focus=question_focus,
                difficulty=difficulty,
                question_number=i+1
            )
        elif question_type == "true_false":
            prompt = question_generator.generate_true_false_question(
                topic=topic,
                subtopic=subtopic,
                focus=question_focus,
                difficulty=difficulty,
                question_number=i+1
            )
        else:  # cloze
            prompt = question_generator.generate_cloze_question(
                topic=topic,
                subtopic=subtopic,
                focus=question_focus,
                difficulty=difficulty,
                question_number=i+1
            )
        
        # No reference to previous questions or series
        
        # Send the prompt to the host agent using the direct implementation to avoid circular references
        response = get_host_agent_response_tool(prompt, model, platform)
        
        # Parse the response into a Question object
        question = question_generator.parse_question_response(
            response=response,
            question_type=question_type,
            topic=topic,
            subtopic=subtopic,
            focus=question_focus
        )
        
        # Add the question to the list
        questions.append(question)
    
    # Create the output file
    if output_format == "bquiz":
        file_path = create_bootable_quiz(questions, topic, subtopic)
    else:  # html
        file_path = create_html_quiz(questions, topic, subtopic)
    
    # Return the result
    return {
        "file_path": file_path,
        "format": output_format,
        "num_questions": len(questions),
        "topic": topic,
        "subtopic": subtopic
    }
