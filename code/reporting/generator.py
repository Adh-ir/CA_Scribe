import os
import datetime

def generate_markdown_content(mappings):
    """
    Generates the markdown content string from mappings.
    """
    lines = []
    lines.append("# SAICA_Scribe Assessment Report\n")
    lines.append(f"**Date Generated**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("**Status**: Draft\n")
    
    lines.append("## Overview")
    lines.append("This report maps the trainee's reported activities to the SAICA Competency Framework.\n")
    
    lines.append("## Mapped Competencies")
    
    if not mappings:
        lines.append("> [!WARNING]")
        lines.append("> No competencies were identified for the given activity.")
    
    for item in mappings:
        lines.append("<br>\n") # Extra visual space
        lines.append(f"### 🎯 {item.get('name', 'Unknown Competency')}\n")
        lines.append(f"**Code**: `{item.get('competency_code', 'N/A')}`\n")
        
        confidence = item.get('confidence', 0)
        # Ensure confidence is 0-100 scale for display if not already
        if confidence <= 1.0: confidence *= 100
            
        confidence_str = f"{confidence:.1f}%"
        
        # Confidence Badge
        if item.get('is_weak_target'):
            badge_type = "CAUTION"
            badge_title = "Proceed with Caution (Low Confidence)"
        elif confidence > 80:
            badge_type = "TIP" # Checkmark / Greenish
            badge_title = "High Confidence"
        elif confidence > 50:
            badge_type = "NOTE"
            badge_title = "Medium Confidence"
        else:
            badge_type = "WARNING"
            badge_title = "Low Confidence"
        
        lines.append(f"> [!{badge_type}]")
        lines.append(f"> **{badge_title}**: {confidence_str}\n")
        
        lines.append("**Reasoning:**")
        lines.append(f"{item.get('reasoning', 'No reasoning provided.')}\n")
        lines.append("---\n")
        
    return "\n".join(lines)

def create_report(mappings, output_format="markdown"):
    """
    Generates a detailed report file.
    """
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"competency_report_{timestamp}.md"
    report_path = os.path.join(output_dir, report_filename)

    content = generate_markdown_content(mappings)

    with open(report_path, "w") as f:
        f.write(content)
            
    return report_path
