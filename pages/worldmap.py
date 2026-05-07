
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("diabetes_worldwide.csv")

# Rename columns to simpler names: Country and Cases
df.columns = ["Country", "Cases"]

# Remove any rows that have empty data
df = df.dropna()


with st.sidebar:
    st.header("Diabetes Worldwide")


    page = st.radio(
        "Go to:",
        ["Overview", "World Map", "Rankings", "Dashboard"]
    )


# p 1 - Overview
if page == "Overview":

    st.subheader("Global Diabetes Overview")
    st.write("Data from the IDF Diabetes Atlas 2024")
    st.info("""
    The **IDF Diabetes Atlas** is the authoritative source on the global impact of diabetes.

    **Published by:** International Diabetes Federation (IDF)

    **First published:** 2000 (1st edition)

    **Current edition:** 11th Edition (2024/2025)

    **Purpose:** Provides global, regional, and national data on:
    - Diabetes prevalence
    - Diabetes-related mortality
    - Health expenditure
    - Future projections
    
    Information about adults aged 20 to 79
    """)
    st.divider()

    # Global numbers
    st.subheader("Global Numbers")
    col1, col2, col3, col4 = st.columns(4)

    # Show global numbers
    col1.metric("Adults with Diabetes", "589 Million", "1 in 9 adults")
    col2.metric("Predicted by 2050", "853 Million", "+45% increase")
    col3.metric("Deaths per Year", "3.4 Million", "1 every 9 seconds")
    col4.metric("Healthcare Cost 2024", "1.015 Trillion", "+338% in 17 years")

    st.divider()

    # Hidden and at-risk cases
    st.subheader("Hidden and At-Risk Cases")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Undiagnosed Cases", "252 Million", "43% unaware")
    col2.metric("People at High Risk", "1.1 Billion", "Could develop diabetes")
    col3.metric("Pregnancies Affected", "1 in 5", "Hyperglycemia cases")
    col4.metric("Urban vs Rural Rate", "12% vs 8%", "Cities are riskier")

    st.divider()

    # Show statistics about the dataset
    st.subheader("About This Dataset")
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Countries", len(df))
    col2.metric("Total Cases", str(round(df["Cases"].sum())) + "M")
    col3.metric("Average", str(round(df["Cases"].mean(), 1)) + "M")
    col4.metric("Highest", str(round(df["Cases"].max(), 1)) + "M")
    col5.metric("Lowest", str(round(df["Cases"].min(), 2)) + "M")

    st.divider()

    # Histogram
    st.subheader("How Are Cases Spread Across Countries?")

    # Most countries have fewer cases, a few have very many
    fig = px.histogram(
        df,
        x="Cases",
        nbins=25,
        title="Most countries have under 10 million cases. A few have much more.",
        labels={"Cases": "Diabetes Cases (Millions)"}
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()


    st.subheader("Who Is Most Affected?")

    # Split screen
    col1, col2 = st.columns(2)

    # Left column
    with col1:
        st.write("By Income Level")
        st.write("81% of people with diabetes live in low or middle-income countries")
        st.write("90% of undiagnosed cases are in poorer nations")
        st.write("Middle-income countries will see a 21% rise by 2050")

    # Right column
    with col2:
        st.write("IDF World Regions Covered")
        st.write("Africa")
        st.write("Europe")
        st.write("Middle East and North Africa")
        st.write("North America and Caribbean")
        st.write("South and Central America")
        st.write("South-East Asia")
        st.write("Western Pacific")

# p 2 - World Map
elif page == "World Map":

    st.subheader("World Map - Diabetes Cases by Country")
    st.write("Hover over any country to see the number of cases")
    st.write("Darker color means more diabetes cases")
    st.divider()

    # color to use for the map
    color = st.radio(
        "Pick a color style:",
        ["Reds", "Blues", "Viridis", "Plasma"],
        horizontal=True
    )


    # world map
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Cases",
        hover_name="Country",
        color_continuous_scale=color,
        title="Diabetes Cases by Country (2024)",
        labels={"Cases": "Cases (Millions)"}
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)


    # Show top 10 and bottom 10
    col1, col2 = st.columns(2)

    # Left column - top 10 countries
    with col1:
        st.subheader("Top 10 Countries with Most Cases")

        # Sort by Cases and get top 10
        top10 = df.sort_values("Cases", ascending=False).head(10)

        # Rename the column
        top10 = top10.rename(columns={"Cases": "Cases (Millions)"})

        # Show as table
        st.dataframe(top10, use_container_width=True, hide_index=True)

    # Right column - bottom 10 countries
    with col2:
        st.subheader("Countries with Lowest Cases")

        # Sort by Cases and get bottom 10
        bottom10 = df.sort_values("Cases", ascending=True).head(10)

        # Rename the column
        bottom10 = bottom10.rename(columns={"Cases": "Cases (Millions)"})
        # Show as table
        st.dataframe(bottom10, use_container_width=True, hide_index=True)

# p 3 - Rankings
elif page == "Rankings":

    st.subheader("Country Rankings by Diabetes Cases")
    st.write("All countries ranked from highest to lowest")
    st.write("Use the slider to control how many countries to show")
    st.divider()

    # Slider
    how_many = st.slider(
        "How many countries to show?",
        min_value=5,
        max_value=len(df),
        value=50
    )

    # Get the top countries (sorted by Cases, highest first)
    top_countries = df.sort_values("Cases", ascending=False).head(how_many)

    # Create horizontal bar chart
    fig = px.bar(
        top_countries,
        x="Cases",
        y="Country",
        orientation="h",
        color="Cases",
        color_continuous_scale="Reds",
        title="Countries Ranked by Diabetes Cases (2024)",
        labels={"Cases": "Cases (Millions)", "Country": ""}
    )

    # Make the chart height change based on how many countries user picked
    fig.update_layout(height=how_many * 25 + 100, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Show highest, lowest, and gap
    st.subheader("Summary")

    # Get the country with highest cases
    highest_country = df.sort_values("Cases", ascending=False).iloc[0]

    # Get the country with lowest cases
    lowest_country = df.sort_values("Cases", ascending=True).iloc[0]

    # Show three metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Highest Burden",
        highest_country["Country"],
        str(round(highest_country["Cases"], 1)) + "M cases"
    )

    col2.metric(
        "Lowest Burden",
        lowest_country["Country"],
        str(round(lowest_country["Cases"], 2)) + "M cases"
    )

    col3.metric(
        "Gap Between Them",
        str(round(highest_country["Cases"] - lowest_country["Cases"], 1)) + "M",
        "difference in cases"
    )

# p 4 - Dashboard
else:

    st.title("Dashboard - Complete View")
    st.write("A complete picture of diabetes around the world")
    st.divider()

    # Show 4 key numbers at top
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Countries", len(df))
    col2.metric("Total Cases", str(round(df["Cases"].sum())) + "M")
    col3.metric("Average", str(round(df["Cases"].mean(), 1)) + "M")
    col4.metric("Median", str(round(df["Cases"].median(), 1)) + "M")

    st.divider()

    # Map on left, top 15 table on right
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("World Map")

        # world map
        fig = px.choropleth(
            df,
            locations="Country",
            locationmode="country names",
            color="Cases",
            hover_name="Country",
            color_continuous_scale="Reds",
            labels={"Cases": "Cases (M)"}
        )

        fig.update_layout(height=450)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top 15 Countries")

        #top 15 countries
        top15 = df.sort_values("Cases", ascending=False).head(15)

        # Rename column
        top15 = top15.rename(columns={"Cases": "Cases (M)"})

        # Show table with height same as map
        st.dataframe(top15, use_container_width=True, hide_index=True, height=450)

    st.divider()

    # Two distribution charts side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribution - Box Plot")

        # Box plot shows min, max, median, quartiles
        fig = px.box(
            df,
            y="Cases",
            labels={"Cases": "Cases (Millions)"}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Distribution - Histogram")

        # Histogramfor  frequency distribution
        fig = px.histogram(
            df,
            x="Cases",
            nbins=20,
            labels={"Cases": "Cases (Millions)"}
        )
        st.plotly_chart(fig, use_container_width=True)




#Footer
st.divider()
st.caption("King Abdulaziz University  . MISE 671 - Big DATA Management", text_alignment="center")