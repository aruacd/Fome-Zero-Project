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
st.set_page_config(page_title='Visão Culinária', page_icon='🍽️',layout='wide')

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

# CONSTRÓI E PLOTA O 1º GRÁFICO DE BARRAS: 'Top 10 melhores tipos de culinária'

def bar_graph1(df_filtered):
    df_aux = (round(df_filtered.loc[:,['cuisines','aggregate_rating']]
                      .groupby('cuisines')
                      .mean()
                      .sort_values('aggregate_rating',ascending=False)
                      .reset_index()
                      .head(10),1))

    fig = px.bar(df_aux,
                  x='cuisines', y='aggregate_rating',
                  title='Top 10 melhores tipos de culinária',
                  labels={'cuisines':'Tipos de Culinária','aggregate_rating':'Média de Avaliação'},
                  text='aggregate_rating')

    fig.update_layout(title_x=0.2, showlegend=False)

    return fig

# CONSTRÓI E PLOTA O 2º GRÁFICO DE BARRAS: 'Top 10 piores tipos de culinária'

def bar_graph2(df_filtered):
    df_aux = (round(df_filtered.loc[:,['cuisines','aggregate_rating']]
                      .groupby('cuisines')
                      .mean()
                      .sort_values('aggregate_rating',ascending=True)
                      .reset_index()
                      .head(10),1))

    fig = px.bar(df_aux,
                  x='cuisines', y='aggregate_rating',
                  title='Top 10 piores tipos de culinária',
                  labels={'cuisines':'Tipos de Culinária','aggregate_rating':'Média de Avaliação'},
                  text='aggregate_rating')

    fig.update_layout(title_x=0.2, showlegend=False)
    
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

# df2_copy criado para as métricas iniciais não variarem com a mudança dos filtros
df2_metrics = df2.copy()

# create a copy of df2 for the cuisines filter
df2_cuisines = df2.copy()

# COUNTRY FILTER
countries = st.sidebar.multiselect(
    'Escolha o(s) país(es) que deseja visualizar os restaurantes',
    df2.loc[:,'country'].unique().tolist(),
    default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])

linhas_selecionadas = df2['country'].isin(countries)
df2 = df2.loc[linhas_selecionadas,:]

# SLIDER
restaurantes = st.sidebar.slider(label='Selecione a quantidade de restaurantes que deseja visualizar',
                                 value=10,
                                 min_value=1,
                                 max_value=20)

# # CUISINES FILTER - filtro somente para a visão cuisines
cuisines_aux = st.sidebar.multiselect(
    'Escolha o(s) tipo(s) culinário(s)',
    df2_cuisines.loc[:,'cuisines'].unique().tolist(),
    default=['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian','American', 'Italian'])

linhas_selecionadas = df2_cuisines['cuisines'].isin(cuisines_aux)
df2_cuisines = df2_cuisines.loc[linhas_selecionadas,:]

# Apply filters to create new DataFrame - para ser usado no dataframe top restaurantes e nos gráficos de barra para eles conseguires sofrer alteração
# de todos os filtros.
df_filtered = df2[df2['country'].isin(countries) & df2['cuisines'].isin(cuisines_aux)].copy()


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

st.markdown('# 🍽️ Visão Tipos Culinários')

with st.container():
    
    st.markdown('### Melhores Restaurantes dos Principais Tipos Culinários')
    
with st.container():
        
    col1, col2, col3 = st.columns(3, gap='large')
    
    with col1:
        
        df_aux = (df2_metrics.loc[df2_metrics['cuisines']=='Italian',['restaurant_id','aggregate_rating','restaurant_name']]
                        .groupby('restaurant_name')
                        .mean()
                        .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])
                        .reset_index())       

        nome_rest = df_aux.iloc[0,0]
        nota_rest = df_aux.iloc[0,2]
        
        col1.metric(label=f'Italiana: {nome_rest}', value=f'{nota_rest}/5.0')
  
    with col2:
            
        df_aux = (df2_metrics.loc[df2_metrics['cuisines'] == 'American',['restaurant_id','restaurant_name','aggregate_rating']]
                     .groupby('restaurant_name')
                     .mean()
                     .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])
                     .reset_index())
        
        nome_rest = df_aux.iloc[0,0]
        nota_rest = df_aux.iloc[0,2]

        col2.metric(label=f'Americana: {nome_rest}', value=f'{nota_rest}/5.0')
           
    with col3:
        
        df_aux = (df2_metrics.loc[df2_metrics['cuisines'] == 'Arabian',['restaurant_id','restaurant_name','aggregate_rating']]
                     .groupby('restaurant_name')
                     .mean()
                     .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])
                     .reset_index())
        
        nome_rest = df_aux.iloc[0,0]
        nota_rest = df_aux.iloc[0,2]

        col3.metric(label=f'Árabe: {nome_rest}', value=f'{nota_rest}/5.0')
                
with st.container():
    
    col1, col2, col3 = st.columns(3, gap='large')       
        
    with col1:
        
        df_aux = (df2_metrics.loc[df2_metrics['cuisines'] == 'Japanese',['restaurant_id','restaurant_name','aggregate_rating']]
                     .groupby('restaurant_name')
                     .mean()
                     .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])
                     .reset_index())
        
        nome_rest = df_aux.iloc[0,0]
        nota_rest = df_aux.iloc[0,2]

        col1.metric(label=f'Japonesa: {nome_rest}', value=f'{nota_rest}/5.0')
        
    with col2:

        df_aux = (df2_metrics.loc[df2_metrics['cuisines'] == 'Brazilian',['restaurant_id','restaurant_name','aggregate_rating']]
                     .groupby('restaurant_name')
                     .mean()
                     .sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True])
                     .reset_index())

        nome_rest = df_aux.iloc[0,0]
        nota_rest = df_aux.iloc[0,2]

        col2.metric(label=f'Brasileira: {nome_rest}', value=f'{nota_rest}/5.0')

with st.container():
     
    st.markdown(f'## Top {restaurantes} Restaurantes')

    df_aux = (df_filtered.loc[:,['restaurant_id',
                        'restaurant_name',
                        'country',
                        'city',
                        'cuisines',
                        'average_cost_for_two',
                        'aggregate_rating','votes']]
              .drop_duplicates(subset=['restaurant_name'])
              .sort_values(['aggregate_rating','restaurant_id'], ascending=[False,True])
              .head(restaurantes))
    
    st.dataframe(df_aux, use_container_width=True)

with st.container():
    
    col1, col2 = st.columns(2, gap='large')
    
    with col1:
        
        fig = bar_graph1(df_filtered)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        
        fig = bar_graph2(df_filtered)
        st.plotly_chart(fig, use_container_width=True)

        
   








        