from CleanData import (
    name_split,
    cleanAG,
    cleanConta,
    cleanCPF,
    cleanValor,
    cleanContaBB,
    fillZerosBCO,
    fillZerosAG,
    removeAG_DV,
)
import re
import pandas as pd
import tabula
import streamlit as st

class ProcessPdf:
    def toDataframe(self, text):
        '''Convert table in PDF text into DataFrame'''
        try:
            # Use regex para encontrar os CNPJs no texto
            cnpj_pattern = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
            cnpjs = re.findall(cnpj_pattern, text)

            # Use a função re.split para dividir o texto com base nos CNPJs
            text_parts = re.split(cnpj_pattern, text)

            # Crie um DataFrame com os CNPJs e o texto após os CNPJs
            data = {'CNPJ': cnpjs, 'Texto_Após_CNPJ': text_parts[1:]}
            df = pd.DataFrame(data)

            # Extraia os dados usando regex
            df['Empresa'] = df['Texto_Após_CNPJ'].str.extract(r'(.*?)\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}')[0]
            df['Qtd.Serv'] = df['Texto_Após_CNPJ'].str.extract(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}(.*?)\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}')[0]
            # Continue com os outros campos...

            # Remova os pontos dos milhares e substitua a vírgula pelo ponto
            df['Valor Líquido'] = df['Texto_Após_CNPJ'].str.extract(r'(\d{3}\.\d{3},\d{2})')[0]
            df['Valor Líquido'] = df['Valor Líquido'].str.replace('.', '').str.replace(',', '.')
         

            # Use a função str.replace() para remover "." (ponto), "/" (barra) e "-" (hífen) da coluna 'CNPJ'
            df['CNPJ'] = df['CNPJ'].str.replace('.', '').str.replace('/', '').str.replace('-', '')

            # Remova a coluna temporária 'Texto_Após_CNPJ'
            df = df.drop('Texto_Após_CNPJ', axis=1)

            self.table_dataframe = df
            self.isValidPdf = True

        except Exception as e:
            st.error(f"Ocorreu um erro no processamento do arquivo: {str(e)}")
            self.isValidPdf = False

        finally:
            return self.table_dataframe
    
    def lenDataframe(self):
        return len(self.table_dataframe.index)
    
    