# ==================================================================
# LIBRARIES
# ==================================================================

import pandas as pd
import inflection
import streamlit as st
from PIL import Image
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import plotly.express as px
import random
import string

# WIDE CONFIG PAGE
st.set_page_config(page_title='Visão Países', page_icon='🌎',layout='wide')

# ==================================================================
# AUXILIARY VARIABLES
# ==================================================================

COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}


COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}

# ==================================================================
# FUNCTIONS
# ==================================================================

## COLUMN RENAME AND ADJUSTMENT FUNCTIONS

def rename_columns(dataframe):
    df = dataframe.copy()

    title = lambda x: inflection.titleize(x)

    snakecase = lambda x: inflection.underscore(x)

    spaces = lambda x: x.replace(" ", "")

    cols_old = list(df.columns)

    cols_old = list(map(title, cols_old))

    cols_old = list(map(spaces, cols_old))

    cols_new = list(map(snakecase, cols_old))

    df.columns = cols_new

    return df

def country_name(country_id):
    return COUNTRIES[country_id]

def color_name(color_code):
    return COLORS[color_code]

def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
    
def adjust_columns_order(dataframe):
    df = dataframe.copy()

    new_cols_order = [
        "restaurant_id",
        "restaurant_name",
        "country",
        "city",
        "address",
        "locality",
        "locality_verbose",
        "longitude",
        "latitude",
        "cuisines",
        "price_type",
        "average_cost_for_two",
        "currency",
        "has_table_booking",
        "has_online_delivery",
        "is_delivering_now",
        "aggregate_rating",
        "rating_color",
        "color_name",
        "rating_text",
        "votes",
    ]

    return df.loc[:, new_cols_order]

## DATA PROCESSING AND CLEANING FUNCTION

def process_data(file_path):
    df = pd.read_csv(file_path)

    df = df.dropna()

    df = rename_columns(df)

    df["price_type"] = df.loc[:, "price_range"].apply(lambda x: create_price_tye(x))

    df["country"] = df.loc[:, "country_code"].apply(lambda x: country_name(x))

    df["color_name"] = df.loc[:, "rating_color"].apply(lambda x: color_name(x))

    df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

    df = df.drop_duplicates()

    df = adjust_columns_order(df)
    
    df = df.reset_index()
    
    df = df.drop(columns=['index'])

    df.to_csv("dataset/processed/data.csv", index=False)

    return df

# CONSTRÓI E PLOTA O 1º GRÁFICO DE BARRAS: 'Quantidade de restaurantes por país'

def bar_graph1(df2):
    df_aux = (df2.loc[:,["country","restaurant_id"]]
                 .groupby("country")
                 .nunique()
                 .sort_values("restaurant_id",ascending=False)
                 .reset_index())

    # Adiciona colunas de cores aleatórias
    df_aux['color'] = ['#' + ''.join(random.choices(string.hexdigits, k=6)) for _ in range(len(df_aux))]

    fig = px.bar(df_aux,
                 x='country',y='restaurant_id',
                 title='Quantidade de restaurantes por país',
                 labels={'country':'Países','restaurant_id':'Número de restaurantes cadastrados'},
                 color='color',
                 text='restaurant_id')

    #remover o color do balão
    fig.update_traces(hovertemplate='País: %{x}<br>Restaurantes: %{y}')

    fig.update_layout(title_x=0.4, showlegend=False)

    return fig
    
# CONSTRÓI E PLOTA O 2º GRÁFICO DE BARRAS: 'Quantidade de cidades registradas por país'

def bar_graph2(df2):
    df_aux = (df2.loc[:,["city","country"]]
                 .groupby("country")
                 .nunique()
                 .sort_values("city",ascending=False)
                 .reset_index())
    
    # Adiciona colunas de cores aleatórias
    df_aux['color'] = ['#' + ''.join(random.choices(string.hexdigits, k=6)) for _ in range(len(df_aux))]

    fig = px.bar(df_aux,
                 x='country', y='city',
                 title='Quantidade de cidades registradas por país',
                 labels={'country': 'Países', 'city': 'Quantidade de cidades'},
                 color='color',
                 text='city')

    #remover o color do balão
    fig.update_traces(hovertemplate='País: %{x}<br>Cidades: %{y}')
    
    fig.update_layout(title_x=0.4, showlegend=False)
    
    return fig

# CONSTRÓI E PLOTA O 3º GRÁFICO DE BARRAS: 'Média das avaliações feitas por país'

def bar_graph3(df2):
    df_aux = (round(df2.loc[:,['votes','country']]
                 .groupby('country')
                 .mean()
                 .sort_values('votes',ascending=False)
                 .reset_index(),1))

    # Adiciona coluna de cores aleatórias
    df_aux['color'] = ['#' + ''.join(random.choices(string.hexdigits, k=6)) for _ in range(len(df_aux))]

    fig = px.bar(df_aux,
                 x='country', y='votes',
                 title='Média das avaliações feitas por país',
                 labels={'country': 'Países', 'votes': 'Quantidade de avaliações'},
                 color='color',
                 text='votes')

    #remover o color do balão
    fig.update_traces(hovertemplate='País: %{x}<br>Média das avaliações: %{y}')

    fig.update_layout(title_x=0.25, showlegend=False)

    return fig

# CONSTRÓI E PLOTA O 4º GRÁFICO DE BARRAS: 'Média preço de prato para 2 por país'

def bar_graph4(df2):
    # preços na moeda local de cada país
    df_aux = round((df2.loc[:,['average_cost_for_two','country']]
                 .groupby('country')
                 .mean()
                 .sort_values('average_cost_for_two', ascending=False)
                 .reset_index()),2)

    # Adiciona coluna de cores aleatórias
    df_aux['color'] = ['#' + ''.join(random.choices(string.hexdigits, k=6)) for _ in range(len(df_aux))]

    fig = px.bar(df_aux,
                 x='country', y='average_cost_for_two',
                 title='Média preço de prato para 2 por país',
                 labels={'country': 'Países', 'average_cost_for_two': 'Preço de um prato para dois'},
                 color='color',
                 text='average_cost_for_two')

    #remover o color do balão
    fig.update_traces(hovertemplate='País: %{x}<br>Média do preço para dois: %{y}')

    fig.update_layout(title_x=0.25, showlegend=False)

    return fig

## LOAD DATA AND COPY
RAW_DATA_PATH = f"dataset/raw/data.csv"
df_raw = pd.read_csv(RAW_DATA_PATH)
df1 = df_raw.copy()

## REMANE COLUMNS
df1 = rename_columns(df1)

## TREAT NA
df1 = df1.dropna()

## PROCESS DATA
df2 = process_data(RAW_DATA_PATH)

# ============================================================= INÍCIO DA ESTRUTURA LÓGICA CÓDIGO =============================================================

# ==================================================================
# SIDE BAR
# ==================================================================

image = Image.open('logo.png')
st.sidebar.image( image, width=120)

st.sidebar.markdown('# Fome Zero!')
st.sidebar.markdown('## Escolha o Melhor Restaurante para sua Fome!')
st.sidebar.markdown('''---''')

st.sidebar.markdown('## Filtros')

# COUNTRY FILTER
countries = st.sidebar.multiselect(
    'Escolha o(s) país(es) que deseja visualizar os restaurantes',
    df2.loc[:,'country'].unique().tolist(),
    default=['Brazil','United States of America','Canada', 'England', 'Australia', 'South Africa'])

linhas_selecionadas = df2['country'].isin(countries)
df2 = df2.loc[linhas_selecionadas,:]

# PROCESSED DATA DOWNLOAD BUTTON
st.sidebar.markdown("### Dados Tratados")
processed_data = pd.read_csv('dataset/processed/data.csv')
st.sidebar.download_button(
    label='Download',
    data=processed_data.to_csv(index=False, sep=';'),
    file_name='data.csv',
    mime='text/csv',
)

# POWERED BY
st.sidebar.markdown('''---''')
st.sidebar.markdown('###### Powered by Aruã Dias')

# ==================================================================
# STREAMLIT LAYOUT
# ==================================================================

st.markdown('# 🌎 Visão Países')

with st.container():
    
    fig = bar_graph1(df2)
    st.plotly_chart(fig, use_container_width=True)
   
with st.container():
    
    fig = bar_graph2(df2)
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns(2, gap='large')
    
    with col1:
        
        fig = bar_graph3(df2)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        
        fig = bar_graph4(df2)
        st.plotly_chart(fig, use_container_width=True)