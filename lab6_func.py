import numpy as np
import pandas as pd

import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

import streamlit as st


yes_no = lambda x: 'Так' if x is True else 'Ні'

def build_graph(df, st_place):
    G = nx.DiGraph()

    for el in df.index:
        G.add_node(el)

    color = lambda w: 'b' if w > 0 else 'o'
    edges = [(ind, col, {"weight" :df.loc[ind, col], 'color': color(df.loc[ind, col])}) for ind in df.index for col in df.columns if df.loc[ind, col]!=0]
    weights = [row[2]['weight']*15 for row in edges]
    G.add_edges_from(edges)

    pos = nx.circular_layout(G)
    fig = plt.figure(figsize=(40, 15))
    plt.gca().set_facecolor('lightgray')
    nx.draw_networkx(
        G,
        pos, 
        # nodes
        node_size=5000,
        font_color='white',
        font_size=30,
        # edges
        connectionstyle='arc3, rad = 0.1',
        width=5,
        edge_color=weights,
        edge_cmap=plt.cm.RdYlBu,
        arrowsize=30
        )
    plt.colorbar(
        plt.cm.ScalarMappable(
            norm=matplotlib.colors.Normalize(vmin=-1, vmax=1), 
            cmap=plt.cm.RdYlBu
            ),
        pad=0.01
        )
    st_place.pyplot(fig)

    return G

def eigvals(df):
    return np.linalg.eigvals(np.array(df))

def get_spectral_radius(df):
    return np.max(np.absolute(eigvals(df)))

def check_perturbation_stability(df):
    return get_spectral_radius(df) <= 1

def check_numerical_stability(df):
    return get_spectral_radius(df) < 1

def find_even_cycles(df, G):
    cycles = pd.Series([c for c in nx.simple_cycles(G)], name='Парні цикли')
    cycles = cycles.apply(lambda row: row+[row[0]])

    is_even = lambda nodes: sum([df.loc[edge[0], edge[1]] < 0 for edge in zip(nodes[:-1], nodes[1:])]) // 2 != 1
    even_mask = cycles.apply(is_even)
    
    return cycles[even_mask].reset_index(drop=True), cycles

def check_structural_stability(df):
    return True