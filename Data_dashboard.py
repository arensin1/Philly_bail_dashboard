#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
from collections import Counter
import dash
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
import numpy as np
import math
import statistics
import datetime
import plotly.express as px


philly_data = pd.read_csv('all.csv')
zip_code = philly_data['zip']
attorney = philly_data['attorney']
offenses = philly_data['offenses']
offense_date = philly_data['offense_date']
age = philly_data['dob']
age.dropna()
arrest_dt = philly_data['arrest_dt']
case_stat = philly_data['case_status']
bail_amt = philly_data['bail_amount']
bail_amt.dropna()
bail_type = philly_data['bail_type']
bail_paid = philly_data['bail_paid']
bail_dt = philly_data['bail_date']
prelim_date = philly_data['prelim_hearing_dt']
prelim_time = philly_data['prelim_hearing_time']


# In[22]:


type_size = []
types = []
amount_monetary = []
amount_ror = []
amount_unsec = []
amount_nonmon = []

bail_type_count = Counter(bail_type)
for bail_tup in bail_type_count.most_common():
    if bail_tup[0] != 'Nominal' and type(bail_tup[0]) != float:
        types.append(bail_tup[0])
        type_size.append(bail_tup[1])

def calculateAge(birthDate):
    days_in_year = 365.2425
    age = int((datetime.date.today() - birthDate).days / days_in_year)
    if age < 0:
        age = age + 100
    return age
i = 0
for bail in bail_amt:
    if bail_type[i] == 'Monetary':
        amount_monetary.append(bail)
    if bail_type[i] == 'ROR':
        amount_ror.append(bail)
    if bail_type[i] == "Unsecured":
        amount_unsec.append(bail)
    if bail_type[i] == 'Nonmonetary':
        amount_nonmon.append(bail)
    i += 1
amount_avgs = [statistics.mean(amount_monetary),statistics.mean(amount_ror),statistics.mean(amount_unsec),statistics.mean(amount_nonmon)]
avgs = np.round(amount_avgs, 2)
colors = ['powderblue', 'coral', 'rosybrown', 'palegreen']
df_1 = pd.DataFrame({'Type_Size':type_size, 'Types of Bail': types, "Average Amount Issued": avgs})
fig1 = px.pie(df_1, values="Type_Size", names="Types of Bail", color_discrete_sequence = colors,title='Types of Bail Issued', hover_data = ["Average Amount Issued"])




# In[51]:


morning_type =[]
afternoon_type = []
evening_type = []
morning_amt =[]
evening_amt =[]
afternoon_amt= []
i = 0
for time in prelim_time:
    parse_time_m = time.split()
    parse_time_c = time.split(':')
    if type(bail_type[i]) == str:
        if parse_time_m[1] == 'AM':
            if int(parse_time_c[0]) >3:
                morning_type.append(bail_type[i])
                morning_amt.append(bail_amt[i])
            else:
                evening_type.append(bail_type[i])
                evening_amt.append(bail_amt[i])
        else:
            if int(parse_time_c[0]) < 6:
                afternoon_type.append(bail_type[i])
                afternoon_amt.append(bail_amt[i])
            else:
                evening_type.append(bail_type[i])
                evening_amt.append(bail_amt[i])
    i += 1

morning_tct = Counter(morning_type).most_common()
value_morn = []
type_morning = []
time_morn = []
for i in morning_tct:
    type_morning.append(i[0])
    value_morn.append(i[1])
    time_morn.append("Morning")

evening_tct = Counter(evening_type).most_common()
value_evening = []
type_evening = []
time_evening = []
for i in evening_tct:
    type_evening.append(i[0])
    value_evening.append(i[1])
    time_evening.append("Evening")

afternoon_tct = Counter(afternoon_type).most_common()
value_aft = []
type_aft = []
time_aft = []
for i in afternoon_tct:
    type_aft.append(i[0])
    value_aft.append(i[1])
    time_aft.append("Afternoon")

time = time_morn
for time_ in time_evening:
    time.append(time_)
for time_ in time_aft:
    time.append(time_)
type_bail  = type_morning
for type_ in type_evening:
    type_bail.append(type_)
for type_ in type_aft:
    type_bail.append(type_)

values = value_morn

for value in value_evening:
    values.append(value)
for value in value_aft:
    values.append(value)
df = pd.DataFrame({"Time":time, 'Type': type_bail, 'Type Issued':values})
fig_overall = px.bar(df, x = 'Type', y = 'Type Issued', color = 'Time', barmode='group',title='Types of Bail Issued Throughout the Day')


time = ['Morning', 'Afternoon','Evening']
avg_amount = [statistics.mean(morning_amt), statistics.mean(afternoon_amt), statistics.mean(evening_amt)]
df_time_type = pd.DataFrame({'Time':time, 'Average Amount Issued':avg_amount})
fig_time = px.bar(df_time_type, x= "Time", y="Average Amount Issued",color_discrete_sequence =['lightpink']*len(df_time_type), title='Amount of Bail Issued Throughout the Day')

debt = []
types = []

age_int = []
i = 0

for birth in age:
    if type(birth) != float:
        date_time = datetime.datetime.strptime(birth, '%m/%d/%y').date()
        num_age = calculateAge(date_time)
        if type(bail_type[i]) != float:
            age_int.append(num_age)
            types.append(bail_type[i])
            debt.append(bail_amt[i] - bail_paid[i])

    i += 1
df_debt = pd.DataFrame({"Amount Bail Owed": debt, "Age": age_int, "Type of Bail": types})
colors = ['firebrick', 'salmon', 'rosybrown', 'peru']
fig_debt = px.scatter(df_debt, x="Age", y="Amount Bail Owed", color = "Type of Bail", log_y = True, title='Amount of Bail Owed')

# In[ ]:


app = dash.Dash()

colors = {'background':'#111111','text':'#7FDBFF'}

app.layout = html.Div(children=[
    html.Div([
        html.Div([
            html.H1(children='Data Visualization of Philly Bail'),
            html.Div(children='''Data on Type of Bail Amount Issued'''),

            dcc.Graph(
                id ='Bail-Types',
                figure=fig1
            ),
    ], className='six columns'),
    html.Div([

        dcc.Graph(
            id ='overall',
            figure=fig_overall
        ),
        ], className='six columns'),
    ],className = 'row'),
    html.Div([

        html.Div(children='''Data on Bail Amount Issued'''),
        dcc.Graph(
                id ='time',
                figure=fig_time
        ),
    ],className = 'row'),
    html.Div([

        dcc.Graph(
                id ='debt',
                figure=fig_debt
        ),
    ],className = 'row'),
])





if __name__ == '__main__':
    app.run_server()
