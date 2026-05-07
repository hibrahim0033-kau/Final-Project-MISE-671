import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


@st.cache_data
def load_data():
    df = pd.read_csv("diabetes.csv")
    # Change numbers 0 and 1 to words for easier to read
    df["Result"] = df["Outcome"].map({1: "Diabetic", 0: "Healthy"})
    return df


df = load_data()

# Count patients we have in total
total = len(df)
diabetic = len(df[df["Outcome"] == 1])
healthy = len(df[df["Outcome"] == 0])

# List of all the health measurements we track
features = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
            "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]

#  sidebar
with st.sidebar:
    st.header("Navigation")


    page = st.radio(
        "Go to page:",
        ["Overview", "Distributions", "Relationships", "Correlation"],
        label_visibility="collapsed"
    )

    st.divider()


    with st.expander("Quick info", expanded=True):
        st.metric("Total Patients", total)
        st.metric("Diabetic", f"{diabetic} ({round(diabetic/total*100)}%)")
        st.metric("Healthy", f"{healthy} ({round(healthy/total*100)}%)")
        st.metric("Features", len(features))

    st.divider()


# p1 - Overview of the dataset
if page == "Overview":

    st.subheader("Dataset EDA after cleaning")
    st.write("The Pima Indians Diabetes Dataset - 768 female patients with 8 health measurements.")
    st.divider()

    # Show 4 big numbers in a row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total", total, help="Number of patients")
    with col2:
        st.metric("Diabetic", diabetic, f"{round(diabetic/total*100)}%")
    with col3:
        st.metric("Healthy", healthy, f"{round(healthy/total*100)}%")
    with col4:
        st.metric("Features", len(features), help="Health measurements")

    st.divider()

    # Split the page into two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Outcome Balance")
        # pie chart to show  diabetic vs healthy
        balance = pd.DataFrame({
            "Group": ["Diabetic", "Healthy"],
            "Count": [diabetic, healthy]
        })
        fig = px.pie(
            balance, names="Group", values="Count",
            color="Group",
            color_discrete_map={"Diabetic": "#e74c3c", "Healthy": "#2ecc71"},
            title="Diabetic vs Healthy Patients"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Feature Descriptions")
        # health measurement means
        descriptions = {
            "Pregnancies": "Number of times pregnant",
            "Glucose": "Blood sugar level (mg/dL)",
            "BloodPressure": "Diastolic blood pressure (mm Hg)",
            "SkinThickness": "Triceps skin fold (mm)",
            "Insulin": "2-hour serum insulin (µU/ml)",
            "BMI": "Body mass index",
            "DiabetesPedigreeFunction": "Family history score",
            "Age": "Age in years"
        }
        for feature, desc in descriptions.items():
            st.write(f"**{feature}** - {desc}")

    st.divider()

    # Three tabs
    tab1, tab2, tab3 = st.tabs(["Statistics", "First 10 Rows", "Download Data"])

    with tab1:
        st.subheader("Statistics for All Features")
        # Show min, max, average
        stats = df[features].describe().round(2)
        st.dataframe(stats, use_container_width=True, height=400)

    with tab2:
        st.subheader("First 10 Rows of Data")
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Download Full Dataset")
        # download data function
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="diabetes_data.csv",
            mime="text/csv"
        )
        st.dataframe(df, use_container_width=True)



# p 2 - See how features are distributed
elif page == "Distributions":

    st.subheader("Feature Distributions")
    st.write("Pick any feature to see how it spreads - and compare diabetic vs healthy patients.")
    st.divider()

    # Three controls in a row
    col1, col2, col3 = st.columns(3)
    with col1:
        feature = st.selectbox("Choose Feature:", features)
    with col2:
        chart_type = st.selectbox("Chart Type:", ["Histogram", "Box Plot", "Violin Plot"])
    with col3:
        show_stats = st.checkbox("Show Statistics", value=True)

    st.divider()

    # Calculate averages for each group
    avg_diabetic = round(df[df["Outcome"] == 1][feature].mean(), 2)
    avg_healthy = round(df[df["Outcome"] == 0][feature].mean(), 2)
    avg_all = round(df[feature].mean(), 2)

    # Show three big numbers
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Overall Avg", avg_all)
    with metric_col2:
        st.metric("Diabetic Avg", avg_diabetic, delta=round(avg_diabetic - avg_all, 2))
    with metric_col3:
        st.metric("Healthy Avg", avg_healthy, delta=round(avg_healthy - avg_all, 2))

    st.divider()

    # Create the chart that user picked
    if chart_type == "Histogram":
        # Bar chart showing frequency
        fig = px.histogram(
            df, x=feature, color="Result",
            barmode="overlay",
            color_discrete_map={"Diabetic": "#e74c3c", "Healthy": "#2ecc71"},
            title=f"{feature} Distribution",
            nbins=30
        )
        fig.update_traces(opacity=0.7)

    elif chart_type == "Box Plot":
        # Box plot showing min, max, median
        fig = px.box(
            df, x="Result", y=feature,
            color="Result",
            color_discrete_map={"Diabetic": "#e74c3c", "Healthy": "#2ecc71"},
            title=f"{feature} Box Plot",
            points="outliers"
        )

    else:
        # Violin plot showing distribution shape
        fig = px.violin(
            df, x="Result", y=feature,
            color="Result",
            color_discrete_map={"Diabetic": "#e74c3c", "Healthy": "#2ecc71"},
            title=f"{feature} Violin Plot"
        )

    st.plotly_chart(fig, use_container_width=True)

    # Optionally show detailed statistics
    if show_stats:
        st.divider()
        st.subheader("Statistics by Group")
        stats_table = df.groupby("Result")[[feature]].describe().round(2)
        st.dataframe(stats_table, use_container_width=True)

    st.divider()

    # Collapsible section comparing all features
    with st.expander("Compare All Features", expanded=False):
        st.subheader("Average by Outcome")
        avg_by_outcome = df.groupby("Result")[features].mean().round(1).T
        st.dataframe(avg_by_outcome, use_container_width=True)

# PAGE 3 - See relationships between two features
elif page == "Relationships":

    st.subheader("Feature Relationships")
    st.write("See how two features relate to each other - do diabetic patients group differently?")
    st.divider()

    # pick two features to compare
    col1, col2, col3 = st.columns(3)
    with col1:
        x_axis = st.selectbox("X Axis:", features, index=1, help="Horizontal")
    with col2:
        y_axis = st.selectbox("Y Axis:", features, index=5, help="Vertical")
    with col3:
        transparency = st.slider("Transparency:", 0.0, 1.0, 0.6, 0.1)

    st.divider()

    # Create scatter plot with user's selections
    fig = px.scatter(
        df, x=x_axis, y=y_axis,
        color="Result",
        color_discrete_map={"Diabetic": "#e74c3c", "Healthy": "#2ecc71"},
        title=f"{x_axis} vs {y_axis}",
        opacity=transparency,
        size="Age",
        hover_data={"Glucose": True, "BMI": True}
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # important relationships
    st.subheader("Key Relationships")
    tab1, tab2, tab3, tab4 = st.tabs(["Glucose-BMI", "Age-Glucose", "Insulin-Glucose", "Healthy-Glucose"])

    with tab1:
        # Scatter plot Glucose vs BMI
        fig = px.scatter(df, x="Glucose", y="BMI", color="Result",
                         color_discrete_map={"Diabetic": "#e74c3c", "Healthy": "#2ecc71"},
                         title="Glucose vs BMI", opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # Scatter plot Age vs Glucose
        fig = px.scatter(df, x="Age", y="Glucose", color="Result",
                         color_discrete_map={"Diabetic": "#e74c3c", "Healthy": "#2ecc71"},
                         title="Age vs Glucose", opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        # Scatter plot Insulin vs Glucose
        fig = px.scatter(df, x="Insulin", y="Glucose", color="Result",
                         color_discrete_map={"Diabetic": "#e74c3c", "Healthy": "#2ecc71"},
                         title="Insulin vs Glucose", opacity=0.6)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        fig =px.pie(df, values="Glucose", names="Result",
                    color_discrete_map={"Diabetic": "#e74c3c",})

        st.plotly_chart(fig, use_container_width=True)

# PAGE 4 - See which features matter most
elif page == "Correlation":

    st.subheader("Feature Correlation Analysis")
    st.write("Correlation ranges from -1 (opposite) to 1 (same). Higher means stronger connection.")
    st.divider()

    # Heatmap showing how features relate
    st.subheader("Correlation Matrix Heatmap")
    corr = df[features + ["Outcome"]].corr().round(2)

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
        aspect="auto",
        title="How features relate to each other"
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Bar chart showing which features matter most
    st.subheader("Which Feature Matters Most?")
    corr_with_outcome = df[features].corrwith(df["Outcome"]).abs().sort_values(ascending=False).reset_index()
    corr_with_outcome.columns = ["Feature", "Correlation"]

    fig = px.bar(
        corr_with_outcome,
        x="Feature",
        y="Correlation",
        color="Correlation",
        color_continuous_scale="Reds",
        title="Feature Importance (Correlation with Diabetes)",
        text="Correlation"
    )
    fig.update_traces(textposition='auto')
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Explanation of correlation
    with st.expander("How to Read Correlation", expanded=True):
        st.write("""
        1.0 means: Both increase together perfectly
        0.5 means: Moderate positive relationship
        0.0 means: No relationship at all
        -0.5 means: Moderate negative relationship
        -1.0 means: One increases, other decreases
        
        In this dataset:
        - High Glucose usually means higher chance of diabetes
        - High Age usually means higher chance of diabetes
        - High BMI usually means higher chance of diabetes
        """)

    # Show the most important feature
    st.divider()
    st.subheader("Key Finding")
    top_feature = corr_with_outcome.iloc[0]["Feature"]
    top_value = round(corr_with_outcome.iloc[0]["Correlation"], 3)

    st.success(f"""
    {top_feature} is MOST connected to diabetes (correlation: {top_value})
    
    This means: Patients with higher {top_feature} are much more likely to be diabetic.
    
    Important note: Correlation does not mean cause.
    {top_feature} is linked to diabetes, but high {top_feature} does not necessarily CAUSE diabetes.
    """)

#Footer
st.divider()
st.caption("King Abdulaziz University  . MISE 671 - Big DATA Management", text_alignment="center")