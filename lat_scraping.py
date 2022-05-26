from itertools import tee
from typing import Text
import requests

from pymongo import MongoClient
import pymongo

import requests
from bs4 import BeautifulSoup


def get_dbconnection():
    myclient = pymongo.MongoClient('mongodb://localhost:27017/') #link mongoDB, note: koneksikan terlebih dahulu
    mydb = myclient['latscrapdb'] #gantinama database kalian, kalau belum ada/belum buat bisa langsung dibuat disini contoh => mydb = myclient['databaseku']

    mycol = mydb['buku'] #nama collection atau table, kalau belum ada lakukan sama seperti sebelumnya
    
    return mycol

# bookinfo = {
#     'Judul':'Lapis lapis keberkahan',
#     'Publisher':'Pro U Media'
# }


# print(var_in.inserted_id)
def save_data(masukin):
    mycol = get_dbconnection()
    var_in = mycol.insert_one(masukin)
    return var_in
    
    
    
def print_data(mycol):
    #mycol = get_dbconnection
    for x in mycol.find():
        print(x)

def scrap_googlebook(url):
    global book_info
    urlnya = url
    page = requests.get(urlnya)
    soup = BeautifulSoup(page.text, 'html.parser')

    tag_judul = soup.select('h1[itemprop="name"] span')
    judul = tag_judul[0].getText()

    tag_penulis = soup.select('a[class="hrTbp R8zArc"]')
    penulis = tag_penulis[0].getText()
    
    # tag_genre = soup.select('span[class="htlgb"] html-blob')
    # genre = tag_genre[0].getText()

    tag_desc = soup.select('span[jsslot=""]')
    desc = tag_desc[0].getText()

    tag_cover = soup.find('img', 'T75of h1kAub')
    cover = tag_cover['src']
    
    halaman = soup.find("div", string='Pages').find_next_sibling().text
    pub_date = ''
    try:
        pub_date = soup.find("div", string='Published on').find_next_sibling().text
        #print(pub_date)
    except AttributeError:
        print("Tanggal terbit tidak ditemukan")
    
    penerbit = soup.find("div", string='Publisher').find_next_sibling().text
    
    bahasa = soup.find("div", string='Language').find_next_sibling().text
    
    kompability = soup.find("div", string='Best for').find_next_sibling().text
    
    genre = soup.find("div", string='Genres').find_next_sibling().text
    
    harga_1 = soup.select('button[class="LkLjZd ScJHi HPiPcc IfEcue"]  meta[itemprop="price"]')[0]['content'].replace('$','')
    harga_2 = float(harga_1) * 14266.00
    harga_final = 'Rp ' + "{:,}".format(int(harga_2)) + ',00'
    # harga_2 = re.sub('[^0-9.]','',harga_1)
    # harga_3 = int(float(harga_2))
    # print(harga_final)
    # print(type(harga_3))
    
    #halaman_value = induk_more_info.find('div', string="Pages").parent.find(class_="IQ1z0d").text
    
    # induk_more_info = soup.findAll("div", {"class":"BgcNfc"})
    tag_rating = soup.select('div[class="BHMmbe"]')
    rating = tag_rating[0].getText()

    tag_jumlah_rating = soup.select('span[class="EymY4b"] span')
    jumlah_rating = tag_jumlah_rating[1].getText()
    

    book_info = {
        'Cover':cover,
        'Judul':judul,
        'Penulis':penulis,
        'Deskripsi':desc,
        'Penerbit':penerbit,
        'Tanggal Terbit':pub_date,
        'Bahasa':bahasa,
        'Halaman':halaman,
        'Baik Untuk':kompability,
        'Genre':genre,
        'Harga':harga_final,
        'Rating':rating,
        'Jumlah Rating':jumlah_rating
    }
    # print(book_info)
    return book_info

def main():
    alamat = input('Masukan URL buku: ')
    scrap_googlebook(alamat)
    save_data(book_info)
    mycol = get_dbconnection()
    print_data(mycol)

if __name__ == '__main__':
    main()

