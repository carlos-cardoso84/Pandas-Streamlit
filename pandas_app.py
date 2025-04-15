import streamlit as st
import pandas as pd
import seaborn as sns
import io

# Carregar dataset de exemplo
df = sns.load_dataset('titanic')

abas = st.tabs(["Principais métodos", "Métodos menos conhecidos"])

# --- Dicionários com explicações e códigos ---
principais_metodos = {
    'info': 'O método info() fornece uma visão geral rápida sobre o DataFrame, incluindo tipos de dados, contagem de valores não nulos e uso de memória.',
    'describe': 'O método describe() gera estatísticas descritivas, como média, desvio padrão e quartis para colunas numéricas.',
    'value_counts': 'O método value_counts() retorna a contagem de ocorrências de valores únicos em uma série. Útil para explorar colunas categóricas.',
    'groupby': 'O método groupby() permite realizar operações agregadas (como média, soma, contagem) com base em uma ou mais chaves de agrupamento.',
    'isnull / fillna': 'Os métodos isnull() e fillna() são usados para identificar e tratar valores ausentes (nulos) em um DataFrame.',
    'loc / iloc': 'loc e iloc são utilizados para acessar linhas e colunas de um DataFrame com base em rótulos (loc) ou posições inteiras (iloc).',
    'apply': 'O método apply() aplica uma função a cada elemento ou linha/coluna do DataFrame, sendo muito útil para transformações personalizadas.',
    'merge': 'O método merge() junta dois DataFrames com base em colunas comuns, similar ao JOIN do SQL.',
    'pivot_table': 'pivot_table() cria tabelas dinâmicas que resumem os dados com agregações como soma ou média.',
    'query': 'O método query() permite filtrar dados usando expressões em string, facilitando consultas mais legíveis.'
}

codigos_principais = {
    'info': """df.info()""",
    'describe': """df.describe()""",
    'value_counts': """df['coluna'].value_counts()""",
    'groupby': """df.groupby('coluna').mean()""",
    'isnull / fillna': """df.isnull().sum()
df['coluna'] = df['coluna'].fillna(valor)""",
    'loc / iloc': """df.loc[0:5, ['coluna']]
df.iloc[0:5, [indice_coluna]]""",
    'apply': """df['nova_coluna'] = df['coluna'].apply(lambda x: funcao(x))""",
    'merge': """pd.merge(df1, df2, on='coluna_comum')""",
    'pivot_table': """df.pivot_table(index='coluna1', columns='coluna2', values='coluna_valor', aggfunc='mean')""",
    'query': """df.query(\"condicao\")"""
}

metodos_menos_conhecidos = {
    'explode': 'explode(): transforma listas em células separadas em linhas distintas.',
    'melt': 'melt(): transforma colunas em linhas, ideal para reestruturar dados.',
    'eval': 'eval(): permite executar operações matemáticas usando strings como expressões.',
    'nsmallest / nlargest': 'nsmallest() / nlargest(): retorna os menores/maiores valores de uma coluna.',
    'pipe': 'pipe(): encadeia funções permitindo aplicar transformações de forma mais legível.'
}

with abas[0]:
    st.title(f"Explorando o Pandas 🐼")

    metodo = st.selectbox('Escolha um método do pandas para explorar:', list(principais_metodos.keys()))

    st.subheader(f" Método: {metodo}")
    st.markdown(f"> {principais_metodos[metodo]}")
    with st.expander("🔍 Ver código utilizado"):
        st.code(codigos_principais[metodo], language='python')

    if metodo == 'info':
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

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
        st.write("Com loc (por rótulo):")
        st.dataframe(df.loc[0:5, ['sex', 'age']])
        st.write("Com iloc (por índice):")
        st.dataframe(df.iloc[0:5, [3, 4]])

    elif metodo == 'apply':
        df_temp = df[['age']].copy()
        df_temp['maior_de_idade'] = df_temp['age'].apply(lambda x: 'Sim' if x >= 18 else 'Não')
        st.dataframe(df_temp.head())

    elif metodo == 'merge':
        df1 = df[['pclass', 'age']].head(5)
        df2 = df[['pclass', 'sex']].head(5)
        df_merged = pd.merge(df1, df2, on='pclass')
        st.dataframe(df_merged)

    elif metodo == 'pivot_table':
        pivot = df.pivot_table(index='sex', columns='class', values='fare', aggfunc='mean')
        st.dataframe(pivot)

    elif metodo == 'query':
        query_result = df.query("sex == 'female' and age < 18")
        st.dataframe(query_result[['sex', 'age', 'class']])

with abas[1]:
    metodo2 = st.selectbox('Escolha um método menos conhecido para explorar:', list(metodos_menos_conhecidos.keys()))

    st.title(f"Explorando o método: {metodo2}")
    st.markdown(f"> {metodos_menos_conhecidos[metodo2]}")

    if metodo2 == 'explode':
        df_explode = pd.DataFrame({
            'id': [1, 2],
            'valores': [[10, 20], [30, 40]]
        })
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