
from datetime import datetime

def generate_cover_letter(user_name, resume_summary, skills, job):
    intro_skills = ", ".join(skills[:3])
    tools_skills = ", ".join(skills[3:6])

    return f"""
Dear Hiring Manager at {job['company']},

I am writing to express my interest in the {job['title']} position at {job['company']}. With a background in {intro_skills} and hands-on experience with technologies such as {tools_skills}, I am confident in my ability to contribute meaningfully to your team.

Throughout my career and projects, I have demonstrated a consistent ability to learn quickly, solve complex problems, and deliver high-quality work. My resume highlights experience with {', '.join(skills[:6])}, which I noticed are closely aligned with your job requirements.

I am excited about the opportunity to work with {job['company']}, and I am particularly drawn to the mission and innovative culture your team promotes. I am eager to bring my passion and skillset to your organization and contribute to its continued success.

Thank you for your time and consideration. I would welcome the chance to further discuss how I can contribute to your team.

Sincerely,  
{user_name}  
{datetime.now().strftime('%B %d, %Y')}
"""

# Example usage
if __name__ == "__main__":
    sample_job = {
        "title": "Python Developer",
        "company": "TechCorp",
        "link": "https://remoteok.com/job/12345"
    }

    resume_summary = "Python, React, Node.js, Docker, Kubernetes, Git, GitHub Actions, CI/CD, Java, HTML"
    skills = [s.strip().lower() for s in resume_summary.split(",")]
    cover_letter = generate_cover_letter("Harsha Shree Parashar", resume_summary, skills, sample_job)

    print("📄 Generated Cover Letter:\n")
    print(cover_letter)
