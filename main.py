import streamlit as st
import pandas as pd
from urllib.parse import quote
from datetime import date

def main():
    st.title("Requerimientos diario de compras")
    # Leer un archivo Excel
    df = pd.read_excel("FORMATO_REQUERIMIENTOS.xlsx")

    # Inicializar el estado de las cantidades si no existe
    if 'quantities' not in st.session_state:
        st.session_state['quantities'] = {row['PRODUCTO']: int(row['CANTIDAD']) if not pd.isnull(row['CANTIDAD']) else 0 for index, row in df.iterrows()}

    # Añadir buscador
    search_query = st.text_input("Buscar producto")
    df_filtrado = df[df['PRODUCTO'].str.contains(search_query, case=False, na=False)] if search_query else df

    # Botón para limpiar cantidades
    if st.button("Limpiar cantidades de requerimientos"):
        for producto in st.session_state['quantities']:
            st.session_state['quantities'][producto] = 0

    # Editar cantidad
    if 'CANTIDAD' in df.columns:
        for index, row in df_filtrado.iterrows():
            cantidad_actual = st.session_state['quantities'][row['PRODUCTO']]
            unique_key = f"quantity_{index}_{row['PRODUCTO']}"
            new_quantity = st.number_input(f"{row['TIPO']} - {row['PRODUCTO']}", min_value=0, value=cantidad_actual, key=unique_key)
            st.session_state['quantities'][row['PRODUCTO']] = new_quantity

        st.markdown("---")
        st.subheader("Enviar Requerimientos por WhatsApp")
        fecha = st.date_input("Seleccione la fecha si es diferente de hoy", date.today())
        phone_number = st.text_input("Escribe el número de teléfono")
        if phone_number:
            message_lines = [f"{producto}: {cantidad}" for producto, cantidad in st.session_state['quantities'].items() if cantidad > 0]
            message = f"Los requerimientos para {fecha}:\n" + "\n".join(message_lines)
            encoded_message = quote(message)
            if st.button("Generar enlace para WhatsApp Web"):
                whatsapp_url = f"https://api.whatsapp.com/send?phone=+58{phone_number}&text={encoded_message}"
                st.markdown(f"[Enviar mensaje por WhatsApp]({whatsapp_url})")
    else:
        st.error("El archivo Excel no tiene una columna 'CANTIDAD'.")

if __name__ == "__main__":
    main()
