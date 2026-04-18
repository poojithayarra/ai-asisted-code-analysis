import os
from groq import Groq

client = Groq(api_key="your_api_key_here")  # Replace with your actual API key

def generate_ai_report(code, issues):
    try:
        prompt = f"""
You are a senior software engineer.

Analyze the given Python code and respond STRICTLY in this format:

### 1. Summary
(Brief explanation of what the code does)

### 2. Issues & Explanations
- Explain each issue clearly

### 3. Suggested Fixes
- Provide actionable improvements

### 4. Maintainability Advice
- Suggest improvements for readability, maintainability, and clean coding practices

Code:
{code}

Detected Issues:
{issues}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # ✅ updated working model
            messages=[
                {"role": "user", "content": prompt}
            ],
            timeout=10
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Groq Error: {str(e)}"

def generate_documentation(code):
    try:
        prompt = f"""
You are a software documentation expert.

Generate professional, industry-grade documentation for the given Python code.

Follow this structure STRICTLY:
### Overview
- What the system/module does

### Features 
- Key functionalities

### Architecture / Design
- High-level explanation of structure

### Functions Description
- Explain each function clearly

### Inputs & Outputs
- Expected inputs and outputs

### Usage Example
- Show how to use the code 

### Limitations 
- Any constraints or weaknesses

### Future Improvements
- Suggestions for scalability and enhancements

Code:
{code}
"""
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # ✅ updated
            messages=[
                {"role": "user", "content": prompt}
            ],
            timeout=10
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Groq Error: {str(e)}"
# # -------- TEST --------
# if __name__ == "__main__":
#     sample_code = """
# def add(a,b):
#     x=10
#     return a+b
# """
#     issues = ["Unused variable: x"]

#     print(generate_ai_report(sample_code, issues))


