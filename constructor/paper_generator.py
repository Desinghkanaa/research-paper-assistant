from shared.llm import chat


def generate_paper(repo_data: dict, analysis: dict, vector_db):
    sections = {}

    # ---------------- TITLE ----------------
    title_prompt = f"""
Generate a concise IEEE-style paper title.

Project: {repo_data.get('name')}
Domain: {analysis.get('TARGET_DOMAIN')}
Technologies: {', '.join(analysis.get('KEY_TECHNOLOGIES', [])[:3])}

Return only the title.
"""
    sections["title"] = chat(
        title_prompt,
        model="llama-3.1-8b-instant",
        max_tokens=60,
        temperature=0.2,
    ).strip()

    # ---------------- RETRIEVE CONTEXT (ONLY ONCE) ----------------
    docs = vector_db.similarity_search(
        "system architecture, algorithms, implementation details",
        k=10
    )
    context = "\n\n".join(d.page_content for d in docs)

    # ---------------- GENERATE FULL PAPER ----------------
    prompt = f"""
Generate an IEEE-style research paper with the following sections:

1. Abstract (~200 words)
2. Introduction (~600 words)
3. Methodology (~700 words)
4. Implementation (~600 words)
5. Results and Evaluation (~600 words)
6. Conclusion (~300 words)

STRICT RULES:
- Use ONLY the provided context
- Do NOT assume anything not present
- If information is missing, mention limitations
- Be technically accurate

Return output in this EXACT format:

Abstract:
...

Introduction:
...

Methodology:
...

Implementation:
...

Results and Evaluation:
...

Conclusion:
...

Context:
{context}
"""

    full_output = chat(
        prompt,
        model="llama-3.3-70b-versatile",
        max_tokens=2000,
        temperature=0.25,
    )

    # ---------------- SPLIT SECTIONS ----------------
    def extract(section_name, text):
        try:
            return text.split(section_name + ":")[1].split("\n\n")[0].strip()
        except:
            return ""

    sections["abstract"] = extract("Abstract", full_output)
    sections["introduction"] = extract("Introduction", full_output)
    sections["methodology"] = extract("Methodology", full_output)
    sections["implementation"] = extract("Implementation", full_output)
    sections["results"] = extract("Results and Evaluation", full_output)
    sections["conclusion"] = extract("Conclusion", full_output)

    # ---------------- REFERENCES ----------------
    refs_prompt = f"""
Generate 8 IEEE-style references relevant to:
{sections['title']}
"""

    sections["references"] = chat(
        refs_prompt,
        model="llama-3.1-8b-instant",
        max_tokens=300,
        temperature=0.2,
    )

    return sections