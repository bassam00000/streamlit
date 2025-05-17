
import streamlit as st
from datetime import datetime, timedelta

st.title("Fair Game Time Cost Calculator")

RATE_PER_HOUR = 85
RATE_PER_MIN = RATE_PER_HOUR / 60

st.markdown("### Enter Player Details")

names = []
starts = []
ends = []

num_players = st.number_input("Number of Players", min_value=1, max_value=20, value=4)

for i in range(num_players):
    name = st.text_input(f"Player {i+1} Name", value=f"Player{i+1}")
    col1, col2 = st.columns(2)
    start = col1.time_input(f"{name} - Start Time", key=f"start_{i}")
    end = col2.time_input(f"{name} - End Time", key=f"end_{i}")
    names.append(name)
    starts.append(start)
    ends.append(end)

def to_datetime(t):
    return datetime.combine(datetime.today(), t)

if st.button("Calculate Cost"):
    players = [{"name": names[i], "start": starts[i], "end": ends[i]} for i in range(num_players)]

    min_time = min(to_datetime(p["start"]) for p in players)
    max_time = max(to_datetime(p["end"]) for p in players)

    timeline = {}
    durations = {}
    current_time = min_time
    while current_time < max_time:
        present = [
            p["name"]
            for p in players
            if to_datetime(p["start"]) <= current_time < to_datetime(p["end"])
        ]
        if present:
            cost_per_person = RATE_PER_MIN / len(present)
            for name in present:
                if name not in timeline:
                    timeline[name] = 0
                    durations[name] = 0
                timeline[name] += cost_per_person
                durations[name] += 1
        current_time += timedelta(minutes=1)

    total_cost = sum(timeline.values())

    st.markdown("### Results:")
    for name in timeline:
        time_minutes = durations[name]
        time_hours = round(time_minutes / 60, 2)
        cost = round(timeline[name], 2)
        st.write(f"**{name}**: Played for {time_hours} hours, Cost: {cost} EGP")

    st.success(f"Total Group Cost: {round(total_cost, 2)} EGP")
