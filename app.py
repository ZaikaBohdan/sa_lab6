import streamlit as st

import numpy as np
import pandas as pd

from lab6_func import *

st.set_page_config(
    page_title='СА Лаб 6: Когнітивне та імпульсивне моделювання',
    page_icon='🎓',
    layout='wide'
)

st.write("# СА Лаб 6: Когнітивне та імпульсивне моделювання")

with st.sidebar.header('1. Виберіть .xlsx файл'):
    uploaded_file = st.sidebar.file_uploader("Виберіть .xlsx файл з когнітивною картою", type=["xlsx"])
    # !!!!!!!!!!!!!! change later with cleaned data
    st.sidebar.markdown("""
        [Приклад необхідного файлу](https://github.com/ZaikaBohdan/datasetsforlabs/blob/main/sa_lab6_raw_input.xlsx?raw=true)
    """)

if uploaded_file is not None:
    st.write("## Когнітивна карта")
    
    c1, c2 = st.columns(2) 

    cogn_map = pd.read_excel(uploaded_file, index_col=0)

    c1.write("### Матриця")
    c1.dataframe(cogn_map)

    c1.write("### Граф")
    graph = build_graph(cogn_map, c1)

    with st.sidebar.header('2. Виберіть тип моделювання'):
        model_type = st.sidebar.selectbox(
            'Виберіть тип моделювання',
            [f'{name} моделювання' for name in ["Когнітивне", "Імпульсивне"]],
            0
        )

    # add effect from select box
    c2.write("### Стійкість")

    stab_funcs = [
        check_perturbation_stability, 
        check_numerical_stability, 
        check_structural_stability
        ]
    stab_df = pd.DataFrame(
        [yes_no(func(cogn_map)) for func in stab_funcs], 
        index = ['За збуренням', 'Чисельна', 'Структурна'],
        columns=['Так/Ні']
        )

    c2.dataframe(stab_df.T)

    eigvals_list = [str(val).strip('()').replace('j', 'i') for val in eigvals(cogn_map)]
    
    c2.write(f"### Власні числа (max|λ| = {get_spectral_radius(cogn_map): .2f})")
    c2.write(eigvals_list)

    c2.write(f"### Парні цикли")
    c2.write(find_even_cycles(cogn_map, graph)[0])

else:
    st.info('Виберіть .xlsx файл з вхідними даними у боковому вікні зліва.')