import streamlit as st
import pandas as pd
import numpy as np

# Load the data
@st.cache_data
def load_data():
    data = pd.read_csv('data.csv')
    return data

df = load_data()

st.title("College Finder App")

st.write("Use the filters below to find the best college for you!")

# Sidebar filters
st.sidebar.header("Filters")

# Acceptance rate slider
accept_rate = st.sidebar.slider("Acceptance Rate (%)", 0, 100, (0, 100))
df = df[(df['accept'] / df['apps'] * 100 >= accept_rate[0]) & (df['accept'] / df['apps'] * 100 <= accept_rate[1])]

# Out-of-state tuition slider
tuition = st.sidebar.slider("Max Out-of-State Tuition ($)", 0, 25000, 25000)
df = df[df['outstate'] <= tuition]

# Top 10% students slider
top10 = st.sidebar.slider("Minimum % of Students from Top 10% of High School Class", 0, 100, 0)
df = df[df['top10perc'] >= top10]

# Student-faculty ratio slider
sf_ratio = st.sidebar.slider("Maximum Student-Faculty Ratio", 0.0, 30.0, 30.0)
df = df[df['s_f_ratio'] <= sf_ratio]

# Graduation rate slider
grad_rate = st.sidebar.slider("Minimum Graduation Rate (%)", 0, 100, 0)
df = df[df['grad_rate'] >= grad_rate]

# Checkbox for private/public
private = st.sidebar.checkbox("Private Colleges Only")
if private:
    df = df[df['private'] == 'Yes']

# Display results
st.subheader(f"Matching Colleges: {len(df)}")

if len(df) > 0:
    # Sort by a combination of factors (you can adjust these weights)
    df['score'] = (
        df['accept'] / df['apps'] * 0.2 +
        (25000 - df['outstate']) / 25000 * 0.2 +
        df['top10perc'] / 100 * 0.2 +
        (30 - df['s_f_ratio']) / 30 * 0.2 +
        df['grad_rate'] / 100 * 0.2
    )
    
    df_sorted = df.sort_values('score', ascending=False)
    
    for i, row in df_sorted.iterrows():
        st.write(f"**{i}**")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Acceptance Rate: {row['accept'] / row['apps'] * 100:.1f}%")
            st.write(f"Out-of-State Tuition: ${row['outstate']:,}")
            st.write(f"Top 10% Students: {row['top10perc']}%")
        with col2:
            st.write(f"Student-Faculty Ratio: {row['s_f_ratio']:.1f}")
            st.write(f"Graduation Rate: {row['grad_rate']}%")
            st.write(f"Private: {row['private']}")
        st.write("---")
else:
    st.write("No colleges match your criteria. Try adjusting the filters.")