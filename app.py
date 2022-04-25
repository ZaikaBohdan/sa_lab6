import streamlit as st

import numpy as np
import pandas as pd

from lab6_func import *

st.set_page_config(
    page_title='СА Лаб 6: Когнітивне та імпульсне моделювання',
    page_icon='🎓',
    layout='wide'
)

st.write("# СА Лаб 6: Когнітивне та імпульсне моделювання")

with st.sidebar.header('1. Виберіть .xlsx файл'):
    uploaded_file = st.sidebar.file_uploader("Виберіть .xlsx файл з когнітивною картою", type=["xlsx"])
    # !!!!!!!!!!!!!! change later with cleaned data
    st.sidebar.markdown("""
        [Приклад необхідного файлу](https://github.com/ZaikaBohdan/datasetsforlabs/blob/main/sa_lab6_raw_input.xlsx?raw=true)
    """)

if uploaded_file is not None:
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Когнітивна карта <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    st.write("## Когнітивна карта")
    
    c1, c2 = st.columns(2) 

    cogn_map = pd.read_excel(uploaded_file, index_col=0)

    c1.write("### Матриця")
    c1.dataframe(cogn_map)

    c1.write("### Граф")
    graph = build_graph(cogn_map, c1)

    c2.write("### Стійкість")

    stab_vals = [
        check_perturbation_stability(cogn_map), 
        check_numerical_stability(cogn_map), 
        check_structural_stability(cogn_map, graph)
        ]
    stab_df = pd.DataFrame(
        [yes_no(val) for val in stab_vals], 
        index = ['За збуренням', 'Чисельна', 'Структурна'],
        columns=['Так/Ні']
        )

    c2.dataframe(stab_df.T)

    eigvals_list = [str(val).strip('()').replace('j', 'i') for val in eigvals(cogn_map)]
    
    c2.write(f"### Власні числа (max|λ| = {get_spectral_radius(cogn_map): .2f})")
    c2.dataframe(pd.Series(eigvals_list, name='Власні числа'), height=205)

    c2.write(f"### Парні цикли")
    if stab_vals[2]:
        c2.write('Відсутні')
    else:
        c2.dataframe(find_even_cycles(cogn_map, graph)[0], height=205)

    
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Імпульсивне моделювання <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    with st.sidebar.header('2. Параметри імпульсного моделювання'):
        Q = np.zeros(8)
        cols = st.sidebar.columns(2)
        t = st.sidebar.number_input('N ітерацій', min_value=0, value=5)
        for i in range(8):
            Q[i] = cols[i%2].selectbox(
                f'Q({i})',
                [-1, 0, 1],
                1
            )
        imp_mod_button = st.sidebar.button('Виконати')

    if imp_mod_button:
        st.write("## Імпульсне моделювання")
        impulse_model(t, Q, cogn_map)

else:
    st.info('Виберіть .xlsx файл з вхідними даними у боковому вікні зліва.')