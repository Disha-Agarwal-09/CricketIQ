import pandas as pd

match_summary = pd.read_csv("data/processed/match_summary.csv")

match_summary["date"] = pd.to_datetime(match_summary["date"])
def get_head_to_head(team1, team2):

    matches = match_summary[
        (
            (match_summary["team1"] == team1) &
            (match_summary["team2"] == team2)
        ) |
        (
            (match_summary["team1"] == team2) &
            (match_summary["team2"] == team1)
        )
    ]

    total = len(matches)

    team1_wins = (matches["match_won_by"] == team1).sum()

    team2_wins = (matches["match_won_by"] == team2).sum()

    return total, team1_wins, team2_wins
def get_venue_stats(venue):

    venue_matches = match_summary[
        match_summary["venue"] == venue
    ]

    return {
        "avg_first":
            venue_matches["first_innings_score"].mean(),

        "bat_first":
            venue_matches["bat_first_won"].mean()*100,

        "chasing":
            venue_matches["chasing_team_won"].mean()*100
    }
def get_recent_form(team):

    recent = match_summary[
        (match_summary["team1"] == team) |
        (match_summary["team2"] == team)
    ].sort_values(
        by="date",
        ascending=False
    ).head(5)

    wins = (recent["match_won_by"] == team).sum()

    return wins
def strategy(team1, team2, venue):

    total, t1, t2 = get_head_to_head(team1, team2)

    venue_stats = get_venue_stats(venue)

    form1 = get_recent_form(team1)

    form2 = get_recent_form(team2)

    if venue_stats["bat_first"] > venue_stats["chasing"]:
        recommendation = "BAT FIRST"
    else:
        recommendation = "CHASE"

    return {
        "team1_h2h": t1,
        "team2_h2h": t2,
        "team1_form": form1,
        "team2_form": form2,
        "avg_score": venue_stats["avg_first"],
        "bat_first": venue_stats["bat_first"],
        "chasing": venue_stats["chasing"],
        "recommendation": recommendation
    }