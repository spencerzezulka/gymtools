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
    formula = st.selectbox('Formula :scientist:', ['Epley', 'Brzycki', 'Kemmler'], help='Epley weak at low reps; Brzycki weak at high reps; Kemmler well-rounded ') #tooltip-'Epley weak at low reps; Brzycki weak at high reps; Kemmler well-rounded and newest.')
    calculation = st.selectbox('Calculation :red_circle:', ['Rounded', 'Exact'])
    rounded = calculation=='Rounded'
    if rounded:
        send_method = st.radio('Send Method: :smiling_imp://:frowning:', ['Full', 'Half'], help='Exclusively round down to half send. Round nearest to full send.')
        round_down = send_method!='Full' #round down if we're half sending, round nearest if full
    else:
        round_down=False




col1, col2 = st.columns([4, 1])
rep_range_filter = col1.selectbox('Filter Range by Goal:', ['All', 'Strength', 'Hypertrophy', 'Endurance'])

stats = GymBroStats(weight, reps, metric=metric, formula=formula, rounded=rounded, round_down=round_down)

plotting_data = pd.DataFrame({'Reps': stats.rep_array, 'Weight': stats.weight_array})
one_rep_max = plotting_data['Weight'][0]

table_data = pd.DataFrame({'Weight': stats.weight_array}, index=stats.rep_array)
table_data.index.name='Reps'


weight_domain=[0, 750]
reps_domain_dictionary={'All': [1, 30], 'Strength':[1, 5], 'Hypertrophy': [8, 12], 'Endurance': [20, 30]}
reps_domain=reps_domain_dictionary[rep_range_filter]
# weight_title=

if rounded:
    chart = alt.Chart(plotting_data, title='Projected Weight and Rep Combinations').mark_bar().encode(
        x=alt.X('Reps:Q', scale=alt.Scale(domain=reps_domain)),
        y=alt.Y('Weight:Q'), #scale=alt.Scale(domain=weight_domain)),
        tooltip=["Weight:Q", alt.Text('Reps:Q')]
    ).interactive()
else:
    base= alt.Chart(plotting_data, title='Projected Weight and Rep Combinations').mark_point().encode(
        x=alt.X('Reps:Q', scale=alt.Scale(domain=reps_domain)),
        y='Weight:Q'
    )
    chart = alt.Chart(plotting_data, title='Projected Weight and Rep Combinations').mark_line().encode(
        x=alt.X('Reps:Q', scale=alt.Scale(domain=reps_domain)),
        y='Weight:Q'
    ).interactive()
    chart=base+chart


chart.properties(
    height=1000,
    width=1000
)

tab1, tab2=col1.tabs(['Visual', 'Table'])
tab1.altair_chart(chart, use_container_width=False)
tab2.write(table_data)
formula_to_latex = {'Epley':r'W=w(1+\frac{r}{30})', 'Brzycki':r'W=w \cdot \frac{36}{37-r}', 'Kemmler':r'W=w( 0.988 + 0.0104r + 0.00190r^2-0.0000584r^3)'}
col2.header(f'1RM: {round(one_rep_max, 1)} {unit}')
col2.header(formula)
col2.latex(formula_to_latex[formula])

# example = GymBroStats()
# chart = alt.mark_line().