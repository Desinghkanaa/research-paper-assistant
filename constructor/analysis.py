import json
from shared.llm import chat


def analyze_repository(repo_data: dict):
    prompt = f"""
You are analyzing a GitHub repository.

STRICT RULES:
- Use ONLY the given information
- Do NOT assume anything
- If information is missing, say "Not enough information"
- Be factual and precise

Name: {repo_data.get('name')}
Description: {repo_data.get('description')}
Languages: {list(repo_data.get('languages', {}).keys())}
README:
{repo_data.get('readme','')[:3000]}

Return valid JSON with keys:
SYSTEM_PURPOSE
PROPOSED_SOLUTION
KEY_TECHNOLOGIES
PROJECT_TYPE
ARCHITECTURE
INNOVATION
TARGET_DOMAIN
SCALABILITY
"""

    response = chat(
        prompt,
        model="llama-3.1-8b-instant",
        max_tokens=1024,
        temperature=0.2,
    )


    try:
        return json.loads(response)
    except Exception:
        return {
            "SYSTEM_PURPOSE": "",
            "PROPOSED_SOLUTION": "",
            "KEY_TECHNOLOGIES": [],
            "PROJECT_TYPE": "",
            "ARCHITECTURE": "",
            "INNOVATION": "",
            "TARGET_DOMAIN": "",
            "SCALABILITY": "",
        }
