import numpy as np
import pandas as pd
import os

all_files = []
for file in os.listdir('data/'):
    all_files.append(file)

clients = pd.read_csv('data/' + 'D_clients.csv')
clients.drop_duplicates(inplace=True, ignore_index=True)
close_loan = pd.read_csv('data/' + 'D_close_loan.csv')
close_loan.drop_duplicates(inplace=True, ignore_index=True)
job = pd.read_csv('data/' + 'D_job.csv')
job.drop_duplicates(inplace=True, ignore_index=True)
last_credit = pd.read_csv('data/' + 'D_last_credit.csv')
last_credit.drop_duplicates(inplace=True, ignore_index=True)
loan = pd.read_csv('data/' + 'D_loan.csv')
loan.drop_duplicates(inplace=True, ignore_index=True)
pens = pd.read_csv('data/' + 'D_pens.csv')
pens.drop_duplicates(inplace=True, ignore_index=True)
salary = pd.read_csv('data/' + 'D_salary.csv')
salary.drop_duplicates(inplace=True, ignore_index=True)
target = pd.read_csv('data/' + 'D_target.csv')
target.drop_duplicates(inplace=True, ignore_index=True)
work = pd.read_csv('data/' + 'D_work.csv')
work.drop_duplicates(inplace=True, ignore_index=True)

merged_df = pd.merge(loan, close_loan, on='ID_LOAN')

merged_loan = merged_df.groupby('ID_CLIENT').agg({'ID_LOAN': 'count', 'CLOSED_FL': 'sum'})

merged_loan = merged_loan.reset_index()

clients['ID_CLIENT'] = clients['ID']

df = pd.merge(target, merged_loan, on='ID_CLIENT', how='left')
df = pd.merge(df, clients, on='ID_CLIENT', how='left')
df = pd.merge(df, salary, on='ID_CLIENT', how='left')

df['ALL_FL'] = df['ID_LOAN']

fin_cols = ['AGREEMENT_RK', 'TARGET', 'ALL_FL',
            'CLOSED_FL', 'AGE', 'GENDER', 'CHILD_TOTAL', 'DEPENDANTS',
            'SOCSTATUS_WORK_FL', 'SOCSTATUS_PENS_FL',
            'FL_PRESENCE_FL', 'OWN_AUTO', 'PERSONAL_INCOME']

df = df[fin_cols]

df.to_csv('fin_data.csv', index=False)