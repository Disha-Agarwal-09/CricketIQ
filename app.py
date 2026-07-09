import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go

from src.cricket_utils import (
    get_head_to_head,
    get_recent_form,
    get_venue_stats,
    strategy
)

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="🏏 CricketIQ",
    page_icon="🏏",
    layout="wide"
)

# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("models/model.pkl")
encoders = joblib.load("models/encoders.pkl")

# -----------------------------
# Load Dataset
# -----------------------------
match_summary = pd.read_csv(
    "data/processed/match_summary.csv"
)

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("🏏 CricketIQ")
st.markdown("### IPL Match Strategy Advisor")

st.divider()
# ==========================================
# Sidebar
# ==========================================

st.sidebar.title("🏏 Match Details")

# ---------- Teams ----------
teams = sorted(
    list(
        set(match_summary["team1"]).union(
            set(match_summary["team2"])
        )
    )
)

team1 = st.sidebar.selectbox(
    "Select Team 1",
    teams
)

team2_options = [team for team in teams if team != team1]

team2 = st.sidebar.selectbox(
    "Select Team 2",
    team2_options
)

# ---------- Venues ----------
venues = sorted(match_summary["venue"].dropna().unique())

venue = st.sidebar.selectbox(
    "Select Venue",
    venues
)

# ---------- Toss ----------
toss_winner = st.sidebar.selectbox(
    "Toss Winner",
    [team1, team2]
)

toss_decision = st.sidebar.radio(
    "Toss Decision",
    ["bat", "field"],
    horizontal=True
)

predict = st.sidebar.button(
    "🚀 Predict Match",
    use_container_width=True
)
# ==========================================
# Prediction
# ==========================================

if predict:

    # Create input dataframe
    input_df = pd.DataFrame({
        "team1": [team1],
        "team2": [team2],
        "venue": [venue],
        "toss_winner": [toss_winner],
        "toss_decision": [toss_decision]
    })

    # Encode categorical features
    for col in input_df.columns:
        input_df[col] = encoders[col].transform(input_df[col])

    # Predict
    prediction = model.predict(input_df)[0]

    # Predict probabilities
    probability = model.predict_proba(input_df)[0]

    # Since target = team1_win
    team1_prob = probability[1] * 100
    team2_prob = probability[0] * 100

    confidence = max(team1_prob, team2_prob)

    predicted_winner = team1 if prediction == 1 else team2

    # ==========================================
    # Winner Card
    # ==========================================

    st.divider()

    st.subheader("🏆 Match Prediction")

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"### 🏆 {predicted_winner}")

    with col2:
        st.metric(
            label="Prediction Confidence",
            value=f"{confidence:.2f}%"
        )

    # ==========================================
    # Match Details
    # ==========================================

    st.write("### Match Details")

    detail1, detail2, detail3 = st.columns(3)

    with detail1:
        st.info(f"**Match**\n\n{team1} vs {team2}")

    with detail2:
        st.info(f"**Venue**\n\n{venue}")

    with detail3:
        st.info(f"**Toss**\n\n{toss_winner} ({toss_decision})")

    st.divider()

    # ==========================================
    # Winning Probability
    # ==========================================

    st.subheader("🎯 Winning Probability")

    prob_df = pd.DataFrame({
        "Team": [team1, team2],
        "Probability": [team1_prob, team2_prob]
    })

    fig = px.bar(
        prob_df,
        x="Team",
        y="Probability",
        text="Probability",
        color="Team"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        showlegend=False,
        height=450,
        yaxis_title="Winning Probability (%)",
        xaxis_title="",
        yaxis=dict(range=[0, 100])
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
        # ==========================================
    # Analytics Dashboard
    # ==========================================

    st.divider()

    st.header("📊 Match Analytics")

    # -------------------------------
    # Get Analytics
    # -------------------------------

    total_matches, team1_h2h, team2_h2h = get_head_to_head(team1, team2)

    team1_form = get_recent_form(team1)

    team2_form = get_recent_form(team2)

    venue_stats = get_venue_stats(venue)

    # -------------------------------
    # Head to Head + Recent Form
    # -------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🤝 Head-to-Head")

        h2h_df = pd.DataFrame({
            "Team":[team1, team2],
            "Wins":[team1_h2h, team2_h2h]
        })

        fig = px.bar(
            h2h_df,
            x="Team",
            y="Wins",
            color="Team",
            text="Wins"
        )

        fig.update_layout(
            showlegend=False,
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("📈 Recent Form (Last 5 Matches)")

        form_df = pd.DataFrame({
            "Team":[team1, team2],
            "Wins":[team1_form, team2_form]
        })

        fig = px.bar(
            form_df,
            x="Team",
            y="Wins",
            color="Team",
            text="Wins"
        )

        fig.update_layout(
            showlegend=False,
            height=400,
            yaxis=dict(range=[0,5])
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # -------------------------------
    # Venue Intelligence
    # -------------------------------

    st.header("🏟 Venue Intelligence")

    m1,m2,m3 = st.columns(3)

    with m1:

        st.metric(
            "Average 1st Innings Score",
            f"{venue_stats['avg_first']:.1f}"
        )

    with m2:

        st.metric(
            "Bat First Wins",
            f"{venue_stats['bat_first']:.1f}%"
        )

    with m3:

        st.metric(
            "Chasing Wins",
            f"{venue_stats['chasing']:.1f}%"
        )

    # -------------------------------
    # Venue Pie Chart
    # -------------------------------

    pie_df = pd.DataFrame({
        "Result":[
            "Bat First Won",
            "Chasing Won"
        ],
        "Percentage":[
            venue_stats["bat_first"],
            venue_stats["chasing"]
        ]
    })

    fig = px.pie(
        pie_df,
        names="Result",
        values="Percentage",
        hole=0.45
    )

    fig.update_layout(
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # -------------------------------
    # Score Distribution
    # -------------------------------

    st.subheader("📉 First Innings Score Distribution")

    venue_data = match_summary[
        match_summary["venue"] == venue
    ]

    fig = px.histogram(
        venue_data,
        x="first_innings_score",
        nbins=20
    )

    fig.update_layout(
        xaxis_title="First Innings Score",
        yaxis_title="Matches",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
        # ==========================================
    # Strategy Recommendation
    # ==========================================

    st.divider()

    st.header("💡 Match Strategy Advisor")

    analysis = strategy(team1, team2, venue)

    left, right = st.columns([2, 1])

    with left:

        st.success(
            f"### 🏏 Recommended Strategy: {analysis['recommendation']}"
        )

        st.markdown("### Key Insights")

        st.markdown(
            f"""
**🤝 Head-to-Head**

- {team1}: **{analysis['team1_h2h']} wins**
- {team2}: **{analysis['team2_h2h']} wins**

**📈 Recent Form**

- {team1}: **{analysis['team1_form']}/5 wins**
- {team2}: **{analysis['team2_form']}/5 wins**

**🏟 Venue**

- Average First Innings Score: **{analysis['avg_score']:.1f}**
- Bat First Win %: **{analysis['bat_first']:.1f}%**
- Chasing Win %: **{analysis['chasing']:.1f}%**
"""
        )

    with right:

        st.metric(
            "Average Score",
            f"{analysis['avg_score']:.1f}"
        )

        st.metric(
            "Bat First %",
            f"{analysis['bat_first']:.1f}%"
        )

        st.metric(
            "Chasing %",
            f"{analysis['chasing']:.1f}%"
        )

    st.divider()

    st.header("🏆 Final Verdict")

    st.success(
        f"""
 ### Predicted Winner

 # 🏏 {predicted_winner}

 Prediction Confidence: **{confidence:.2f}%**
 """
    )

 # ===================================================
 # Footer (THIS IS OUTSIDE if predict)
 # ===================================================

    st.divider()

    st.markdown(
    """
 <div style="text-align:center">

 ### 🏏 CricketIQ

 IPL Match Prediction & Strategy Dashboard

 Developed using **Python • Streamlit • Scikit-Learn • Plotly**

 Made by **Disha Agarwal**

 </div>
 """,
    unsafe_allow_html=True,
 )