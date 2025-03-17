"""
HTML components for quiz templates.
"""

def get_sidebar_html(topic, subtopic=None, has_microcourse=False):
    """
    Returns the HTML for the sidebar.
    
    Args:
        topic: The main topic of the quiz
        subtopic: Optional subtopic of the quiz
        has_microcourse: Whether the quiz has a microcourse
        
    Returns:
        str: HTML for the sidebar as a string
    """
    subtitle = f"{topic}{f' - {subtopic}' if subtopic else ''}"
    
    # Add microcourse tab if available
    microcourse_tab = ""
    if has_microcourse:
        microcourse_tab = """
        <div class="nav-item" id="microcourse-tab">Microcourse</div>
        """
    
    return f"""
    <div class="sidebar">
        <div class="sidebar-header">
            <h2>Quiz Navigation</h2>
            <p>{subtitle}</p>
        </div>
        <div class="tabs">
            {microcourse_tab}
            <div class="nav-items" id="questionNav">
                <!-- Navigation items will be added here by JavaScript -->
            </div>
        </div>
    </div>
    """

def get_main_content_html(topic, subtopic=None, has_microcourse=False):
    """
    Returns the HTML for the main content area.
    
    Args:
        topic: The main topic of the quiz
        subtopic: Optional subtopic of the quiz
        has_microcourse: Whether the quiz has a microcourse
        
    Returns:
        str: HTML for the main content as a string
    """
    title = f"Quiz on {topic}{f' - {subtopic}' if subtopic else ''}"
    
    # Add microcourse container if available
    microcourse_container = ""
    if has_microcourse:
        microcourse_container = """
        <div id="microcourseContainer" style="display: none;">
            <!-- Microcourse content will be added here by JavaScript -->
        </div>
        """
    
    return f"""
    <div class="main-content">
        <div class="quiz-header">
            <h1>{title}</h1>
        </div>
        
        {microcourse_container}
        
        <div id="questionsContainer">
            <!-- Question containers will be added here by JavaScript -->
        </div>
    </div>
    """
