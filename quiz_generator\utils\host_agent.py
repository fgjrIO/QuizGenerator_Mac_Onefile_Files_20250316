"""
Host agent utilities for interacting with the Anthropic API, GROQ API, OpenRouter API, and Ollama API.

This module contains functions for sending prompts to various LLM APIs and handling responses.
"""

import json
import logging
import os
import re
import subprocess
from typing import Optional, Dict, Any, List, Tuple

import anthropic
import openai

# Get the logger
logger = logging.getLogger("quiz_generator")


def select_platform_and_model(specified_platform: Optional[str] = None, specified_model: Optional[str] = None) -> Tuple[str, str]:
    """
    Select the appropriate platform and model based on specified values and available API keys.
    
    This function implements a fallback mechanism:
    1. If platform and model are explicitly specified, use them
    2. Otherwise, check for available API keys in this order:
       - Anthropic (default to claude-3-7-sonnet-20250219)
       - OpenAI (default to gpt-4o)
       - OpenRouter (default to qwen/qwen-2.5-72b-instruct:free)
       - GROQ (default to llama3-70b-8192)
       - Ollama (use smallest available model)
    
    Args:
        specified_platform: Optional explicitly specified platform
        specified_model: Optional explicitly specified model
    
    Returns:
        A tuple of (platform, model) to use
    """
    # If both platform and model are specified, use them
    if specified_platform and specified_model:
        logger.info(f"Using explicitly specified platform: {specified_platform} and model: {specified_model}")
        return specified_platform, specified_model
    
    # If only model is specified, determine the platform from the model name
    if specified_model:
        if specified_model.startswith("claude"):
            platform = "anthropic"
        elif specified_model.startswith("gpt"):
            platform = "openai"
        elif specified_model.startswith("llama"):
            platform = "groq"
        elif specified_model.startswith("qwen") or "openrouter" in specified_model:
            platform = "openrouter"
        elif specified_model == "ollama" or specified_model.startswith("ollama:"):
            platform = "ollama"
        else:
            # Default to anthropic for unknown models
            platform = "anthropic"
        
        logger.info(f"Determined platform {platform} from specified model: {specified_model}")
        return platform, specified_model
    
    # If only platform is specified, use the default model for that platform
    if specified_platform:
        if specified_platform == "anthropic":
            model = "claude-3-7-sonnet-20250219"
        elif specified_platform == "openai":
            model = "gpt-4o"
        elif specified_platform == "groq":
            model = "llama3-70b-8192"
        elif specified_platform == "openrouter":
            model = "qwen/qwen-2.5-72b-instruct:free"
        elif specified_platform == "ollama":
            model = "ollama"  # Will select smallest available model
        else:
            # Default to anthropic for unknown platforms
            specified_platform = "anthropic"
            model = "claude-3-7-sonnet-20250219"
        
        logger.info(f"Using specified platform: {specified_platform} with default model: {model}")
        return specified_platform, model
    
    # If neither platform nor model is specified, implement the fallback mechanism
    # Check for API keys in order of preference
    
    # Check for Anthropic API key
    if os.environ.get("ANTHROPIC_API_KEY"):
        logger.info("Using Anthropic platform (API key found)")
        return "anthropic", "claude-3-7-sonnet-20250219"
    
    # Check for OpenAI API key
    if os.environ.get("OPENAI_API_KEY"):
        logger.info("Using OpenAI platform (API key found)")
        return "openai", "gpt-4o"
    
    # Check for OpenRouter API key
    if os.environ.get("OPENROUTER_API_KEY"):
        logger.info("Using OpenRouter platform (API key found)")
        return "openrouter", "qwen/qwen-2.5-72b-instruct:free"
    
    # Check for GROQ API key
    if os.environ.get("GROQ_API_KEY"):
        logger.info("Using GROQ platform (API key found)")
        return "groq", "llama3-70b-8192"
    
    # If no API keys are found, fall back to Ollama
    # Check if Ollama is available
    available_models = get_available_ollama_models()
    if available_models:
        logger.info(f"Using Ollama platform with model: {available_models[0]}")
        return "ollama", f"ollama:{available_models[0]}"
    
    # If no options are available, log a warning and return a special value
    # to indicate that no valid model or platform is available
    logger.warning("No API keys or Ollama models found. Returning special 'no_model_available' value.")
    return "no_model_available", "no_model_available"


def get_available_ollama_models() -> List[str]:
    """
    Get a list of available Ollama models on the user's system.
    
    Returns:
        A list of model names available in Ollama, sorted by parameter size (smallest first),
        or an empty list if Ollama is not running or no models are available.
    """
    try:
        # Try to list available models using curl
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the JSON response
        models_data = json.loads(result.stdout)
        
        if "models" in models_data and len(models_data["models"]) > 0:
            # Extract model names
            model_names = [model["name"] for model in models_data["models"]]
            logger.info(f"Found {len(model_names)} Ollama models: {', '.join(model_names)}")
            
            # Sort models by parameter size (smallest first)
            # Extract parameter size from model name (e.g., "qwen2.5:3b" -> 3)
            def get_param_size(model_name):
                # Look for patterns like "1b", "3b", "7b", "13b", "70b", etc.
                match = re.search(r'(\d+)b', model_name.lower())
                if match:
                    return int(match.group(1))
                # If no parameter size found, return a large number to put it at the end
                return 1000
            
            # Sort models by parameter size
            sorted_models = sorted(model_names, key=get_param_size)
            logger.info(f"Sorted models by parameter size (smallest first): {', '.join(sorted_models)}")
            return sorted_models
        else:
            logger.warning("Ollama is running but no models are available")
            return []
    except subprocess.CalledProcessError:
        logger.warning("Failed to connect to Ollama API. Is Ollama running?")
        return []
    except json.JSONDecodeError:
        logger.warning("Failed to parse Ollama API response. Unexpected format.")
        return []
    except Exception as e:
        logger.warning(f"Error checking Ollama models: {str(e)}")
        return []


def initialize_anthropic_client() -> Optional[anthropic.Anthropic]:
    """
    Initialize the Anthropic client using the API key from environment variables.
    
    Returns:
        An Anthropic client instance if the API key is available, None otherwise
    """
    # Get the Anthropic API key from environment variables
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.warning("ANTHROPIC_API_KEY environment variable not found.")
        logger.warning("The server will not be able to generate questions without a valid API key.")
        logger.warning("When run through the MCP system, this key will be provided automatically.")
        return None
    
    # Create an Anthropic client
    try:
        client = anthropic.Anthropic(api_key=api_key)
        logger.info("Anthropic client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Error initializing Anthropic client: {str(e)}")
        return None


def get_host_agent_response(prompt: str, client: Optional[anthropic.Anthropic] = None, model: str = None, platform: str = None) -> str:
    """
    Send a prompt to the selected model and get a response.
    
    Args:
        prompt: The prompt to send to the model
        client: An optional Anthropic client instance. If not provided, a new client will be initialized.
        model: The model to use for generation (default: determined by select_platform_and_model)
               Can be:
               - Anthropic models like "claude-3-7-sonnet-20250219"
               - OpenAI models like "gpt-4o"
               - GROQ models like "llama3-70b-8192"
               - OpenRouter models like "qwen/qwen-2.5-72b-instruct:free"
               - Ollama models like "ollama:llama3" (format: "ollama:model_name")
        platform: The platform to use (anthropic, openai, groq, openrouter, ollama)
               If specified, will use the default model for that platform
        
    Returns:
        The model's response as a string
    """
    # Select the platform and model based on specified values and available API keys
    selected_platform, selected_model = select_platform_and_model(platform, model)
    
    # Log the selected platform and model
    logger.info(f"Using platform: {selected_platform} with model: {selected_model}")
    
    # If no client is provided and we're using Anthropic, initialize a new one
    if not client and selected_platform == "anthropic":
        client = initialize_anthropic_client()
    
    try:
        # Handle based on the selected platform
        if selected_platform == "groq":
            # Import GROQ client if needed
            try:
                import groq
            except ImportError:
                logger.error("GROQ client not installed. Please install with 'pip install groq'")
                return json.dumps({
                    "error": "GROQ client not installed",
                    "question": "Error generating question. Please try again.",
                    "explanation": "The GROQ client is not installed. Please install with 'pip install groq'."
                })
            
            # Get the GROQ API key from environment variables
            groq_api_key = os.environ.get("GROQ_API_KEY")
            if not groq_api_key:
                logger.error("GROQ_API_KEY environment variable not found")
                return json.dumps({
                    "error": "No GROQ API key available",
                    "question": "Error generating question. Please try again.",
                    "explanation": "The GROQ API key is not available. Make sure the GROQ_API_KEY environment variable is set."
                })
            
            # Create a GROQ client
            groq_client = groq.Client(api_key=groq_api_key)
            
            # Generate the response using the GROQ API
            response = groq_client.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": "system", "content": "You are a quiz question generator. You MUST return ONLY a valid JSON object with no additional text or commentary. Do not review or comment on the question. Your JSON response MUST include ALL fields specified in the prompt, including the explanation field."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2048
            )
            
            # Extract the response text
            response_text = response.choices[0].message.content
            logger.info(f"Generated response from GROQ: {response_text[:100]}...")
            
            return response_text
        # Handle OpenAI platform
        elif selected_platform == "openai":
            # Import OpenAI client if needed
            try:
                import openai
            except ImportError:
                logger.error("OpenAI client not installed. Please install with 'pip install openai'")
                return json.dumps({
                    "error": "OpenAI client not installed",
                    "question": "Error generating question. Please try again.",
                    "explanation": "The OpenAI client is not installed. Please install with 'pip install openai'."
                })
            
            # Get the OpenAI API key from environment variables
            openai_api_key = os.environ.get("OPENAI_API_KEY")
            if not openai_api_key:
                logger.error("OPENAI_API_KEY environment variable not found")
                return json.dumps({
                    "error": "No OpenAI API key available",
                    "question": "Error generating question. Please try again.",
                    "explanation": "The OpenAI API key is not available. Make sure the OPENAI_API_KEY environment variable is set."
                })
            
            # Create an OpenAI client
            openai_client = openai.OpenAI(api_key=openai_api_key)
            
            # Generate the response using the OpenAI API
            response = openai_client.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": "system", "content": "You are a quiz question generator. You MUST return ONLY a valid JSON object with no additional text or commentary. Do not review or comment on the question. Your JSON response MUST include ALL fields specified in the prompt, including the explanation field."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2048
            )
            
            # Extract the response text
            response_text = response.choices[0].message.content
            logger.info(f"Generated response from OpenAI: {response_text[:100]}...")
            
            return response_text
        # Handle OpenRouter platform
        elif selected_platform == "openrouter":
            # Get the OpenRouter API key from environment variables
            openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
            if not openrouter_api_key:
                logger.error("OPENROUTER_API_KEY environment variable not found")
                return json.dumps({
                    "error": "No OpenRouter API key available",
                    "question": "Error generating question. Please try again.",
                    "explanation": "The OpenRouter API key is not available. Make sure the OPENROUTER_API_KEY environment variable is set."
                })
            
            # Create an OpenAI client with OpenRouter base URL
            openai_client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=openrouter_api_key,
            )
            
            # Generate the response using the OpenRouter API
            response = openai_client.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": "system", "content": "You are a quiz question generator. You MUST return ONLY a valid JSON object with no additional text or commentary. Do not review or comment on the question. Your JSON response MUST include ALL fields specified in the prompt, including the explanation field."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2048
            )
            
            # Extract the response text
            response_text = response.choices[0].message.content
            logger.info(f"Generated response from OpenRouter: {response_text[:100]}...")
            
            return response_text
        # Handle Ollama platform
        elif selected_platform == "ollama":
            # Import OpenAI client
            try:
                import openai
            except ImportError:
                logger.error("OpenAI client not installed. Please install with 'pip install openai'")
                return json.dumps({
                    "error": "OpenAI client not installed",
                    "question": "Error generating question. Please try again.",
                    "explanation": "The OpenAI client is not installed. Please install with 'pip install openai'."
                })
            
            # If just "ollama" is specified, get available models and use the first one
            if selected_model == "ollama":
                available_models = get_available_ollama_models()
                if not available_models:
                    error_message = "No Ollama models available. Please pull a model using 'ollama pull llama3' or similar."
                    logger.error(error_message)
                    return json.dumps({
                        "error": error_message,
                        "question": "Error generating question. Please try again.",
                        "explanation": "No Ollama models are available. Please pull a model using 'ollama pull llama3' or similar."
                    })
                
                # Use the smallest available model (already sorted by parameter size)
                ollama_model = available_models[0]
                logger.info(f"Using automatically selected smallest Ollama model: {ollama_model}")
            else:
                # Extract the actual model name from the string (remove "ollama:" prefix)
                if selected_model.startswith("ollama:"):
                    ollama_model = selected_model.split(":", 1)[1]
                else:
                    ollama_model = selected_model
            
            # Create an OpenAI client with Ollama base URL
            try:
                ollama_client = openai.OpenAI(
                    base_url="http://localhost:11434/v1",
                    api_key="ollama",  # Ollama doesn't require an API key, but the client requires a non-empty string
                )
                
                # Generate the response using the Ollama API
                response = ollama_client.chat.completions.create(
                    model=ollama_model,
                    messages=[
                        {"role": "system", "content": "You are a quiz question generator. You MUST return ONLY a valid JSON object with no additional text or commentary. Do not review or comment on the question. Your JSON response MUST include ALL fields specified in the prompt, including the explanation field."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2048
                )
                
                # Extract the response text
                response_text = response.choices[0].message.content
                logger.info(f"Generated response from Ollama ({ollama_model}): {response_text[:100]}...")
                
                return response_text
            except Exception as e:
                error_message = f"Error generating response from Ollama: {str(e)}"
                logger.error(error_message)
                return json.dumps({
                    "error": error_message,
                    "question": f"Error generating question. Please try again.",
                    "explanation": "An error occurred while generating the question with Ollama. Make sure Ollama is running and the model is available."
                })
        # Handle Anthropic platform
        elif selected_platform == "anthropic":
            # Check if we have a valid client
            if not client:
                logger.error("No Anthropic client available")
                return json.dumps({
                    "error": "No Anthropic client available",
                    "question": "Error generating question. Please try again.",
                    "explanation": "The Anthropic client is not initialized. Make sure the ANTHROPIC_API_KEY environment variable is set."
                })
            
            # Generate the response using the Anthropic API
            response = client.messages.create(
                model=selected_model,
                max_tokens=2048,
                temperature=0.7,
                system="You are a quiz question generator. You MUST return ONLY a valid JSON object with no additional text or commentary. Do not review or comment on the question. Your JSON response MUST include ALL fields specified in the prompt, including the explanation field.",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )
            
            # Extract the response text
            response_text = response.content[0].text
            logger.info(f"Generated response from Anthropic: {response_text[:100]}...")
            
            return response_text
        else:
            # Unknown platform
            error_message = f"Unknown platform: {selected_platform}"
            logger.error(error_message)
            return json.dumps({
                "error": error_message,
                "question": "Error generating question. Please try again.",
                "explanation": f"The platform '{selected_platform}' is not supported."
            })
    except Exception as e:
        error_message = f"Error generating response: {str(e)}"
        logger.error(error_message)
        return json.dumps({
            "error": error_message,
            "question": f"Error generating question. Please try again.",
            "explanation": "An error occurred while generating the question."
        })


def clean_json_response(response: str) -> str:
    """
    Clean up JSON response that might be wrapped in markdown code blocks or contain escaped characters.
    
    Args:
        response: The response string from the model
        
    Returns:
        A cleaned JSON string
    """
    # Check if the response contains thinking tags from OpenRouter
    if "<think>" in response and "</think>" in response:
        # Extract the content after the thinking section
        try:
            response = response.split("</think>")[1].strip()
            logger.info(f"Extracted content after thinking tags: {response[:100]}...")
        except IndexError:
            logger.warning("Failed to extract content after thinking tags")
    
    # Check if the response is wrapped in a code block
    if response.startswith("```json") and response.endswith("```"):
        response = response[7:-3].strip()
    elif response.startswith("```") and response.endswith("```"):
        response = response[3:-3].strip()
    
    # Try to extract a JSON object from the response
    try:
        # First, try to parse the response directly as JSON
        json.loads(response)
        return response
    except json.JSONDecodeError:
        # If that fails, try to extract a JSON object from the text
        logger.info("Response is not valid JSON, attempting to extract JSON object")
        
        # Try to construct a JSON object from the key-value pairs in the response
        # Check for various possible formats
        question_headers = ["**Question:**", "**Question Stem:**"]
        options_headers = ["**Options:**"]
        answer_headers = ["**Correct Answer:**", "**Answer:**"]
        concept_headers = ["**Concept Phrase:**"]
        explanation_headers = ["**Explanation:**"]
        
        # Find which headers are present
        question_header = next((h for h in question_headers if h in response), None)
        options_header = next((h for h in options_headers if h in response), None)
        answer_header = next((h for h in answer_headers if h in response), None)
        concept_header = next((h for h in concept_headers if h in response), None)
        explanation_header = next((h for h in explanation_headers if h in response), None)
        
        if question_header and options_header and answer_header:
            logger.info("Found question format, constructing JSON object")
            
            # Extract question
            question_match = re.search(fr'{re.escape(question_header)}\s*(.*?)(?={"|".join([re.escape(h) for h in question_headers + options_headers + answer_headers + concept_headers + explanation_headers if h != question_header])}|\Z)', response, re.DOTALL)
            question = question_match.group(1).strip() if question_match else ""
            
            # Extract options
            options_text = re.search(fr'{re.escape(options_header)}\s*(.*?)(?={"|".join([re.escape(h) for h in question_headers + options_headers + answer_headers + concept_headers + explanation_headers if h != options_header])}|\Z)', response, re.DOTALL)
            options = []
            if options_text:
                options_lines = options_text.group(1).strip().split('\n')
                for line in options_lines:
                    line = line.strip()
                    if line.startswith(('A.', 'B.', 'C.', 'D.')):
                        options.append(line)
            
            # Extract correct answer
            correct_answer_match = re.search(fr'{re.escape(answer_header)}\s*(.*?)(?={"|".join([re.escape(h) for h in question_headers + options_headers + answer_headers + concept_headers + explanation_headers if h != answer_header])}|\Z)', response, re.DOTALL)
            correct_answer = correct_answer_match.group(1).strip() if correct_answer_match else ""
            
            # Extract concept phrase
            concept_phrase = ""
            if concept_header:
                concept_phrase_match = re.search(fr'{re.escape(concept_header)}\s*(.*?)(?={"|".join([re.escape(h) for h in question_headers + options_headers + answer_headers + concept_headers + explanation_headers if h != concept_header])}|\Z)', response, re.DOTALL)
                concept_phrase = concept_phrase_match.group(1).strip() if concept_phrase_match else ""
            
            # Extract explanation
            explanation = ""
            if explanation_header:
                explanation_match = re.search(fr'{re.escape(explanation_header)}\s*(.*?)(?={"|".join([re.escape(h) for h in question_headers + options_headers + answer_headers + concept_headers + explanation_headers if h != explanation_header])}|\Z)', response, re.DOTALL)
                explanation = explanation_match.group(1).strip() if explanation_match else ""
            
            # Construct JSON object
            json_obj = {
                "question": question,
                "options": options,
                "correct_answer": correct_answer,
                "type": "multiple_choice",
                "concept_phrase": concept_phrase,
                "explanation": explanation
            }
            
            # Convert to JSON string
            response = json.dumps(json_obj)
            logger.info(f"Constructed JSON object: {response[:100]}...")
            return response
        
        # Handle case where there might be text before or after the JSON
        import re
        json_pattern = r'({[\s\S]*})'
        match = re.search(json_pattern, response)
        if match:
            response = match.group(1)
            logger.info(f"Extracted JSON object using regex: {response[:100]}...")
            return response
        
        # If all else fails, return the original response
        logger.warning("Failed to extract JSON object from response")
        return response
