import streamlit as st
import model as m
import numpy as np

st.title('Buscador de tiendas similares')
st.write('Introduce los datos de tu tienda y te mostraremos las tiendas más similares')

st.header('Datos de la tienda:')
size = st.number_input('Insertar tamaño de la tienda en m2', min_value=0, max_value=10000, value=0, step=1)
tarifa = st.selectbox('Seleccionar tarifa', ['Agresiva', 'Estandar', 'Plus', 'XPlus'])
rol = st.selectbox('Seleccionar rol', ['Conveniencia', 'Urbana Comercial', 'Urbana Residencial', 'Rural'])
surtido = st.selectbox('Seleccionar surtido', ['Nacional 3', 'Nacional 4', 'Nacional 5', 'Nacional 6', 'Nacional 7', 'Nacional 8'])
cp = st.number_input('Insertar código postal', min_value=0, max_value=99999, value=0, step=1)
tiendas = st.number_input('Insertar número de tiendas a devolver', min_value=0, max_value=10, value=0, step=1)

#add a button to search for the nearest neighbors
if st.button('Buscar'):
    # transform the tarifa, rol and surtido to numeric
    if tarifa == 'Agresiva':
        tarifa = 1
    elif tarifa == 'Estandar':
        tarifa = 2
    elif tarifa == 'Plus':
        tarifa = 3
    else:
        tarifa = 4
    
    if rol == 'Conveniencia':
        rol = 1
    elif rol == 'Urbana Comercial':
        rol = 2
    elif rol == 'Urbana Residencial':
        rol = 3
    else:
        rol = 4
    
    if surtido == 'Nacional 3':
        surtido = 1
    elif surtido == 'Nacional 4':
        surtido = 2
    elif surtido == 'Nacional 5':
        surtido = 3
    elif surtido == 'Nacional 6':
        surtido = 4
    elif surtido == 'Nacional 7':
        surtido = 5
    else:
        surtido = 6
    st.write('Las tiendas más similares son:')
    st.dataframe(m.tienda_espejo_CP(size,tarifa,rol,surtido,cp,tiendas))
