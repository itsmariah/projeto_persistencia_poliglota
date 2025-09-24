from geopy.distance import geodesic

def calcular_distancia(coord1, coord2):
    """
    Recebe duas coordenadas no formato (lat, lon) e retorna a distância em km.
    """
    return geodesic(coord1, coord2).km

def locais_proximos(lista_locais, ponto_referencia, raio_km=10):
    """
    Retorna os locais dentro de um raio em km a partir de um ponto de referência.
    lista_locais deve ser uma lista de dicionários com { 'coordenadas': {lat, lon} }
    """
    proximos = []
    for local in lista_locais:
        lat = local["coordenadas"]["latitude"]
        lon = local["coordenadas"]["longitude"]
        distancia = calcular_distancia(ponto_referencia, (lat, lon))
        if distancia <= raio_km:
            local["distancia_km"] = round(distancia, 2)
            proximos.append(local)
    return proximos
