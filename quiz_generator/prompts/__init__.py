"""
Prompts module for the Quiz Generator package.

This module contains prompt templates for different question types.
"""

from .multiple_choice_prompts import get_multiple_choice_prompt
from .true_false_prompts import get_true_false_prompt
from .cloze_prompts import get_cloze_prompt

__all__ = [
    'get_multiple_choice_prompt',
    'get_true_false_prompt',
    'get_cloze_prompt'
]
