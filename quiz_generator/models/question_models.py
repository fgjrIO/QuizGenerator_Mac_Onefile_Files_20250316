"""
Question model classes for the Quiz Generator package.

This module contains the base question class and specific question type classes.
"""

from typing import Dict, Any, List, Optional


class BaseQuestion:
    """
    Base class for all question types.
    
    Attributes:
        question: The question text
        type: The type of question (e.g., "multiple_choice", "true_false", "cloze")
        explanation: An explanation of the correct answer
        topic: The main topic of the question
        subtopic: Optional subtopic for more specific questions
        focus: Whether the question focuses on code or text
        language: The programming language if the question involves code
        concept_phrase: A short phrase describing what the question is about
    """
    
    def __init__(self, question: str, type: str, explanation: str, topic: str, 
                 subtopic: Optional[str] = None, focus: str = "text", 
                 language: Optional[str] = None, concept_phrase: str = ""):
        self.question = question
        self.type = type
        self.explanation = explanation
        self.topic = topic
        self.subtopic = subtopic
        self.focus = focus
        self.language = language
        self.concept_phrase = concept_phrase
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the question to a dictionary."""
        return {
            "question": self.question,
            "type": self.type,
            "explanation": self.explanation,
            "topic": self.topic,
            "subtopic": self.subtopic,
            "focus": self.focus,
            "language": self.language,
            "concept_phrase": self.concept_phrase
        }


class MultipleChoiceQuestion(BaseQuestion):
    """
    Multiple-choice question class.
    
    Attributes:
        options: List of option strings
        correct_answer: The correct option string
    """
    
    def __init__(self, question: str, options: List[str], correct_answer: str, 
                 explanation: str, topic: str, subtopic: Optional[str] = None, 
                 focus: str = "text", language: Optional[str] = None, 
                 concept_phrase: str = ""):
        super().__init__(question, "multiple_choice", explanation, topic, 
                         subtopic, focus, language, concept_phrase)
        self.options = options
        self.correct_answer = correct_answer
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the question to a dictionary."""
        result = super().to_dict()
        result["options"] = self.options
        result["correct_answer"] = self.correct_answer
        return result


class TrueFalseQuestion(BaseQuestion):
    """
    True/False question class.
    
    Attributes:
        correct_answer: Boolean indicating whether the statement is true or false
    """
    
    def __init__(self, question: str, correct_answer: bool, explanation: str, 
                 topic: str, subtopic: Optional[str] = None, focus: str = "text", 
                 language: Optional[str] = None, concept_phrase: str = ""):
        super().__init__(question, "true_false", explanation, topic, 
                         subtopic, focus, language, concept_phrase)
        self.correct_answer = correct_answer
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the question to a dictionary."""
        result = super().to_dict()
        result["correct_answer"] = self.correct_answer
        return result


class ClozeQuestion(BaseQuestion):
    """
    Cloze (fill-in-the-blank) question class.
    
    Attributes:
        correct_answer: The correct answer to fill in the blank
    """
    
    def __init__(self, question: str, correct_answer: str, explanation: str, 
                 topic: str, subtopic: Optional[str] = None, focus: str = "text", 
                 language: Optional[str] = None, concept_phrase: str = ""):
        super().__init__(question, "cloze", explanation, topic, 
                         subtopic, focus, language, concept_phrase)
        self.correct_answer = correct_answer
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the question to a dictionary."""
        result = super().to_dict()
        result["correct_answer"] = self.correct_answer
        return result
