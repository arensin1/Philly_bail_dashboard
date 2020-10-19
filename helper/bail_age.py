
import pandas as pd
import numpy as np
import datetime


def calculateAge(birthDate):
    days_in_year = 365.2425
    age = int((datetime.date.today() - birthDate).days / days_in_year)
    if age < 0:
        age = age + 100
    return age


def Bail_age(big_df):
    debt = []
    types = []

    age_int = []
    i = 0

    for birth in big_df['Age']:
        if type(birth) != float:
            date_time = datetime.datetime.strptime(birth, '%m/%d/%y').date()
            num_age = calculateAge(date_time)
            if type(big_df['Type of Bail'][i]) != float and big_df['Type of Bail'][i] != 'Nominal' :
                age_int.append(num_age)
                types.append(big_df['Type of Bail'][i])
                debt.append(big_df['Bail Amount Issued'][i] - big_df['Bail Paid'][i])

        i += 1
    color_type = []
    for i in types:
        if i == 'Monetary':
            color_type.append('powderblue')
        if i == 'ROR':
            color_type.append('coral')
        if i == 'Unsecured':
            color_type.append('rosybrown')
        if i == 'Nonmonetary':
            color_type.append('palegreen')
    df_debt = pd.DataFrame({"Amount Bail Owed": debt, "Age": age_int, "Type of Bail": types, 'Colors': color_type})
    return df_debt
