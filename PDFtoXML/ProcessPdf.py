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
import streamlit as st



class ProcessPdf:
    def toDataframe(self, text):
       
                 
            # Use regex para encontrar os CNPJs no texto
            cnpj_pattern = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
            cnpjs = re.findall(cnpj_pattern, text)

            # Use a função re.split para dividir o texto com base nos CNPJs
            text_parts = re.split(cnpj_pattern, text)

            # Crie um DataFrame com os CNPJs e o texto após os CNPJs
            data = {'CNPJ': cnpjs, 'Texto_Após_CNPJ': text_parts[1:]}
            df = pd.DataFrame(data)

            df['Empresa'] = df['Texto_Após_CNPJ'].str[:33]
            df['Qtd.Serv'] = df['Texto_Após_CNPJ'].str[38:43]
            df['Valor Bruto'] = df['Texto_Após_CNPJ'].str[46:60]
            df['Rubrica'] = df['Texto_Após_CNPJ'].str[61:68]
            df['BCO'] = df['Texto_Após_CNPJ'].str[219:222]
            df['AG'] = df['Texto_Após_CNPJ'].str[223:229]
            df['Conta'] = df['Texto_Após_CNPJ'].str[230:244]
            df['Valor Líquido'] = df['Texto_Após_CNPJ'].str[279:297]

            # Remova os pontos dos milhares e substitua a vírgula pelo ponto
            df['Valor Líquido'] = df['Valor Líquido'].str.replace('.', '').str.replace(',', '.')
            # Use a função str.replace() para remover "." (ponto), "/" (barra) e "-" (hífen) da coluna 'CNPJ'
            df['CNPJ'] = df['CNPJ'].str.replace('.', '').str.replace('/', '').str.replace('-', '')

            df_final = df.drop('Texto_Após_CNPJ', axis=1)
            st.success("O arquivo foi processado com sucesso!")
            self.table_dataframe = df_final                    
            self.table_dataframe.index += 1
            self.isValidPdf = True
        

    def lenDataframe(self):
        return len(self.table_dataframe.index)

    
    