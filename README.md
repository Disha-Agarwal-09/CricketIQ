# 🏏 CricketIQ

CricketIQ is an interactive IPL match prediction and analytics dashboard built using Python, Streamlit, and Machine Learning.

The application predicts the likely winner of an IPL match based on historical match data and also provides useful insights such as head-to-head records, recent team form, venue analysis, and a strategy recommendation.

The idea behind this project was to combine data analysis with machine learning and present the results through a simple, interactive web application.

---

## Features

- Predicts the winner of an IPL match
- Displays prediction confidence
- Team vs Team head-to-head statistics
- Recent form analysis
- Venue intelligence
- Winning probability visualization
- First innings score distribution
- Match strategy recommendation
- Interactive Streamlit dashboard

---

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Plotly
- Joblib

---

## Project Structure

```
CricketIQ/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   ├── model.pkl
│   └── encoders.pkl
│
├── notebooks/
│
└── src/
    └── cricket_utils.py
```

---

## How It Works

The application follows a simple workflow:

1. Load and preprocess historical IPL match data.
2. Encode categorical features such as teams, venues, and toss information.
3. Use the trained machine learning model to predict the match outcome.
4. Display additional insights including:
   - Head-to-head record
   - Recent team performance
   - Venue statistics
   - Winning probability
   - Strategy recommendation

---

## Running the Project

Clone the repository

```bash
git clone <repository-url>
```

Move into the project directory

```bash
cd CricketIQ
```

Install the required packages

```bash
pip install -r requirements.txt
```

Start the Streamlit application

```bash
python -m streamlit run app.py
```

---

## Future Improvements

Some features that can be added in future versions include:

- Player-level performance analysis
- Live match data integration
- More advanced prediction models
- Interactive team comparison dashboard
- Deployment on Streamlit Cloud

---



---

## Author

**Disha Agarwal**

Feel free to connect or share feedback if you have suggestions for improving the project.
