from flask import Flask, render_template, request
from openai import OpenAI
import markdown
import os

app = Flask(__name__)

# Get OpenRouter API key from Render Environment Variables
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    try:
        career_goal = request.form["career_goal"]
        level = request.form["level"]
        hours = request.form["hours"]
        duration = request.form["duration"]

        prompt = f"""
You are an expert career mentor and AI learning advisor.

Create a detailed learning roadmap.

Career Goal: {career_goal}
Current Skill Level: {level}
Study Hours Per Week: {hours}
Roadmap Duration: {duration}

Provide:

# Overview

# Month-by-Month Roadmap

# Skills To Learn

# Recommended Courses

# Recommended Projects

# Weekly Study Schedule


# Expected Outcome

Format professionally using headings and bullet points.
"""

        response = client.chat.completions.create(
            model="openrouter/auto",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional career mentor."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000
        )

        roadmap_text = response.choices[0].message.content

        roadmap_html = markdown.markdown(
            roadmap_text,
            extensions=["extra"]
        )

        return render_template(
            "result.html",
            roadmap=roadmap_html
        )

    except Exception as e:
        return render_template(
            "result.html",
            roadmap=f"<h2>Error</h2><p>{str(e)}</p>"
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)