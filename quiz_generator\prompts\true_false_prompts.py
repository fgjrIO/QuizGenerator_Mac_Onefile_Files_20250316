"""
True/False question prompt templates.

This module contains functions for generating prompts for true/false questions.
"""

from typing import Optional


def get_true_false_prompt(
    topic: str,
    subtopic: Optional[str] = None,
    focus: str = "text",
    difficulty: str = "challenging",
    question_number: int = 1
) -> str:
    """
    Generate a prompt for creating a true/false question.
    
    Args:
        topic: The main topic for the question
        subtopic: Optional subtopic for more specific questions
        focus: Whether the question should focus on code or text
        difficulty: The difficulty level of the question (e.g., "easy", "medium", "challenging", "hard")
        question_number: The number of the question in the series
            
    Returns:
        A prompt for the Anthropic model
    """
    topic_text = f"{topic}"
    if subtopic:
        topic_text += f" (subtopic: {subtopic})"
    
    difficulty_desc = difficulty
    
    # Generate the prompt based on the focus
    if focus == "code":
        prompt = f"""
        Create a {difficulty_desc} true/false question about {topic_text} that MUST include code.
        
        IMPORTANT REQUIREMENTS:
        1. This MUST be a code-focused question
        2. The question MUST contain an actual code snippet (not just mentions of code concepts)
        3. You MUST specify the programming language being used in the question
        4. Code must be properly formatted and indented as it would appear in an IDE
        5. DO NOT use escaped backticks like \\` - use regular backticks ` instead
        6. DO NOT wrap your JSON response in ```json code blocks
        7. Aim for specificity in your questions and avoid asking overly broad elementary questions when the user requests a difficult question above difficulty 5.
        8. Ask specific true or false questions that focuses on where, how, if/then, logic, complex routines, and other high-level questions that avoid asking about generic definitions of concepts.
        
        Return ONLY a JSON object with the following structure:
        {{
            "question": "The question text with code snippet and language specification",
            "correct_answer": true or false (boolean value),
            "type": "true_false",
            "language": "The programming language of the code (e.g., 'python', 'javascript', 'java', etc.)",
            "concept_phrase": "A short 4-5 word phrase describing what this question is about (e.g., 'binary tree traversal algorithms', 'JavaScript closure scope', 'SQL join operations')",
            "explanation": "A detailed explanation of why the answer is true or false"
        }}
        """
    else:
        prompt = f"""
        Create a {difficulty_desc} true/false question about {topic_text}.
        
        This should be a text-focused question about concepts. Do not include code snippets.
        1. Aim for specificity in your questions and avoid asking overly broad elementary questions when the user requests a difficult question above difficulty 5.
        2. Ask specific true or false questions that focuses on where, how, if/then, logic, complex routines, and other high-level questions that avoid asking about generic definitions of concepts.
        
        IMPORTANT: DO NOT wrap your JSON response in ```json code blocks. Return the raw JSON object only.
        
        Return ONLY a JSON object with the following structure:
        {{
            "question": "The question text",
            "correct_answer": true or false (boolean value),
            "type": "true_false",
            "concept_phrase": "A short 4-5 word phrase describing what this question is about (e.g., 'binary tree traversal algorithms', 'JavaScript closure scope', 'SQL join operations')",
            "explanation": "A detailed explanation of why the answer is true or false"
        }}
        """
    
    return prompt
