# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from datetime import datetime
import os

# Sidebar Overview
st.sidebar.title("About TGT")
st.sidebar.markdown("""
**Temporal Gravity Theory (TGT)** is a framework for understanding how we distribute our attention and emotional energy across time: the past, present, and future.

- **Past Gravity**: Memory, nostalgia, trauma, reflection  
- **Present Gravity**: Sensory awareness, mindfulness, flow  
- **Future Gravity**: Ambition, imagination, worry, planning  

TGT helps identify where your mental energy tends to gravitate—your **Temporal Focus Ratio (TFR)**—and offers insights to rebalance.

**Goal:** Achieve *Temporal Integration*, where attention is fluid and balanced across time zones.

### Archetypes:
- 🕰️ **The Reflector** – Past-dominant
- 🌿 **The Practitioner** – Present-centered
- 🚀 **The Visionary** – Future-driven
- 🔄 **The Integrator** – Balanced and adaptable

The 15-question assessment measures your focus and plots it into this temporal model to offer clarity and action steps.
""")

# Download White Paper
with st.sidebar.expander("📄 Download the Full White Paper"):
    with open("Temporal_Gravity_Theory_White_Paper.pdf", "rb") as f:
        st.download_button("Download PDF", f, file_name="Temporal_Gravity_Theory_White_Paper.pdf")

# Title and Introduction
st.title("Temporal Focus Assessment")
st.write("""
Welcome to the Temporal Gravity Theory (TGT) Assessment.
Answer the questions to discover your dominant temporal focus and receive personalized insights.
""")

# Load questions (will be dynamic in future updates)
questions = {
    "P1": ("I often find myself replaying moments from my past.", "Past"),
    "P2": ("I think about what I could have done differently in the past.", "Past"),
    "P3": ("My past experiences influence my emotions frequently.", "Past"),
    "P4": ("I dwell on regrets more than I’d like.", "Past"),
    "P5": ("Memories from earlier in life come to mind daily.", "Past"),
    "PR1": ("I focus on what’s happening in the current moment.", "Present"),
    "PR2": ("I feel most alive when I’m engaged in the now.", "Present"),
    "PR3": ("I practice mindfulness or being present regularly.", "Present"),
    "PR4": ("I often lose track of time when I’m doing something I enjoy.", "Present"),
    "PR5": ("I don’t get easily distracted by future or past thoughts.", "Present"),
    "F1": ("I often think about what I want to accomplish in the future.", "Future"),
    "F2": ("I have a strong vision for my future.", "Future"),
    "F3": ("I make detailed plans to reach long-term goals.", "Future"),
    "F4": ("I frequently imagine what my ideal future looks like.", "Future"),
    "F5": ("The future motivates my actions today.", "Future")
}

# User identity input
st.header("Participant Info")
user_id = st.text_input("Enter your name or ID")

# View previous history
if user_id.strip():
    results_file = "results.csv"
    if os.path.exists(results_file):
        all_results = pd.read_csv(results_file)
        user_history = all_results[all_results['User ID'] == user_id]

        if not user_history.empty:
            st.subheader("📈 Your Past Assessments")
            st.dataframe(user_history.sort_values("Timestamp", ascending=False))
            st.line_chart(user_history.set_index("Timestamp")[['Past Score', 'Present Score', 'Future Score']])
        else:
            st.info("No past results found for this ID yet.")

# User input section
responses = {}
st.header("Assessment Questions")
st.write("Rate each statement from 1 (Strongly Disagree) to 7 (Strongly Agree)")

for q_id, (question_text, _) in questions.items():
    responses[q_id] = st.slider(question_text, 1, 7, 4)

# Handle submission
submit_clicked = st.button("Submit & Get Results")

if submit_clicked:
    if not user_id.strip():
        st.warning("Please enter your name or ID before submitting.")
    else:
        scores = {"Past": 0, "Present": 0, "Future": 0}
        counts = {"Past": 0, "Present": 0, "Future": 0}

        for q_id, score in responses.items():
            category = questions[q_id][1]
            scores[category] += score
            counts[category] += 1

        normalized_scores = {k: (scores[k] / (counts[k] * 7)) * 100 for k in scores}

        # Display results
        st.subheader("Your Temporal Profile")
        df_scores = pd.DataFrame.from_dict(normalized_scores, orient='index', columns=['Score (%)'])
        st.bar_chart(df_scores)

        # Radar chart visualization
        st.subheader("Radar Chart")
        categories = list(normalized_scores.keys())
        values = list(normalized_scores.values())
        values += values[:1]  # Repeat first value to close the radar chart
        num_vars = len(categories)

        angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.plot(angles, values, linewidth=2, linestyle='solid')
        ax.fill(angles, values, alpha=0.3)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_yticklabels(["0", "20", "40", "60", "80", "100"])
        st.pyplot(fig)

        # Archetype assignment logic
        dominant_focus = max(normalized_scores, key=normalized_scores.get)
        archetypes = {
            "Past": "The Nostalgic",
            "Present": "The Flow-Seeker",
            "Future": "The Visionary"
        }

        st.markdown(f"### Dominant Temporal Focus: **{dominant_focus}**")
        st.markdown(f"### Your Archetype: **{archetypes[dominant_focus]}**")

        # Add extended insights and tips
        insights = {
            "Past": (
                "You tend to reflect on past experiences. Try channeling those memories into wisdom without getting stuck in regret.",
                [
                    "Keep a gratitude journal to reframe past events positively.",
                    "Write a letter to your past self, then reflect on how you've grown.",
                    "Practice letting go rituals, like writing and burning old regrets."
                ]
            ),
            "Present": (
                "You thrive in the moment. Consider how staying grounded helps you enjoy life and stay resilient.",
                [
                    "Practice mindful breathing for 2 minutes a day.",
                    "Schedule daily 'flow time'—uninterrupted periods to enjoy what you love.",
                    "Notice and name what you're sensing throughout the day."
                ]
            ),
            "Future": (
                "You’re future-focused. Harness your vision, but don’t forget to enjoy the present journey.",
                [
                    "Create a vision board and revisit it weekly.",
                    "Break down big goals into small, daily action steps.",
                    "Balance planning with spontaneous activities to stay present."
                ]
            )
        }

        summary, tips = insights[dominant_focus]
        st.write(summary)
        st.markdown("#### Try These Tips:")
        for tip in tips:
            st.markdown(f"- {tip}")

        # Save results to CSV
        result_entry = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "User ID": user_id,
            "Past Score": round(normalized_scores["Past"], 2),
            "Present Score": round(normalized_scores["Present"], 2),
            "Future Score": round(normalized_scores["Future"], 2),
            "Archetype": archetypes[dominant_focus]
        }
        result_df = pd.DataFrame([result_entry])
        results_file = "results.csv"

        if os.path.exists(results_file):
            existing_df = pd.read_csv(results_file)
            updated_df = pd.concat([existing_df, result_df], ignore_index=True)
        else:
            updated_df = result_df

        updated_df.to_csv(results_file, index=False)
        st.success("Your results have been saved!")

        # Optional: download or save
        st.download_button("Download My Results", df_scores.to_csv().encode(), file_name="temporal_focus_results.csv")

     
