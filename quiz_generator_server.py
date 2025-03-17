#!/usr/bin/env python3
"""
Quiz Generator Server

This is the main entry point for the Quiz Generator MCP server.
It sets up logging, initializes the Anthropic client, and registers MCP tools.
"""

import os
import logging
import json
import webbrowser
from datetime import datetime

import anthropic
from mcp.server.fastmcp import FastMCP

from quiz_generator.utils.host_agent import initialize_anthropic_client
from quiz_generator.tools.mcp_tools import (
    get_host_agent_response_tool,
    test_host_agent,
    generate_quiz
)

# Set up logging
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"quiz_generator_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("quiz_generator")

# Create output directory
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(output_dir, exist_ok=True)

# Initialize the Anthropic client
anthropic_client = initialize_anthropic_client()

# Create an MCP server
mcp = FastMCP("Quiz Generator")


def get_host_agent_response(prompt: str, model: str = None, platform: str = None) -> str:
    """
    Send a prompt to the host agent (Anthropic, OpenAI, GROQ, OpenRouter, or Ollama) and get a response.
    
    This tool is used to communicate with the host agent to generate questions.
    
    Parameters:
    - prompt: The prompt to send to the host agent
    - model: The model to use (default: determined automatically based on available API keys)
             Can be:
             - Anthropic model, can only be "claude-3-7-sonnet-20250219"
             - OpenAI models like "gpt-4o"
             - GROQ models, can only be "llama3-70b-8192"
             - OpenRouter model, can only be "qwen/qwen-2.5-72b-instruct:free"
             - Ollama models on user's PC, must ask for specific model or will determine at runtime: "ollama:llama3" (format: "ollama:model_name")
    - platform: The platform to use (anthropic, openai, groq, openrouter, ollama)
             If specified, will use the default model for that platform
    
    Returns:
    - The host agent's response as a string
    """
    # Import the host_agent module to use the get_host_agent_response function
    from quiz_generator.utils.host_agent import get_host_agent_response as host_agent_get_response
    
    # Get the response using the imported function
    response = host_agent_get_response(prompt, None, model, platform)
    
    return response

def test_host_agent(prompt: str = None, model: str = None, platform: str = None) -> str:
    """
    Test the host agent response with a simple prompt.
    
    This tool is used to test the API connection and response parsing.
    
    Parameters:
    - prompt: Optional custom prompt to send to the host agent. If not provided, a default prompt will be used.
    - model: The model to use (default: determined automatically based on available API keys)
             Can be:
             - Anthropic models like "claude-3-7-sonnet-20250219"
             - OpenAI models like "gpt-4o"
             - GROQ models like "llama3-70b-8192"
             - OpenRouter models like "qwen/qwen-2.5-72b-instruct:free"
             - Ollama models like "ollama:llama3" (format: "ollama:model_name")
    - platform: The platform to use (anthropic, openai, groq, openrouter, ollama)
             If specified, will use the default model for that platform
    
    Returns:
    - The host agent's response as a string
    """
    if not prompt:
        # Default prompt for a multiple-choice question about Python data structures
        prompt = """
        Create a challenging multiple-choice question about Python Programming (subtopic: Data Structures).
        
        This should be a text-focused question about concepts. Do not include code snippets.
          
        IMPORTANT: DO NOT wrap your JSON response in ```json code blocks. Return the raw JSON object only.
        
        Return ONLY a JSON object with the following structure:
        {
            "question": "The question text",
            "options": ["A. Option text", "B. Option text", "C. Option text", "D. Option text"],
            "correct_answer": "The correct option (exactly as it appears in options)",
            "type": "multiple_choice",
            "concept_phrase": "A short 4-5 word phrase describing what this question is about",
            "explanation": "A detailed explanation of why the correct answer is right and why the other options are wrong"
        }
        """
    
    # Import the host_agent module to use the correct function
    from quiz_generator.utils.host_agent import get_host_agent_response as host_agent_get_response
    
    # Get the response using the imported function
    response = host_agent_get_response(prompt, None, model, platform)
    
    # Try to parse the JSON response
    try:
        data = json.loads(response)
        logger.info(f"Successfully parsed JSON response: {data}")
        return json.dumps({
            "raw_response": response,
            "parsed_json": data,
            "is_valid_json": True
        }, indent=2)
    except json.JSONDecodeError as e:
        error_message = f"Error parsing JSON: {str(e)}"
        logger.error(error_message)
        return json.dumps({
            "raw_response": response,
            "error": error_message,
            "is_valid_json": False
        }, indent=2)

@mcp.tool()
def generate_quiz(topic: str, subtopic: str = None, question_focus: str = "text", 
                 question_type: str = "multiple_choice", difficulty: str = "challenging",
                 num_questions: int = 5, output_format: str = "html", 
                 model: str = None, platform: str = None) -> dict:
    """
    Generate a microcourse or quiz based on the provided parameters. A microcourse consists of a microlearning module and quiz questions.
    
    This tool creates a quiz with the specified number of questions about the given topic.
    The quiz can be generated in two formats:
    - .bquiz: A bootable quiz file that can be opened directly in MagicTutor
    - .html: A self-contained HTML file that can be opened in any web browser
    
    Parameters:
    - topic: The main topic for the quiz
    - subtopic: Optional subtopic for more specific questions
    - question_focus: Whether questions should focus on code or text
    - question_type: The type of questions to generate (multiple_choice, true_false, cloze)
    - difficulty: The difficulty level of the questions (e.g., "easy", "medium", "challenging", "hard")
    - num_questions: Number of questions to generate (1 minimum and 5 maximum)
    - output_format: Output format ('bquiz' for MagicTutor bootable quiz or 'html' for self-contained HTML)
    - model: The model to use (default: determined automatically based on available API keys if not specified by the user)
             Can be:
             - Anthropic models like "claude-3-7-sonnet-20250219"
             - OpenAI models like "gpt-4o"
             - GROQ models like "llama3-70b-8192"
             - OpenRouter models like "qwen/qwen-2.5-72b-instruct:free"
             - Ollama models like "ollama:llama3" (format: "ollama:model_name")
    - platform: The platform to use (anthropic, openai, groq, openrouter, ollama)
             If specified, will use the default model for that platform
    
    Returns:
    - file_path: Path to the generated quiz file
    - format: Format of the generated quiz file
    - num_questions: Number of questions in the quiz
    - topic: Topic of the quiz
    - subtopic: Subtopic of the quiz if provided
    """
    # Import necessary modules
    import json
    import os
    from datetime import datetime
    from quiz_generator.generators.question_generator import AnthropicQuestionGenerator
    from quiz_generator.utils.output_utils import create_bootable_quiz, create_html_quiz
    from quiz_generator.prompts.prompt_templates import get_microcourse_prompt
    
    # Create a question generator
    question_generator = AnthropicQuestionGenerator()
    
    # Generate a microcourse
    microcourse_prompt = get_microcourse_prompt(topic, subtopic if subtopic else topic)
    
    # Import the host_agent module to use the select_platform_and_model function
    from quiz_generator.utils.host_agent import select_platform_and_model
    
    # Select the platform and model based on specified values and available API keys
    selected_platform, selected_model = select_platform_and_model(platform, model)
    
    # Log the selected platform and model
    logger.info(f"Using platform: {selected_platform} with model: {selected_model}")
    
    # Check if no valid model or platform is available
    if selected_platform == "no_model_available":
        # Create a tutorial HTML file explaining how to set up API keys or install Ollama
        tutorial_content = """
        <html>
        <head>
            <title>MagicTutor - Model Setup Tutorial</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    color: #333;
                }
                h1 {
                    color: #2c3e50;
                    border-bottom: 2px solid #3498db;
                    padding-bottom: 10px;
                }
                h2 {
                    color: #2980b9;
                    margin-top: 30px;
                }
                .card {
                    background-color: #f9f9f9;
                    border-left: 4px solid #3498db;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 4px;
                }
                code {
                    background-color: #f0f0f0;
                    padding: 2px 5px;
                    border-radius: 3px;
                    font-family: monospace;
                }
                .btn {
                    display: inline-block;
                    background-color: #3498db;
                    color: white;
                    padding: 10px 15px;
                    text-decoration: none;
                    border-radius: 4px;
                    margin-top: 10px;
                }
                .btn:hover {
                    background-color: #2980b9;
                }
                .note {
                    background-color: #fffacd;
                    border-left: 4px solid #f1c40f;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            <h1>MagicTutor - Model Setup Tutorial</h1>
            
            <div class="card">
                <p>To generate quizzes with MagicTutor, you need to set up at least one of the following:</p>
                <ul>
                    <li>An API key for a cloud-based LLM service (Anthropic, OpenAI, GROQ, or OpenRouter)</li>
                    <li>Ollama installed on your computer with at least one model</li>
                </ul>
            </div>
            
            <h2>Option 1: Set up a cloud-based LLM service</h2>
            
            <h3>Anthropic Claude (Recommended)</h3>
            <ol>
                <li>Go to <a href="https://console.anthropic.com/" target="_blank">https://console.anthropic.com/</a></li>
                <li>Create an account or sign in</li>
                <li>Navigate to the API Keys section</li>
                <li>Create a new API key</li>
                <li>Set the environment variable <code>ANTHROPIC_API_KEY</code> to your API key</li>
            </ol>
            
            <h3>OpenAI</h3>
            <ol>
                <li>Go to <a href="https://platform.openai.com/" target="_blank">https://platform.openai.com/</a></li>
                <li>Create an account or sign in</li>
                <li>Navigate to the API Keys section</li>
                <li>Create a new API key</li>
                <li>Set the environment variable <code>OPENAI_API_KEY</code> to your API key</li>
            </ol>
            
            <h3>GROQ (Free Option)</h3>
            <ol>
                <li>Go to <a href="https://console.groq.com/" target="_blank">https://console.groq.com/</a></li>
                <li>Create an account or sign in</li>
                <li>Navigate to the API Keys section</li>
                <li>Create a new API key</li>
                <li>Set the environment variable <code>GROQ_API_KEY</code> to your API key</li>
            </ol>
            
            <h3>OpenRouter (Free Option)</h3>
            <ol>
                <li>Go to <a href="https://openrouter.ai/" target="_blank">https://openrouter.ai/</a></li>
                <li>Create an account or sign in</li>
                <li>Navigate to the API Keys section</li>
                <li>Create a new API key</li>
                <li>Set the environment variable <code>OPENROUTER_API_KEY</code> to your API key</li>
            </ol>
            
            <div class="note">
                <p><strong>Note:</strong> To set environment variables:</p>
                <p>On Windows:</p>
                <code>setx ANTHROPIC_API_KEY "your-api-key"</code>
                <p>On macOS/Linux:</p>
                <code>export ANTHROPIC_API_KEY="your-api-key"</code>
                <p>Add this to your <code>.bashrc</code> or <code>.zshrc</code> file to make it permanent.</p>
            </div>
            
            <h2>Option 2: Set up Ollama (Local LLM)</h2>
            
            <ol>
                <li>Go to <a href="https://ollama.ai/" target="_blank">https://ollama.ai/</a></li>
                <li>Download and install Ollama for your operating system</li>
                <li>Open a terminal and run: <code>ollama pull qwen2.5:3b</code> (or another model of your choice)</li>
                <li>Make sure the Ollama service is running</li>
            </ol>
            
            <div class="note">
                <p><strong>Note:</strong> Ollama runs locally on your computer and doesn't require an API key. However, it requires more system resources than using a cloud-based service.</p>
            </div>
            
            <h2>Additional Features: Brave Search Integration</h2>
            
            <p>To enable search functionality in MagicTutor:</p>
            <ol>
                <li>Go to <a href="https://brave.com/search/api/" target="_blank">https://brave.com/search/api/</a></li>
                <li>Create an account or sign in</li>
                <li>Get an API key</li>
                <li>Set the environment variable <code>BRAVE_SEARCH_API_KEY</code> to your API key</li>
            </ol>
            
            <h2>Next Steps</h2>
            
            <p>After setting up at least one of the options above:</p>
            <ol>
                <li>Restart MagicTutor</li>
                <li>Try generating a quiz again</li>
            </ol>
            
            <p>If you continue to have issues, please check the logs for more information.</p>
        </body>
        </html>
        """
        
        # Create a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Create the output file path
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", f"model_setup_tutorial_{timestamp}.html")
        
        # Write the tutorial content to the file
        with open(file_path, "w") as f:
            f.write(tutorial_content)
        
        # Open the file in the default web browser
        try:
            webbrowser.open(file_path)
            logger.info(f"Automatically opened tutorial at {file_path} in the default browser")
        except Exception as e:
            logger.error(f"Error opening tutorial in browser: {str(e)}")
        
        # Return the result with information about the tutorial
        return {
            "file_path": file_path,
            "format": "html",
            "num_questions": 0,
            "topic": "Model Setup Tutorial",
            "subtopic": "How to set up API keys or install Ollama",
            "model_used": "none"
        }
    
    # Generate microcourse content using the selected model
    if selected_platform == "groq":
        # Use GROQ for microcourse generation
        try:
            import groq
            
            # Get the GROQ API key from environment variables
            groq_api_key = os.environ.get("GROQ_API_KEY")
            if not groq_api_key:
                logger.error("GROQ_API_KEY environment variable not found")
                microcourse_content = "# Microcourse content could not be generated\n\nThe GROQ API key is not available."
            else:
                # Create a GROQ client
                groq_client = groq.Client(api_key=groq_api_key)
                
                # Generate the response using the GROQ API
                response = groq_client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": "You are an educational content creator. You create clear, concise, and informative content in markdown format. Format your response using markdown with proper headings, bullet points, and code blocks where appropriate."},
                        {"role": "user", "content": microcourse_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4000
                )
                
                # Extract the response text
                microcourse_content = response.choices[0].message.content
                logger.info(f"Generated microcourse from GROQ: {microcourse_content[:100]}...")
        except Exception as e:
            error_message = f"Error generating microcourse from GROQ: {str(e)}"
            logger.error(error_message)
            microcourse_content = f"# Error generating microcourse\n\n{error_message}"
    elif selected_platform == "openrouter":
        # Use OpenRouter for microcourse generation
        try:
            import openai
            
            # Get the OpenRouter API key from environment variables
            openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
            if not openrouter_api_key:
                logger.error("OPENROUTER_API_KEY environment variable not found")
                microcourse_content = "# Microcourse content could not be generated\n\nThe OpenRouter API key is not available."
            else:
                # Create an OpenAI client with OpenRouter base URL
                openai_client = openai.OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=openrouter_api_key,
                )
                
                # Generate the response using the OpenRouter API
                response = openai_client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": "You are an educational content creator. You create clear, concise, and informative content in markdown format. Format your response using markdown with proper headings, bullet points, and code blocks where appropriate."},
                        {"role": "user", "content": microcourse_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4000
                )
                
                # Extract the response text
                microcourse_content = response.choices[0].message.content
                logger.info(f"Generated microcourse from OpenRouter: {microcourse_content[:100]}...")
        except Exception as e:
            error_message = f"Error generating microcourse from OpenRouter: {str(e)}"
            logger.error(error_message)
            microcourse_content = f"# Error generating microcourse\n\n{error_message}"
    elif selected_platform == "ollama":
        # Use Ollama for microcourse generation
        try:
            import openai
            
            # Import the function to get available Ollama models
            from quiz_generator.utils.host_agent import get_available_ollama_models
            
            # If just "ollama" is specified, get available models and use the first one
            if selected_model == "ollama":
                available_models = get_available_ollama_models()
                if not available_models:
                    logger.error("No Ollama models available")
                    microcourse_content = "# Microcourse content could not be generated\n\nNo Ollama models are available. Please pull a model using 'ollama pull llama3' or similar."
                else:
                    # Use the first available model
                    ollama_model = available_models[0]
                    logger.info(f"Using automatically selected Ollama model: {ollama_model}")
                    
                    # Create an OpenAI client with Ollama base URL
                    ollama_client = openai.OpenAI(
                        base_url="http://localhost:11434/v1",
                        api_key="ollama",  # Ollama doesn't require an API key, but the client requires a non-empty string
                    )
                    
                    # Generate the response using the Ollama API
                    response = ollama_client.chat.completions.create(
                        model=ollama_model,
                        messages=[
                            {"role": "system", "content": "You are an educational content creator. You create clear, concise, and informative content in markdown format. Format your response using markdown with proper headings, bullet points, and code blocks where appropriate."},
                            {"role": "user", "content": microcourse_prompt}
                        ],
                        temperature=0.7,
                        max_tokens=4000
                    )
                    
                    # Extract the response text
                    microcourse_content = response.choices[0].message.content
                    logger.info(f"Generated microcourse from Ollama ({ollama_model}): {microcourse_content[:100]}...")
            else:
                # Extract the actual model name from the string (remove "ollama:" prefix)
                if selected_model.startswith("ollama:"):
                    ollama_model = selected_model.split(":", 1)[1]
                else:
                    ollama_model = selected_model
                
                # Create an OpenAI client with Ollama base URL
                ollama_client = openai.OpenAI(
                    base_url="http://localhost:11434/v1",
                    api_key="ollama",  # Ollama doesn't require an API key, but the client requires a non-empty string
                )
                
                # Generate the response using the Ollama API
                response = ollama_client.chat.completions.create(
                    model=ollama_model,
                    messages=[
                        {"role": "system", "content": "You are an educational content creator. You create clear, concise, and informative content in markdown format. Format your response using markdown with proper headings, bullet points, and code blocks where appropriate."},
                        {"role": "user", "content": microcourse_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=4000
                )
                
                # Extract the response text
                microcourse_content = response.choices[0].message.content
                logger.info(f"Generated microcourse from Ollama ({ollama_model}): {microcourse_content[:100]}...")
            
        except Exception as e:
            error_message = f"Error generating microcourse from Ollama: {str(e)}"
            logger.error(error_message)
            microcourse_content = f"# Error generating microcourse\n\n{error_message}"
    elif selected_platform == "anthropic":
        # Use Anthropic for microcourse generation
        import anthropic
        
        # Get the Anthropic API key from environment variables
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            microcourse_content = "# Microcourse content could not be generated\n\nThe Anthropic API key is not available."
        else:
            # Create an Anthropic client
            client = anthropic.Anthropic(api_key=api_key)
            
            try:
                # Generate the response using the Anthropic API with a different system prompt
                response = client.messages.create(
                    model=selected_model,
                    max_tokens=4000,
                    temperature=0.7,
                    system="You are an educational content creator. You create clear, concise, and informative content in markdown format. Format your response using markdown with proper headings, bullet points, and code blocks where appropriate.",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": microcourse_prompt
                                }
                            ]
                        }
                    ]
                )
                
                # Extract the response text
                microcourse_content = response.content[0].text
            except Exception as e:
                microcourse_content = f"# Error generating microcourse\n\n{str(e)}"
    
    # Generate questions
    questions = []
    for i in range(num_questions):
        # Generate a prompt based on the question type
        if question_type == "multiple_choice":
            prompt = question_generator.generate_multiple_choice_question(
                topic=topic,
                subtopic=subtopic,
                focus=question_focus,
                difficulty=difficulty,
                question_number=i+1
            )
        elif question_type == "true_false":
            prompt = question_generator.generate_true_false_question(
                topic=topic,
                subtopic=subtopic,
                focus=question_focus,
                difficulty=difficulty,
                question_number=i+1
            )
        else:  # cloze
            prompt = question_generator.generate_cloze_question(
                topic=topic,
                subtopic=subtopic,
                focus=question_focus,
                difficulty=difficulty,
                question_number=i+1
            )
        
        # Import the host_agent module to use the correct function
        from quiz_generator.utils.host_agent import get_host_agent_response as host_agent_get_response
        
        # Send the prompt to the host agent using the imported function
        response = host_agent_get_response(prompt, None, selected_model, selected_platform)
        
        # Parse the response into a Question object
        question = question_generator.parse_question_response(
            response=response,
            question_type=question_type,
            topic=topic,
            subtopic=subtopic,
            focus=question_focus
        )
        
        # Add the question to the list
        questions.append(question)
    
    # Create the output file
    if output_format == "bquiz":
        file_path = create_bootable_quiz(questions, topic, subtopic, microcourse_content)
    else:  # html
        file_path = create_html_quiz(questions, topic, subtopic, microcourse_content)
    
    # Open the file if it's an HTML file
    if output_format == "html":
        try:
            # Open the HTML file in the default web browser
            webbrowser.open(file_path)
            logger.info(f"Automatically opened {file_path} in the default browser")
        except Exception as e:
            logger.error(f"Error opening file in browser: {str(e)}")
    
    # Return the result, including the model used
    result = {
        "file_path": file_path,
        "format": output_format,
        "num_questions": len(questions),
        "topic": topic,
        "subtopic": subtopic
    }
    
    # Add the model used to the result
    if selected_platform == "ollama":
        # For automatic Ollama model selection, include the actual model used
        result["model_used"] = f"ollama:{ollama_model}" if 'ollama_model' in locals() else "ollama:unknown"
    else:
        # For other models (Claude, GROQ, OpenRouter)
        result["model_used"] = selected_model
    
    return result

# Run the MCP server
if __name__ == "__main__":
    mcp.run()
