from bs4 import BeautifulSoup
import requests

url = "https://play.google.com/store/books/details/Tere_Liye_PULANG_unedited_version?id=qQVnDwAAQBAJ"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

prices = doc.find_all(text="IDR")
parent = prices[0].parent
print(prices)