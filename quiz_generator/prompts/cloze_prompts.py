"""
Cloze (fill-in-the-blank) question prompt templates.

This module contains functions for generating prompts for cloze questions.
"""

from typing import Optional


def get_cloze_prompt(
    topic: str,
    subtopic: Optional[str] = None,
    focus: str = "text",
    difficulty: str = "challenging",
    question_number: int = 1
) -> str:
    """
    Generate a prompt for creating a cloze (fill-in-the-blank) question.
    
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
        Create a {difficulty_desc} fill-in-the-blank (cloze) question about {topic_text} that MUST include code.
        
        IMPORTANT REQUIREMENTS:
        1. This MUST be a code-focused question
        2. The question MUST contain an actual code snippet with a blank (not just mentions of code concepts)
        3. You MUST specify the programming language being used in the question
        4. Code must be properly formatted and indented as it would appear in an IDE
        5. The blank should be represented by "___" (three underscores) in the code
        6. DO NOT use escaped backticks like \\` - use regular backticks ` instead
        7. DO NOT wrap your JSON response in ```json code blocks
        
        IMPORTANT: DO NOT wrap your JSON response in ```json code blocks. Return the raw JSON object only.
        
        Return ONLY a JSON object with the following structure:
        {{
            "question": "The question text with code snippet containing a blank represented by '___'",
            "correct_answer": "The correct answer that should fill in the blank",
            "type": "cloze",
            "language": "The programming language of the code (e.g., 'python', 'javascript', 'java', etc.)",
            "concept_phrase": "A short 4-5 word phrase describing what this question is about (e.g., 'binary tree traversal algorithms', 'JavaScript closure scope', 'SQL join operations')",
            "explanation": "A detailed explanation of the correct answer"
        }}
        """
    else:
        prompt = f"""
        Create a {difficulty_desc} fill-in-the-blank (cloze) question about {topic_text}.
        
        This should be a text-focused question about concepts. Do not include code snippets.
        The blank should be represented by "___" (three underscores) in the question text.
        
        IMPORTANT: DO NOT wrap your JSON response in ```json code blocks. Return the raw JSON object only.
        
        Return ONLY a JSON object with the following structure:
        {{
            "question": "The question text with a blank represented by '___'",
            "correct_answer": "The correct answer that should fill in the blank",
            "type": "cloze",
            "concept_phrase": "A short 4-5 word phrase describing what this question is about (e.g., 'binary tree traversal algorithms', 'JavaScript closure scope', 'SQL join operations')",
            "explanation": "A detailed explanation of the correct answer"
        }}
        """
    
    return prompt
