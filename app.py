import streamlit as st
import numpy as np
import altair as alt
import pandas as pd

from time import sleep


def y_func(t, t_max=100, dt=1):
    t = t + dt
    while t < t_max:
        yield t, np.sin(t) + op_input


def reset_sim():
    del st.session_state["data"]
    st.session_state.data = pd.DataFrame([{"t": 0, "y": 0}], columns=["t", "y"])


if not "sleep_time" in st.session_state:
    st.session_state.sleep_time = 1

if not "data" in st.session_state:
    st.session_state.data = pd.DataFrame([{"t": 0, "y": 0}], columns=["t", "y"])


with st.sidebar:
    st.title("Altair Plotting Bug")
    st.session_state.run = st.toggle("Start")
    st.button("Reset", on_click=reset_sim)
    op_input = st.slider("Input", 0, 10, 0, 1)


@st.cache_data(ttl=5)
def write_graph(data):
    chart1 = alt.layer(
        alt.Chart(data)
        .mark_line(color="black")
        .encode(x=alt.X("t:Q", title="Time (s)"), y=alt.Y("y:Q", title="Output")),
    )

    return chart1


chart = write_graph(st.session_state.data)
st.altair_chart(chart)
buggy_chart = st.altair_chart(chart)


if st.session_state.run:
    data = st.session_state.data

    try:
        t_step, y = next(y_func(data["t"].iloc[-1]))
        df_n = pd.DataFrame([{"t": t_step, "y": y}])

        buggy_chart.add_rows(df_n)

        st.session_state["data"] = pd.concat(
            [data, df_n],
        )
    except StopIteration:
        st.toast("Complete!")


if st.session_state.run:
    sleep(st.session_state.sleep_time)
    st.experimental_rerun()
