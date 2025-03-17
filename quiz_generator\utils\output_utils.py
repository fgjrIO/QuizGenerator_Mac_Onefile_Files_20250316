"""
Output utilities for creating quiz files.

This module contains functions for creating bootable quizzes and HTML quizzes.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any

from ..models.question_models import BaseQuestion
from .common_utils import sanitize_filename
from .templates.html.base import get_base_html
from .templates.html.head import get_head_content
from .templates.html.styles import get_css_styles
from .templates.html.scripts import get_javascript_code
from .templates.html.components import get_sidebar_html, get_main_content_html


def create_bootable_quiz(questions: List[BaseQuestion], topic: str, subtopic: str = None, microcourse_content: str = None) -> str:
    """
    Create a bootable quiz file (.bquiz) for MagicTutor.
    
    Args:
        questions: List of Question objects
        topic: The main topic of the quiz
        subtopic: Optional subtopic of the quiz
        microcourse_content: Optional microcourse content
        
    Returns:
        The path to the created file
    """
    # Create the quiz data structure
    quiz_data = {
        "name": f"Quiz on {topic}" + (f" - {subtopic}" if subtopic else ""),
        "topic": topic,
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "questions": [q.to_dict() for q in questions],
        "microcourse": microcourse_content
    }
    
    # Create a filename with sanitized topic and subtopic
    sanitized_topic = sanitize_filename(topic)
    filename = f"{sanitized_topic.replace(' ', '_').lower()}"
    if subtopic:
        sanitized_subtopic = sanitize_filename(subtopic)
        filename += f"_{sanitized_subtopic.replace(' ', '_').lower()}"
    filename += f"_{datetime.now().strftime('%Y%m%d%H%M%S')}.bquiz"
    
    # Get the output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the file
    file_path = os.path.join(output_dir, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, indent=2, ensure_ascii=False)
    
    return file_path


def create_html_quiz(questions: List[BaseQuestion], topic: str, subtopic: str = None, microcourse_content: str = None) -> str:
    """
    Create a self-contained HTML quiz file with an interactive interface.
    
    Args:
        questions: List of Question objects
        topic: The main topic of the quiz
        subtopic: Optional subtopic of the quiz
        microcourse_content: Optional microcourse content
        
    Returns:
        The path to the created file
    """
    # Create a filename with sanitized topic and subtopic
    sanitized_topic = sanitize_filename(topic)
    filename = f"{sanitized_topic.replace(' ', '_').lower()}"
    if subtopic:
        sanitized_subtopic = sanitize_filename(subtopic)
        filename += f"_{sanitized_subtopic.replace(' ', '_').lower()}"
    filename += f"_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
    
    # Get the output directory
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare questions data for JavaScript
    questions_json = []
    for q in questions:
        question_data = {
            "question": q.question,
            "explanation": q.explanation,
            "type": q.type,
            "concept_phrase": q.concept_phrase
        }
        
        if q.type == 'multiple_choice':
            question_data["options"] = q.options
            question_data["correctAnswer"] = q.correct_answer
        elif q.type == 'true_false':
            question_data["correctAnswer"] = "True" if q.correct_answer else "False"
        else:  # cloze
            question_data["correctAnswer"] = q.correct_answer
            
        questions_json.append(question_data)
    
    # Get the title for the quiz
    title = f"Quiz on {topic}{f' - {subtopic}' if subtopic else ''}"
    
    # Get the HTML components
    head_content = get_head_content(title)
    css_styles = get_css_styles()
    
    # Get the JavaScript code and replace the placeholders with the actual data
    javascript_code = get_javascript_code()
    javascript_code = javascript_code.replace(
        "QUESTIONS_JSON_PLACEHOLDER", 
        json.dumps(questions_json)
    )
    
    # Add microcourse content if available
    if microcourse_content:
        javascript_code = javascript_code.replace(
            "MICROCOURSE_CONTENT_PLACEHOLDER",
            json.dumps(microcourse_content)
        )
    else:
        javascript_code = javascript_code.replace(
            "MICROCOURSE_CONTENT_PLACEHOLDER",
            "null"
        )
    
    # Get the body content
    sidebar_html = get_sidebar_html(topic, subtopic, has_microcourse=microcourse_content is not None)
    main_content_html = get_main_content_html(topic, subtopic, has_microcourse=microcourse_content is not None)
    body_content = f"{sidebar_html}\n    {main_content_html}"
    
    # Generate the complete HTML content
    html_content = get_base_html(
        head_content=head_content,
        body_content=body_content,
        css_styles=css_styles,
        javascript_code=javascript_code
    )
    
    # Save the file
    file_path = os.path.join(output_dir, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return file_path
