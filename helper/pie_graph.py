
import pandas as pd
from collections import Counter
import numpy as np
import math
import statistics
import plotly.express as px

colors = ['powderblue', 'coral', 'rosybrown', 'palegreen']
def _Counter(type_array):
    types =[]
    type_size = []
    bail_type_count = Counter(type_array)
    for bail_tup in bail_type_count.most_common(5):
        if type(bail_tup[0]) == str:
            types.append(bail_tup[0])
            type_size.append(bail_tup[1])
    return types, type_size
def Pie_chart(big_df):

    types, type_size = _Counter(big_df['Type of Bail'])

    bail_avg_type =[]

    for _type in types:

        df_filter_type = big_df[big_df['Type of Bail'] == _type]
        amt_arr = df_filter_type['Bail Amount Issued']
        bail_avg_type.append(statistics.mean(amt_arr))

    bail_avg_type = np.round(bail_avg_type, 2)
    df_type = pd.DataFrame({'Type Size':type_size, 'Types of Bail': types, "Average Amount Issued": bail_avg_type})
    fig_type = px.pie(df_type, values="Type Size", names="Types of Bail", color_discrete_sequence = colors,title='Types of Bail Issued', hover_data = ["Average Amount Issued"])

    return fig_type
