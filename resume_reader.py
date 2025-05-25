


import pdfplumber

def extract_skills(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"
    except Exception as e:
        return {"error": f"Failed to read PDF: {e}"}

    lines = all_text.split("\n")
    skills = []
    education = []
    location = ""
    summary = ""

    for i, line in enumerate(lines):
        line_lower = line.lower()

        # Skills extraction
        if "skills" in line_lower:
            for j in range(i+1, i+6):
                if j < len(lines):
                    skills_line = lines[j].strip()
                    if skills_line:
                        # Support commas, semicolons, or new lines
                        for item in skills_line.replace(";", ",").split(","):
                            if item.strip():
                                skills.append(item.strip())
                                summary += item.strip() + ", "

        # Education extraction
        if "education" in line_lower:
            for j in range(i+1, i+6):
                if j < len(lines):
                    edu_line = lines[j].strip()
                    if edu_line:
                        education.append(edu_line)

        # Location detection
        if "indore" in line_lower:
            location = "Indore"

    # Deduplicate and clean
    skills = list(set(s.strip().lower() for s in skills if s.strip()))
    education = list(dict.fromkeys(education))  # preserve order, remove duplicates

    return {
        "skills": skills,
        "education": education,
        "location": location or "Not found",
        "summary": summary.strip(", "),
        "raw_text": all_text.strip()
    }

# Test
if __name__ == "__main__":
    result = extract_skills("resume.pdf")
    print("📍 Location:", result["location"])
    print("🎓 Education:", result["education"])
    print("🛠️ Skills:", result["skills"])
    print("🧠 Summary:", result["summary"])
