import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.write('Анализ данных клиентов банка')

df = st.cache_data(pd.read_csv)('data/fin_data.csv')
cols = ['TARGET', 'ALL_FL', 'CLOSED_FL',
        'AGE', 'GENDER', 'CHILD_TOTAL', 'DEPENDANTS',
        'SOCSTATUS_WORK_FL', 'SOCSTATUS_PENS_FL', 'FL_PRESENCE_FL',
        'OWN_AUTO', 'PERSONAL_INCOME']
st.write(df)

feature = st.sidebar.selectbox("Выберите признак для гистограммы: ", ('NONE', 'ALL_FL', 'CLOSED_FL',
                                          'AGE',  'DEPENDANTS', 'FL_PRESENCE_FL',
                                          'OWN_AUTO', 'PERSONAL_INCOME'))

if feature != 'NONE':
    fig = px.histogram(df[feature], x=feature)
    st.plotly_chart(fig)

pie_feat = st.sidebar.selectbox("Выберите признак для круговой диаграммы: ", ('NONE', 'TARGET', 'GENDER', 'CHILD_TOTAL',
                                                       'SOCSTATUS_WORK_FL', 'SOCSTATUS_PENS_FL'))

if pie_feat != 'NONE':
    fig = px.pie(values=df[pie_feat].value_counts(), names=df[pie_feat].unique(), title=pie_feat)
    st.plotly_chart(fig)

corr_map = st.sidebar.selectbox("Показать матрицу корреляций?: ", ('NO', 'YES'))

if corr_map == 'YES':
    df_corr = df[cols].corr()
    fig = go.Figure()
    fig.add_trace(
        go.Heatmap(
            x=df_corr.columns,
            y=df_corr.index,
            z=np.array(df_corr),
            text=df_corr.values,
            texttemplate='%{text:.2f}'
        )
    )
    st.plotly_chart(fig)

corr_feat = st.sidebar.selectbox("Показать корреляцию отдельных признаков?: ", ('NO', 'YES'))

if corr_feat == 'YES':
    feats = st.sidebar.multiselect('Выберите 2 признака', cols)
    if len(feats) != 2:
        st.write('Выберите, пожалуйста, ровно 2 признака')
    else:
        corr_level = round(df[feats[0]].corr(df[feats[1]]), 2)
        st.write(f'Корреляция между {feats[0]} и {feats[1]} равна '
                 f'{corr_level}')
        if -0.5 < corr_level < 0.5:
            st.write('Уровень корреляции низкий')
        else:
            st.write('Уровень корреляции высокий')

stat_feat = st.sidebar.selectbox("Показать статистики признаков?: ", ('NO', 'YES'))

if stat_feat == 'YES':
    st.write(df[cols].describe())

nan_feat = st.sidebar.selectbox("Показать пропуски и дубли?: ", ('NO', 'YES'))

if nan_feat == 'YES':
    st.write('Количество пропущенных значений:')
    st.write(df[cols].isnull().sum())
    st.write('')
    st.write(f'Количество дублированных строк: {int(df.duplicated().sum())}')

fin = st.sidebar.selectbox("Всё верно?: ", ('NO', 'YES'))

if fin == 'YES':
    st.balloons()
    st.write('Спасибо за уделенное время!')
