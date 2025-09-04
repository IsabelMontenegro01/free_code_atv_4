# 1. Importar bibliotecas necessárias

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# 2. Importar dados com Pandas
# - Carregamos o arquivo CSV
# - Definimos a coluna "date" como índice
# - Garantimos que seja reconhecida como tipo datetime

df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")


# 3. Limpar os dados
# - Remover valores fora dos 2,5% inferiores e 2,5% superiores

df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]

# 4. Função: Gráfico de Linhas
# - Mostrar evolução das visualizações por dia

def draw_line_plot():
    # Criar a figura
    fig, ax = plt.subplots(figsize=(15, 5))
    
    # Plotar gráfico de linha
    ax.plot(df.index, df["value"], color="red", linewidth=1)
    
    # Definir título e rótulos
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    
    # Salvar figura
    fig.savefig("line_plot.png")
    return fig


# 5. Função: Gráfico de Barras
# - Mostrar média mensal de visualizações agrupadas por ano

def draw_bar_plot():
    # Criar cópia do DataFrame
    df_bar = df.copy()
    
    # Adicionar colunas de Ano e Mês
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month
    
    # Calcular médias mensais
    df_bar = df_bar.groupby(["year", "month"])["value"].mean().unstack()
    
    # Criar figura
    fig = df_bar.plot.bar(legend=True, figsize=(10, 8)).figure
    
    # Ajustar legenda
    plt.legend(
        title="Months",
        labels=[
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
    )
    
    # Rótulos dos eixos
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    
    # Salvar figura
    fig.savefig("bar_plot.png")
    return fig

# 6. Função: Gráficos de Caixa (Boxplots)
# - Dois gráficos: por ano (tendência) e por mês (sazonalidade)

def draw_box_plot():
    # Preparar os dados
    df_box = df.copy().reset_index()
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")
    df_box["month_num"] = df_box["date"].dt.month
    
    # Ordenar meses
    df_box = df_box.sort_values("month_num")
    
    # Criar figura com 2 gráficos lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Boxplot por Ano
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    
    # Boxplot por Mês
    sns.boxplot(x="month", y="value", data=df_box, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    
    # Salvar figura
    fig.savefig("box_plot.png")
    return fig

