#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pandas as pd
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from helper import pie_graph, bail_age, Bail_time


philly_data = pd.read_csv('parsed1.csv')
zip_code = philly_data['zip']
attorney = philly_data['attorney']
#offenses = philly_data['offenses']
#offense_date = philly_data['offense_date']
age = philly_data['dob']
arrest_dt = philly_data['arrest_dt']
#case_stat = philly_data['case_status']
bail_amt = philly_data['bail_amount']
bail_type = philly_data['bail_type']
bail_paid = philly_data['bail_paid']
bail_dt = philly_data['bail_date']
prelim_date = philly_data['prelim_hearing_dt']
prelim_time = philly_data['prelim_hearing_time']


big_df = pd.DataFrame({'Zip':zip, 'Attorney': attorney, 'Age':age,'Arrest Date':arrest_dt,'Bail Amount Issued': bail_amt, 'Type of Bail': bail_type, 'Bail Paid': bail_paid,
                       'Bail Date': bail_dt, 'Preliminary Date': prelim_date, 'Preliminary Time': prelim_time})


fig_type = pie_graph.Pie_chart(big_df)
df_debt = bail_age.Bail_age(big_df)
fig_overall,fig_time = Bail_time.Bail_day(big_df)

app = dash.Dash()

server = app.server

colors = {'background':'#595354','text':'#F6F6F6'}
fig_type.update_layout(
    plot_bgcolor = colors['background'],
    paper_bgcolor = colors['background'],
    font_color = colors['text'],
)
fig_overall.update_layout(
    plot_bgcolor = colors['background'],
    paper_bgcolor = colors['background'],
    font_color = colors['text'],
)
fig_time.update_layout(
    plot_bgcolor = colors['background'],
    paper_bgcolor = colors['background'],
    font_color = colors['text'],
)
intro = '''
### Philadephia Bail Fund

Research shows that just three days in jail makes people more likely to lose their jobs and housing, be separated from their families, and commit crimes in the future.
The Philadelphia Bail Fund pays bail at the earliest possible moment for people who are indigent and cannot afford bail — ideally before they are transferred from their holding cell to jail.
The goal of the Philadelphia Bail Fund is to eliminate money bail in Philadelphia.

**Donate Here**: https://www.phillybailfund.org/

'''
markdown_bailtype = '''
### Types of Bail
**ROR (Release on Recognizance)**
This type of bail is the least restrictive. Release from jail only requires the defendant’s written agreement or promise to return to court and otherwise comply with any conditions of bail.

**Conditional Release (Nonmonetary Bail)**
When the court orders conditional release, the defendant is required to comply with specific conditions the court sees fit, i.e., drug test, reporting to probation office, electronic monitoring.

**Unsecured Bail – Monetary Amount Not Required**
A defendant in a criminal case may be released upon an agreement to be liable for a specific amount of money for failing to appear or otherwise failing to comply with the conditions of bail. In the event of a failure to appear, the defendant would be required to pay the agreed upon amount.

**Monetary Bail - Monetary Amount Required**
Defendant must make monetary payment to be released.
'''

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(children='Data Visualization of Bail in Philadephia',
        style = {'textAlign': 'center', 'color': colors['text']}
    ),
    html.H3(children='Hover over the Data!',
        style = {'textAlign': 'center', 'color': colors['text']}
    ),
    html.Div([
        dcc.Markdown(children = intro,
        style = {'color': colors['text']}),
        html.Div([
            dcc.Graph(
                    id ='debt_figure',
            ),
            dcc.Checklist(
                id = 'bail_type',
                options=[
                    {'label': 'Monetary', 'value': 'Monetary'},
                    {'label': 'ROR', 'value': 'ROR'},
                    {'label': 'Unsecured', 'value': 'Unsecured'},
                    {'label': 'Nonmonetary', 'value': 'Nonmonetary'},
                ],
                value = ['Monetary', 'ROR', 'Unsecured', 'Nonmonetary']
            ),
        ],style ={'width': '70%', 'display':'inline-block'}),
        html.Div([
            dcc.Markdown(children = markdown_bailtype,
            style = {'color': colors['text']})

        ],style ={'width': '30%', 'display':'inline-block'}),

    ]),
    html.Div([
        html.Div([
            dcc.Graph(
                id ='Bail-Types',
                figure=fig_type
            ),
        ], style ={'width': '49%', 'display':'inline-block'}),
        html.Div([
            dcc.Graph(
                id ='overall',
                figure=fig_overall
            ),
        ], style ={'width': '49%', 'display':'inline-block'}),
    ]),
    html.Div([
        dcc.Graph(
                id ='time',
                figure=fig_time
        ),
    ]),
])

@app.callback(
    Output('debt_figure', 'figure'),
    [Input('bail_type', 'value')])

def update_figure(selected_type):
    fig_debt = go.Figure()
    for _type in selected_type:
        filtered_df= df_debt[df_debt['Type of Bail'] == _type]
        fig_debt.add_trace(go.Scatter(x=filtered_df['Age'],
                                    y=filtered_df['Amount Bail Owed'],
                                    mode='markers',text=filtered_df['Type of Bail'],
                                    name = _type, marker_color = filtered_df['Colors']))
    fig_debt.update_xaxes(
        title_text = "Age",
        title_font = {"size": 20},
        title_standoff = 25)

    fig_debt.update_yaxes(
        title_text = "Bail Owed",
        title_standoff = 25)
    fig_debt.update_layout(
        title = 'Amount of Bail Debt',
        plot_bgcolor = colors['background'],
        paper_bgcolor = colors['background'],
        font_color = colors['text'],
    )
    fig_debt.update_layout(transition_duration =500)
    return fig_debt

if __name__ == '__main__':
    app.run_server(debug=True)
