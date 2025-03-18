import pandas as pd
import os

# Definir caminhos
raw_data_path = "data/raw"
processed_data_path = "data/processed"

# Criar pasta de destino caso não exista
os.makedirs(processed_data_path, exist_ok=True)

# Carregar dados dos clubes
clubes_file = os.path.join(raw_data_path, "clubes.csv")
df_clubes = pd.read_csv(clubes_file, sep=';')

# Selecionar apenas as colunas necessárias (ID, Nome Oficial e UF)
df_clubes = df_clubes[['ID', 'Nome Oficial', 'UF']]

# Carregar dados de transferências
transferencias_file = os.path.join(raw_data_path, "transferencias.csv")
df_transferencias = pd.read_csv(transferencias_file, sep=';')

# Realizar o join com base na coluna Clube_ID
df_final = df_transferencias.merge(df_clubes, left_on='Clube_ID', right_on='ID', how='left')

# Remover a coluna ID duplicada (do df_clubes) e renomear a coluna
df_final = df_final.drop(columns=['ID_y'])
df_final = df_final.rename(columns={'ID_x': 'ID'})

# Definir a cotação do Euro para Real (exemplo: 1 Euro = 6.20 Reais)
exchange_rate = 6.20

# Converter a coluna Valor de Euro para Real
df_final["Valor"] = df_final["Valor"] * exchange_rate

# Salvar o resultado
output_file = os.path.join(processed_data_path, "transferencias_processed.csv")
df_final.to_csv(output_file, sep=';', index=False)

print(f"Arquivo processado salvo em: {output_file}")
