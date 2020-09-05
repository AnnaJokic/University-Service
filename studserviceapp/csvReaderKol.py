import csv

import os
import codecs

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studservice.settings")
import django

django.setup()

from studserviceapp.models import *
from datetime import datetime


def unos_rasporeda(file, brKlk):

    # with open(file, encoding='utf-8') as csvfile:
    # raspored_csv = csv.reader(csvfile, delimiter=',')

    raspored_csv = csv.reader(codecs.iterdecode(file, 'utf-8'), delimiter=',')

    brojac = 0
    brojKlk=" "
    greske=[]
    cela=[]
    oba={}


    if brKlk == '1':
        brojKlk = "prva"

    elif brKlk == '2':
        brojKlk = "druga"

    elif brKlk == '3':
        brojKlk = "treca"

    elif brKlk == '4':
        brojKlk = "cetvrta"

    if not RasporedPolaganja.objects.filter(kolokvijumska_nedelja=brojKlk).exists():
        rasporedPolaganja = RasporedPolaganja(kolokvijumska_nedelja=brojKlk)
        rasporedPolaganja.save()

    rasporedPolaganja = RasporedPolaganja.objects.get(kolokvijumska_nedelja=brojKlk)

    nastavnik_ne_postoji = 1

    for red in raspored_csv:

        #oba.setdefault(brojac, [])


        if brojac == 0:

            brojac += 1

        else:

            brojac += 1

            predmet = red[0]
            profesor = red[3]
            ucionica = red[4]
            vreme = red[5].split('-')
            # dan = red[6]
            dan = red[7].split('.')[0]
            mesec = red[7].split('.')[1]
            datum = datetime.strptime(dan + ' ' + mesec + ' 2018', '%d %m %Y').date()

            provera_profesora = profesor.split()

            i = 0
            profesori = []

            if len(provera_profesora) == 2:
                ime = provera_profesora[0]
                prezime = provera_profesora[1]
                #print(ime + " " + prezime)
                if Nastavnik.objects.filter(ime=ime, prezime=prezime).exists():
                    nastavnik = Nastavnik.objects.get(ime=ime, prezime=prezime)
                    profesori.append(nastavnik)
                    nastavnik_ne_postoji = 1
                else:
                    nastavnik_ne_postoji = 0
                    #print("nastavni ne postoji ili mu ime/prezime nije lepo uneto" + " " + str(brojac))
                    greska = "nastavnik ne postoji ili mu ime/prezime nije lepo uneto" + " (linija broj " + str(brojac)+")"
                    greske.append(greska)
                    cela.append(red)

                    if brojac in oba:
                        oba[brojac].append(greska)
                    else:
                        oba[brojac] = [greska]

                    #oba[brojac].append(greska)
                    #oba[brojac] =  greska




            if len(provera_profesora) == 3:
                ime = provera_profesora[0]
                prezime = provera_profesora[1] + " " + provera_profesora[2]
                #print(ime + " " + prezime)
                if Nastavnik.objects.filter(ime=ime, prezime=prezime).exists():
                    nastavnik = Nastavnik.objects.get(ime=ime, prezime=prezime)
                    profesori.append(nastavnik)
                    nastavnik_ne_postoji = 1
                else:
                    nastavnik_ne_postoji = 0
                    #print("nastavni ne postoji ili mu ime/prezime nije lepo uneto" + " " + str(brojac))
                    greska = "nastavnik ne postoji ili mu ime/prezime nije lepo uneto" + " (linija broj " + str(brojac)+")"
                    greske.append(greska)
                    cela.append(red)
                    #oba[brojac]=greska
                    #oba[brojac].append(greska)

                    if brojac in oba:
                        oba[brojac].append(greska)
                    else:
                        oba[brojac] = [greska]



            if len(provera_profesora) > 3:

                if (len(provera_profesora) % 2 == 0):

                    while (i < len(provera_profesora)):

                        ime = provera_profesora[i]
                        prezime = provera_profesora[i + 1]
                        # profa = ime + " " + prezime
                        # profesori.append(profa)
                        # profesori.append(ime)
                        i += 2
                        #print(ime + " " + prezime)
                        if Nastavnik.objects.filter(ime=ime, prezime=prezime).exists():
                            nastavnik = Nastavnik.objects.get(ime=ime, prezime=prezime)
                            profesori.append(nastavnik)
                            nastavnik_ne_postoji = 1
                        else:
                            nastavnik_ne_postoji = 0
                            #print("nastavnik ne postoji ili mu ime/prezime nije lepo uneto" + " " + str(brojac))
                            greska = "nastavnik ne postoji ili mu ime/prezime nije lepo uneto" + " (linija broj " + str(brojac)+")"
                            greske.append(greska)
                            cela.append(red)
                            #oba[brojac] = greska
                            #oba[brojac].append(greska)

                            if brojac in oba:
                                oba[brojac].append(greska)
                            else:
                                oba[brojac] = [greska]




                else:
                    # hard
                    ime1 = provera_profesora[0]
                    prezime1 = provera_profesora[1]
                    ime2 = provera_profesora[2]
                    prezime2 = provera_profesora[3] + " " + provera_profesora[4]

                    if Nastavnik.objects.filter(ime=ime1, prezime=prezime1).exists():
                        nastavnik = Nastavnik.objects.get(ime=ime1, prezime=prezime1)
                        profesori.append(nastavnik)
                        nastavnik_ne_postoji = 1
                    else:
                        nastavnik_ne_postoji = 0
                        #print("nastavnik ne postoji ili mu ime/prezime nije lepo uneto" + " " + "(linija broj "+str(brojac)+")")
                        greska="nastavnik ne postoji ili mu ime/prezime nije lepo uneto" + " " + "(linija broj "+str(brojac)+")"
                        greske.append(greska)
                        cela.append(red)
                        #oba[brojac] = greska
                        #oba[brojac].append(greska)

                        if brojac in oba:
                            oba[brojac].append(greska)
                        else:
                            oba[brojac] = [greska]




                    if Nastavnik.objects.filter(ime=ime2, prezime=prezime2).exists():
                        nastavnik = Nastavnik.objects.get(ime=ime2, prezime=prezime2)
                        profesori.append(nastavnik)
                        nastavnik_ne_postoji = 1
                    else:
                        nastavnik_ne_postoji = 0
                        #print("nastavnik ne postoji ili mu ime/prezime nije lepo uneto" + " " + "(linija broj "+str(brojac)+")")
                        greska = "nastavnik ne postoji ili mu ime/prezime nije lepo uneto" + " " + "(linija broj " + str(brojac) + ")"
                        greske.append(greska)
                        cela.append(red)
                        #oba[brojac] = greska
                        #oba[brojac].append(greska)

                        if brojac in oba:
                            oba[brojac].append(greska)
                        else:
                            oba[brojac] = [greska]




                    #print(ime1 + " " + prezime1)
                    #print(ime2 + " " + prezime2)

            if not Predmet.objects.filter(naziv=predmet).exists():
                #print(predmet)

                #print("predmet ne postiji ili nije pravilno upisan (linija broj" + " " + str(brojac) + ")")
                #print(" ")
                greska ="predmet ne postiji ili nije pravilno upisan (linija broj" + " " + str(brojac) + ")"
                greske.append(greska)
                cela.append(red)
                #oba[brojac] = greska
                #oba[brojac].append(greska)

                if brojac in oba:
                    oba[brojac].append(greska)
                else:
                    oba[brojac] = [greska]


            else:

                if (nastavnik_ne_postoji):

                    pravi_predmet = Predmet.objects.get(naziv=predmet.strip())

                    # proevri koliko ima profesora ako ima samo jedan dodaj ga odmah i sacuvaj predmet, ako ima vise
                    # dodaj prvo jednog normalno sacuvaj predmet pa onda dodaj drugog

                    if (len(profesori) == 1):

                        if "." not in ucionica:

                            if not TerminPolaganja.objects.filter(ucionice=ucionica, pocetak=vreme[0] + ":00",
                                                                  zavrsetak=vreme[1] + ":00", datum=datum,
                                                                  raspored_polaganja=rasporedPolaganja,
                                                                  predmet=pravi_predmet).exists():
                                termin = TerminPolaganja(ucionice=ucionica, pocetak=vreme[0] + ":00",
                                                         zavrsetak=vreme[1] + ":00", datum=datum,
                                                         raspored_polaganja=rasporedPolaganja, predmet=pravi_predmet)
                                #print(predmet)
                                #print(nastavnik.ime)
                                #print(ucionica)
                                #print(vreme[0] + " " + vreme[1])
                                #print(datum)
                                #print(" ")
                                termin.save()

                                for p in profesori:
                                    termin.nastavnik.add(p)
                        else:
                            #print("oznake ucionica nisu pravilno unete, moraju biti razdvojene zarezom" + " (linija broj " + str(brojac)+")")
                            greska="oznake ucionica nisu pravilno unete, moraju biti razdvojene zarezom" + " (linija broj " + str(brojac)+")"
                            greske.append(greska)
                            cela.append(red)
                            #oba[brojac] = greska
                            #oba[brojac].append(greska)

                            if brojac in oba:
                                oba[brojac].append(greska)
                            else:
                                oba[brojac] = [greska]



                    else:

                        if "." not in ucionica:

                            if not TerminPolaganja.objects.filter(ucionice=ucionica, pocetak=vreme[0] + ":00",
                                                                  zavrsetak=vreme[1] + ":00", datum=datum,
                                                                  raspored_polaganja=rasporedPolaganja,
                                                                  predmet=pravi_predmet).exists():
                                termin = TerminPolaganja(ucionice=ucionica, pocetak=vreme[0] + ":00",
                                                         zavrsetak=vreme[1] + ":00", datum=datum,
                                                         raspored_polaganja=rasporedPolaganja, predmet=pravi_predmet)
                                #print(predmet)
                                #print(nastavnik.ime)
                                #print(ucionica)
                                #print(vreme[0] + " " + vreme[1])
                                #print(datum)
                                #print(" ")
                                termin.save()

                                for p in profesori:
                                    termin.nastavnik.add(p)

                        else:
                            #print("oznake ucionica nisu pravilno unete, moraju biti razdvojene zarezom" + " (linija broj " + str(brojac) + ")")
                            greska = "oznake ucionica nisu pravilno unete, moraju biti razdvojene zarezom" + " (linija broj " + str(brojac) + ")"
                            greske.append(greska)
                            cela.append(red)
                            #oba[brojac] = greska
                            #oba[brojac].append(greska)

                            if brojac in oba:
                                oba[brojac].append(greska)
                            else:
                                oba[brojac] = [greska]

                            #print(brojac)
                            #print(greska)



    return greske,cela,oba

# unos_rasporeda("kol1.csv", 2)
