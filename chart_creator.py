import altair as alt
from formulas import GymBroStats
import streamlit as st
import pandas as pd
# import altair_latimes as lat

# alt.themes.register('latimes', lat.theme)
# alt.themes.enable('latimes')


st.title('What kinda weight can you push, brah?')
with st.sidebar:
    unit_system = st.radio('Unit System:', ['Imperial', 'Metric'])
    metric = unit_system=='Metric'
    unit = 'kg' if metric else 'lb'
    weight = st.number_input(f'Weight ({unit}) :rock:', 0, 500, 135, step=5)  # min: 0lb, max: 23h, default: 17h
    rpe = st.slider(f'RPE :tired_face:', 1, 10, 10)  # min: 1, max: 10, default: 10 (i.e. to failure)
    reps = st.number_input('Reps :repeat:', 1, 30, 1) #min 1 rep; max 30 for epley limitations
    formula = st.selectbox('Formula :scientist:', ['Epley', 'Brzycki', 'Kemmler et al.']) #tooltip-'Epley weak at low reps; Brzycki weak at high reps; Kemmler well-rounded and newest.')
    calculation = st.selectbox('Calculation :red_circle:', ['Rounded', 'Exact'])


rounded = calculation=='Rounded'

col1, col2 = st.columns([3, 1])
rep_range_filter = col1.selectbox('Range Filter:', ['All', 'Strength', 'Hypertrophy', 'Endurance'])

stats = GymBroStats(weight, reps, metric=metric)



df = pd.DataFrame({'Reps':stats.rep_array, 'Weight': stats.weight_array})
one_rep_max = df['Weight'][0]

weight_domain=[0, 750]
reps_domain_dictionary={'All': [1, 30], 'Strength':[1, 5], 'Hypertrophy': [8, 12], 'Endurance': [20, 30]}
reps_domain=reps_domain_dictionary[rep_range_filter]
# weight_title=

if rounded:
    chart = alt.Chart(df, title='Projected Weight and Rep Combinations').mark_bar().encode(
        x=alt.X('Reps:Q', scale=alt.Scale(domain=reps_domain)),
        y=alt.Y('Weight:Q', scale=alt.Scale(domain=weight_domain)),
        tooltip=["Weight:Q", alt.Text('Reps:Q')]
    ).interactive()
else:
    chart = alt.Chart(df, title='Projected Weight and Rep Combinations').mark_line().encode(
        x='Reps:Q',
        y='Weight:Q'
    ).interactive()

chart.properties(
    height=1000,
    width=1000
)

tab1, tab2=col1.tabs(['Visual', 'Table'])
tab1.altair_chart(chart, use_container_width=False)
tab2.write(df)
col2.header(f'1RM: {round(one_rep_max, 1)} {unit}')

# example = GymBroStats()
# chart = alt.mark_line().