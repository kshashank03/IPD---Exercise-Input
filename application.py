import streamlit as st
import pandas as pd
import data_access as da
import base64
import io

st.set_page_config(layout="wide")
@st.cache(allow_output_mutation=True)
def get_data():
    return []

# def clear_data():
#     get_data().clear()

data_options = da.data_options()
exercise_options = da.exercise_database()

# primary_group_options = exercise_options["PrimaryGroups"].unique().dropna()
different_groupings = exercise_options["PrimaryGroups"].dropna().unique()

individual_exercises = []
for i in different_groupings:
    for x in i.split("-"):
        if x not in individual_exercises:
            individual_exercises.append(x)

title = st.header("Exercise Dashboard Input Tool")

password = st.text_input(label="Password (Remember to clear when done)")

if password == st.secrets["password"]:
    l_column, m_column, r_column = st.beta_columns((1, 1, 1))

    players = l_column.selectbox(label="Players", options=data_options["Players"].dropna(), index=0)
    dates = m_column.date_input(label="Date")
    exercise_groups = r_column.multiselect(label="Primary Groups", options=individual_exercises, default=individual_exercises[0])
    # print(exercise_groups)
    if exercise_groups != None:
        for i in exercise_groups:
            exercise_options_list = exercise_options[exercise_options["PrimaryGroups"].notna()]
            exercise_options_list = exercise_options_list[exercise_options_list["PrimaryGroups"].str.contains(i)]

    # exercise_options = []
    filtered_exercise_options = exercise_options_list["ExerciseName"].dropna()
    # print(filtered_exercise_options)

    exercise = l_column.selectbox(label="Exercises", options=filtered_exercise_options, index=0)

    blocks = m_column.selectbox(label="Block", options=data_options["Block"].dropna(), index=0)
    sets = r_column.selectbox(label="Sets", options=data_options["Sets"].dropna(), index=0)
    reps = l_column.selectbox(label="Reps", options=data_options["Reps"].dropna(), index=0)
    time = m_column.selectbox(label="Time", options=data_options["Time"].dropna(), index=0)
    weight = r_column.text_input(label="Weight")
    tempo = l_column.selectbox(label="Tempo", options=data_options["Tempo"].dropna(), index=0)
    strength_goal = m_column.selectbox(label="Strength Goal", options=data_options["Strength Goal"].dropna(), index=0)
    notes = r_column.text_area(label="Notes")
    include_type = l_column.selectbox(label="Include", options=data_options["Include"].dropna(), index=0)
    contraction_type = m_column.selectbox(label="Contraction Type", options=data_options["Contraction Type"].dropna(), index=0)
    contraction_speed = r_column.selectbox(label="Contraction Speed", options=data_options["Contraction Speed"].dropna(), index=0)
    time_of_day = l_column.selectbox(label="Time of Day", options=data_options["Time Of Day"].dropna(), index=0)
    # submit = st.button(label="Submit")

    # comments = st.subheader("After adding your exercises, they'll automatically be copied to your clipboard")

    if st.button(label="Add Row"):
        get_data().append({"Player Name":players,
                    "Date Picker":"",
                    "Block":blocks,
                    "Exercise":exercise,
                    "Set":sets,
                    "Rep":reps,
                    "Time":time,
                    "Weight":weight,
                    "Tempo":tempo,
                    "Strength":strength_goal,
                    "Notes":notes,
                    "Contraction Type":contraction_type,
                    "Include":include_type,
                    "Contraction Speed":contraction_speed,
                    "Time":time_of_day})
        # st.write(pd.DataFrame(get_data()))
        # pd.DataFrame(get_data()).to_clipboard(index=False) # Removed this for now, doesn't work on Streamlit Sharing
    # if st.button(label="Download CSV"):

    if st.button(label="Clear Table"):
        get_data().clear()
        # st.subheader("Are you sure?")
        # st.write(pd.DataFrame(get_data()))
        # if st.button(label="Yes"):
        #     clear_data()
            # st.write(pd.DataFrame(get_data()))
        # if st.button(label="No"):
        #     break

    if st.button(label="Clear Last Row"):
        get_data().pop()
        # st.write(pd.DataFrame(get_data()))

    st.write(pd.DataFrame(get_data()))

    csv = pd.DataFrame(get_data()).to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings
    linko= f'<a href="data:file/csv;base64,{b64}" download="exercises.csv">Download csv file</a>'
    st.markdown(linko, unsafe_allow_html=True)