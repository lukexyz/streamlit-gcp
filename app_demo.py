from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

import os
import asyncio

from session_state import get
from httpx_oauth.clients.google import GoogleOAuth2

# Oauth credentials
client_id = os.environ['GOOGLE_CLIENT_ID']
client_secret = os.environ['GOOGLE_CLIENT_SECRET']
redirect_uri = os.environ['GOOGLE_REDIRECT_URI']

client = GoogleOAuth2(client_id, client_secret)







# ====================== Placeholder App ====================== #

st.title('Counter Example')


# check if `count` has already been initialized in st.session_state.
if 'count' not in st.session_state:
	st.session_state.count = 0

# Create a button which will increment the counter
increment = st.button('Increment')
if increment:
    st.session_state.count += 1

# A button to decrement the counter
decrement = st.button('Decrement')
if decrement:
    st.session_state.count -= 1

st.write('Count = ', st.session_state.count)


# Altair showcase

with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
