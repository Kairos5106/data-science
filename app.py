import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Phishing Site Detector",
    layout="wide"
)

# CSS styling ------------------------------------------------------------------------------------------------------------
st.markdown("""
<style>
            
[data-testid="stMetric"] {
    background-color: #e8e9eb;
    text-align: center;
    padding: 15px 0;
}
            
[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>
""", unsafe_allow_html=True)

# Model integration ------------------------------------------------------------------------------------------------------------
# For debugging - display status on terminal
def predict_website_status(user_input):
    try:
        # Wrap the user input in a list
        website_status = classifier.predict([user_input])
        print(f"Predicted status: {website_status}")
        return website_status
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

# Page title & header
st.title("Phishing Website Detector")
st.markdown("A machine learning application used to identify a malicious website from its link. Input a link to get started!")

# Get user input
user_input = st.text_input("Enter a website link here")
st.markdown(f"Your input is: {user_input}")

# Load phishing detector model
try:
    with open("phishing.pkl", "rb") as pickle_in:
        classifier = pickle.load(pickle_in)
except Exception as e:
    st.error(f"Error loading model: {e}")

# Pass data to model & produce output
result = None
if st.button("Predict"):
    result = predict_website_status(user_input)

# Produce output and show in output section
if result is not None:
    if result[0] == 'good':  # Assuming 'good' means safe
        st.success("This website is safe")
    elif result[0] == 'bad':  # Assuming 'bad' means malicious
        st.warning("This website is malicious!")
else:
    st.error("Unable to predict the status of the website.")

# Dashboard ---------------------------------------------------------------------------------------------------------------
# Load the dataset
phish_data = pd.read_csv('phishing_site_urls.csv')

# Row 1
row1_col = st.columns((8, 4), gap='medium')

with row1_col[0]:
    # Dataset used
    st.write("### Dataset Used")
    st.write("Scroll through the dataset:")
    st.write(phish_data)

with row1_col[1]:
    # URL Counts from Dataset
    st.write("### URL Counts from Dataset")
    st.write("This dataset contains phishing urls (bad) and legitimate urls (good)")
    num_bad_urls = phish_data[phish_data['Label'] == 'bad'].shape[0]
    num_good_urls = phish_data[phish_data['Label'] == 'good'].shape[0]
    
    st.metric(label="Bad URL", value=num_bad_urls, delta=None)
    st.metric(label="Good URL", value=num_good_urls, delta=None)

# Row 2
row2_col = st.columns((8, 4), gap='medium')

with row2_col[0]:
    # TLD information
    st.write("### Top Level Domain Used in Phishing and Legitimate URL")
    bad_sites = phish_data[phish_data['Label'] == 'bad']
    good_sites = phish_data[phish_data['Label'] == 'good']

    top_tlds_phish = bad_sites['URL'].apply(lambda x: x.split('.')[-1])
    top_tlds_good = good_sites['URL'].apply(lambda x: x.split('.')[-1])

    plt.figure(figsize=(10, 6))
    sns.countplot(y=top_tlds_phish, order=top_tlds_phish.value_counts().index[:10], color='red', alpha=1.0, label='Phishing')
    sns.countplot(y=top_tlds_good, order=top_tlds_good.value_counts().index[:10], color='yellow', alpha=1.0, label='Legitimate')

    plt.title('Top 10 TLDs for Phishing and Legitimate URLs')
    plt.xlabel('Frequency')
    plt.ylabel('Top-Level Domain (TLD)')
    plt.legend()
    st.pyplot(plt)

    # Keyword Frequency in Phishing and Legitimate URLs
    st.write("### Keyword Frequency in Phishing and Legitimate URLs")
    def count_keywords(urls, keyword):
        return sum(url.count(keyword) for url in urls)
    
    keywords = ['login', 'bank', 'search', 'secure', 'account']

    keyword_counts_good = {keyword: count_keywords(good_sites['URL'], keyword) for keyword in keywords}
    keyword_counts_bad = {keyword: count_keywords(bad_sites['URL'], keyword) for keyword in keywords}

    plt.figure(figsize=(10, 6))
    plt.bar(keyword_counts_good.keys(), keyword_counts_good.values(), color='yellow', alpha=0.7, label='Good Sites')
    plt.bar(keyword_counts_bad.keys(), keyword_counts_bad.values(), color='red', alpha=0.7, label='Bad Sites')
    plt.title('Keyword Frequency in Good and Bad Sites')
    plt.xlabel('Keyword')
    plt.ylabel('Frequency')
    plt.legend()
    st.pyplot(plt)

with row2_col[1]:
    st.write("### URL Length Statistics")

    # Calculate URL length statistics
    url_length_stats = phish_data.groupby('Label')['URL'].apply(lambda x: x.str.len().describe()).unstack()

    # Separate statistics for good and bad URLs
    url_length_stats_bad = url_length_stats.loc['bad']
    url_length_stats_good = url_length_stats.loc['good']

    # Create DataFrames for good and bad URL length statistics
    df_bad = pd.DataFrame(url_length_stats_bad).reset_index().rename(columns={'index': 'Statistic', 'bad': 'Value'})
    df_good = pd.DataFrame(url_length_stats_good).reset_index().rename(columns={'index': 'Statistic', 'good': 'Value'})
    
    # Display the statistics for bad URLs
    st.write("##### Bad URLs Statistics")
    st.dataframe(df_bad,
                 column_order=("Statistic", "Value"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Statistic": st.column_config.TextColumn("Statistic"),
                    "Value": st.column_config.NumberColumn("Value", format="%f")
                 })
    
    # Display the statistics for good URLs
    st.write("##### Good URLs Statistics")
    st.dataframe(df_good,
                 column_order=("Statistic", "Value"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Statistic": st.column_config.TextColumn("Statistic"),
                    "Value": st.column_config.NumberColumn("Value", format="%f")
                 })