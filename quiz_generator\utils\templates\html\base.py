"""
Base HTML structure for quiz templates.
"""

def get_base_html(head_content, body_content, css_styles, javascript_code):
    """
    Returns the base HTML structure.
    
    Args:
        head_content: The content for the head section
        body_content: The content for the body section
        css_styles: The CSS styles
        javascript_code: The JavaScript code
        
    Returns:
        str: Complete HTML document as a string
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    {head_content}
    <style>
    {css_styles}
    </style>
</head>
<body>
    {body_content}

    <script>
    {javascript_code}
    </script>
</body>
</html>"""
