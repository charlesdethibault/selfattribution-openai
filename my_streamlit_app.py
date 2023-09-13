#to run : streamlit run streamlit_app.py

import streamlit as st
import plotly.express as px

# Add a donation button using HTML and Markdown
donation_button_html = '''
<a href="https://www.example.com/donate" target="_blank">
  <button style="background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;">Donate</button>
</a>
'''

st.markdown(donation_button_html, unsafe_allow_html=True)


# Title
st.title("My First Streamlit App")

# Input box
user_input = st.text_input("Enter something:")
st.write(f'You entered: {user_input}')

# Sample Bar Chart
data = {
    'x': [1, 2, 3],
    'y1': [4, 1, 2],
    'y2': [2, 4, 3]
}

fig = px.bar(data, x='x', y=['y1', 'y2'], labels={'y1': 'A', 'y2': 'B'}, title='Sample Bar Chart')
st.plotly_chart(fig)


