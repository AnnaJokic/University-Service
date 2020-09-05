import csv

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studservice.settings")
import django

django.setup()

from studserviceapp.models import Grupa, Termin, RasporedNastave, Predmet, Nastavnik, Nalog, Semestar


#3. STAVKA U SPECIFIKACIJI, ova metoda se koristi kada popunjavamo bazu
def napraviUsernameNaloga(imeiprezime):

    ime_prezime = imeiprezime.split()
    username = ''


    if len(ime_prezime) > 2:
        username = ime_prezime[2][0] + ime_prezime[0] + ime_prezime[1]
    else:
        username = ime_prezime[1][0] + ime_prezime[0]

    return  username.lower()



with open ("rasporedCSV.csv", encoding='utf-8') as csvfile:

    raspored_csv = csv.reader(csvfile, delimiter = ';')
    brojac = 0

    if len(RasporedNastave.objects.all()) == 0:
        glavniRasporedNastave = RasporedNastave(semestar=Semestar.objects.get(id=1))
        glavniRasporedNastave.save()

    for red in raspored_csv:
        if not red:
            continue
        else:
            if brojac == 0:
                brojac += 1;
                continue
            elif brojac == 1:
                indeksPredavanja = red.index("Predavanja")
                indeksPraktikuma = red.index("Praktikum")
                indeksPredavanjaIPraktikuma = red.index("Predavanja i vezbe")
                indeksVezbi = red.index("Vezbe")
                brojac += 1;
            else:
               # red sa podacima sta raditi sa njima?
                if red[1] == "Nastavnik(ci)":
                    #print("ovo mi ne treba valjda")
                    continue
                if red[0]!='':
                    naziv_predmeta = red[0]
                    trenutni_predmet = red[0]
                    predmet = Predmet(naziv=naziv_predmeta)
                    if not Predmet.objects.filter(naziv=naziv_predmeta).exists():
                        predmet.save()
                    print(red[0])
                else:
##########################################################################################################
                    if red[indeksPredavanja]!='':
                        #print(red[indeksPredavanja])
                        # print(red[indeksPredavanja+2])
                        ime_prezime_nastavnika = red[indeksPredavanja].split()
                        if len(ime_prezime_nastavnika)>2:
                            ime_natsavnika = ime_prezime_nastavnika[2]
                            prezime_nastavnika = ime_prezime_nastavnika[0]+ " "+ ime_prezime_nastavnika[1]
                        else:
                            ime_nastavnika = ime_prezime_nastavnika[1]
                            prezime_nastavnika = ime_prezime_nastavnika[0]

                        username = napraviUsernameNaloga(red[indeksPredavanja])
                        nalog = Nalog(username=username, uloga="Nastavnik")

                        if not Nalog.objects.filter(username=username).exists():
                            nalog.save()
                            nastavnik = Nastavnik(ime=ime_nastavnika, prezime=prezime_nastavnika, nalog=nalog,nalog_id=nalog.id)
                            predmet_za_nastavnika = Predmet.objects.get(naziv = trenutni_predmet)
                            if not Nastavnik.objects.filter(nalog=nalog).exists():
                                nastavnik.save()
                                nastavnik.predmet.add(predmet_za_nastavnika)
                                nastavnik_za_termin = Nastavnik.objects.get(nalog_id=nalog.id)
                                predmet_za_termin = Predmet.objects.get(naziv=trenutni_predmet)
                                oznaka_ucionice = red[indeksPredavanja + 6]
                                vreme = red[indeksPredavanja + 5].split('-')
                                pocetak = vreme[0]
                                kraj = vreme[1] + ":00"
                                dan = red[indeksPredavanja + 4]
                                tip_nastave = "Predavanje"
                                print("1 nastavnik_za_termin.ime =" + nastavnik_za_termin.ime)
                                print("1 predmet_za_termin =" + predmet_za_termin.naziv)
                                print("1 oznaka_ucionice =" + oznaka_ucionice)
                                print("1 vreme_za_termin =" + red[indeksPredavanja + 5])
                                raspored = raspored = RasporedNastave.objects.get(id=1)
                                termin = Termin(oznaka_ucionice=oznaka_ucionice, pocetak=pocetak, zavrsetak=kraj,
                                                dan=dan, tip_nastave=tip_nastave,
                                                nastavnik=nastavnik_za_termin, predmet=predmet_za_termin,
                                                raspored=RasporedNastave.objects.get(id=1))
                                termin.save()
                                grupe = red[indeksPredavanja + 2].split(', ')
                                for a in grupe:
                                    grupa = Grupa(oznaka_grupe=a, semestar=Semestar.objects.get(id=1))
                                    if not Grupa.objects.filter(oznaka_grupe=a).exists():
                                        grupa.save()
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)
                                    else:
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)

                        else:
                            nalog2 = Nalog.objects.get(username=username)
                            nastavnik2 = Nastavnik.objects.get(nalog_id=nalog2.id)
                            premdet2 = Predmet.objects.get(naziv=trenutni_predmet)
                            nastavnik2.predmet.add(premdet2)
                            vreme = red[indeksPredavanja + 5].split('-')
                            tip_nastave = "Predavanja"
                            termin = Termin(oznaka_ucionice=red[indeksPredavanja + 6], pocetak=vreme[0],
                                           zavrsetak=vreme[1] + ":00", dan=red[indeksPredavanja + 4],tip_nastave=tip_nastave,
                                          nastavnik=nastavnik2, predmet=premdet2,
                                         raspored=RasporedNastave.objects.get(id=1))

                            if not Termin.objects.filter(oznaka_ucionice=red[indeksPredavanja + 6],
                                    pocetak=vreme[0],zavrsetak=vreme[1] + ":00",dan=red[indeksPredavanja + 4],
                                tip_nastave=tip_nastave,nastavnik=nastavnik2,
                                predmet=premdet2).exists():
                                print("PRVI")
                                termin.save()

                                grupe2 = red[indeksPredavanja + 2].split(', ')
                                print("11 nastavnik_za_termin.ime =" + nastavnik2.ime)
                                print("11 predmet_za_termin =" + premdet2.naziv)
                                print("11 oznaka_ucionice =" + red[indeksPredavanja + 6])
                                print("11 vreme_za_termin =" + red[indeksPredavanja + 5])
                                for a in grupe2:
                                    grupa = Grupa(oznaka_grupe=a, semestar=Semestar.objects.get(id=1))
                                    if not Grupa.objects.filter(oznaka_grupe=a).exists():
                                        grupa.save()
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)
                                    else:
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)


##########################################################################################################
                    if red[indeksPraktikuma]!='':
                        #print(red[indeksPraktikuma])
                        #print(red[indeksPraktikuma+2])
                        ime_prezime_nastavnika = red[indeksPraktikuma].split()
                        if len(ime_prezime_nastavnika)>2:
                            ime_natsavnika = ime_prezime_nastavnika[2]
                            prezime_nastavnika = ime_prezime_nastavnika[0] + " " + ime_prezime_nastavnika[1]
                        else:
                            ime_nastavnika = ime_prezime_nastavnika[1]
                            prezime_nastavnika = ime_prezime_nastavnika[0]

                        username = napraviUsernameNaloga(red[indeksPraktikuma])


                        nalog = Nalog(username=username, uloga="Nastavnik")
                        if not Nalog.objects.filter(username=username).exists():
                           nalog.save()
                           nastavnik = Nastavnik(ime=ime_nastavnika, prezime=prezime_nastavnika, nalog=nalog,nalog_id=nalog.id)
                           predmet_za_nastavnika = Predmet.objects.get(naziv=trenutni_predmet)
                           if not Nastavnik.objects.filter(nalog=nalog).exists():
                               nastavnik.save()
                               nastavnik.predmet.add(predmet_za_nastavnika)
                               nastavnik_za_termin = Nastavnik.objects.get(nalog_id=nalog.id)
                               nastavnik.predmet.add(predmet_za_nastavnika)
                               predmet_za_termin = Predmet.objects.get(naziv=trenutni_predmet)
                               oznaka_ucionice = red[indeksPraktikuma + 6]
                               vreme = red[indeksPraktikuma + 5].split('-')
                               pocetak = vreme[0]
                               kraj = vreme[1] + ":00"
                               dan = red[indeksPraktikuma + 4]
                               tip_nastave = "Praktikum"
                               print("2 nastavnik_za_termin.ime =" + nastavnik_za_termin.ime)
                               print("2 predmet_za_termin =" + predmet_za_termin.naziv)
                               print("2 oznaka_ucionice =" + oznaka_ucionice)
                               print("2 vreme_za_termin =" + red[indeksPredavanja + 5])
                               raspored = raspored = RasporedNastave.objects.get(id=1)
                               termin = Termin(oznaka_ucionice=oznaka_ucionice, pocetak=pocetak, zavrsetak=kraj,
                                               dan=dan, tip_nastave=tip_nastave,
                                               nastavnik=nastavnik_za_termin, predmet=predmet_za_termin,
                                               raspored=RasporedNastave.objects.get(id=1))
                               termin.save()

                               #else znaci da taj nastavnik vec postoji samo njegovim predmetima dodaj trenutni predmet

                               grupe = red[indeksPraktikuma + 2].split(', ')
                               for a in grupe:
                                    grupa = Grupa(oznaka_grupe=a, semestar=Semestar.objects.get(id=1))
                                    if not Grupa.objects.filter(oznaka_grupe=a).exists():
                                        grupa.save()
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)
                                    else:
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)

                        else:
                            nalog2 = Nalog.objects.get(username = username)
                            nastavnik2 = Nastavnik.objects.get(nalog_id = nalog2.id)
                            premdet2 = Predmet.objects.get(naziv = trenutni_predmet)
                            nastavnik2.predmet.add(premdet2)
                            vreme = red[indeksPraktikuma+5].split('-')
                            tip_nastave = "Praktikum"
                            termin = Termin(oznaka_ucionice= red[indeksPraktikuma+6], pocetak= vreme[0], zavrsetak = vreme[1]+":00",
                                            dan = red[indeksPraktikuma+4],tip_nastave=tip_nastave,
                                            nastavnik = nastavnik2, predmet = premdet2, raspored = RasporedNastave.objects.get(id=1))


                            if not Termin.objects.filter(oznaka_ucionice=red[indeksPraktikuma + 6],pocetak=vreme[0],
                                    zavrsetak=vreme[1] + ":00",dan=red[indeksPraktikuma + 4],
                                tip_nastave=tip_nastave,nastavnik=nastavnik2,
                                predmet=premdet2).exists():
                                print("DRUGI")

                                termin.save()
                                grupe2 = red[indeksPraktikuma+2].split(', ')
                                print("22 nastavnik_za_termin.ime =" + nastavnik2.ime)
                                print("22 predmet_za_termin =" + premdet2.naziv)
                                print("22 oznaka_ucionice =" + red[indeksPraktikuma+6])
                                print("22 vreme_za_termin =" + red[indeksPraktikuma + 5])
                                for a in grupe2:
                                    grupa = Grupa(oznaka_grupe=a, semestar=Semestar.objects.get(id=1))
                                    if not Grupa.objects.filter(oznaka_grupe=a).exists():
                                        grupa.save()
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)
                                    else:
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)

##########################################################################################################
                    if red[indeksVezbi]!='':
                        #print(red[indeksVezbi])
                        #print(red[indeksVezbi+2])

                        ime_prezime_nastavnika = red[indeksVezbi].split()

                        if len(ime_prezime_nastavnika) > 2:
                            ime_natsavnika = ime_prezime_nastavnika[2]
                            prezime_nastavnika = ime_prezime_nastavnika[0] + " " + ime_prezime_nastavnika[1]
                        else:
                            ime_nastavnika = ime_prezime_nastavnika[1]
                            prezime_nastavnika = ime_prezime_nastavnika[0]

                        username = napraviUsernameNaloga(red[indeksVezbi])

                        nalog = Nalog(username=username, uloga="Nastavnik")
                        if not Nalog.objects.filter(username=username).exists():
                            nalog.save()
                            nastavnik = Nastavnik(ime=ime_nastavnika, prezime=prezime_nastavnika, nalog=nalog,nalog_id=nalog.id)
                            predmet_za_nastavnika = Predmet.objects.get(naziv=trenutni_predmet)
                            if not Nastavnik.objects.filter(nalog=nalog).exists():
                                nastavnik.save()
                                nastavnik.predmet.add(predmet_za_nastavnika)
                                nastavnik_za_termin = Nastavnik.objects.get(nalog_id=nalog.id)
                                predmet_za_termin = Predmet.objects.get(naziv=trenutni_predmet)
                                print("3 nastavnik_za_termin.ime =" + nastavnik_za_termin.ime)
                                print("3 predmet_za_termin =" + predmet_za_termin.naziv)
                                print("3 oznaka_ucionice =" + oznaka_ucionice)
                                print("3 vreme_za_termin =" + red[indeksVezbi + 5])
                                tip_nastave = "Vezbe"
                                vreme = red[indeksVezbi + 5].split('-')
                                termin = Termin(oznaka_ucionice=red[indeksVezbi + 6], pocetak=vreme[0],
                                                zavrsetak=vreme[1] + ":00", dan=red[indeksVezbi + 4],tip_nastave=tip_nastave,
                                                nastavnik=nastavnik_za_termin, predmet=predmet_za_termin,
                                                raspored=RasporedNastave.objects.get(id=1))
                                termin.save()

                                grupe = red[indeksVezbi + 2].split(', ')
                                for a in grupe:
                                    grupa = Grupa(oznaka_grupe=a, semestar=Semestar.objects.get(id=1))
                                    if not Grupa.objects.filter(oznaka_grupe=a).exists():
                                        grupa.save()
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)
                                    else:
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)

                        else:
                            nalog2 = Nalog.objects.get(username = username)
                            nastavnik2 = Nastavnik.objects.get(nalog_id = nalog2.id)
                            premdet2 = Predmet.objects.get(naziv = trenutni_predmet)
                            nastavnik2.predmet.add(premdet2)
                            vreme = red[indeksVezbi+5].split('-')
                            tip_nastave = "Vezbe"
                            termin = Termin(oznaka_ucionice= red[indeksVezbi+6], pocetak= vreme[0], zavrsetak = vreme[1]+":00", dan = red[indeksVezbi+4],
                                            tip_nastave=tip_nastave,
                                            nastavnik = nastavnik2, predmet = premdet2, raspored = RasporedNastave.objects.get(id=1))

                            if not Termin.objects.filter(oznaka_ucionice=red[indeksVezbi + 6], pocetak=vreme[0],
                                                     zavrsetak=vreme[1] + ":00" , dan=red[indeksVezbi + 4],
                                                     tip_nastave=tip_nastave,nastavnik=nastavnik2 ,predmet=premdet2).exists():
                                print("TRECI")
                                termin.save()
                                grupe2 = red[indeksVezbi+2].split(', ')
                                print("33 nastavnik_za_termin.ime =" + nastavnik2.ime)
                                print("33 predmet_za_termin =" + premdet2.naziv)
                                print("33 oznaka_ucionice =" + red[indeksVezbi+6])
                                print("33 vreme_za_termin =" + red[indeksVezbi + 5])
                                for a in grupe2:
                                    grupa = Grupa(oznaka_grupe=a, semestar=Semestar.objects.get(id=1))
                                    if not Grupa.objects.filter(oznaka_grupe=a).exists():
                                        grupa.save()
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)
                                    else:
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)



##########################################################################################################
                    if red[indeksPredavanjaIPraktikuma]!='':

                        ime_prezime_nastavnika = red[indeksPredavanjaIPraktikuma].split()

                        if len(ime_prezime_nastavnika) > 2:
                            ime_natsavnika = ime_prezime_nastavnika[2]
                            prezime_nastavnika = ime_prezime_nastavnika[0] + " " + ime_prezime_nastavnika[1]
                        else:
                            ime_nastavnika = ime_prezime_nastavnika[1]
                            prezime_nastavnika = ime_prezime_nastavnika[0]

                        username = napraviUsernameNaloga(red[indeksPredavanjaIPraktikuma])

                        nalog = Nalog(username=username, uloga="Nastavnik")
                        if not Nalog.objects.filter(username=username).exists():
                            nalog.save()
                            nastavnik = Nastavnik(ime=ime_nastavnika, prezime=prezime_nastavnika, nalog=nalog,nalog_id=nalog.id)
                            predmet_za_nastavnika = Predmet.objects.get(naziv=trenutni_predmet)
                            if not Nastavnik.objects.filter(nalog=nalog).exists():
                                nastavnik.save()
                                nastavnik.predmet.add(predmet_za_nastavnika)
                                nastavnik_za_termin = Nastavnik.objects.get(nalog_id=nalog.id)
                                nastavnik.predmet.add(predmet_za_nastavnika)
                                predmet_za_termin = Predmet.objects.get(naziv=trenutni_predmet)
                                oznaka_ucionice = red[indeksPredavanjaIPraktikuma + 6]
                                vreme = red[indeksPredavanjaIPraktikuma + 5].split('-')
                                pocetak = vreme[0]
                                kraj = vreme[1] + ":00"
                                dan = red[indeksPredavanjaIPraktikuma + 4]
                                tip_nastave = "Predavanja"
                                print("4 nastavnik_za_termin.ime =" + nastavnik_za_termin.ime)
                                print("4 predmet_za_termin =" + predmet_za_termin.naziv)
                                print("4 oznaka_ucionice =" + oznaka_ucionice)
                                print("4 vreme_za_termin =" + red[indeksPredavanjaIPraktikuma + 5])

                                raspored = raspored = RasporedNastave.objects.get(id=1)
                                termin = Termin(oznaka_ucionice=oznaka_ucionice, pocetak=pocetak, zavrsetak=kraj,
                                                dan=dan, tip_nastave=tip_nastave,
                                                nastavnik=nastavnik_za_termin, predmet=predmet_za_termin,
                                                raspored=RasporedNastave.objects.get(id=1))

                                termin.save()

                                grupe = red[indeksPredavanjaIPraktikuma + 2].split(', ')
                                for a in grupe:
                                    grupa = Grupa(oznaka_grupe=a, semestar=Semestar.objects.get(id=1))
                                    if not Grupa.objects.filter(oznaka_grupe=a).exists():
                                        grupa.save()
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)
                                    else:
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)

                        else:
                            nalog2 = Nalog.objects.get(username = username)
                            nastavnik2 = Nastavnik.objects.get(nalog_id = nalog2.id)
                            premdet2 = Predmet.objects.get(naziv = trenutni_predmet)
                            nastavnik2.predmet.add(premdet2)
                            vreme = red[indeksPredavanjaIPraktikuma+5].split('-')
                            tip_nastave = "PredavanjeP"
                            termin = Termin(oznaka_ucionice= red[indeksPredavanjaIPraktikuma+6], pocetak= vreme[0], zavrsetak = vreme[1]+":00",
                                            dan = red[indeksPredavanjaIPraktikuma+4],tip_nastave=tip_nastave,
                                            nastavnik = nastavnik2, predmet = premdet2, raspored = RasporedNastave.objects.get(id=1))

                            if not Termin.objects.filter(oznaka_ucionice=red[indeksPredavanjaIPraktikuma + 6],pocetak=vreme[0],zavrsetak=vreme[1] + ":00"
                                    ,dan=red[indeksPredavanjaIPraktikuma + 4],tip_nastave=tip_nastave,nastavnik=nastavnik2,predmet=premdet2).exists():
                                print("CETVTRI")
                                termin.save()
                                grupe2 = red[indeksPredavanjaIPraktikuma+2].split(', ')
                                print("44 nastavnik_za_termin.ime =" + nastavnik2.ime)
                                print("44 predmet_za_termin =" + premdet2.naziv)
                                print("44 oznaka_ucionice =" + red[indeksPredavanjaIPraktikuma+6])
                                print("44 vreme_za_termin =" + red[indeksPredavanjaIPraktikuma + 5])
                                for a in grupe2:
                                    grupa = Grupa(oznaka_grupe=a, semestar=Semestar.objects.get(id=1))
                                    if not Grupa.objects.filter(oznaka_grupe=a).exists():
                                        grupa.save()
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)
                                    else:
                                        grupa_za_termin = Grupa.objects.get(oznaka_grupe=a)
                                        termin.grupe.add(grupa_za_termin)


