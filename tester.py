def create_test_cases():
    senders = ["matti.meikalainen@gmail.com", "otto.opiskelija@student.oulu.fi", "paju-admin@oulu.fi", "ict-tiedote@oulu.fi", "maija.meikalainen@student.oulu.fi", "tero.teekkari@oulu.fi", "megahacker@hotmail.com", "superhacker@gmail.com", "scam.phisher@gmail.com", "hackerman@gmail.com"]
    subjects = ["tietoturvakurssi", "loppukoe", "kurssien aloitus", "sitsit perjantaina", "password change", "ICT services are down", "free trip to germany", "claim your posti","you have been pwned change your password", "free iphone"]
    bodies = ["tietoturvakurssin aloitusluento on ensi viikon tiistaina", "biosignaalien käsittely 1 kurssin loppukoe on examinarium tenttinä 14.12-15.12", "get your free iphone here now fast!!!!!!!!!!!" "change your password here as soon as possible  linkki  ", "ict services are down starting 16.00 on 15.12", "change you password here now!!!!!!  linkki * ", "redeem your free trip to germany here  linkki  ", "claim your package here  link ", "uudet kurssit alkavat 10.1.2022", "sitsit perjantaina 10.12 kello 18.00 alkaen", "jotain dataaaaaa"]
    links = [[],[],[],[],[],[],[],[],[],[]]
    ids = [1,2,3,4,5,6,7,8,9,10]
    attachments = [[],[],[],["image.jpg"],[],[],["file.pdf"],["virus2.exe"],["virus.exe"],["maliciousfile.docx"]]
    return senders, subjects, bodies, links, ids, attachments
