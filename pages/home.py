import streamlit as st
import pandas as pd


df = pd.read_csv('diabetes.csv')

st.badge("Student Group Information", color="green")

students = {
    "Student Name":["Hamid Ibrahim", "Faisal Alshehri", "Saeed Alhothali"],
    "Student ID": ["2602998","2602981", "2603000"]
}
st.dataframe(students, use_container_width=True, hide_index=True)
st.divider()

st.subheader("Diabetes Dataset understanding", text_alignment='center')

feature_data = {
    "Feature": ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"],
    "Type": ["Input", "Input", "Input", "Input", "Input", "Input", "Input", "Input", "Target"],
    "Description": [
        "Number of times pregnant",
        "Plasma glucose concentration (2-hour oral glucose tolerance test)",
        "Diastolic blood pressure (mm Hg)",
        "Triceps skin fold thickness (mm)",
        "2-Hour serum insulin (mu U/ml)",
        "Body mass index (weight in kg / height in m²)",
        "Diabetes pedigree function (genetic risk score)",
        "Age of the patient (years)",
        "Class variable — 0: Non-diabetic, 1: Diabetic"
    ]
}
st.dataframe(feature_data, use_container_width=True, hide_index=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Records", "768", "All females")
with col2:
    st.metric("Features", "8", "Diagnostic measurements")
with col3:
    st.metric("Target Variable", "Outcome", "0 = No, 1 = Yes")
with col4:
    st.metric("Population", "Pima Indian", "21+ years old")



with st.expander("Dataset Information"):
    st.info("""
About This Dataset
The **Pima Indians Diabetes Dataset** was collected by the National Institute of Diabetes and Digestive and Kidney Diseases.
It contains diagnostic health measurements for **768 female patients** of Pima Indian heritage, all aged **21 years or older**.
The goal is to predict whether a patient has diabetes based on 8 medical features.

500 patients are non-diabetic (65%) and 268 are diabetic (35%)
""")
    st.info("""

This dataset is originally from the (National Institute of Diabetes and Digestive and Kidney Diseases). 
The objective is to predict based on diagnostic measurements whether a patient has diabetes.

Sources:
(a) Original owners: National Institute of Diabetes and Digestive and
Kidney Diseases
(b) Donor of database: Vincent Sigillito (vgs@aplcen.apl.jhu.edu)
Research Center, RMI Group Leader
Applied Physics Laboratory
The Johns Hopkins University
Johns Hopkins Road
Laurel, MD 20707
(301) 953-6231
(c) Date received: 9 May 1990

https://www.kaggle.com/datasets/mathchi/diabetes-data-set/data
""")

with st.expander("Diabetes Dataset understanding"):
    st.write("Display first rows to confirm loading, Show first 5 rows ", df.head(5))
    st.write("Show last 5 rows ", df.tail(5))
    st.divider()
    st.badge("Show dimensions", color="green")
    st.write("0 is the number of raws   --  ", df.shape[0] ," 1 = number of columns", df.shape[1])
    st.divider()
    st.write (" see all categories", df.nunique())
    st.divider()
    st.subheader("displays a statistical summary ")
    st.write(df.describe())
    st.subheader("value counts")
    st.write(df.value_counts())
    st.divider()
    st.badge("Value counts how many diabetics. 0 Non-diabetic and 1 diabetic ", color="green")

    st.write(df['Outcome'].value_counts())
    st.divider()
    st.badge("counts youngest and oldest Age ", color="green")
    st.write("youngest women in the dataset = ", df['Age'].min(), "oldest women in the dataset = ", df['Age'].max())


#-Dataset Preview
st.subheader("Dataset Preview")
st.dataframe(df.head(10), use_container_width=True)


st.subheader("Summary Statistics")
st.dataframe(df.describe(), use_container_width=True)

#Footer
st.divider()
st.caption("King Abdulaziz University  . MISE 671 - Big DATA Management", text_alignment="center")