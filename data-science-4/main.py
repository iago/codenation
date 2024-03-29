#!/usr/bin/env python
# coding: utf-8

# # Desafio 6
# 
# Neste desafio, vamos praticar _feature engineering_, um dos processos mais importantes e trabalhosos de ML. Utilizaremos o _data set_ [Countries of the world](https://www.kaggle.com/fernandol/countries-of-the-world), que contém dados sobre os 227 países do mundo com informações sobre tamanho da população, área, imigração e setores de produção.
# 
# > Obs.: Por favor, não modifique o nome das funções de resposta.

# ## _Setup_ geral

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.preprocessing import KBinsDiscretizer, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


# In[2]:


# Algumas configurações para o matplotlib.
'''%matplotlib inline

from IPython.core.pylabtools import figsize


figsize(12, 8)

sns.set()'''


# In[2]:


countries = pd.read_csv("countries.csv")


# In[3]:


new_column_names = [
    "Country", "Region", "Population", "Area", "Pop_density", "Coastline_ratio",
    "Net_migration", "Infant_mortality", "GDP", "Literacy", "Phones_per_1000",
    "Arable", "Crops", "Other", "Climate", "Birthrate", "Deathrate", "Agriculture",
    "Industry", "Service"
]

countries.columns = new_column_names

countries.head(5)


# ## Observações
# 
# Esse _data set_ ainda precisa de alguns ajustes iniciais. Primeiro, note que as variáveis numéricas estão usando vírgula como separador decimal e estão codificadas como strings. Corrija isso antes de continuar: transforme essas variáveis em numéricas adequadamente.
# 
# Além disso, as variáveis `Country` e `Region` possuem espaços a mais no começo e no final da string. Você pode utilizar o método `str.strip()` para remover esses espaços.

# ## Inicia sua análise a partir daqui

# In[4]:


# Sua análise começa aqui.
countries[countries.select_dtypes(include='object').columns] = countries.select_dtypes(include='object').apply(lambda x: x.str.replace(',', '.'))

countries[countries.select_dtypes(include='object').columns] = countries.select_dtypes(include='object').apply(lambda x: x.str.strip())

countries = countries.apply(lambda x: pd.to_numeric(x, errors='ignore'))


# In[5]:


countries.head()


# ## Questão 1
# 
# Quais são as regiões (variável `Region`) presentes no _data set_? Retorne uma lista com as regiões únicas do _data set_ com os espaços à frente e atrás da string removidos (mas mantenha pontuação: ponto, hífen etc) e ordenadas em ordem alfabética.

# In[6]:


def q1():
    return sorted(countries['Region'].unique())


# ## Questão 2
# 
# Discretizando a variável `Pop_density` em 10 intervalos com `KBinsDiscretizer`, seguindo o encode `ordinal` e estratégia `quantile`, quantos países se encontram acima do 90º percentil? Responda como um único escalar inteiro.

# In[7]:


def q2():
    disc = KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile')
    bins = disc.fit_transform(countries[['Pop_density']])
    return len([bin for bin in bins if bin == 9])


# # Questão 3
# 
# Se codificarmos as variáveis `Region` e `Climate` usando _one-hot encoding_, quantos novos atributos seriam criados? Responda como um único escalar.

# In[8]:


def q3():
    return len(countries['Region'].unique()) + len(countries['Climate'].unique())


# In[9]:


test_country = [
    'Test Country', 'NEAR EAST', -0.19032480757326514,
    -0.3232636124824411, -0.04421734470810142, -0.27528113360605316,
    0.13255850810281325, -0.8054845935643491, 1.0119784924248225,
    0.6189182532646624, 1.0074863283776458, 0.20239896852403538,
    -0.043678728558593366, -0.13929748680369286, 1.3163604645710438,
    -0.3699637766938669, -0.6149300604558857, -0.854369594993175,
    0.263445277972641, 0.5712416961268142
]


# ## Questão 4
# 
# Aplique o seguinte _pipeline_:
# 
# 1. Preencha as variáveis do tipo `int64` e `float64` com suas respectivas medianas.
# 2. Padronize essas variáveis.
# 
# Após aplicado o _pipeline_ descrito acima aos dados (somente nas variáveis dos tipos especificados), aplique o mesmo _pipeline_ (ou `ColumnTransformer`) ao dado abaixo. Qual o valor da variável `Arable` após o _pipeline_? Responda como um único float arredondado para três casas decimais.

# In[30]:


def q4():
    num_column_indexes = list(countries.select_dtypes(include='number').columns)

    imputer = SimpleImputer(strategy='median')
    scaler = StandardScaler()
    num_pipe = Pipeline([('imputer', imputer), ('scaler', scaler)])
    transformer = ColumnTransformer(transformers=[('num', num_pipe, num_column_indexes)])

    countries_transformed = transformer.fit_transform(countries)

    df_test_country = pd.DataFrame({column: [value] for column, value in zip(new_column_names, test_country)})
    test_country_transformed = transformer.transform(df_test_country)

    arable_index = df_test_country.select_dtypes(include='number').columns.get_loc('Arable')
    return float(round(test_country_transformed[0, arable_index], 3))


# ## Questão 5
# 
# Descubra o número de _outliers_ da variável `Net_migration` segundo o método do _boxplot_, ou seja, usando a lógica:
# 
# $$x \notin [Q1 - 1.5 \times \text{IQR}, Q3 + 1.5 \times \text{IQR}] \Rightarrow x \text{ é outlier}$$
# 
# que se encontram no grupo inferior e no grupo superior.
# 
# Você deveria remover da análise as observações consideradas _outliers_ segundo esse método? Responda como uma tupla de três elementos `(outliers_abaixo, outliers_acima, removeria?)` ((int, int, bool)).

# In[13]:


def q5():
    quartile_1 = countries['Net_migration'].quantile(0.25)
    quartile_3 = countries['Net_migration'].quantile(0.75)
    iqr = quartile_3 - quartile_1

    countries['Net_migration_outlier'] = countries['Net_migration'].apply(lambda x: 'Outlier abaixo' if x < quartile_1 - 1.5 * iqr else ('Outlier acima' if x > quartile_3 + 1.5 * iqr else 'Não é outlier'))

    outliers_abaixo = countries['Net_migration_outlier'].value_counts()['Outlier abaixo']
    outliers_acima = countries['Net_migration_outlier'].value_counts()['Outlier acima']

    return int(outliers_abaixo), int(outliers_acima), bool((outliers_abaixo + outliers_acima) / len(countries) < 0.1)


# ## Questão 6
# Para as questões 6 e 7 utilize a biblioteca `fetch_20newsgroups` de datasets de test do `sklearn`
# 
# Considere carregar as seguintes categorias e o dataset `newsgroups`:
# 
# ```
# categories = ['sci.electronics', 'comp.graphics', 'rec.motorcycles']
# newsgroup = fetch_20newsgroups(subset="train", categories=categories, shuffle=True, random_state=42)
# ```
# 
# 
# Aplique `CountVectorizer` ao _data set_ `newsgroups` e descubra o número de vezes que a palavra _phone_ aparece no corpus. Responda como um único escalar.

# In[14]:


categories = ['sci.electronics', 'comp.graphics', 'rec.motorcycles']
newsgroup = fetch_20newsgroups(subset="train", categories=categories, shuffle=True, random_state=42)


# In[15]:


def q6():
    cv = CountVectorizer()
    newsgroup_cv = cv.fit_transform(newsgroup['data'])

    index_phone = 0
    for index, token in enumerate(cv.get_feature_names()):
        if token == 'phone':
            index_phone = index
            break
    return int(sum(newsgroup_cv.toarray()[:,index_phone]))


# ## Questão 7
# 
# Aplique `TfidfVectorizer` ao _data set_ `newsgroups` e descubra o TF-IDF da palavra _phone_. Responda como um único escalar arredondado para três casas decimais.

# In[16]:


def q7():
    tfidf = TfidfVectorizer()
    newsgroup_tfidf = tfidf.fit_transform(newsgroup['data'])
    tfidf.get_feature_names()

    index_phone = 0
    for index, token in enumerate(tfidf.get_feature_names()):
        if token == 'phone':
            index_phone = index
            break

    return float(round(sum(newsgroup_tfidf.toarray()[:,index_phone]), 3))


# In[ ]:




