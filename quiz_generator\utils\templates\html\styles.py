"""
CSS styles for HTML quiz templates.
"""

def get_css_styles():
    """
    Returns the CSS styles for the HTML quiz template.
    
    Returns:
        str: CSS styles as a string
    """
    return """
    :root {
        --primary-color: #4a6fa5;
        --secondary-color: #6b8cae;
        --accent-color: #ff7e5f;
        --light-bg: #f8f9fa;
        --dark-bg: #343a40;
        --text-color: #333;
        --light-text: #f8f9fa;
        --correct-color: #28a745;
        --incorrect-color: #dc3545;
    }
    
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: var(--text-color);
        background-color: #f5f7fa;
        display: flex;
        min-height: 100vh;
    }
    
    .sidebar {
        width: 250px;
        background-color: var(--dark-bg);
        color: var(--light-text);
        padding: 20px 0;
        position: fixed;
        height: 100vh;
        overflow-y: auto;
        transition: all 0.3s;
    }
    
    .sidebar-header {
        padding: 0 20px 20px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    
    .sidebar-header h2 {
        font-size: 1.2rem;
        color: var(--light-text);
        margin-bottom: 5px;
    }
    
    .sidebar-header p {
        font-size: 0.9rem;
        opacity: 0.7;
    }
    
    .tabs {
        display: flex;
        flex-direction: column;
    }
    
    .nav-item {
        padding: 10px 20px;
        cursor: pointer;
        transition: all 0.2s;
        border-left: 3px solid transparent;
    }
    
    .nav-item:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }
    
    .nav-item.active {
        background-color: rgba(255, 255, 255, 0.2);
        border-left: 3px solid var(--accent-color);
    }
    
    #microcourse-tab {
        font-weight: bold;
        background-color: rgba(255, 255, 255, 0.05);
        margin-bottom: 10px;
    }
    
    #microcourse-tab.active {
        background-color: rgba(255, 255, 255, 0.2);
        border-left: 3px solid var(--accent-color);
    }
    
    /* This rule ensures that when any question tab is active, the microcourse tab is not highlighted */
    #questionNav .nav-item.active ~ #microcourse-tab.active,
    #questionNav .nav-item.active + #microcourse-tab.active,
    .nav-items:has(.nav-item.active) ~ #microcourse-tab.active,
    .tabs:has(#questionNav .nav-item.active) #microcourse-tab {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-left: 3px solid transparent !important;
    }
    
    /* Force mutual exclusivity between tabs */
    .deactivated {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-left: 3px solid transparent !important;
    }
    
    #microcourseContainer {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        padding: 25px;
        margin-bottom: 20px;
    }
    
    .microcourse-content {
        margin-bottom: 20px;
    }
    
    .main-content {
        flex: 1;
        margin-left: 250px;
        padding: 30px;
        max-width: 900px;
    }
    
    .quiz-header {
        margin-bottom: 30px;
        padding-bottom: 20px;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .quiz-header h1 {
        font-size: 2rem;
        color: var(--primary-color);
        margin-bottom: 10px;
    }
    
    .question-container {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        padding: 25px;
        margin-bottom: 20px;
        display: none;
    }
    
    .question-container.active {
        display: block;
    }
    
    .question-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .question-number {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--primary-color);
    }
    
    .question-text {
        font-size: 1.2rem;
        margin-bottom: 20px;
        line-height: 1.5;
    }
    
    .options-list {
        list-style-type: none;
        margin-bottom: 20px;
    }
    
    .option-item {
        padding: 12px 15px;
        margin-bottom: 10px;
        background-color: var(--light-bg);
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.2s;
        border: 2px solid transparent;
    }
    
    .option-item:hover {
        background-color: #e9ecef;
    }
    
    .option-item.selected {
        border-color: var(--primary-color);
        background-color: rgba(74, 111, 165, 0.1);
    }
    
    .option-item.correct {
        border-color: var(--correct-color);
        background-color: rgba(40, 167, 69, 0.1);
    }
    
    .option-item.incorrect {
        border-color: var(--incorrect-color);
        background-color: rgba(220, 53, 69, 0.1);
    }
    
    /* True/False question styles */
    .true-false-container {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    
    .tf-option {
        display: flex;
        align-items: center;
        padding: 12px 20px;
        background-color: var(--light-bg);
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.2s;
        border: 2px solid transparent;
        min-width: 120px;
    }
    
    .tf-option:hover {
        background-color: #e9ecef;
    }
    
    .tf-option.selected {
        border-color: var(--primary-color);
        background-color: rgba(74, 111, 165, 0.1);
    }
    
    .tf-option.correct {
        border-color: var(--correct-color);
        background-color: rgba(40, 167, 69, 0.1);
    }
    
    .tf-option.incorrect {
        border-color: var(--incorrect-color);
        background-color: rgba(220, 53, 69, 0.1);
    }
    
    .tf-radio {
        display: inline-block;
        width: 18px;
        height: 18px;
        border: 2px solid #adb5bd;
        border-radius: 50%;
        margin-right: 10px;
        position: relative;
    }
    
    .tf-option.selected .tf-radio::after {
        content: '';
        position: absolute;
        top: 3px;
        left: 3px;
        width: 8px;
        height: 8px;
        background-color: var(--primary-color);
        border-radius: 50%;
    }
    
    .tf-option.correct .tf-radio {
        border-color: var(--correct-color);
    }
    
    .tf-option.correct .tf-radio::after {
        background-color: var(--correct-color);
    }
    
    .tf-option.incorrect .tf-radio {
        border-color: var(--incorrect-color);
    }
    
    .tf-option.incorrect .tf-radio::after {
        background-color: var(--incorrect-color);
    }
    
    .tf-label {
        font-weight: 500;
    }
    
    /* Cloze (fill-in-the-blank) question styles */
    .cloze-container {
        margin-bottom: 20px;
    }
    
    .cloze-input {
        display: block;
        width: 100%;
        max-width: 400px;
        padding: 12px 15px;
        font-size: 1rem;
        border: 2px solid #ced4da;
        border-radius: 5px;
        background-color: var(--light-bg);
        transition: all 0.2s;
        margin-top: 10px;
    }
    
    .cloze-input:focus {
        outline: none;
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(74, 111, 165, 0.2);
    }
    
    .cloze-input.correct-input {
        border-color: var(--correct-color);
        background-color: rgba(40, 167, 69, 0.1);
    }
    
    .cloze-input.incorrect-input {
        border-color: var(--incorrect-color);
        background-color: rgba(220, 53, 69, 0.1);
    }
    
    .answer-section {
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid #e0e0e0;
    }
    
    .answer-label {
        font-weight: 600;
        color: var(--primary-color);
        margin-bottom: 5px;
    }
    
    .explanation-section {
        margin-top: 20px;
        display: none;
    }
    
    .explanation-content {
        background-color: #f0f7ff;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid var(--primary-color);
    }
    
    .button {
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .primary-button {
        background-color: var(--primary-color);
        color: white;
    }
    
    .primary-button:hover {
        background-color: var(--secondary-color);
    }
    
    .secondary-button {
        background-color: #e9ecef;
        color: var(--text-color);
    }
    
    .secondary-button:hover {
        background-color: #dee2e6;
    }
    
    .button-group {
        display: flex;
        justify-content: space-between;
        margin-top: 30px;
    }
    
    .explanation-toggle {
        margin-top: 15px;
    }
    
    .feedback-message {
        margin-top: 15px;
        padding: 10px;
        border-radius: 5px;
        font-weight: 600;
    }
    
    .feedback-correct {
        background-color: rgba(40, 167, 69, 0.1);
        color: var(--correct-color);
        border: 1px solid var(--correct-color);
    }
    
    .feedback-incorrect {
        background-color: rgba(220, 53, 69, 0.1);
        color: var(--incorrect-color);
        border: 1px solid var(--incorrect-color);
    }
    
    /* Results page styles */
    .results-container {
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        padding: 25px;
        margin-bottom: 20px;
    }
    
    .results-header {
        margin-bottom: 25px;
    }
    
    .results-header h2 {
        font-size: 1.8rem;
        color: var(--primary-color);
        margin-bottom: 15px;
    }
    
    .results-summary {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        background-color: var(--light-bg);
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    
    .summary-item {
        display: flex;
        flex-direction: column;
        min-width: 120px;
    }
    
    .summary-label {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 5px;
    }
    
    .summary-value {
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .passing-score {
        color: var(--correct-color);
    }
    
    .failing-score {
        color: var(--incorrect-color);
    }
    
    .results-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 25px;
    }
    
    .results-table th,
    .results-table td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .results-table th {
        background-color: var(--light-bg);
        font-weight: 600;
        color: var(--primary-color);
    }
    
    .results-table tr:hover {
        background-color: rgba(0, 0, 0, 0.02);
    }
    
    .question-cell {
        color: var(--primary-color);
        cursor: pointer;
        font-weight: 500;
    }
    
    .question-cell:hover {
        text-decoration: underline;
    }
    
    .correct-result {
        color: var(--correct-color);
        font-weight: 500;
    }
    
    .incorrect-result {
        color: var(--incorrect-color);
        font-weight: 500;
    }
    
    .not-answered {
        color: #6c757d;
        font-style: italic;
    }
    
    .result-icon {
        display: inline-block;
        width: 20px;
        height: 20px;
        line-height: 20px;
        text-align: center;
        border-radius: 50%;
        margin-right: 5px;
    }
    
    .correct-result .result-icon {
        background-color: var(--correct-color);
        color: white;
    }
    
    .incorrect-result .result-icon {
        background-color: var(--incorrect-color);
        color: white;
    }
    
    @media (max-width: 768px) {
        .sidebar {
            width: 200px;
        }
        
        .main-content {
            margin-left: 200px;
        }
    }
    
    @media (max-width: 576px) {
        body {
            flex-direction: column;
        }
        
        .sidebar {
            width: 100%;
            height: auto;
            position: relative;
            padding: 15px;
        }
        
        .main-content {
            margin-left: 0;
            padding: 20px;
        }
        
        .nav-items {
            display: flex;
            overflow-x: auto;
            padding-bottom: 10px;
        }
        
        .nav-item {
            padding: 8px 12px;
            border-left: none;
            border-bottom: 3px solid transparent;
            white-space: nowrap;
        }
        
        .nav-item.active {
            border-left: none;
            border-bottom: 3px solid var(--accent-color);
        }
    }
    
    /* Code block styling */
    pre {
        background-color: #282c34;
        border-radius: 6px;
        padding: 16px;
        overflow-x: auto;
        margin: 1.5em 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    pre code {
        font-family: 'Fira Code', 'Consolas', 'Monaco', 'Courier New', monospace;
        font-size: 0.9em;
        line-height: 1.5;
        color: #abb2bf;
        background-color: transparent;
        padding: 0;
        border-radius: 0;
    }
    
    code {
        font-family: 'Fira Code', 'Consolas', 'Monaco', 'Courier New', monospace;
        background-color: rgba(110, 118, 129, 0.1);
        padding: 0.2em 0.4em;
        border-radius: 3px;
        font-size: 0.9em;
        color: #e06c75;
    }
    
    /* Markdown styling */
    .markdown-content h1,
    .markdown-content h2,
    .markdown-content h3,
    .markdown-content h4,
    .markdown-content h5,
    .markdown-content h6 {
        margin-top: 1.5em;
        margin-bottom: 0.5em;
        font-weight: 600;
        line-height: 1.25;
        color: var(--primary-color);
    }
    
    .markdown-content h1 { font-size: 2em; }
    .markdown-content h2 { font-size: 1.5em; }
    .markdown-content h3 { font-size: 1.25em; }
    
    .markdown-content p {
        margin-bottom: 1em;
        line-height: 1.6;
    }
    
    .markdown-content ul,
    .markdown-content ol {
        margin-bottom: 1em;
        padding-left: 2em;
    }
    
    .markdown-content li {
        margin-bottom: 0.5em;
    }
    
    .markdown-content blockquote {
        padding: 0.5em 1em;
        margin: 1em 0;
        border-left: 4px solid var(--primary-color);
        background-color: rgba(0, 0, 0, 0.03);
        color: #666;
    }
    
    .markdown-content img {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 1.5em auto;
        border-radius: 6px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .markdown-content table {
        width: 100%;
        border-collapse: collapse;
        margin: 1.5em 0;
    }
    
    .markdown-content th,
    .markdown-content td {
        padding: 8px 12px;
        border: 1px solid #ddd;
        text-align: left;
    }
    
    .markdown-content th {
        background-color: #f5f5f5;
        font-weight: 600;
    }
    
    .markdown-content tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    """
