# Python-NLP-Yapay-Zeka-Projesi-Dogal-Dil-Isleme-

EN:

This Python project is designed to analyze Turkish texts using advanced Natural Language Processing (NLP) techniques and retrieve relevant information from the internet via Google searches. The project handles a text input from the user, identifying the main topic and subtopics within the text. After processing, the user is prompted to choose the next action: search for more information about the main topic, select a subtopic to explore, or input a new text. Once at least two texts have been analyzed, the project can also perform a search based on the overall discussion topic.

A key feature of this project is its focus on the Turkish language, which presents unique challenges compared to English. Turkish is an agglutinative language ("sondan eklemeli dil"), where words are formed by adding suffixes to a root. This structure increases the complexity of text analysis. Additionally, there are fewer libraries available for Turkish NLP, making the task of accurately identifying and processing topics more difficult :

Complex Word Formation: In Turkish, words are formed by adding multiple suffixes to a root word. This can lead to a vast number of word forms from a single root, making it difficult for NLP models to recognize and process them. For example, the root word "ev" (house) can have many variations like "evde" (in the house), "evden" (from the house), "evler" (houses), etc.

Ambiguity: The extensive use of suffixes can create ambiguities that are difficult for NLP algorithms to resolve. The same word form might be interpreted differently based on its context. For example, "gidiyorum" can mean "I am going" or "I am leaving," depending on the context.

Morphological Complexity: Turkish words often carry multiple pieces of grammatical information within a single word due to the suffixes. This can include tense, person, number, possession, and more, all within one word. NLP tools must accurately parse this information to understand the meaning of the text.

Limited Resources: Compared to English, there are fewer NLP libraries and tools tailored specifically for Turkish, which means less support for developers working on Turkish text analysis. This lack of resources can lead to increased development time and the need for custom solutions.

These factors contribute to the complexity of processing Turkish text, making it more challenging than working with languages like English, where word forms are typically simpler and more resources are available.

Despite these challenges, the project effectively parses and analyzes Turkish text, storing all identified topics and subtopics in an SQLite3 database for easy retrieval and further analysis.
The project demonstrates how to integrate NLP with real-time web searches, offering an interactive and dynamic approach to understanding and expanding on textual content.



TR:

Bu proje, gelişmiş Doğal Dil İşleme (NLP) tekniklerini kullanarak Türkçe metinleri analiz etmek ve Google aramaları aracılığıyla internetten ilgili bilgileri getirmek için tasarlanmıştır. Proje, kullanıcıdan gelen bir metin girişini ele alarak metindeki ana konuyu ve alt konuları belirler. İşlemden sonra, kullanıcıdan bir sonraki eylemi seçmesi istenir: ana konu hakkında daha fazla bilgi arama, keşfetmek için bir alt konu seçme veya yeni bir metin girme. En az iki metin analiz edildikten sonra, proje genel sohbet konusuna göre bir arama da gerçekleştirebilir.

Bu projenin temel bir özelliği, İngilizceye kıyasla benzersiz zorluklar sunan Türkçe diline odaklanmasıdır. Türkçe, kelimelerin bir köke ekler eklenerek oluşturulduğu, sondan eklemeli bir dildir. Bu yapı, metin analizinin karmaşıklığını artırır. Ek olarak, Türkçe NLP için daha az kütüphane mevcuttur ve bu da konuları doğru bir şekilde belirleme ve işleme görevini daha zor hale getirir :

Karmaşık Sözcük Oluşumu: Türkçede, sözcükler bir kök sözcüğe birden fazla ek eklenerek oluşturulur. Bu, tek bir kökten çok sayıda sözcük biçimine yol açabilir ve NLP modellerinin bunları tanımasını ve işlemesini zorlaştırır. Örneğin, "ev" kök sözcüğü "evde", "evden", "evlerindekiler", "evlendiğin" gibi birçok varyasyona sahip olabilir.

Belirsizlik: Eklerin yaygın kullanımı, NLP algoritmalarının çözmesi zor olan belirsizlikler yaratabilir. Aynı sözcük biçimi, bağlamına göre farklı şekilde yorumlanabilir. Örneğin, "gidiyorum" bağlama bağlı olarak "gidiyorum" veya "ayrılıyorum" anlamına gelebilir.

Morfolojik Karmaşıklık: Türkçe sözcükler, ekler nedeniyle genellikle tek bir sözcük içinde birden fazla dil bilgisi bilgisi taşır. Bunlara zaman, kişi, sayı, sahiplik ve daha fazlası dahil olabilir ve hepsi tek bir sözcük içindedir. NLP araçları, metnin anlamını anlamak için bu bilgileri doğru bir şekilde ayrıştırmalıdır.

Sınırlı Kaynaklar: İngilizce ile karşılaştırıldığında, Türkçe için özel olarak tasarlanmış daha az NLP kütüphanesi ve aracı vardır, bu da Türkçe metin analizi üzerinde çalışan geliştiriciler için daha az destek anlamına gelir. Bu kaynak eksikliği, geliştirme süresinin artmasına ve özel çözümlere ihtiyaç duyulmasına yol açabilir.

Bu zorluklara rağmen, proje Türkçe metinleri etkili bir şekilde ayrıştırır ve analiz eder, tüm tanımlanmış konuları ve alt konuları kolay erişim ve daha fazla analiz için bir SQLite3 veritabanında depolar.

Proje, NLP'nin gerçek zamanlı web aramalarıyla nasıl entegre edileceğini göstererek, metinsel içeriği anlamak ve genişletmek için etkileşimli ve dinamik bir yaklaşım sunar.

RO:

Acest proiect Python este conceput pentru a analiza textele in limba turca folosind tehnici avansate de procesare a limbajului natural (NLP) și pentru a prelua informații relevante de pe internet prin căutări Google. Proiectul analizează textul introdus de catre utilizator, identificând subiectul principal și subiectele secundare. După procesare, utilizatorului i se solicită să aleagă următoarea acțiune: să caute mai multe informații despre subiectul principal, să selecteze un subiect secundar de explorat sau să introducă un text nou. Odată ce au fost analizate cel puțin două texte, proiectul poate efectua și o căutare bazată pe tema generală de discuție.

O caracteristică cheie a acestui proiect este concentrarea pe limba turcă, care prezintă provocări unice în comparație cu engleza. Turca este o limbă aglutinantă („sondan eklemeli dil”), în care cuvintele sunt formate prin adăugarea de sufixe la o rădăcină. Această structură crește complexitatea analizei textului. În plus, există mai puține librarii disponibile pentru NLP in limba turca, ceea ce face ca sarcina identificării și procesării cu precizie a subiectelor să fie mai dificilă:

Formarea complexă a cuvintelor: în turcă, cuvintele sunt formate prin adăugarea mai multor sufixe la un cuvânt rădăcină. Acest lucru poate duce la un număr mare de forme de cuvinte dintr-o singură rădăcină, ceea ce face dificil pentru modelele NLP să le recunoască și să le proceseze. De exemplu, cuvântul rădăcină „ev” (casă) poate avea multe variații precum „evde” (în casă), „evden” (din casă), „evler” (case), etc.

Ambiguitate: Utilizarea extensivă a sufixelor poate crea ambiguități care sunt dificil de rezolvat de către algoritmii NLP. Aceeași formă de cuvânt poate fi interpretată diferit în funcție de context. De exemplu, „gidiyorum” poate însemna „merg” sau „plec”, în funcție de context.

Complexitate morfologică: Cuvintele turcești poartă adesea mai multe informații gramaticale într-un singur cuvânt datorită sufixelor. Aceasta poate include timp, persoană, număr, posesie și multe altele, toate într-un singur cuvânt. Instrumentele NLP trebuie să analizeze cu acuratețe aceste informații pentru a înțelege sensul textului.

Resurse limitate: în comparație cu limba engleză, există mai puține librarii și instrumente NLP adaptate special pentru limba turcă, ceea ce înseamnă mai puțin suport pentru dezvoltatorii care lucrează la analiza textului în limba turcă. Această lipsă de resurse poate duce la creșterea timpului de dezvoltare și la nevoia de soluții personalizate.

Acești factori contribuie la complexitatea procesării textului in turca, făcându-l mai dificil decât lucrul cu limbi precum engleza, unde formele de cuvinte sunt de obicei mai simple și sunt disponibile mai multe resurse.

În ciuda acestor provocări, proiectul analizează și analizează în mod eficient textul in limba turca, stocând toate subiectele principale și secundare identificate într-o bază de date SQLite3 pentru o regăsire ușoară și o analiză ulterioară.
Proiectul demonstrează cum NLP se poate integra cu căutările web în timp real, oferind o abordare interactivă și dinamică pentru înțelegerea și extinderea conținutului textual.


