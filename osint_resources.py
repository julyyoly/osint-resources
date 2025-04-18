import streamlit as st
import json

def get_data(ruta_fichero):
    """Carga datos JSON desde un fichero."""
    try:
        with open(ruta_fichero, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Error: El fichero '{ruta_fichero}' no fue encontrado.")
        return {}
    except json.JSONDecodeError:
        st.error(f"Error: El fichero '{ruta_fichero}' no contiene un JSON válido.")
        return {}

def filtrar_data(data, opciones_seleccionadas, filtro_por):
    """Filtra los datos según las opciones seleccionadas en el filtro especificado."""
    if not opciones_seleccionadas:
        return data  # Si no se selecciona nada, devuelve todos los datos

    resultados_filtrados = {}
    for registro_nombre, registro_data in data.items():
        if filtro_por in registro_data:
            # Comprueba si al menos una de las opciones seleccionadas está presente en el filtro especificado
            if any(opcion in registro_data[filtro_por] for opcion in opciones_seleccionadas):
                resultados_filtrados[registro_nombre] = registro_data
    return resultados_filtrados

def filtrar_por_categoria(data, categorias_seleccionadas):
    """Filtra los datos según las categorías seleccionadas."""
    if not categorias_seleccionadas:
        return data  # Si no se selecciona nada, devuelve todos los datos

    resultados_filtrados = {}
    for registro_nombre, registro_data in data.items():
        if "categoria" in registro_data:
            # Comprueba si al menos una de las categorías seleccionadas está presente
            if registro_data["categoria"] in categorias_seleccionadas:
                resultados_filtrados[registro_nombre] = registro_data
    return resultados_filtrados

st.title("OSINT resources")

ruta_del_fichero = "data/osintToolsData.json"
data_completa = get_data(ruta_del_fichero)

if data_completa:
    # Selector para elegir el tipo de filtro en horizontal
    filtro_por = st.radio(
        "Selecciona el tipo de filtro:",
        options=["input", "categoria"],
        index=0,
        horizontal=True  # Coloca el selector en horizontal
    )

    if filtro_por == "categoria":
        opciones_seleccionadas = st.multiselect(
            "Filtrar por categoría:",
            sorted({registro.get("categoria", "No disponible") for registro in data_completa.values()}),
        )
        data_filtrada = filtrar_por_categoria(data_completa, opciones_seleccionadas)
    else:
        opciones_seleccionadas = st.multiselect(
            "Filtrar por input:",
            sorted({valor for registro in data_completa.values() if "input_types" in registro for valor in registro["input_types"]}),
        )
        data_filtrada = filtrar_data(data_completa, opciones_seleccionadas, "input_types")

    if not isinstance(data_filtrada, dict):
        st.error("Error: Los datos filtrados no son un diccionario.")
    elif not data_filtrada:
        st.info("No se encontraron herramientas que coincidan con los filtros seleccionados.")
    else:
        st.subheader("Herramientas encontradas:")
        st.write(f"Número de resultados mostrados: **{len(data_filtrada)}**")
        for registro_nombre, registro_data in data_filtrada.items():
            with st.expander(f"**{registro_nombre}**", expanded=True):
                st.write(f"**Descripción:** {registro_data.get('descripcion', 'No disponible')}")
                st.write(f"**URL:** {registro_data.get('url', 'No disponible')}")
                st.write(f"**Categoría:** {registro_data.get('categoria', 'No disponible')}")

                if "input_types" in registro_data and registro_data["input_types"]:
                    st.write(f"**Input Types:** {', '.join(registro_data['input_types'])}")
                else:
                    st.write("No disponible")

                if "output_types" in registro_data and registro_data["output_types"]:
                    st.markdown(f"**Output Types:** {', '.join(registro_data['output_types'])}")
                else:
                    st.write("No disponible")
else:
    st.error("No se pudieron cargar los datos JSON.")