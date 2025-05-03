import streamlit as st
import pandas as pd
import seaborn as sns
import io
import numpy as np

# Estilo escuro para o app
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: black;
        color: white;
    }
    .stMarkdown, .stDataFrame, .stText, .stTitle, .stHeader, .stSubheader, .stExpander {
        color: white !important;
    }
    label, .stSelectbox label {
        color: white !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #111111 !important;
        color: white !important;
    }
    div[data-baseweb="select"] span {
        color: white !important;
    }

    
    </style>
    """,
    unsafe_allow_html=True
)

# Carregar dados
df = sns.load_dataset('titanic')

# Abas do aplicativo
abas = st.tabs([
    "Principais métodos",
    "Métodos menos conhecidos",
    "Métodos Estatísticos",
    "Manipulação de Textos"
])

# ---------------------------- Aba 1: Principais Métodos ----------------------------
principais_metodos = {
    'info': 'Visão geral do DataFrame com tipos de dados e valores não nulos.',
    'describe': 'Estatísticas descritivas para colunas numéricas.',
    'value_counts': 'Contagem de valores únicos em uma coluna.',
    'groupby': 'Agrupamento de dados com operações agregadas.',
    'isnull / fillna': 'Identificação e preenchimento de valores nulos.',
    'loc / iloc': 'Seleção de dados por rótulo (loc) ou índice (iloc).',
    'apply': 'Aplicação de funções personalizadas.',
    'merge': 'Junção de DataFrames.',
    'pivot_table': 'Tabela dinâmica com agregações.',
    'query': 'Consulta de dados com expressões.'
}

codigos_principais = {
    'info': "df.info()",
    'describe': "df.describe()",
    'value_counts': "df['coluna'].value_counts()",
    'groupby': "df.groupby('coluna').mean()",
    'isnull / fillna': "df.isnull().sum()\ndf['coluna'] = df['coluna'].fillna(valor)",
    'loc / iloc': "df.loc[0:5, ['coluna']]\ndf.iloc[0:5, [indice_coluna]]",
    'apply': "df['nova_coluna'] = df['coluna'].apply(lambda x: funcao(x))",
    'merge': "pd.merge(df1, df2, on='coluna_comum')",
    'pivot_table': "df.pivot_table(index='coluna1', columns='coluna2', values='coluna_valor', aggfunc='mean')",
    'query': "df.query(\"condicao\")"
}

with abas[0]:
    st.title("Explorando o Pandas 🐼")
    metodo = st.selectbox('Escolha um método do pandas para explorar:', list(principais_metodos.keys()))
    st.subheader(f"Método: {metodo}")
    st.markdown(f"> {principais_metodos[metodo]}")
    with st.expander("🔍 Ver código utilizado"):
        st.code(codigos_principais[metodo], language='python')

    if metodo == 'info':
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())
    elif metodo == 'describe':
        st.dataframe(df.describe())
    elif metodo == 'value_counts':
        col = st.selectbox('Escolha a coluna:', df.select_dtypes(include='object').columns)
        st.dataframe(df[col].value_counts())
    elif metodo == 'groupby':
        col = st.selectbox('Escolha a coluna para agrupar:', df.select_dtypes(include='object').columns)
        st.dataframe(df.groupby(col).mean(numeric_only=True))
    elif metodo == 'isnull / fillna':
        st.write("Valores nulos antes:")
        st.dataframe(df.isnull().sum())
        df_filled = df.copy()
        df_filled['age'] = df_filled['age'].fillna(df_filled['age'].mean())
        st.write("Preenchendo idade nula com a média:")
        st.dataframe(df_filled[['age']].head())
    elif metodo == 'loc / iloc':
        st.dataframe(df.loc[0:5, ['sex', 'age']])
        st.dataframe(df.iloc[0:5, [3, 4]])
    elif metodo == 'apply':
        df_temp = df[['age']].copy()
        df_temp['maior_de_idade'] = df_temp['age'].apply(lambda x: 'Sim' if x >= 18 else 'Não')
        st.dataframe(df_temp.head())
    elif metodo == 'merge':
        df1 = df[['pclass', 'age']].head(5)
        df2 = df[['pclass', 'sex']].head(5)
        st.dataframe(pd.merge(df1, df2, on='pclass'))
    elif metodo == 'pivot_table':
        pivot = df.pivot_table(index='sex', columns='class', values='fare', aggfunc='mean')
        st.dataframe(pivot)
    elif metodo == 'query':
        st.dataframe(df.query("sex == 'female' and age < 18")[['sex', 'age', 'class']])

# ---------------------------- Aba 2: Métodos Menos Conhecidos ----------------------------
metodos_menos_conhecidos = {
    'explode': 'Transforma listas em células separadas em linhas.',
    'melt': 'Transforma colunas em linhas.',
    'eval': 'Executa expressões usando strings.',
    'nsmallest / nlargest': 'Retorna os menores/maiores valores.',
    'pipe': 'Aplica uma função de forma mais legível.'
}

with abas[1]:
    metodo2 = st.selectbox('Escolha um método menos conhecido para explorar:', list(metodos_menos_conhecidos.keys()))
    st.title(f"Explorando o método: {metodo2}")
    st.markdown(f"> {metodos_menos_conhecidos[metodo2]}")

    if metodo2 == 'explode':
        df_explode = pd.DataFrame({'id': [1, 2], 'valores': [[10, 20], [30, 40]]})
        with st.expander("🔍 Ver código utilizado"):
            st.code("df_explode.explode('valores')")
        st.dataframe(df_explode.explode('valores'))
    elif metodo2 == 'melt':
        df_melt = df[['sex', 'age', 'fare']].head()
        with st.expander("🔍 Ver código utilizado"):
            st.code("df_melt.melt(id_vars='sex')")
        st.dataframe(df_melt.melt(id_vars='sex'))
    elif metodo2 == 'eval':
        df_eval = df[['age', 'fare']].copy()
        df_eval['nova_coluna'] = df_eval.eval('age + fare')
        with st.expander("🔍 Ver código utilizado"):
            st.code("df_eval.eval('nova_coluna = age + fare')")
        st.dataframe(df_eval.head())
    elif metodo2 == 'nsmallest / nlargest':
        with st.expander("🔍 Ver código utilizado"):
            st.code("df.nsmallest(5, 'fare')")
        st.dataframe(df.nsmallest(5, 'fare'))
    elif metodo2 == 'pipe':
        def normalizar(df):
            return (df - df.min()) / (df.max() - df.min())
        with st.expander("🔍 Ver código utilizado"):
            st.code("""
def normalizar(df):
    return (df - df.min()) / (df.max() - df.min())

df[['fare', 'age']].pipe(normalizar)
""")
        st.dataframe(df[['fare', 'age']].pipe(normalizar).head())

# ---------------------------- Aba 3: Visualização de Dados ----------------------------
# ---------------- Aba 3 ----------------
with abas[2]:
    metodos_est = {
        "kurtosis": "Calcula a curtose, que mede caudas pesadas ou leves.",
        "skew": "Calcula a assimetria da distribuição."
        
    }
    metodo = st.selectbox("Escolha o método estatístico", list(metodos_est.keys()))
    st.title(f"📊 Estatística: {metodo}")
    st.markdown(f"> {metodos_est[metodo]}")
    if metodo == "kurtosis":
        #st.code("df.kurt(numeric_only=True)")
        st.dataframe(df.kurt(numeric_only=True))
        with st.expander("🔍 Ver código utilizado"):
            st.code("""
df.kurt(numeric_only=True)
""")
    elif metodo == "skew":
        #st.code("df.skew(numeric_only=True)")
        st.dataframe(df.skew(numeric_only=True))
        with st.expander("🔍 Ver código utilizado"):
            st.code("""
df.skew(numeric_only=True)
""")
    

# ---------------------------- Aba 4: Manipulação de Textos ----------------------------
manipulacao_metodos = {
    'upper': 'Transforma os valores da coluna em maiúsculas.',
    'lower': 'Transforma os valores da coluna em minúsculas.',
    'length': 'Calcula o comprimento dos valores da coluna.',
    'split': 'Divide os valores da coluna de acordo com um separador.'
}

with abas[3]:
    metodo4 = st.selectbox('Escolha um método de manipulação de texto para explorar:', list(manipulacao_metodos.keys()))
    st.title(f"Explorando o método de manipulação de texto: {metodo4}")
    st.markdown(f"> {manipulacao_metodos[metodo4]}")

    if metodo4 == 'upper':
        df_txt = df[['sex']].dropna().copy()
        df_txt['maiusculas'] = df_txt['sex'].str.upper()
        with st.expander("🔍 Ver código utilizado"):
            st.code("""
df_txt['maiusculas'] = df_txt['sex'].str.upper()
""")
        st.dataframe(df_txt.head())
    elif metodo4 == 'lower':
        df_txt = df[['sex']].dropna().copy()
        df_txt['minusculas'] = df_txt['sex'].str.lower()
        with st.expander("🔍 Ver código utilizado"):
            st.code("""
df_txt['minusculas'] = df_txt['sex'].str.lower()
""")
        st.dataframe(df_txt.head())
    elif metodo4 == 'length':
        df_txt = df[['sex']].dropna().copy()
        df_txt['tamanho'] = df_txt['sex'].str.len()
        with st.expander("🔍 Ver código utilizado"):
            st.code("""
df_txt['tamanho'] = df_txt['sex'].str.len()
""")
        st.dataframe(df_txt.head())
    elif metodo4 == 'split':
        df_txt = df[['sex']].dropna().copy()
        df_txt['primeiro_nome'] = df_txt['sex'].str.split().str[0]
        with st.expander("🔍 Ver código utilizado"):
            st.code("""
df_txt['primeiro_nome'] = df_txt['sex'].str.split().str[0]
""")
        st.dataframe(df_txt.head())
