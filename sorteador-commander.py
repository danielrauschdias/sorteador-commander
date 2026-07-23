import requests
import pandas as pd
import time
import random

#Link de acesso da API já com o filtro de cartas de comandantes do MTG:Arena
api_url = "https://api.scryfall.com/cards/search?q=game%3Aarena+t%3Alegendary+is%3Acommander"

#Cria o dicionário com os nomes dos jogadores
playersQuantity = int(input("Digite o número de jogadores: "))

playersNames = []

for i in range(0, playersQuantity):
   playersNames.append(input(f"Digite o nome do(a) {i+1}o(a) jogador(a): "))

playersDict = {}

for i in range(playersQuantity):
  playersDict[playersNames[i]] = ""

response = requests.get(api_url, headers={"Accept": "application/json;q=0.9,*/*;q=0.8"})

dfCards = pd.DataFrame(response.json()["data"])

columns_to_drop = []

for i in range(len(dfCards.columns)):
    if dfCards.columns[i] != "name":
        columns_to_drop.append(dfCards.columns[i])

dfCards.drop(columns=columns_to_drop, axis=1,inplace=True)

has_more_pages = response.json()["has_more"]

while has_more_pages:
  next_page = response.json()["next_page"]
  time.sleep(2)
  response = requests.get(next_page, headers={"Accept": "application/json;q=0.9,*/*;q=0.8"})
  dfTemp = pd.DataFrame(response.json()["data"])
  columns_to_drop = []
  for i in range(len(dfTemp.columns)):
      if dfTemp.columns[i] != "name":
           columns_to_drop.append(dfTemp.columns[i])
  dfTemp.drop(columns=columns_to_drop, axis=1, inplace=True)
  dfCards = pd.concat([dfCards, dfTemp], ignore_index=True)
  has_more_pages = response.json()["has_more"]

for i in range(playersQuantity):
  randomCardNumber = random.randint(0, len(dfCards) - 1)
  randomCardName = dfCards.iloc[randomCardNumber]["name"]
  playersDict[playersNames[i]] = randomCardName

print("Comandantes de cada jogador:")
for i in range(playersQuantity):
  print(f"{playersNames[i]}: {playersDict[playersNames[i]]}")
