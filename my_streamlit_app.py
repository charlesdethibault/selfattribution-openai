#to run : streamlit run streamlit_app.py

import streamlit as st
import plotly.express as px
import openai
import altair as alt
import pandas as pd
pd.set_option('display.max_colwidth', 500)


st.set_page_config(layout="wide")

#FUNCTIONS
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

# SIDEBAR

st.sidebar.write("______________________________")
# Create a sidebar with a radio button to choose between loading an example or uploading a file
st.sidebar.write("The Example Data contains artificial data")
st.sidebar.write("Make sure the column name of the self attribution free text is 'hdyhau'. You can look at the example file for reference.")
choice = st.sidebar.radio("Choose an option:", ("Load Example Data", "Upload Your Own"))

if choice == "Load Example Data":
    # Load the example CSV file
    df = pd.read_csv("hdyhau.csv")

else:
    # Allow the user to upload their own CSV file
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the uploaded file into a DataFrame
        df = pd.read_csv(uploaded_file)
        #st.write("Uploaded Data:")
        #st.write(df)


csv = convert_df(df)

st.sidebar.download_button(
   "Download Example Data",
   csv,
   "selfattribution.csv",
   "text/csv",
   key='download-csv'
)


#BODY

st.write('*Disclaimer: This app does not retain any user data. All processing is done through Streamlit and OpenAI services.It is the responsibility of the user to ensure that the Streamlit and OpenAI terms of service are acceptable and comply with applicable laws in their jurisdiction. The creators of this app assume no liability or responsibility for individual use.*')
st.write("______________________________")
openai.api_key = str(st.secrets["openai_key"])
st.write(":pray: Support our research and deployment efforts! Click here to Donate :pray:")

# PayPal logo image URL
paypal_logo_url = "https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif"
# PayPal donation link
paypal_donation_link = "https://www.paypal.com/donate/?hosted_button_id=J454HKB6V8QPS"
# Embed the PayPal button with the logo and link
paypal_button_code = f"""
<div style="text-align: center;">
  <a href="{paypal_donation_link}" target="_blank">
    <img src="{paypal_logo_url}" alt="PayPal Logo" style="max-width: 100%;">
  </a>
  <p><a href="{paypal_donation_link}" target="_blank">Donate with PayPal</a></p>
</div>
"""
# Embed the PayPal button
st.markdown(paypal_button_code, unsafe_allow_html=True)


# Title
st.title("Self Attribution Freetext Handler using AI")

st.write("Introducing the 'Self Attribution Freetext Handler using AI' app, a powerful tool designed to transform your data effortlessly. Whether you're working with example data or your very own freetext self-attribution CSV file, our app simplifies the process. With just a few clicks, watch as your data comes to life. The magic begins with a click of the 'Run Code' button, which seamlessly queries the OpenAI API, turning your raw data into a neatly organized CSV file. This file not only preserves your original freetext responses but also adds valuable context, including the channel and source. Say goodbye to tedious data handling and hello to a more streamlined and exciting data analysis experience!")




st.write("first 10 of the list")
st.dataframe(df.head(10))
#create prompt
list_hdyhau = list(df['hdyhau'])
intro_prompt ='we ask the prospects how they heard about us. Below are their responses, can you provide a category for each response in the below list. The categories should be Referral, Social Media, Online research, Podcast, Event, Online ads, blog, newsletters, and others. I also would like to list the name of the source: whom referred, which website, what podcast. The output structure should the "prospect freext - Category name - Source name" '
#st.write(intro_prompt)
#st.write(str(list_hdyhau))
prompt = intro_prompt + str(list_hdyhau)

if st.button('Run Code'):
    # Put your code here that should run when clicked
    st.write("Let's roll!")
    st.write("Connecting to OpenAI")


    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0,
    max_tokens=2484,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)
    r = (response["choices"][0])
    print(r["text"])
    data_lines = r["text"].split('\n')
    data_rows = [line.split(' - ') for line in data_lines]
    df_result = pd.DataFrame(data_rows, columns=['response', 'channel', 'source'])
    df_result = df_result.dropna(how='any',axis=0) 
    csv = convert_df(df_result)

    st.download_button(
      ":rocket: Download The Results :rocket:",
      csv,
      "selfattribution.csv",
      "text/csv",
      key='download-results-csv')

    st.dataframe(df_result)

#df_test = pd.read_csv("selfattribution-2.csv")


    # Get channel counts
    channel_counts = df_result['channel'].value_counts() 
    # Create bar chart
    chart = (alt.Chart(channel_counts.reset_index())
            .mark_bar()
             .encode(x='channel', y='count')
             .properties(title='Channel Counts', width=600)
            )

    st.altair_chart(chart, use_container_width=True)