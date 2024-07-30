import pandas as pd
from geopy.distance import great_circle

# Exemplo simplificado dos dados
data = {
    'CIDADE_ENDERECO': ['São Paulo', 'Campinas', 'Belo Horizonte', 'Rio de Janeiro'],
    'CAMPUS': ['Campus A', 'Campus B', 'Campus A', 'Campus C'],
    'LATITUDE_CAMPUS': [-23.5505, -22.9068, -19.9190, -22.9083],
    'LONGITUDE_CAMPUS': [-46.6333, -47.0594, -43.9388, -43.1964]
}

df = pd.DataFrame(data)

# Coordenadas das capitais estaduais (exemplo)
capitais = {
    'São Paulo': (-23.5505, -46.6333),
    'Campinas': (-22.9068, -47.0594),
    'Belo Horizonte': (-19.9190, -43.9388),
    'Rio de Janeiro': (-22.9083, -43.1964)
}

# Calcular distâncias para o campus mais próximo
df['DISTANCIA_MINIMA'] = df.apply(lambda row: min([great_circle((row['LATITUDE_CAMPUS'], row['LONGITUDE_CAMPUS']), cap).kilometers for cap in capitais.values()]), axis=1)

print(df[['CIDADE_ENDERECO', 'CAMPUS', 'DISTANCIA_MINIMA']])
