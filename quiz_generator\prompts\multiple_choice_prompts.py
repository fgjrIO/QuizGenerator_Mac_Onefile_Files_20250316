"""
Multiple-choice question prompt templates.

This module contains functions for generating prompts for multiple-choice questions.
"""

from typing import Optional


def get_multiple_choice_prompt(
    topic: str,
    subtopic: Optional[str] = None,
    focus: str = "text",
    difficulty: str = "challenging",
    question_number: int = 1
) -> str:
    """
    Generate a prompt for creating a multiple-choice question.
    
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
    
    # Common question stems that can be used for any question type
    question_stems = [
        "What best explains",
        "Which most accurately describes",
        "What is the primary",
        "How does it relate",
        "What underlying factor is",
        "Which option most effectively",
        "What is most critical",
        "How best can one",
        "Which factor contributes most",
        "What element is most",
        "How can we characterize",
        "Which answer best illustrates",
        "What is the key",
        "Which most directly impacts",
        "What primarily influences",
        "How best explains",
        "Which factor explains",
        "What is the dominant",
        "How would you classify",
        "Which statement most reflects"
    ]
    
    # Generate the prompt based on the focus
    if focus == "code":
        prompt = f"""
        Create a {difficulty_desc} multiple-choice question about {topic_text} that MUST include code.
        
        CRITICAL REQUIREMENTS:
        1. This MUST be a code-focused question but keep the code brief (2 - 5 lines maximum)
        2. ALL answer options MUST contain actual code snippets (not just text about code)
        3. You MUST specify the programming language being used in the question
        4. Code must be properly formatted and indented as it would appear in an IDE
        5. ALL code MUST be enclosed in triple backticks with the language specified
        6. The code in the option choices should NOT repeat any code (if applicable) that is in the question. They should be distinct.
        7. The option choices must be able to actually answer the question. They should be directly related to and answer the question and not be unreleated code blocks.
        8. Do not give a code snippet in the question that does not align with the answer choices. The code in the question (if any) and code in the answer choices must be combinable into a cohesive whole. Otherwise, do NOT provide code in the question text, only in the choices.
        9. If any code is in the question text, it should be conceptually and very clearly related to what is being asked.
        10. Do NOT give away the answer in the question. The question text should not provide the answer in text or code, as the answer should be reserved for the option choices.
        
        HELPFUL QUESTION STEMS:
        You may use these question stems to help generate creative questions by randomly selecting amongst them:
        {', '.join(question_stems)}
        
        FORMATTING INSTRUCTIONS:
        - For the question, format any code as: ```language\\ncode here\\n```
        - For EACH option, format any code as: ```language\\ncode here\\n```
        - Make sure the code is properly indented and formatted
        - Do NOT abbreviate or simplify the code - show complete, properly formatted code
        - DO NOT use escaped backticks like \\` - use regular backticks ` instead
        - DO NOT wrap your JSON response in ```json code blocks
        
        For example, the question might ask about what a code snippet does, or the options might be different code implementations.
        
        Return ONLY a JSON object with the following structure:
        {{
            "question": "The question text with code snippet properly formatted with triple backticks",
            "options": [
                "A. \\n Option with code formatted as ```language\\ncode here\\n```",
                "B. \\n Option with code formatted as ```language\\ncode here\\n```",
                "C. \\n Option with code formatted as ```language\\ncode here\\n```",
                "D. \\n Option with code formatted as ```language\\ncode here\\n```"
            ],
            "correct_answer": "The correct option (exactly as it appears in options)",
            "type": "multiple_choice",
            "language": "The programming language of the code (e.g., 'python', 'javascript', 'java', etc.)",
            "concept_phrase": "A short 4-5 word phrase describing what this question is about (e.g., 'binary tree traversal algorithms', 'JavaScript closure scope', 'SQL join operations')",
            "explanation": "A detailed explanation of why the correct answer is right and why the other options are wrong"
        }}
        """
    else:
        prompt = f"""
        Create a {difficulty_desc} multiple-choice question about {topic_text}.
        
        This should be a text-focused question about concepts. Do not include code snippets.
          
        HELPFUL QUESTION STEMS:
        You may use these question stems to help generate creative questions by randomly selecting amongst them:
        {', '.join(question_stems)}
        
        IMPORTANT: DO NOT wrap your JSON response in ```json code blocks. Return the raw JSON object only.
        
        Return ONLY a JSON object with the following structure:
        {{
            "question": "The question text",
            "options": ["A. Option text", "B. Option text", "C. Option text", "D. Option text"],
            "correct_answer": "The correct option (exactly as it appears in options)",
            "type": "multiple_choice",
            "concept_phrase": "A short 4-5 word phrase describing what this question is about (e.g., 'binary tree traversal algorithms', 'JavaScript closure scope', 'SQL join operations')",
            "explanation": "A detailed explanation of why the correct answer is right and why the other options are wrong"
        }}
        """
    
    return prompt
