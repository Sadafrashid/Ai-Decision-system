import streamlit as st
import json, os
import matplotlib.pyplot as plt
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from personality import calculate_personality
from decision import recommend_decision

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Decision System", layout="centered")

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.main-title {text-align:center; font-size:32px; color:#4CAF50;}
.card {background:#1e1e1e; padding:15px; border-radius:12px; margin:10px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🧠 AI Personality Intelligence System</p>', unsafe_allow_html=True)

# ---------------- LOAD ----------------
file_path = os.path.join(os.path.dirname(__file__), "questions.json")
questions = json.load(open(file_path))

# Load saved personality
traits = None
if os.path.exists("user_personality.json"):
    traits = json.load(open("user_personality.json"))

# ---------------- FUNCTIONS ----------------
def plot_radar(traits):
    labels = list(traits.keys())
    values = list(traits.values())
    values += values[:1]
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw={'polar': True})
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    return fig

def interpret_personality(traits):
    desc = []
    if traits["Openness"] > 6: desc.append("creative")
    if traits["Conscientiousness"] > 6: desc.append("disciplined")
    if traits["Extraversion"] > 6: desc.append("social")
    if traits["Agreeableness"] > 6: desc.append("kind")
    if traits["Neuroticism"] > 6: desc.append("emotionally sensitive")
    return "You are " + ", ".join(desc) + "."

def strengths_weaknesses(traits):
    s, w = [], []
    if traits["Openness"] > 6: s.append("Creative thinking")
    else: w.append("Low openness")
    if traits["Conscientiousness"] > 6: s.append("Strong discipline")
    else: w.append("Needs planning")
    if traits["Neuroticism"] > 6: w.append("Overthinking")
    return s, w

def career_suggestions(traits):
    if traits["Openness"] > 6 and traits["Extraversion"] > 6:
        return ["Entrepreneurship", "Marketing", "Design"]
    elif traits["Conscientiousness"] > 6:
        return ["Software Engineering", "Data Science"]
    else:
        return ["Research", "Writing"]

def stress_advice(text, traits):
    text = text.lower()
    if "exam" in text:
        return "Use Pomodoro technique and take breaks."
    if "stress" in text:
        return "Practice deep breathing and relaxation."
    if traits and traits["Neuroticism"] > 6:
        return "Try meditation and journaling."
    return "Stay balanced and calm."

def chatbot_response(text, traits):
    text = text.lower()
    if "career" in text:
        return ", ".join(career_suggestions(traits))
    if "stress" in text:
        return stress_advice(text, traits)
    if "personality" in text:
        return interpret_personality(traits)
    return "Ask about career, stress, or personality."

def generate_pdf(traits):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()
    content = [Paragraph("Personality Report", styles["Title"])]

    for k,v in traits.items():
        content.append(Paragraph(f"{k}: {v}", styles["Normal"]))

    doc.build(content)
    return "report.pdf"

# ---------------- MENU ----------------
mode = st.sidebar.selectbox("Choose Feature",
["Personality Test","Decision Support","Stress Relief","AI Chatbot"])

# ---------------- PERSONALITY ----------------
if mode == "Personality Test":
    st.header("🧠 Personality Analysis")
    answers = [st.slider(q,1,5,3) for q in questions]

    if st.button("Analyze"):
        traits = calculate_personality(answers)
        json.dump(traits, open("user_personality.json","w"))

        st.success(interpret_personality(traits))
        st.pyplot(plot_radar(traits))

        s,w = strengths_weaknesses(traits)

        st.subheader("💪 Strengths")
        for i in s: st.write("✔️",i)

        st.subheader("⚠️ Improvements")
        for i in w: st.write("🔹",i)

        st.subheader("🎯 Careers")
        for c in career_suggestions(traits): st.write("👉",c)

        if st.button("Download Report"):
            file = generate_pdf(traits)
            st.download_button("Download PDF", open(file,"rb"), file_name="report.pdf")

# ---------------- DECISION ----------------
elif mode == "Decision Support":
    st.header("🤔 Decision Support")

    if not traits:
        st.warning("Complete Personality Test first.")
    else:
        c1 = st.text_input("Option 1")
        c2 = st.text_input("Option 2")

        if st.button("Recommend"):
            d,r = recommend_decision(traits,c1,c2)
            st.success(d)
            st.info(r)

# ---------------- STRESS ----------------
elif mode == "Stress Relief":
    st.header("😌 Stress Advisor")
    text = st.text_area("How are you feeling?")

    if st.button("Get Advice"):
        st.success(stress_advice(text, traits))

# ---------------- CHATBOT ----------------
elif mode == "AI Chatbot":
    st.header("🤖 AI Assistant")
    msg = st.text_input("Ask something")

    if st.button("Send"):
        st.success(chatbot_response(msg, traits))