import json
import re


def _escape_control_chars(value: str) -> str:
    """
    Escape unescaped control characters (newlines, tabs, carriage returns) in a string.
    Preserves already escaped sequences.
    
    Args:
        value: The string value to fix
        
    Returns:
        String with properly escaped control characters
    """
    fixed_chars = []
    i = 0
    
    while i < len(value):
        if value[i] == '\\' and i + 1 < len(value):
            # Already escaped character, keep it as is
            fixed_chars.append(value[i])
            fixed_chars.append(value[i + 1])
            i += 2
        elif value[i] == '\n':
            fixed_chars.append('\\n')
            i += 1
        elif value[i] == '\r':
            # Check if followed by \n (CRLF)
            if i + 1 < len(value) and value[i + 1] == '\n':
                fixed_chars.append('\\n')
                i += 2
            else:
                fixed_chars.append('\\n')
                i += 1
        elif value[i] == '\t':
            fixed_chars.append('\\t')
            i += 1
        else:
            fixed_chars.append(value[i])
            i += 1
    
    return ''.join(fixed_chars)


def load_job_json(file_path: str) -> dict:
    """
    Load job.json file with automatic newline fixing.
    Specifically handles the job_description field which often contains unescaped newlines
    when copy-pasting job descriptions.
    
    Args:
        file_path: Path to the job.json file
        
    Returns:
        Dictionary with 'job_description' and 'company' keys
        
    Raises:
        ValueError: If the JSON cannot be parsed even after fixing newlines
        FileNotFoundError: If the file doesn't exist
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Try to parse JSON normally first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # If parsing fails, try to fix unescaped newlines in job_description field
        job_desc_match = re.search(r'"job_description"\s*:\s*"', content)
        if job_desc_match:
            start_pos = job_desc_match.end()
            # Find the matching closing quote (accounting for escaped quotes)
            pos = start_pos
            while pos < len(content):
                if content[pos] == '\\' and pos + 1 < len(content):
                    pos += 2
                    continue
                if content[pos] == '"':
                    # Check if this is the closing quote (followed by comma or closing brace)
                    next_char_pos = pos + 1
                    while next_char_pos < len(content) and content[next_char_pos] in ' \t\n\r':
                        next_char_pos += 1
                    if next_char_pos < len(content) and content[next_char_pos] in ',}':
                        break
                pos += 1
            
            # Extract and fix the value
            value = content[start_pos:pos]
            fixed_value = _escape_control_chars(value)
            fixed_content = content[:start_pos] + fixed_value + content[pos:]
            
            try:
                return json.loads(fixed_content)
            except json.JSONDecodeError as parse_error:
                raise ValueError(f"Could not parse job.json even after fixing newlines: {parse_error}")
        else:
            raise ValueError("Could not find 'job_description' field in job.json")

