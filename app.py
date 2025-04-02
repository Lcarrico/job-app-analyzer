import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.analyzer import analyze_texts_as_json
from utils.scoring import score_resume_from_json, score_cover_letter_from_json

st.set_page_config(page_title="Resume & Cover Letter Analyzer", layout="wide")
st.title("📄 Resume & Cover Letter Analyzer (GPT-4o + Visual Scoring)")

api_key = st.text_input("🔑 OpenAI API Key", type="password")

resume = st.text_area("📄 Paste Resume", height=200)
cover_letter = st.text_area("✉️ Paste Cover Letter", height=200)
job_description = st.text_area("💼 Paste Job Description", height=200)

if st.button("Analyze"):
    if not api_key or not resume or not cover_letter or not job_description:
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Analyzing with GPT-4o..."):
            resume_json, cover_json = analyze_texts_as_json(api_key, resume, cover_letter, job_description)

        if "error" in resume_json:
            st.error(f"Error: {resume_json['error']}")
        else:
            # Resume scoring
            resume_score = score_resume_from_json(resume_json)
            cover_score = score_cover_letter_from_json(cover_json)

            # Prep resume category scores
            resume_scores = {}
            resume_required = resume_json.get("all_items_required", {})
            resume_matched = resume_json.get("skills_match", {})
            categories = list(resume_required.keys())

            for category in categories:
                required = set(resume_required.get(category, []))
                matched = set(resume_matched.get(category, []))
                score = round((len(matched) / len(required)) * 100, 2) if required else 0
                resume_scores[category] = {
                    "required": len(required),
                    "matched": len(matched),
                    "score": score,
                    "missing": list(required - matched)
                }

            # Resume Match Breakdown
            st.header("Resume Match Breakdown")
            st.metric("Overall Resume Score", f"{resume_score} / 100")

            # Match Table
            st.subheader("Category-by-Category Table")
            resume_df = pd.DataFrame([
                {
                    "Category": cat.replace("_", " ").title(),
                    "Required": data["required"],
                    "Matched": data["matched"],
                    "Score (%)": data["score"],
                    "Missing Items": ", ".join(data["missing"]) if data["missing"] else "-"
                }
                for cat, data in resume_scores.items()
            ])
            st.dataframe(resume_df)

            # Charts in a single row
            st.subheader("Visual Analysis")
            col1, col2 = st.columns(2)

            with col1:
                # Match Progress by Category
                for cat, data in resume_scores.items():
                    st.write(f"**{cat.replace('_', ' ').title()}**")
                    st.progress(int(data["score"]))

            with col2:
                radar = go.Figure()
                radar.add_trace(go.Scatterpolar(
                    r=[data["score"] for data in resume_scores.values()],
                    theta=[cat.replace("_", " ").title() for cat in resume_scores.keys()],
                    fill='toself',
                    name='Current Match'
                ))
                radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
                st.plotly_chart(radar, use_container_width=True)

            # Missing Skills
            st.subheader("Skill Match Checklist")
            for cat, data in resume_scores.items():
                if data["missing"]:
                    with st.expander(f"{cat.replace('_', ' ').title()} – Missing Items"):
                        for item in data["missing"]:
                            st.markdown(f"- {item}")

            # Cover Letter Breakdown
            st.header("Cover Letter Rubric Breakdown")
            st.metric("Overall Cover Letter Score", f"{cover_score} / 100")

            rubric_data = cover_json["rubric"]
            rubric_df = pd.DataFrame([
                {
                    "Category": cat.replace("_", " ").title(),
                    "Score": data["score"],
                    "Reason": data["reason"]
                }
                for cat, data in rubric_data.items()
            ])
            st.dataframe(rubric_df)

            # Cover Letter Charts
            st.subheader("Cover Letter Analysis")
            col1, col2 = st.columns(2)

            with col1:
                rubric_chart = pd.DataFrame({
                    "Category": rubric_df["Category"],
                    "Score": rubric_df["Score"]
                })
                st.plotly_chart(px.bar(rubric_chart, x="Category", y="Score", color="Score", color_continuous_scale="Tealgrn", range_y=[0, 20]), use_container_width=True)

            with col2:
                radar = go.Figure()
                radar.add_trace(go.Scatterpolar(
                    r=rubric_df["Score"],
                    theta=rubric_df["Category"],
                    fill='toself',
                    name='Rubric Scores'
                ))
                radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 20])), showlegend=False)
                st.plotly_chart(radar, use_container_width=True)

            # Easy-to-read layout for rubric details
            st.subheader("Detailed Rubric Breakdown")
            for _, row in rubric_df.iterrows():
                st.markdown(f"**{row['Category']}**: {row['Score']} points")
                st.markdown(f"Reason: {row['Reason']}")
                st.markdown("---")

            # Suggestions
            st.subheader("Top 3 Suggestions to Improve")
            all_missing = [
                (cat.replace("_", " ").title(), item)
                for cat, data in resume_scores.items()
                for item in data["missing"]
            ]
            low_rubric = sorted(rubric_data.items(), key=lambda x: x[1]["score"])[:3]

            suggestions = []
            if all_missing:
                suggestions.append(f"Add missing resume item: **{all_missing[0][1]}** in **{all_missing[0][0]}**.")

            for r in low_rubric:
                suggestions.append(f"Improve **{r[0].replace('_', ' ').title()}** in the cover letter — {r[1]['reason']}")

            for s in suggestions[:3]:
                st.markdown(f"- {s}")
