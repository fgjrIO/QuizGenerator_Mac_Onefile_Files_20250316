"""
Tools module for the Quiz Generator package.

This module contains MCP tool functions.
"""

from .mcp_tools import get_host_agent_response, test_host_agent, generate_quiz

__all__ = [
    'get_host_agent_response',
    'test_host_agent',
    'generate_quiz'
]
