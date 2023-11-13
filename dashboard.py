import streamlit as st
import os
import pandas as pd
import yaml
from streamlit_authenticator import Authenticate
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="Search Trends",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:tjishnudas@gmail.com'
    }
)
st.markdown('<div style="text-align: center;font-size:30px;">PG Buddy Trends</div>', unsafe_allow_html=True)
st.markdown("""---""")
st.markdown('')
st.markdown('')

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    top_level = os.listdir('data/')
    with st.form(key='my_form'):
        country = st.sidebar.selectbox("Country", top_level)
        search_terms = (os.listdir(f'data/{country}/'))
    option = st.selectbox(
        "Search Term",
        search_terms,
        index=None,
        placeholder="Search Term", label_visibility='hidden'
    )
    st.markdown('#')
    st.markdown('#')
    st.markdown('#')
    if option is not None:
        data = pd.read_csv(f'data/{country}/{option}/multiTimeline.csv')
        col1, col2, col3 = st.columns(3)
        col1.metric("Interest Over Time Acquired Percentage",
                    f"{round(data[f'{option}'].describe().mean(), 2)}%")
        col2.metric("Period", f"{data['Week'][0]} to {data['Week'][len(data) - 1]}")
        col3.metric("Rate", f"{round(data[f'{option}'].describe().mean(), 2)}%",
                    f"{round(data[f'{option}'].describe().mean(), 2)}%")
        charts_names = os.listdir(f'data/{country}/{option}/')
        st.markdown('#')
        st.markdown('#')
        data = pd.read_csv(f'data/{country}/{option}/multiTimeline.csv')
        st.subheader('Interest Over Time', divider='blue')
        radio_markdown = '''
        Numbers represent search interest relative to the highest point on the chart for the given region and time. A value of 100 is the peak popularity for the term. A value of 50 means that the term is half as popular. A score of 0 means that there was not enough data for this term.
        '''.strip()
        st.radio("How to read the graph", [""], help=radio_markdown, disabled=True, horizontal=True)
        st.line_chart(data=data, x='Week', y=f'{option}', color=None, width=0, height=0,
                      use_container_width=True)
        st.markdown('#')
        st.markdown('#')
        data = pd.read_csv(f'data/{country}/{option}/geoMap.csv')
        st.subheader('Interest by sub-region', divider='blue')
        radio_markdown = '''
        See in which location your term was most popular during the specified time frame. Values are calculated on a scale from 0 to 100, where 100 is the location with the most popularity as a fraction of total searches in that location, a value of 50 indicates a location which is half as popular. A value of 0 indicates a location where there was not enough data for this term.
        '''.strip()
        st.radio("How to read the graph", [""], help=radio_markdown, disabled=True, horizontal=True)
        st.bar_chart(data=data, x='Region', y=f'{option}', color=None, width=0, height=0,
                     use_container_width=True)
        st.markdown('#')
        st.markdown('#')
        col11, col12, col13 = st.columns(3)
        with col11:
            st.subheader('Related queries 🙋', divider='blue')
            if 'relatedQueries.csv' in charts_names:
                data = pd.read_csv(f'data/{country}/{option}/relatedQueries.csv')
                radio_markdown = '''
                Users searching for your term also searched for these queries.
                '''.strip()
                st.radio("How to read the Table", [""], help=radio_markdown, disabled=True, horizontal=True)
                st.data_editor(
                    data,
                    column_config={
                        "Count": st.column_config.ProgressColumn(
                            "Query Count",
                            help="The Query Count",
                            min_value=0,
                            max_value=100,
                        ),
                    },
                    hide_index=True,
                )
            else:
                st.warning('Data Not Available')
                st.markdown('#')
        with col12:
            st.subheader('Related Topics Top 🔝', divider='blue')
            if 'relatedEntitiesTop.csv' in charts_names:
                data = pd.read_csv(f'data/{country}/{option}/relatedEntitiesTop.csv')
                radio_markdown = '''
        Users searching for your term also searched for these topics. You can view by the following metrics:
        * Top – The most popular topics. Scoring is on a relative scale where a value of 100 is the most commonly searched topic and a value of 50 is a topic searched half as often as the most popular term, and so on.
        
        * Rising – Related topics with the biggest increase in search frequency since the last time period. Results marked 'Breakout' had a tremendous increase, probably because these topics are new and had few (if any) prior searches.        '''.strip()
                st.radio("How to read the Table", [""], help=radio_markdown, disabled=True, horizontal=True)
                st.data_editor(
                    data,
                    column_config={
                        "Count": st.column_config.ProgressColumn(
                            "Query Count",
                            help="The Query Count",
                            min_value=0,
                            max_value=100,
                        ),
                    },
                    hide_index=True,
                )
            else:
                st.warning('Data Not Available')
                st.markdown('#')
        with col13:
            st.subheader('Related Topics Rising 🚀', divider='blue')
            if 'relatedEntitiesRising.csv' in charts_names:
                data = pd.read_csv(f'data/{country}/{option}/relatedEntitiesRising.csv')
                radio_markdown = '''
        Users searching for your term also searched for these topics. You can view by the following metrics:
        * Top – The most popular topics. Scoring is on a relative scale where a value of 100 is the most commonly searched topic and a value of 50 is a topic searched half as often as the most popular term, and so on.
    
        * Rising – Related topics with the biggest increase in search frequency since the last time period. Results marked 'Breakout' had a tremendous increase, probably because these topics are new and had few (if any) prior searches.        '''.strip()
                st.radio("How to read the Table", [""], help=radio_markdown, disabled=True, horizontal=True)
                st.data_editor(
                    data,
                    column_config={
                        "Percentage": st.column_config.ProgressColumn(
                            "Query Count",
                            help="The Query Count",
                            min_value=0,
                            max_value=100,
                        ),
                    },
                    hide_index=True,
                )
            else:
                st.warning('Data Not Available')
                st.markdown('#')

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
