import streamlit as st
import pandas as pd
import altair as alt
from collections import namedtuple
import math

import os
import asyncio

from SessionState import get
from httpx_oauth.clients.google import GoogleOAuth2

from config import *

async def write_authorization_url(client,
                                  redirect_uri):
    authorization_url = await client.get_authorization_url(
        redirect_uri,
        scope=["profile", "email"],
        extras_params={"access_type": "offline"},
    )
    return authorization_url


async def write_access_token(client,
                             redirect_uri,
                             code):
    token = await client.get_access_token(code, redirect_uri)
    return token


async def get_email(client,
                    token):
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email


def main(user_id, user_email):
    st.write(f"You're logged in as {user_email}")

    if user_email.split('@')[1] == domain:
        st.success('Login Successful')
        st.title('Secret Algorithm 🤫 ')

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

            # Aarons refactor
            Point = namedtuple('Point', 'x y')
            data = [None] * total_points
            points_per_turn = total_points / num_turns
            baseAngle = 2 * math.pi / points_per_turn
            baseRadius = 1 / total_points
            for curr_point_num in range(total_points):
                angle = curr_point_num * baseAngle
                radius = curr_point_num * baseRadius
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                data[curr_point_num] = Point(x, y)
            st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
                .mark_circle(color='#0068c9', opacity=0.5)
                .encode(x='x:Q', y='y:Q'))

    else:
        st.error('Login Rejected')
        st.text(f'No secrets for you, {user_email}.')


if __name__ == '__main__':
    # client_id = os.environ['GOOGLE_CLIENT_ID']
    # client_secret = os.environ['GOOGLE_CLIENT_SECRET']
    # redirect_uri = os.environ['GOOGLE_REDIRECT_URI']

    client = GoogleOAuth2(client_id, client_secret)
    authorization_url = asyncio.run(
        write_authorization_url(client=client,
                                redirect_uri=redirect_uri)
    )

    session_state = get(token=None)
    if session_state.token is None:
        try:
            code = st.experimental_get_query_params()['code']
        except:
            st.write(f'''<h2>
                Authorised Accounts Only: <a target="_self"
                href="{authorization_url}">Google Oauth Login</a></h2>''',
                     unsafe_allow_html=True)
        else:
            # Verify token is correct:
            try:
                token = asyncio.run(
                    write_access_token(client=client,
                                       redirect_uri=redirect_uri,
                                       code=code))
            except:
                st.write(f'''<h2>
                    This account is not allowed or page was refreshed.
                    Please try again: <a target="_self"
                    href="{authorization_url}">Google Oauth Login</a></h2>''',
                         unsafe_allow_html=True)
            else:
                # Check if token has expired:
                if token.is_expired():
                    if token.is_expired():
                        st.write(f'''<h2>
                        Login session has ended,
                        please <a target="_self" href="{authorization_url}">
                        login</a> again.</h2>
                        ''')
                else:
                    session_state.token = token
                    user_id, user_email = asyncio.run(
                        get_email(client=client,
                                  token=token['access_token'])
                    )
                    session_state.user_id = user_id
                    session_state.user_email = user_email
                    main(user_id=session_state.user_id,
                         user_email=session_state.user_email)
    else:
        main(user_id=session_state.user_id,
             user_email=session_state.user_email)