import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np
from sklearn.preprocessing import StandardScaler

    
def info_CP(cp):
    pob = municipios.at[(municipios["Codigo Postal"] == cp).idxmax(),"Poblacion"]
    #remove non numeric characters from pob
    pob = int(''.join(filter(str.isdigit, pob)))
    #density in hab/m2 (shops)
    den = municipios.at[(municipios["Codigo Postal"] == cp).idxmax(),"Densidad Comercial"]
    rent = municipios.at[(municipios["Codigo Postal"] == cp).idxmax(),"Renta Por Hogar"]
    #rent is in €
    #remove non numeric characters from rent
    rent = int(''.join(filter(str.isdigit, rent)))
    
    return (pob, den, rent)
    
#read the csv file
shops = pd.read_csv("Fichero surtido tiendas 10062023.csv", sep=";")
#clean the dataframe
shops = shops.drop(columns=['COMUNIDAD','PROVINCIA','FECHA APERTURA'])
shops.rename(columns={'CV 2021':'CV_1'}, inplace=True)
shops.rename(columns={'CV 2022':'CV_2'}, inplace=True)
shops.rename(columns={'Nivel de surtido':'SURTIDO'}, inplace=True)
shops.rename(columns={'SUP M2':'M2'}, inplace=True)
shops.rename(columns={'C. POSTAL':'CP'}, inplace=True)

#get location data from zipcodes
municipios = pd.read_csv("Variables Geoblink Codigo Postal.csv", sep=";")
#remove lines with empty data
municipios = municipios.dropna()

shops["CP"] = shops.CP.apply(info_CP)

#Define a mapping of string values of TARIFA to numerical equivalents
mapping = {'AGRESIVA': 1, 'ESTANDAR': 2, 'PLUS': 3, 'XPLUS': 4}

#Apply the mapping to the TARIFA column
shops['TARIFA'] = shops['TARIFA'].map(mapping)

#Define a mapping of string values of ROL to numerical equivalents
mapping = {'CONVENIENCIA':1, 'URB.RESIDENCIAL': 3, 'URB.COMERCIAL': 2, 'RURAL': 4}

#Apply the mapping to the ROL column
shops['ROL'] = shops['ROL'].map(mapping)

#Define a mapping of string values of SURTIDO to numerical equivalents
mapping = {'NACIONAL3':1, 'NACIONAL4': 2, 'NACIONAL5': 3, 'NACIONAL6': 4, 'NACIONAL7': 5, 'NACIONAL8': 6}

#Apply the mapping to the SURTIDO column
shops['SURTIDO'] = shops['SURTIDO'].map(mapping)

#remove non numeric characters from CV_1 and CV_2
shops['CV_1'] = shops['CV_1'].str.replace("’",'')
shops['CV_1'] = shops['CV_1'].str.replace("€",'')
shops['CV_1'] = shops['CV_1'].str.replace(" ",'')

shops['CV_2'] = shops['CV_2'].str.replace("’",'')
shops['CV_2'] = shops['CV_2'].str.replace("€",'')
shops['CV_2'] = shops['CV_2'].str.replace(" ",'')

#transform CV_1 and CV_2 to numeric
shops['CV_1'] = pd.to_numeric(shops['CV_1'])
shops['CV_2'] = pd.to_numeric(shops['CV_2'])

#split the tuple into 3 columns
shops[['POBLACION','DENSIDAD','RENTA']] = pd.DataFrame(shops.CP.tolist(), index= shops.index)

shops = shops.drop(columns=['CV_1','MUNICIPIO','CP'])

# M2 en metros cuadrados de la tienda
# TARIFA: 1: Agresiva, 2: Estandar, 3: Plus, 4: XPlus
# ROL: 1: Conveniencia, 2: Urbana Comercial, 3: Urbana Residencial, 4: Rural
# SURTIDO: 1: Nacional 3, 2: Nacional 4, 3: Nacional 5, 4: Nacional 6, 5: Nacional 7, 6: Nacional 8
# CP: Codigo Postal
# tiendas: numero de tiendas a devolver
# Devuelve un dataframe con la tienda mas parecida a la tienda de entrada
def tienda_espejo_CP(M2,TARIFA,ROL,SURTIDO,CP, tiendas):
    features = shops.drop(['CV_2','TIENDA'], axis = 1)
    scaler_raw = StandardScaler()
    X_nn = scaler_raw.fit_transform(features)
    X = np.array([M2,TARIFA,ROL,SURTIDO,info_CP(CP)[0],info_CP(CP)[1],info_CP(CP)[2]])
    X = scaler_raw.transform(X.reshape(1, -1))
    #find nearest neighbors
    nbrs = NearestNeighbors(n_neighbors=tiendas, algorithm='auto').fit(X_nn)
    result = nbrs.kneighbors(X,tiendas,return_distance=False)
    
    # for i in range(tiendas):
    #     print(shops.iloc[result[0][i]])
    #idea: once the shops selected, do a reframe of just those with the actual word and return only then=> should work quite easy
    answer = shops[shops.index.isin(result[0])]
    # reframe the numbers in the columns to the actual words
    answer['TARIFA'] = answer['TARIFA'].replace({1: 'AGRESIVA', 2: 'ESTANDAR', 3: 'PLUS', 4: 'XPLUS'})
    answer['ROL'] = answer['ROL'].replace({1: 'CONVENIENCIA', 2: 'URB.COMERCIAL', 3: 'URB.RESIDENCIAL', 4: 'RURAL'})
    answer['SURTIDO'] = answer['SURTIDO'].replace({1: 'NACIONAL3', 2: 'NACIONAL4', 3: 'NACIONAL5', 4: 'NACIONAL6', 5: 'NACIONAL7', 6: 'NACIONAL8'})
    return answer
    # return shops[shops.index.isin(result[0])]


