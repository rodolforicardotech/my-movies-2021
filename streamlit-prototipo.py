import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

st.title("Olá, mundo!")


upload = st.file_uploader("Escolha um arquivo:")
if upload is not None:
    df = pd.read_csv(upload)
    df = df[['Created', 'Title', 'Title Type', 'IMDb Rating', 
         'Runtime (mins)', 'Year', 'Genres', 'Num Votes', 
         'Release Date', 'Directors']]
    df = df.rename(columns={'Created': 'Adicionado', 
                   'Title': 'Título', 'Title Type': 'Tipo', 
                   'IMDb Rating': 'Nota IMDb', 'Runtime (mins)': 'Duração', 
                   'Year': 'Ano', 'Genres': 'Gênero', 'Num Votes': 'Votos', 
                   'Release Date': 'Lançamento', 'Directors': 'Diretores'})
    df.Diretores = df.Diretores.fillna('-')
    #df.iloc[50] = df.iloc[50].replace('video', 'movie')
    df[df.Tipo == 'tvMiniSeries'] = df[df.Tipo == 'tvMiniSeries'].replace('tvMiniSeries', 'tvSeries')
    df[df.Tipo == 'short'] = df[df.Tipo == 'short'].replace('short', 'tvSeries')
    df[df.Tipo == 'video']= df[df.Tipo == 'video'].replace('video', 'tvSeries')

    df[df.Tipo.isin(['tvSpecial', 
                 'tvEpisode'])] = df[df.Tipo.isin(['tvSpecial', 'tvEpisode'])].replace(['tvSpecial', 'tvEpisode'], 
                                                                                                    ['tvSeries', 'tvSeries'])

    st.write("# O total de filmes/séries assistidos:")
    st.write(df.Tipo.value_counts())
    teste = df.Tipo.value_counts()
    st.write(df.shape[0])
    
    datas = df[['Título', 'Lançamento']].sort_values(by='Lançamento')   
    st.write("# O mais antigo e o mais recente da lista:")
    st.write(datas.head(1))
    st.write(datas.tail(1))
    
    st.write("# O menos votado e o mais votado:")
    votos = df[['Título', 'Votos']].sort_values(by='Votos')
    st.write(votos.head(1))
    st.write(votos.tail(1))
    
    df.Duração = df.Duração.fillna(0)
    duracao = df[['Título', 'Duração']].sort_values('Duração')
    duracaosemzero = duracao[duracao.Duração != 0]
    st.write("# Menor e Maior Duração (minutos):")
    st.write(duracaosemzero.head(1))
    st.write(duracaosemzero.tail(1))

    notas = df[['Título', 'Nota IMDb']].sort_values('Nota IMDb')
    st.write("# Maiores e Menores notas no IMDb")
    st.write(notas.head(1))
    st.write(notas.tail(1))

    dummies = df.Gênero.str.get_dummies(sep=', ')
    soma = dummies.sum().sort_values(ascending=False)
    #soma = pd.DataFrame({soma['Tipo'], soma['Contagem'])
    st.write("# Gráfico - Gêneros Assistidos")
    st.bar_chart(soma)

    st.write("# Filmes por mês:")
    df["Adicionado"] = pd.to_datetime(df["Adicionado"])
    meses = df[["Adicionado"]]
    meses['Adicionado'] = pd.DatetimeIndex(meses['Adicionado']).month
    meses = meses["Adicionado"].value_counts().rename_axis("Meses").reset_index(name="Contagem")
    meses = meses.sort_values(by="Meses")
    
    nomes_meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", 
                   "Junho", "Julho", "Agosto", "Setembro", "Outubro",
                    "Novembro", "Dezembro"]
    
    numeros_meses = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    
    meses = meses.replace(numeros_meses, nomes_meses)
    
    #st.write(meses)
    
    #st.line_chart(meses["Contagem"])
    
    c = alt.Chart(meses).mark_line().encode(
     x='Meses', y='Contagem').interactive()
    st.altair_chart(c)

    st.write("# Média dos filmes assistidos:")
    filmes = df[df.Tipo == 'movie']
    st.write(filmes['Nota IMDb'].mean().round(2))
    
    st.write("# Média das séries assistidas:")
    series = df[df.Tipo == 'tvSeries']
    st.write(series['Nota IMDb'].mean().round(2))
    
    #plt.show()
    fig = plt.figure(figsize=(5, 3))
    plt.pie(teste, labels = teste.index, autopct='%.0f%%')
    #plt.pie(teste)
    st.pyplot(fig)