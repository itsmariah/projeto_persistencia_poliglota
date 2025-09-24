import streamlit as st
import pandas as pd
import folium
import sqlite3
from streamlit_folium import st_folium
from geopy.distance import geodesic

from db_sqlite import criar_tabelas, inserir_cidade, listar_cidades
from db_mongo import inserir_local, listar_locais
from geoprocessamento import locais_proximos

# Criar tabelas no SQLite
criar_tabelas()

st.title("🌍 Projeto de Persistência Poliglota (SQLite + MongoDB)")

menu = st.sidebar.selectbox("Menu", ["Cadastrar Cidade", "Cadastrar Local", "Visualizar Locais", "Consulta Geográfica"])

# Cadastro de cidades (SQLite)
if menu == "Cadastrar Cidade":
    st.subheader("Cadastrar Cidade (SQLite)")
    nome = st.text_input("Nome da cidade")
    estado = st.text_input("Estado")
    pais = st.text_input("País")
    if st.button("Salvar Cidade"):
        inserir_cidade(nome, estado, pais)
        st.success("Cidade cadastrada com sucesso!")

    st.write("📋 Cidades cadastradas:")
    st.table(listar_cidades())

# Cadastro de locais (MongoDB)
elif menu == "Cadastrar Local":
    st.subheader("Cadastrar Local (MongoDB)")
    nome_local = st.text_input("Nome do local")
    cidade = st.text_input("Cidade")
    latitude = st.number_input("Latitude", format="%.6f")
    longitude = st.number_input("Longitude", format="%.6f")
    descricao = st.text_area("Descrição")

    if st.button("Salvar Local"):
        inserir_local(nome_local, cidade, latitude, longitude, descricao)
        st.success("Local cadastrado com sucesso!")

    st.write("📋 Locais cadastrados:")
    st.json(listar_locais())

# Visualizar locais em mapa
elif menu == "Visualizar Locais":
    st.subheader("Mapa de Locais")
    locais = listar_locais()
    if locais:
        mapa = folium.Map(location=[-15.78, -47.93], zoom_start=4)  # Brasil
        for local in locais:
            coords = (local["coordenadas"]["latitude"], local["coordenadas"]["longitude"])
            folium.Marker(coords, popup=local["nome_local"]).add_to(mapa)
        st_folium(mapa, width=700, height=500)
    else:
        st.warning("Nenhum local cadastrado.")

# Consulta geográfica (distância/raio)
elif menu == "Consulta Geográfica":
    st.subheader("Consulta por Raio de Distância")
    
    # Inputs do usuário
    lat_ref = st.number_input(
        "Latitude de referência", min_value=-90.0, max_value=90.0, format="%.6f", value=-7.1354
    )
    lon_ref = st.number_input(
        "Longitude de referência", min_value=-180.0, max_value=180.0, format="%.6f", value=-34.7906
    )
    raio = st.slider("Raio (km)", 1, 100, 10)

    # Corrigir vírgula caso o usuário use
    lat_ref = float(str(lat_ref).replace(",", "."))
    lon_ref = float(str(lon_ref).replace(",", "."))

    if st.button("Buscar Locais Próximos"):
        if lat_ref == 0 and lon_ref == 0:
            st.error("❌ Insira uma latitude e longitude de referência válidas!")
        else:
            locais = listar_locais()  # mock de teste (se quiser)
            proximos = []

            from geopy.distance import geodesic
            import folium
            from streamlit_folium import st_folium

            # Processar cada local
            for local in locais:
                lat = local["coordenadas"].get("latitude")
                lon = local["coordenadas"].get("longitude")

                # Tentar converter para float
                try:
                    lat = float(lat)
                    lon = float(lon)
                except (ValueError, TypeError):
                    continue  # ignora valores inválidos

                # Validar coordenadas
                if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                    continue

                # Calcular distância
                distancia = geodesic((lat_ref, lon_ref), (lat, lon)).km
                print(f"{local['nome_local']}: distância = {distancia:.2f} km")  # depuração

                if distancia <= raio:
                    local["distancia_km"] = round(distancia, 2)
                    proximos.append(local)

            st.write("📍 Locais encontrados:", proximos)

            if proximos:
                mapa = folium.Map(location=[lat_ref, lon_ref], zoom_start=12)
                folium.Marker(
                    [lat_ref, lon_ref],
                    popup="Ponto de referência",
                    icon=folium.Icon(color="red")
                ).add_to(mapa)

                for local in proximos:
                    coords = (local["coordenadas"]["latitude"], local["coordenadas"]["longitude"])
                    folium.Marker(
                        coords,
                        popup=f"{local['nome_local']} ({local['distancia_km']} km)"
                    ).add_to(mapa)

                st_folium(mapa, width=700, height=500)
                