import json
import requests


# usar self.all_champs si no es nulo, y si lo es obtener la info y setearlo
# lo mismo con free champs
class LolApi:
    def __init__(self):
        self.all_champs = []
        self.free_champs = []

    
    def get_champs_by_ids(self, id_list):
        result = []
        for c_id in id_list:
            for champ in self.all_champs:
                if self.all_champs[champ] == str(c_id):
                    result.append(champ)
        return result

    def get_all_champions(self):
        # cambiar a la ultima version de lol, actual 12.4.1
        # https://ddragon.leagueoflegends.com/cdn/12.4.1/data/en_US/champion.json
        all_champs = {}

        try:
            file = open("all_champions.json", "r", encoding="UTF-8")
            data = json.loads(file.read())
            file.close()

            for item in data["data"]:
                champ_name = data["data"][item]["name"]
                champ_id = data["data"][item]["key"]
                all_champs[champ_name] = champ_id
        except Exception as e:
            print(e)
        return all_champs

    def get_free_champions(self):
        champs = None
        try:
            response = requests.get(
                "https://la2.api.riotgames.com/lol/platform/v3/champion-rotations?api_key=RGAPI-97424029-1583-40c7-a708-dcc686fb5845")
            champs = json.loads(response.text)["freeChampionIds"]
        except Exception as e:
            print(e)
        return champs