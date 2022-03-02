import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import warnings

dataFrameOriginal_NoCovid = pd.read_excel('dataset.xlsx')


#DROPANDO CID
df = dataFrameOriginal_NoCovid
df = df.drop('CID',axis=1)

#Tranformando o ID do paciente em valir numérico enconded
labelencoder = LabelEncoder()
df['PACIENTE'] = labelencoder.fit_transform(df['PACIENTE'])

#Renaming collumns to english
df.rename(columns = {'PACIENTE': 'PATIENT', 'IDADE': 'AGE', 'SEXO': 'SEX'}, inplace = True)
df.rename(columns = {'HR_COLETA': 'HOURS_HOSPT', 'OBITO': 'DECEASED'}, inplace = True)
df.rename(columns = {'REINTERN60': 'READMISSION', 'FREQ_RESP(RPM)': 'RESP_RATE', 'FC-PULSE(BPM)': 'PULSE'}, inplace = True)
df.rename(columns = {'PAS(mmHg)': 'SYS_BLOOD_PRESS', 'PAD(mmHg)': 'DYAS_BLOOD_PRESS', 'TEMP(Graus Celsius)': 'TEMP'}, inplace = True)
df.rename(columns = {'GLUCOSE(MG/DL)': 'GLUCOSE', 'SODIO_SANGUE(mmol/l)': 'SODIUM', 'HEMATOCRITO(%)': 'HEMATOCRIT'}, inplace = True)
df.rename(columns = {'UREIA_SANGUE(mg/dl)': 'BLOOD_UREA', 'CONSCIEN_ALTERADA(1/0)': 'ALT_MENTAL', 'VENT_MECANICA(1/0)': 'MECH_VENTILATION'}, inplace = True)
df.rename(columns = {'DOEN_CARDIO_VASCULAR(1/0)': 'HIST_CARDIOVASCULAR', 'INSU_CARDIO_CONGEST(1/0)': 'CONG_CARDIAC_FAIL', 'NEOPLASIAS(1/0)': 'NEOPLASTIC_HIST'}, inplace = True)
df.rename(columns = {'DOEN_NEUROLOGICAS(1/0)': 'HIST_NEUROLOG', 'DOEN_CEREBROVASCULAR(1/0)': 'HIST_CEREBROVAS', 'DOEN_RENAL(1/0)': 'HIST_RENAL'}, inplace = True)
df.rename(columns = {'DOEN_PULMONAR_CRONICA(1/0)': 'HIST_CRON_PULMON', 'DOEN_HEPATICA(1/0)': 'HIST_LIVER', 'DOEN_PSIQUIATRICA(1/0)': 'HIST_PSYCHI'}, inplace = True)
df.rename(columns = {'MORA_EM_ASILO(1/0)': 'NURS_HOME_RESID', 'FUMANTE(1/0)': 'SMOKER'}, inplace = True)
df.rename(columns = {'HFAM_CARDIO_VASCULAR(1/0)': 'HIST_FAM_CARDIOVASC', 'HFAM_NEOPLASIAS(1/0)': 'HIST_FAM_NEOPLAS', 'HFAM_DOEN_NEUROLOGICAS(1/0)': 'HIST_FAM_NEUROLOGIC', 'HFAM_DOEN_PSIQUIATRICA(1/0)': 'HIST_FAM_PSYCHI'}, inplace = True)

#Null Values treatment and Text replacing
df['DECEASED'].fillna('N', inplace = True)
df['DECEASED'].replace({"N": 0, "S": 1}, inplace=True)

df['SEX'].replace({"F": 0, "M": 1}, inplace=True)

df['READMISSION'].fillna(0, inplace = True)
df['ALT_MENTAL'].fillna(0, inplace = True)
df['MECH_VENTILATION'].fillna(0, inplace = True)
df['HIST_CARDIOVASCULAR'].fillna(0, inplace = True)
df['CONG_CARDIAC_FAIL'].fillna(0, inplace = True)
df['NEOPLASTIC_HIST'].fillna(0, inplace = True)
df['HIST_NEUROLOG'].fillna(0, inplace = True)
df['HIST_CEREBROVAS'].fillna(0, inplace = True)
df['HIST_RENAL'].fillna(0, inplace = True)
df['HIST_CRON_PULMON'].fillna(0, inplace = True)
df['HIST_LIVER'].fillna(0, inplace = True)
df['HIST_PSYCHI'].fillna(0, inplace = True)
df['NURS_HOME_RESID'].fillna(0, inplace = True)
df['SMOKER'].fillna(0, inplace = True)
df['HIST_FAM_CARDIOVASC'].fillna(0, inplace = True)
df['HIST_FAM_NEOPLAS'].fillna(0, inplace = True)
df['HIST_FAM_NEUROLOGIC'].fillna(0, inplace = True)
df['HIST_FAM_PSYCHI'].fillna(0, inplace = True)


df['RESP_RATE']=df.groupby('PATIENT')['RESP_RATE'].apply(lambda x:x.fillna(x.median()))
df['PULSE']=df.groupby('PATIENT')['PULSE'].apply(lambda x:x.fillna(x.median()))
df['SYS_BLOOD_PRESS']=df.groupby('PATIENT')['SYS_BLOOD_PRESS'].apply(lambda x:x.fillna(x.median()))
df['DYAS_BLOOD_PRESS']=df.groupby('PATIENT')['DYAS_BLOOD_PRESS'].apply(lambda x:x.fillna(x.median()))
df['TEMP']=df.groupby('PATIENT')['TEMP'].apply(lambda x:x.fillna(x.median()))
df['GLUCOSE']=df.groupby('PATIENT')['GLUCOSE'].apply(lambda x:x.fillna(x.median()))
df['SODIUM']=df.groupby('PATIENT')['SODIUM'].apply(lambda x:x.fillna(x.median()))
df['HEMATOCRIT']=df.groupby('PATIENT')['HEMATOCRIT'].apply(lambda x:x.fillna(x.median()))
df['BLOOD_UREA']=df.groupby('PATIENT')['BLOOD_UREA'].apply(lambda x:x.fillna(x.median()))

GLMedian = df['GLUCOSE'].median()
SOMedian = df['SODIUM'].median()
HMMedian = df['HEMATOCRIT'].median()
BUMedian = df['BLOOD_UREA'].median()

df['GLUCOSE'].fillna(GLMedian, inplace = True)
df['SODIUM'].fillna(SOMedian, inplace = True)
df['HEMATOCRIT'].fillna(HMMedian, inplace = True)
df['BLOOD_UREA'].fillna(BUMedian, inplace = True)

df = df.reindex(columns=["PATIENT","AGE","SEX","HOURS_HOSPT","PULSE","DYAS_BLOOD_PRESS","GLUCOSE","SODIUM","HEMATOCRIT","BLOOD_UREA","ALT_MENTAL","MECH_VENTILATION","DECEASED"])

def get_dataframe():
    return df