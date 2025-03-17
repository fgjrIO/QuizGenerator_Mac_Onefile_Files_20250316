"""
Common utility functions for the Quiz Generator package.

This module contains utility functions used across the package.
"""

import re
from typing import Dict, Any, List


def sanitize_filename(text: str) -> str:
    """
    Sanitize a string to be used as a filename by replacing invalid characters.
    
    Args:
        text: The string to sanitize
        
    Returns:
        A sanitized string that can be used as a filename
    """
    # Replace characters that are invalid in filenames
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    result = text
    for char in invalid_chars:
        result = result.replace(char, '_')
    return result


def format_topic_text(topic: str, subtopic: str = None) -> str:
    """
    Format the topic and subtopic into a single string.
    
    Args:
        topic: The main topic
        subtopic: Optional subtopic
        
    Returns:
        A formatted string containing the topic and subtopic
    """
    if subtopic:
        return f"{topic} (subtopic: {subtopic})"
    return topic


def extract_code_blocks(text: str) -> List[Dict[str, str]]:
    """
    Extract code blocks from a markdown-formatted string.
    
    Args:
        text: The markdown-formatted string
        
    Returns:
        A list of dictionaries, each containing 'language' and 'code' keys
    """
    # Regular expression to match code blocks
    pattern = r"```(\w+)?\n([\s\S]*?)```"
    matches = re.findall(pattern, text)
    
    # Convert matches to a list of dictionaries
    code_blocks = []
    for match in matches:
        language = match[0] if match[0] else "text"
        code = match[1]
        code_blocks.append({
            "language": language,
            "code": code
        })
    
    return code_blocks


def merge_dictionaries(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two dictionaries, with values from dict2 taking precedence.
    
    Args:
        dict1: The first dictionary
        dict2: The second dictionary
        
    Returns:
        A merged dictionary
    """
    result = dict1.copy()
    result.update(dict2)
    return result
