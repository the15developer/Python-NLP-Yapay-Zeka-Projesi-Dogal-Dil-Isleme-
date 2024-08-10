# -*- coding: utf-8 -*-
"""
Created on 8.08.2024

@author: Dannya Chami
"""

from internet_arama_modulu_2 import *
from nlp_modulu import *
import sqlite3

    
def main():
    
    api_key = 'AIzaSyBXJrBvvGYBvPPWppf5LB2qK5DeIOjzRc8'
    search_engine_id = 'e631aed3d856b4358'
    text_searcher = TextSearcher(api_key, search_engine_id)

    #Veri tabanı mevcut ise bağlanılır, mevcut
    #değilse veri tabanı oluşturulur.

    baglan=sqlite3.connect('konular.db')
    imlec=baglan.cursor()

    try: 
        
        imlec.execute("CREATE TABLE IF NOT EXISTS konular(metin_no INTEGER PRIMARY KEY, genel_konu TEXT, alt_konu1 TEXT, alt_konu2 TEXT, alt_konu3 TEXT, alt_konu4 TEXT, alt_konu5 TEXT, alt_konu6 TEXT, alt_konu7 TEXT)")
        
        baglan.commit()
          
        response=0;
        enable=0;
        alt_konu=""
        genel_konular=[]
        sohbet=0
        metin_no=0
        global main_topic
      
        
        print("Hos geldiniz !")
        
        while(1):
            
            enable+=1
            
            if(enable>4):
                print("4 metin girdiniz. Yeni sohbet baslatiliyor :")
                sohbet+=1
                enable=1
                genel_konular=[]
                
            text = input('Lutfen bir metin giriniz :')
        
            
            main_topic=obtain_main_topic(text)
            alt_konular, main_topic=obtain_sub_topics(text)
            metin_no=enable+sohbet*4
            imlec.execute("INSERT INTO konular (metin_no, genel_konu, alt_konu1, alt_konu2, alt_konu3, alt_konu4, alt_konu5) VALUES(?, ?, ?, ?, ?, ?, ?)", (metin_no, main_topic, alt_konular[0], alt_konular[1], alt_konular[2], alt_konular[3], alt_konular[4] ))
            baglan.commit()
            genel_konular.append(main_topic)
          
            print("Metnin genel konusu:\n")
            
            print(main_topic)
            
            print('Metnin alt konulari :\n')
            print(alt_konular)
            
            if(enable<2):
                response=input("Simdi ne yapmak istiyorsunuz ? 1. `{}` hakkinda sonuclar getir (1)/ 2. bir alt konu hakkinda sonuclar getir (2) / 3. yeni bir metin gir (3) / 4. sohbetin genel konusu hakkinda bilgi getir - en az bir metin daha girmelisiniz (4)/ 5. programi bitir (exit) /".format(main_topic))
            else:
                response=input("Simdi ne yapmak istiyorsunuz ? 1. `{}` hakkinda sonuclar getir (1)/ 2. bir alt konu hakkinda sonuclar getir (2) / 3. yeni bir metin gir (3) / 4. sohbetin genel konusu hakkinda bilgi getir ({} tane metniniz var) (4)/ 5. programi bitir (exit) /".format(main_topic, enable))
            if(response=="1"):
                query=main_topic+" nedir"
                #search_show_text(query)
                text_searcher.search_show_text(query)
            elif(response=="2"):
                while(1):
                    print("Bilgi istediginiz alt konuyu seciniz :")
                    print(alt_konular)
                    alt_konu=input("Alt konu : ")
                    try:
                     index=alt_konular.index(alt_konu)
                     break
                    except ValueError:
                      print("Girdiginiz alt konu bulunamamistir !")
                  
                query=alt_konular[index]+" nedir"
                #search_show_text(query)
                text_searcher.search_show_text(query)
            elif(response=="3"):
                continue;
            elif(response=="4"):
                if(enable<2):
                    print("sohbetin genel konusu hakkinda bilgi getirmek icin en az bir metin daha girmelisiniz ! " )
                    continue
                else:
                    sohbet_konusu=sohbet_genel_konu(genel_konular)
                    print("Sohbetinizin genel konusu : {}", sohbet_konusu)
                    query=sohbet_konusu
                    #search_show_text(query)
                    text_searcher.search_show_text(query)
                    
                
                    
                   
                
            else:
                print("Gorusmek uzere !")
                imlec.execute('DELETE FROM konular')
                baglan.commit()
                baglan.close()
                break;
    except Exception as e:
            print(e)
            imlec.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='konular'")
            tablo_var_mi = (imlec.fetchone() is not None)
            if tablo_var_mi == True:
                 imlec.execute('DELETE FROM konular')
                 baglan.commit()
                 print("Hatadan dolayi program kapatiliyor (veri tabani sifirlandi)")
            else:
                print("Hatadan dolayi program kapatiliyor")
            baglan.close()



if __name__ == "__main__":
    
    main()
    
    
    
    
    
    
    
    
    
    