import streamlit as st
import pandas as pd
from urllib.parse import quote

def main():
    st.title("Requerimientos diario de compras")
    # leer un excel
    df = pd.read_excel("FORMATO_REQUERIMIENTOS.xlsx")


    # Editar cantidad
    if 'CANTIDAD' in df.columns:
        CONTEO = 0
        for index, row in df.iterrows():
            # Convertir el valor a entero si es flotante
            cantidad_actual = int(row['CANTIDAD']) if not pd.isnull(row['CANTIDAD']) else 0
            # Añadir una clave única a cada número de entrada utilizando el índice y el nombre del producto
            unique_key = f"quantity_{index}_{row['PRODUCTO']}_{CONTEO}"
            CONTEO += 1
            new_quantity = st.number_input(f"{row['TIPO']} - {row['PRODUCTO']}", min_value=0, value=cantidad_actual, key=unique_key)
            df.at[index, 'CANTIDAD'] = new_quantity

        #st.write("Datos actualizados:")
        #st.dataframe(df)
        st.divider()
        st.subheader("Enviar Requerimientos por WhatsApp")
        # Número de teléfono y mensaje
        fecha = st.date_input("Selecciones la  fecha si es diferente de hoy", "today")
        phone_number = st.text_input("Escribe el número de teléfono")
        if phone_number:
            # Filtrar las filas con cantidades mayores a 0
            df_filtrado = df[df['CANTIDAD'] > 0]
            message_lines = [f"{row['PRODUCTO']}: {row['CANTIDAD']}" for index, row in df_filtrado.iterrows()]
            message = f"Los requerimientos para {fecha}:\n" + "\n".join(message_lines)
            # Codificar el mensaje para la URL
            encoded_message = quote(message)

            if st.button("Generar enlace para WhatsApp Web"):
                # Crear enlace para WhatsApp Web
                whatsapp_url = f"https://api.whatsapp.com/send?phone=+58{phone_number}&text={encoded_message}"
                st.markdown(f"[Enviar mensaje por WhatsApp]({whatsapp_url})")

    else:
        st.error("El archivo Excel no tiene una columna 'CANTIDAD'.")

if __name__ == "__main__":
    main()
