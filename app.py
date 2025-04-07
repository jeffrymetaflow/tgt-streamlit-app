# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

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

# User input section
responses = {}
st.header("Assessment Questions")
st.write("Rate each statement from 1 (Strongly Disagree) to 7 (Strongly Agree)")

for q_id, (question_text, _) in questions.items():
    responses[q_id] = st.slider(question_text, 1, 7, 4)

# Compute results if user has submitted answers
if st.button("Submit & Get Results"):
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

    # Add insight
    if dominant_focus == "Past":
        st.write("You tend to reflect on past experiences. Try channeling those memories into wisdom without getting stuck in regret.")
    elif dominant_focus == "Present":
        st.write("You thrive in the moment. Consider how staying grounded helps you enjoy life and stay resilient.")
    elif dominant_focus == "Future":
        st.write("You’re future-focused. Harness your vision, but don’t forget to enjoy the present journey.")

    # Optional: download or save
    st.download_button("Download My Results", df_scores.to_csv().encode(), file_name="temporal_focus_results.csv")
