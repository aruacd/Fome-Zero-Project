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

# WIDE CONFIG PAGE
st.set_page_config(page_title='Main Page', page_icon='📊',layout='wide')

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

## MAP
def create_map(dataframe):
    f = folium.Figure(width=1920, height=1080)

    m = folium.Map(max_bounds=True).add_to(f)

    marker_cluster = MarkerCluster().add_to(m)

    for _, line in dataframe.iterrows():

        name = line["restaurant_name"]
        price_for_two = line["average_cost_for_two"]
        cuisine = line["cuisines"]
        currency = line["currency"]
        rating = line["aggregate_rating"]
        color = f'{line["color_name"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: {},00 ({}) para dois"
        html += "<br />Type: {}"
        html += "<br />Aggragate Rating: {}/5.0"
        html = html.format(name, price_for_two, currency, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["latitude"], line["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    folium_static(m, width=800, height=600)

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

st.markdown('# Fome Zero!')
st.markdown('## O Melhor lugar para encontrar o seu mais novo restaurante Favorito!')

with st.container():
    
    st.markdown('### Temos as seguintes métricas dentro da nossa plataforma:')
    
    col1, col2, col3 = st.columns(3, gap='large')
    
    with col1:
        # Quantidade de restaurantes registrados
        qnt_rest_reg = df2_metrics['restaurant_id'].nunique()
        col1.metric('Restaurantes Cadastrados:',qnt_rest_reg)
    
    with col2:
        # Quantidade de países únicos registrados
        qnt_pai_reg = df2_metrics["country"].nunique()
        col2.metric('Países Cadastrados: ',qnt_pai_reg)
        
    with col3:
       # Quantidade de cidades únicas registradas
        qnt_cid_reg = df2_metrics["city"].nunique() 
        col3.metric('Cidades Registradas: ',qnt_cid_reg)

with st.container():
    
    col1, col2, col3 = st.columns(3, gap='large')
    
    with col1:
        # Total de avaliações feitas
        tot_av = df2_metrics["votes"].sum()
        tot_av_format = '{:,.0f}'.format(tot_av).replace(',','.')
        col1.metric('Avaliações cadastradas na plataforma: ', tot_av_format)
        
    with col2:
        # Total de tipos de culinária registrados
        tot_culi = df2_metrics["cuisines"].nunique()
        col2.metric('Tipos de culinária cadastrados',tot_culi)
        
with st.container():
    
    st.markdown('### Visualize no mapa os restaurantes cadastrados na plataforma:')
    create_map(df2)
    
    