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
import pandas
import tabula
import streamlit as st
from PyPDF2 import PdfReader
import re

class ProcessPdf:
    '''Process a File PDF Uploaded for the user in a dataframe'''
    def __init__(self) -> None:
        self.table_raw_list = []
        self.table_dataframe = pandas.DataFrame()
        self.isValidPdf = False
        self.colunms_to_use =  [
            "CNPJ",
            "EMPRESA",
            "QTD.SERV",
            "VALOR BRUTO",
            "RUBRICA",
            "BCO",
            "AG",
            "CONTA CORRENTE",
            "VALOR LÍQUIDO"
        ]
    
    def processar_pdf(file):
        try:
            with st.spinner('Lendo e Processando dados do PDF...'):
                text = "..."  # Substitua isso pelo seu código para ler o texto do PDF

                cnpj_pattern = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
                cnpjs = re.findall(cnpj_pattern, text)

                # Use a função re.split para dividir o texto com base nos CNPJs
                text_parts = re.split(cnpj_pattern, text)

                # Crie um DataFrame com os CNPJs e o texto após os CNPJs
                data = {'CNPJ': cnpjs, 'Texto_Após_CNPJ': text_parts[1:]}
                df = pd.DataFrame(data)

                # Adicione colunas com base nos índices de caracteres
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
                # Converta a coluna para tipo float
                df['Valor Líquido'] = df['Valor Líquido'].astype(float)
                # Use a função str.replace() para remover "." (ponto), "/" (barra) e "-" (hífen) da coluna 'CNPJ'
                df['CNPJ'] = df['CNPJ'].str.replace('.', '').str.replace('/', '').str.replace('-', '')

                df_final = df.drop('Texto_Após_CNPJ', axis=1)
                # Substitua [2:] por algo mais significativo no seu contexto
                # df_final = df_final[2:]

                st.success("O arquivo foi processado com sucesso!")
                return df_final
        except Exception as e:
            st.error(f"Ocorreu um erro no processamento do arquivo: {str(e)}")
            return None
    
    def lenDataframe(self):
        return len(self.table_dataframe.index)
    
    def cleanDataframe(self):
        if self.isValidPdf:
            self.table_dataframe['NOME'] = self.table_dataframe['NOME'].apply(name_split)
            self.table_dataframe['C.P.F.'] = self.table_dataframe['C.P.F.'].apply(cleanCPF)
            self.table_dataframe['BCO No'] = self.table_dataframe['BCO No'].apply(fillZerosBCO)
            self.table_dataframe['AG. No'] = self.table_dataframe['AG. No'].apply(cleanAG)
            self.table_dataframe['AG. No'] = self.table_dataframe['AG. No'].apply(fillZerosAG)
            self.table_dataframe['AG. No'] = self.table_dataframe['AG. No'].apply(removeAG_DV)
            self.table_dataframe['C/C'] = self.table_dataframe['C/C'].apply(cleanConta)
            self.table_dataframe['C/C'] = self.table_dataframe['C/C'].apply(cleanContaBB)
            self.table_dataframe['VALOR'] = self.table_dataframe['VALOR'].apply(cleanValor)
            self.table_dataframe['VALOR'] = pandas.to_numeric(self.table_dataframe['VALOR'])
