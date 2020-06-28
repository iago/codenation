import pandas as pd
import json

def carregar_dados(nome_arquivo):
    return pd.read_csv(nome_arquivo)

def escrever_json(dados, nome_arquivo):
    with open(nome_arquivo, 'w') as json_file:
        json.dump(dados, json_file)

def analise_exploratoria(dados):
    resultados = {}
    estados = list(dados['estado_residencia'].unique())
    coluna_alvo = 'pontuacao_credito'

    for estado in estados:
        dados_estado = dados[dados['estado_residencia'] == estado]
        resultados[estado] = {}
        
        resultados[estado]['moda'] = float(dados_estado[coluna_alvo].mode()[0])
        resultados[estado]['mediana'] = float(dados_estado[coluna_alvo].median())
        resultados[estado]['media'] = float(dados_estado[coluna_alvo].mean())
        resultados[estado]['desvio_padrao'] = float(dados_estado[coluna_alvo].std())
    
    return resultados

def main():
    dados = carregar_dados('desafio1.csv')
    resultados = analise_exploratoria(dados)
    escrever_json(resultados, 'submission.json')
    print('Sucesso!')

if __name__ == "__main__":
    main()

