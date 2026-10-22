import os
import requests
from dotenv import load_dotenv
from folium import Map, Marker, Icon

URL = "http://api.olhovivo.sptrans.com.br/v2.1"
CODIGO_LINHA = 2450
load_dotenv(".env")

s = requests.Session()
res = s.post(f"{URL}/Login/Autenticar?token={os.getenv('SPTRANS_TOKEN')}")
print("Autenticado:", res.text) 

res = s.get(f"{URL}/Parada/BuscarParadasPorLinha?codigoLinha={CODIGO_LINHA}")
paradas = res.json()
print("Total de paradas:", len(paradas))

pos = s.get(f"{URL}/Posicao/Linha?codigoLinha={CODIGO_LINHA}")
onibus = pos.json()["vs"]
print("Ônibus em circulação:", len(onibus))

if len(paradas) == 0:
    raise SystemExit("A linha não retornou paradas. Confira o token e o código da linha.")
if len(onibus) == 0:
    print("Aviso: nenhum ônibus circulando agora. O mapa terá só as paradas.")

m = Map(
    location=[paradas[0]["py"], paradas[0]["px"]],
    zoom_start=13,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    attr="Esri, HERE, Garmin, OpenStreetMap contributors",
)

for i in paradas:
    Marker(
        location=[i["py"], i["px"]],
        popup=i["np"],
        icon=Icon(color="blue", icon="info-sign"),
    ).add_to(m)

for i in onibus:
    Marker(
        location=[i["py"], i["px"]],
        popup=f"Ônibus {i['p']} - {i['ta']}",
        icon=Icon(color="red", icon="bus", prefix="fa"),
    ).add_to(m)

m.save("mapa_onibus.html")
print("Mapa salvo em mapa_onibus.html")
