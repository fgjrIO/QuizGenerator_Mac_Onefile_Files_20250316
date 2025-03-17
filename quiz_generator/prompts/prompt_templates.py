"""
Common prompt elements for question generation.

This module contains shared elements used across different question type prompts.
"""

def get_microcourse_prompt(topic, subtopics_text):
    """Generate a prompt for creating a microcourse"""
    return f"""
    Create a comprehensive 400-600 word educational course on {topic}, focusing on the following subtopics: {subtopics_text}.
    
    Format the content using markdown with headings, bullet points, and emphasis where appropriate, but avoid using tables or complex formatting that would be difficult to display.
    
    The content should be:
    1. Educational and informative
    2. Well-structured with clear headings
    3. Between 400-600 words in total
    
    Use this structure:
    - Start with a brief introduction to {topic}
    - For each subtopic, provide a section with relevant information
    - End with a brief conclusion or summary
    
    IMPORTANT FORMATTING GUIDELINES:
    - Use ## for main headings and ### for subheadings
    - Use bullet points (- or *) for lists
    - Use **bold** for emphasis or key terms
    - Keep paragraphs relatively short
    - DO NOT include tables or complex layouts
    - DO NOT include images or non-text elements
    - Use simple markdown only
    - When inserting code, be sure to include the language for the markdown
    - IMPORTANT: Never enclose your response in backticks or backticks with the markdown keyword. Provide the response only.
    - IMPORTANT: Always include the language keyword only once after the backticks for code blocks
    - IMPORTANT: Always include the ending backticks for code blocks to complete the code block
    
    Provide ONLY the course content in markdown format, without any additional commentary.
    """

# Common question stems that can be used for any question type
QUESTION_STEMS = [
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

# Common formatting instructions for code-focused questions
CODE_FORMATTING_INSTRUCTIONS = """
FORMATTING INSTRUCTIONS:
- For the question, format any code as: ```language\\ncode here\\n```
- Make sure the code is properly indented and formatted
- Do NOT abbreviate or simplify the code - show complete, properly formatted code
- DO NOT use escaped backticks like \\` - use regular backticks ` instead
- DO NOT wrap your JSON response in ```json code blocks
"""

# Common JSON response format instructions
JSON_RESPONSE_INSTRUCTIONS = """
IMPORTANT: DO NOT wrap your JSON response in ```json code blocks. Return the raw JSON object only.
"""

# System message for the Anthropic model
SYSTEM_MESSAGE = """
You are a quiz question generator. You MUST return ONLY a valid JSON object with no additional text or commentary. 
Do not review or comment on the question. Your JSON response MUST include ALL fields specified in the prompt, 
including the explanation field.
"""
