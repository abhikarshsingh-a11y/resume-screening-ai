def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra spaces
    text = text.strip()
    
    # Replace new lines with space
    text = text.replace("\n", " ")
    
    # Remove double spaces
    while "  " in text:
        text = text.replace("  ", " ")
    
    return text

# Test it
sample = "  ABHIKARSH SINGH\n2ND YEAR    B.Tech  "
result = clean_text(sample)
print(result)