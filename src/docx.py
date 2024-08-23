from docx import Document

def wrap_text(text, width=80):
    wrapped_lines = []
    for line in text.splitlines():
        current_line = ""
        for word in line.split():
            if len(current_line) + len(word) + 1 <= width:
                if current_line:
                    current_line += " "
                current_line += word
            else:
                wrapped_lines.append(current_line)
                current_line = word
        wrapped_lines.append(current_line)
    return wrapped_lines

def convert_docx_to_lines(docx_path, width=80, substitutions=None):
    # Load the DOCX file
    doc = Document(docx_path)
    full_text = []

    # Extract the text from the DOCX
    for para in doc.paragraphs:
        full_text.append(para.text)
    
    # Combine the paragraphs into a single text block
    content = '\n'.join(full_text)

    # Perform character substitutions if any
    if substitutions:
        for key, value in substitutions.items():
            content = content.replace(key, value)
    
    # Wrap the text to the specified width
    wrapped_lines = wrap_text(content, width)

    return wrapped_lines


