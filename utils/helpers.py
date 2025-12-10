"""Helper functions"""

def format_percentage(value: float) -> str:
    """Format number as percentage"""
    return f"{value:.1f}%"

def get_score_color(score: float) -> str:
    """Get color based on score"""
    if score >= 80:
        return "🟢"
    elif score >= 60:
        return "🟡"
    else:
        return "🔴"

def get_score_label(score: float) -> str:
    """Get label based on score"""
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    else:
        return "Fair"

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text"""
    if len(text) > max_length:
        return text[:max_length-3] + "..."
    return text
