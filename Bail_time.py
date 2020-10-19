import pandas as pd
from collections import Counter
import math
import statistics
import plotly.express as px
import numpy as np


colors = ['powderblue', 'coral', 'rosybrown', 'palegreen']

def Bail_day(big_df):
    #Type of bail issued throughut the day

    morning_type =[]
    afternoon_type = []
    evening_type = []
    morning_amt =[]
    evening_amt =[]
    afternoon_amt= []
    i = 0
    for time in big_df['Preliminary Time']:
        parse_time_m = time.split()
        parse_time_c = time.split(':')
        if type(big_df['Type of Bail'][i]) == str and big_df['Type of Bail'][i] != 'Nominal':
            if parse_time_m[1] == 'AM':
                if int(parse_time_c[0]) >3:
                    morning_type.append(big_df['Type of Bail'][i])
                    morning_amt.append(big_df['Bail Amount Issued'][i])
                else:
                    evening_type.append(big_df['Type of Bail'][i])
                    evening_amt.append(big_df['Bail Amount Issued'][i])
            else:
                if int(parse_time_c[0]) < 6:
                    afternoon_type.append(big_df['Type of Bail'][i])
                    afternoon_amt.append(big_df['Bail Amount Issued'][i])
                else:
                    evening_type.append(big_df['Type of Bail'][i])
                    evening_amt.append(big_df['Bail Amount Issued'][i])
        i += 1




    morn_df = pd.DataFrame({'Type': morning_type, 'Bail Amount Issued': morning_amt})
    afternoon_df = pd.DataFrame({'Type': afternoon_type, 'Bail Amount Issued': afternoon_amt})
    evening_df = pd.DataFrame({'Type': evening_type, 'Bail Amount Issued': evening_amt})

    morning_tct = Counter(morning_type).most_common()
    value_morn = []
    type_morning = []
    time_morn = []
    avgs_morn = []
    for i in morning_tct:
        morn_filter = morn_df[morn_df['Type'] == i[0]]
        avg = statistics.mean(morn_filter['Bail Amount Issued'])
        avgs_morn.append(avg)
        type_morning.append(i[0])
        value_morn.append(i[1])
        time_morn.append("Morning")


    evening_tct = Counter(evening_type).most_common()
    value_evening = []
    type_evening = []
    time_evening = []
    avgs_evening = []
    for i in evening_tct:
        evening_filter = evening_df[evening_df['Type'] == i[0]]
        avg = statistics.mean(evening_filter['Bail Amount Issued'])
        avgs_evening.append(avg)
        type_evening.append(i[0])
        value_evening.append(i[1])
        time_evening.append("Evening")

    afternoon_tct = Counter(afternoon_type).most_common()
    value_aft = []
    type_aft = []
    time_aft = []
    avgs_aft = []
    for i in afternoon_tct:
        aft_filter = afternoon_df[afternoon_df['Type'] == i[0]]
        avg = statistics.mean(aft_filter['Bail Amount Issued'])
        avgs_aft.append(avg)
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

    avg_time = avgs_morn

    for avg in avgs_evening:
        avg_time.append(avg)
    for avg in avgs_aft:
        avg_time.append(avg)
    avg_time = np.round(avg_time, 2)

    df = pd.DataFrame({"Time":time, 'Type': type_bail, 'Type Issued':values, 'Bail Amount Avg': avg_time})
    fig_overall = px.bar(df, x = 'Type', y = 'Type Issued', color = 'Time', barmode='group',
                    color_discrete_sequence = colors,hover_data = ["Bail Amount Avg"],title='Types of Bail Issued Throughout the Day')
    #Graph bail issued by time

    time = ['Morning', 'Afternoon','Evening']
    avg_amount = [statistics.mean(morning_amt), statistics.mean(afternoon_amt), statistics.mean(evening_amt)]
    df_time_type = pd.DataFrame({'Time':time, 'Average Amount Issued':avg_amount})
    fig_time = px.bar(df_time_type, x= "Time", y="Average Amount Issued",color_discrete_sequence =['palegreen']*len(df_time_type),
                        title='Amount of Bail Issued Throughout the Day')



    return fig_overall, fig_time
