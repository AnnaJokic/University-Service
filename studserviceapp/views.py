# Create your views here.
import send_gmail
from django.core import serializers

from datetime import datetime

def index(request):
    return HttpResponse("Dobrodošli na studentski servis")


from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from datetime import datetime

import os
import json
from studserviceapp.forms import ImageUploadForm, UnosKolokvijumaForm, SimpleTable,SimpleTable2
from studserviceapp.csvReaderKol import unos_rasporeda

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studservice.settings")
import django

django.setup()
from studserviceapp.models import *
from django.template import Template
import datetime

# Create your views here.
listaTermina = []


def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__


def index(request):
    return HttpResponse("Dobrodošli na studentski servis")



# 5. STAVKA U SPECIFIKACIJI
def timetable(username):
    terministring = ""
    listaTermina.clear()
    student = False
    nastavnik = False

    try:
        nalog = Nalog.objects.get(username=username)
    except Nalog.DoesNotExist:
        raise Http404("Nema korisnika")
    if nalog.uloga == "student":
        student = True
    else:
        nastavnik = True

    if student == True:
        student = Student.objects.get(nalog=nalog)
        grupa = Student.grupa.through.objects.get(student_id=student.id)
        grupa = Grupa.objects.get(id=grupa.grupa_id)
        termin = Termin.grupe.through.objects.filter(grupa_id=grupa.id)
        for i in range(0, len(termin)):
            termin2 = Termin.objects.get(id=termin[i].termin_id)
            listaTermina.append(termin2)
            terministring += str(termin2) + "<br>"

    elif nastavnik == True:
        nastavnik = Nastavnik.objects.get(nalog=nalog)
        termin = Termin.objects.filter(nastavnik_id=nastavnik.id)
        for i in range(0, len(termin)):
            termin2 = Termin.objects.get(id=termin[i].id)
            terministring += str(termin2) + "<br>"
            listaTermina.append(termin2)
    return terministring


def timetableforuser(request, username):
    uloga = timetable(username)
    return HttpResponse(uloga)


def nastavnik_details(request, username):
    try:
        qs = Nastavnik.objects.filter(nalog__username=username)
        n = qs[0]
        str = "Ime: " + n.ime + "<br>Prezime:" + n.prezime
        return HttpResponse("Podaci o nastavniku<br> %s." % str)
    except IndexError:
        raise Http404("Ne postoji nastavnik sa nalogom %s" % username)


def nastavnici_template(request):
    qs = Nastavnik.objects.all()
    template = django.template.loader.get_template('studserviceapp/nastavnici.html')
    context = {'nastavnici': qs}
    return HttpResponse(template.render(context, request))


def unos_obavestenja_form(request, user):
    try:
        n = Nalog.objects.get(username=user)
        if n.uloga == 'sekretar' or n.uloga == 'administrator':
            context = {'nalog': n}
            return render(request, 'studserviceapp/unosobavestenja.html', context)
        else:
            return HttpResponse('<h1>Korisnik mora biti sekretar iliadministrator</h1>')
    except Nalog.DoesNotExist:
        return HttpResponse('<h1>Username ' + user + ' not found</h1>')


def save_obavestenje(request):
    tekst = request.POST['tekst']
    postavio = Nalog.objects.get(username=request.POST['postavio'])
    obavestenje = Obavestenje(tekst=tekst, postavio=postavio, datum_postavljanja=datetime.datetime.now())
    obavestenje.save()
    return HttpResponse('<h1>Obavestenje sačuvano</h1>')


def napravi_grupu(request):
    if request.method == 'POST':

        nazivi = request.POST['naziv'].split(',')
        semestar = int(request.POST['semestar'])
        vrsta_semestra = 'parni' if semestar % 2 == 0 else 'neparni'
        poc_god = request.POST['poc-godina']
        kraj_god = request.POST['kraj-godina']
        kapacitet = request.POST['kapacitet']
        smer = request.POST['smer']
        aktivna = False
        if request.POST.get('aktivnost') == 'da':
            aktivna = True

        predmeti = request.POST.getlist('biraj')
        if len(predmeti) == 0:
            return HttpResponse('Prvo izaberite predmete za grupu')

        if '' in (nazivi, semestar, vrsta_semestra, poc_god, kraj_god, kapacitet, smer, aktivna):
            return HttpResponse('Potrebno je popuniti sva polja')
        else:

            sem = Semestar(vrsta=vrsta_semestra, skolska_godina_pocetak=poc_god, skolska_godina_kraj=kraj_god)

            if not Semestar.objects.filter(vrsta=vrsta_semestra, skolska_godina_pocetak=poc_god,
                                           skolska_godina_kraj=kraj_god).exists():
                sem.save()

            else:
                sem = Semestar.objects.get(vrsta=vrsta_semestra, skolska_godina_pocetak=poc_god,
                                           skolska_godina_kraj=kraj_god)

            for n in nazivi:
                grupa = IzbornaGrupa(oznaka_grupe=n, oznaka_semestra=semestar, kapacitet=kapacitet,
                                     smer=smer, aktivna=aktivna, za_semestar=sem)
                grupa.save()
                for pred in predmeti:

                    #print(pred)
                    predmet = Predmet.objects.get(naziv=pred)
                    grupa.predmeti.add(predmet)

            return HttpResponse('bravo')
    else:


        predmeti = Predmet.objects.all()
        #json_predmeti = json.dumps(predmeti, indent=4)
        #json_predmeti =  Predmet.objects.all()
        #json_predmeti = json.dumps(str(predmeti))
        #json_predmeti = predmeti[0].toJSON()
        json_predmeti = serializers.serialize("json", Predmet.objects.all())

        #print(json_predmeti)
        context = {
            'predmeti': predmeti,
            'json': json_predmeti
        }

        template = django.template.loader.get_template('studserviceapp/unosgrupe.html')

        return HttpResponse(template.render(context, request))


def izmena_grupe(request, oznaka_grupe):
    if request.method == 'POST':
        oznaka_semestra = request.POST['tip_semestra']
        if int(oznaka_semestra) % 2 == 0:
            vrsta_semestra = 'parni'
        else:
            vrsta_semestra = 'neparni'
        pocetak_godine = request.POST['pocetna_godina']
        kraj_godine = request.POST['zavrsna_godina']
        try:
            za_semestar = Semestar.objects.get(vrsta=vrsta_semestra, skolska_godina_pocetak=pocetak_godine,
                                               skolska_godina_kraj=kraj_godine)
        except:
            za_semestar = Semestar(vrsta=vrsta_semestra, skolska_godina_pocetak=pocetak_godine,
                                   skolska_godina_kraj=kraj_godine)
            za_semestar.save()
        grupaedit = IzbornaGrupa.objects.get(oznaka_grupe=oznaka_grupe)

        predmeti_grupe = request.POST.getlist('subject')
        kapacitet = request.POST['kapacitet']
        smer = request.POST.get('smer')
        if request.POST.get('aktivna') == 'Da':
            aktivna = True
        else:
            aktivna = False
        grupaedit.oznaka_semestra = oznaka_semestra
        grupaedit.kapacitet = kapacitet
        grupaedit.smer = smer
        grupaedit.aktivna = aktivna
        grupaedit.za_semestar = za_semestar
        grupaedit.predmeti.clear()
        grupaedit.save()

        for predmet in predmeti_grupe:
            predmet = Predmet.objects.get(naziv=predmet)
            grupaedit.predmeti.add(predmet)
        return HttpResponseRedirect('bravo')
    else:
        prosledi_grupu = None
        for grupa in IzbornaGrupa.objects.all():
            if str(grupa.oznaka_grupe) == str(oznaka_grupe):
                prosledi_grupu = grupa

        data = {
            "subjects": Predmet.objects.all(),
            "grupa_za_izmenu": prosledi_grupu
        }
        return render(request, 'studserviceapp/izmenagrupe.html', data)


def izbor_grupe(request, username):
    if not Nalog.objects.filter(username=username, uloga="student").exists():
        #print(username)
        return HttpResponse("taj nalog ne postoji")

    else:
        nalog = Nalog.objects.get(username=username, uloga="student")

    student = Student.objects.get(nalog=nalog)

    if IzborGrupe.objects.filter(student=student):
        return HttpResponse('vec si izabrao grupu ne moze')

    semestar = Semestar.objects.latest('id')
    grupe = IzbornaGrupa.objects.filter(smer=student.smer, aktivna=True)
    sve_grupe = IzbornaGrupa.objects.all()
    popunjenost_grupa = dict()

    for grupa in sve_grupe:
        popunjenost_grupa[grupa.oznaka_grupe] = 0

    svi_izbori = IzborGrupe.objects.all()

    for izbor in svi_izbori:
        popunjenost_grupa[izbor.izabrana_grupa.oznaka_grupe] += 1

    grupe = list(x for x in grupe if (x.kapacitet > popunjenost_grupa[x.oznaka_grupe]))

    if request.method == 'POST':

        if request.POST.get('upis') == 'da':
            prvi_put_upisuje_semestar = True
        else:
            prvi_put_upisuje_semestar = False

        if not IzbornaGrupa.objects.filter(oznaka_grupe=request.POST.get('biraj')).exists():
            return HttpResponse("grupa ne postoji")

        else:
            izabrana_grupa = IzbornaGrupa.objects.get(oznaka_grupe=request.POST.get('biraj'))

        lista_predmeta = request.POST.getlist('predmet')

        izbor = IzborGrupe(
            ostvarenoESPB=request.POST['osvojeni_espb'],
            upisujeESPB=request.POST['upisujem_espb'],
            broj_polozenih_ispita=request.POST['broj_polozenih'],
            upisuje_semestar=int(request.POST.get('semestar')),
            prvi_put_upisuje_semestar=prvi_put_upisuje_semestar,
            nacin_placanja=request.POST.get('placanje'),
            upisan=False,
            izabrana_grupa=izabrana_grupa,
            student=student)
        izbor.save()

        for predmet in lista_predmeta:
            predmet = Predmet.objects.get(naziv=predmet)
            izbor.nepolozeni_predmeti.add(predmet)
        return HttpResponse('Uspesno ste izabrali grupu')
    else:

        json_grupe = json.dumps(grupe, default=dumper, indent=4)

        data = {
            'student': student,
            'semestar': semestar,
            'grupe': grupe,
            'predmeti': Predmet.objects.all(),
            'json': json_grupe
        }
        #print(json_grupe)

        return render(request, 'studserviceapp/izborgrupe.html', data)


def pregled_grupa(request):
    grupe = IzborGrupe.objects.all()
    filtrirane = list()

    for g in grupe:

        oznaka = g.izabrana_grupa.oznaka_grupe

        if oznaka not in filtrirane:
            filtrirane.append(oznaka)

    data = {'grupe': filtrirane}

    return render(request, 'studserviceapp/pregledgrupa.html', data)


def detalji_grupe(request, grupa):
    grupa = IzbornaGrupa.objects.get(oznaka_grupe=grupa)
    grupa1 = IzborGrupe.objects.filter(izabrana_grupa=grupa)

    studenti = list()

    for s in grupa1:
        studenti.append(s.student)

    data = {'studenti': studenti}

    return render(request, 'studserviceapp/detaljigrupe.html', data)


def detalji_studenta(request, username):
    nalog = Nalog.objects.get(username=username)
    if (nalog.uloga == "student"):
        student = Student.objects.get(nalog=nalog)
        grupe = student.grupa.all()
    if request.method == 'GET':
        data = {
            'student': student,
            'grupe': grupe
        }
        return render(request, 'studserviceapp/detaljistudenta.html', data)
    else:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            student.slika = form.cleaned_data['image']
            student.save()
            return HttpResponse("slika je sacuvana u bazi")


def grupe_profesora(request, username):
    nalog = Nalog.objects.get(username=username)

    if (nalog.uloga == "Nastavnik"):
        nastavnik = Nastavnik.objects.get(nalog=nalog)
        termini = Termin.objects.filter(nastavnik=nastavnik)
        recnik = dict()

        for t in termini:

            predmet = t.predmet
            recnik.setdefault(predmet, [])

            for g in t.grupe.all():
                recnik[predmet].append(g.oznaka_grupe)
        data = {
            'nastavnik': nastavnik,
            'recnik': recnik,
            'nalog':nalog
        }

        return render(request, 'studserviceapp/grupeprofesora.html', data)
    elif nalog.uloga =='sekretar' or nalog.uloga=='administrator':
        grupe=Grupa.objects.all()
        oznake_grupe=[]
        for g in grupe:
            oznake_grupe.append(g.oznaka_grupe)

        data={'recnik':oznake_grupe,'uloga':nalog.uloga,'nalog':nalog}
        return render(request, 'studserviceapp/grupeprofesora.html', data)




def grupe_profesora_detalji(request, oznaka_grupe):
    grupa = Grupa.objects.get(oznaka_grupe=oznaka_grupe)
    studenti = Student.objects.filter(grupa=grupa)

    data = {

        'studenti': studenti
    }

    return render(request, 'studserviceapp/grupeprofesoradetalji.html', data)


def grupe_profesora_slika(request, username):
    nalog = Nalog.objects.get(username=username)

    student = Student.objects.get(nalog=nalog)

    data = {

        'slika': student.slika.url
    }

    # print(student.slika.url)

    return render(request, 'studserviceapp/grupeprofesoraslika.html', data)


def unos_kolokvijuma(request):
    if request.method == 'POST':

        form = UnosKolokvijumaForm(request.POST, request.FILES)

        if form.is_valid():
            kolokvijumska_nedelja = RasporedPolaganja(kolokvijumska_nedelja=request.POST['nedelja'])
            kolokvijum_file = request.FILES['raspored']

            greske, cele, oba = unos_rasporeda(kolokvijum_file, kolokvijumska_nedelja.kolokvijumska_nedelja)

            if len(greske) == 0:
                return HttpResponse("nema gresaka, uspesan unos")
            else:
                global greske1
                greske1 = {'greske': greske}

                global greske_cele

                global proba
                proba = []

                for k,v in oba.items():

                    proba.append(str(k)+" :"+str(v))
                    #print(str(k)+str(v))

                greske_cele = {'greske': greske, 'cele': cele, 'oba': proba}

                global oba1
                oba1 = {'oba':oba}

                return HttpResponseRedirect('izvestajgresaka')

    else:

        form = UnosKolokvijumaForm()
        return render(request, 'unoskolokvijuma.html', {'form': form})


def izvestaj_gresaka(request):
    if request.method == 'POST':

        if request.POST.get('unesi'):
            #print("unesi ")
            return redirect('unoskolokvijuma')

        elif request.POST.get('ispravi'):
            #print("ispravi ")

            return redirect('formazaispravkugresaka')

    return render(request, 'studserviceapp/izvestajgresaka.html', greske1)


def forma_za_ispravku_gresaka(request):

    if request.method == 'POST':


            if request.POST.get('sacuvaj'):

                greska = request.POST['select1']
                print(greska)

                predmet = request.POST.get('predmeti')

                prof = request.POST.get('izaberi_profu')

                ucionice = request.POST.get('ucionice')

                vreme1 = request.POST.get('vreme')
                vreme=vreme1.split('-')

                datumalo = request.POST.get('datum')

                rasporedPolaganja=RasporedPolaganja.objects.latest('id')

                dan1 = datumalo.split('.')[0]
                mesec1 = datumalo.split('.')[1]
                datum = datetime.datetime.strptime(dan1 + ' ' + mesec1 + ' 2018', '%d %m %Y').date()

                provera_profesora = prof.split()

                i = 0
                profesori = []
                nastavnik_ne_postoji = 1

                if len(provera_profesora) == 2:
                    ime = provera_profesora[0]
                    prezime = provera_profesora[1]
                    # print(ime + " " + prezime)
                    if Nastavnik.objects.filter(ime=ime, prezime=prezime).exists():
                        nastavnik = Nastavnik.objects.get(ime=ime, prezime=prezime)
                        profesori.append(nastavnik)
                        nastavnik_ne_postoji = 1
                    else:
                        nastavnik_ne_postoji = 0
                        return HttpResponse("nastavnik ne postoji ili mu ime/prezime nije lepo uneto")

                if len(provera_profesora) == 3:
                    ime = provera_profesora[0]
                    prezime = provera_profesora[1] + " " + provera_profesora[2]
                    # print(ime + " " + prezime)
                    if Nastavnik.objects.filter(ime=ime, prezime=prezime).exists():
                        nastavnik = Nastavnik.objects.get(ime=ime, prezime=prezime)
                        profesori.append(nastavnik)
                        nastavnik_ne_postoji = 1
                    else:
                        nastavnik_ne_postoji = 0
                        return HttpResponse("nastavnik ne postoji ili mu ime/prezime nije lepo uneto")

                if len(provera_profesora) > 3:

                    if (len(provera_profesora) % 2 == 0):

                        while (i < len(provera_profesora)):

                            ime = provera_profesora[i]
                            prezime = provera_profesora[i + 1]

                            i += 2
                            if Nastavnik.objects.filter(ime=ime, prezime=prezime).exists():
                                nastavnik = Nastavnik.objects.get(ime=ime, prezime=prezime)
                                profesori.append(nastavnik)
                                nastavnik_ne_postoji = 1
                            else:
                                nastavnik_ne_postoji = 0
                                return HttpResponse("nastavnik ne postoji ili mu ime/prezime nije lepo uneto")

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
                            return HttpResponse("nastavnik ne postoji ili mu ime/prezime nije lepo uneto")

                        if Nastavnik.objects.filter(ime=ime2, prezime=prezime2).exists():
                            nastavnik = Nastavnik.objects.get(ime=ime2, prezime=prezime2)
                            profesori.append(nastavnik)
                            nastavnik_ne_postoji = 1
                        else:
                            nastavnik_ne_postoji = 0
                            return HttpResponse("nastavnik ne postoji ili mu ime/prezime nije lepo uneto")

                if not Predmet.objects.filter(naziv=predmet).exists():
                    #print(predmet)

                    return HttpResponse("predmet ne postoji ili mu ime/prezime nije lepo uneto")

                else:

                    if (nastavnik_ne_postoji):

                        pravi_predmet = Predmet.objects.get(naziv=predmet.strip())

                        # proevri koliko ima profesora ako ima samo jedan dodaj ga odmah i sacuvaj predmet, ako ima vise
                        # dodaj prvo jednog normalno sacuvaj predmet pa onda dodaj drugog

                        if (len(profesori) == 1):


                                if not TerminPolaganja.objects.filter(ucionice=ucionice, pocetak=vreme[0] + ":00",
                                                                      zavrsetak=vreme[1] + ":00", datum=datum,
                                                                      raspored_polaganja=rasporedPolaganja,
                                                                      predmet=pravi_predmet).exists():
                                    termin = TerminPolaganja(ucionice=ucionice, pocetak=vreme[0] + ":00",
                                                             zavrsetak=vreme[1] + ":00", datum=datum,
                                                             raspored_polaganja=rasporedPolaganja,
                                                             predmet=pravi_predmet)
                                    #print(predmet)
                                    #print(nastavnik.ime)
                                    #print(ucionice)
                                    #print(vreme[0] + " " + vreme[1])
                                    #print(datum)
                                    #print(" ")
                                    termin.save()

                                    for p in profesori:
                                        termin.nastavnik.add(p)


                        else:


                                if not TerminPolaganja.objects.filter(ucionice=ucionice, pocetak=vreme[0] + ":00",
                                                                      zavrsetak=vreme[1] + ":00", datum=datum,
                                                                      raspored_polaganja=rasporedPolaganja,
                                                                      predmet=pravi_predmet).exists():
                                    termin = TerminPolaganja(ucionice=ucionice, pocetak=vreme[0] + ":00",
                                                             zavrsetak=vreme[1] + ":00", datum=datum,
                                                             raspored_polaganja=rasporedPolaganja,
                                                             predmet=pravi_predmet)
                                    #print(predmet)
                                    #print(nastavnik.ime)
                                    #print(ucionice)
                                    #print(vreme[0] + " " + vreme[1])
                                    #print(datum)
                                    #print(" ")
                                    termin.save()

                                    for p in profesori:
                                        termin.nastavnik.add(p)



                za_brisanje=""

                for p in proba:

                    provera = p[:2].strip()


                    if provera == greska:


                        za_brisanje = p
                        print(greska)
                        print(za_brisanje)


                proba.remove(za_brisanje)

                return render(request, 'studserviceapp/formazaispravkugresaka.html', {'oba': proba})




    else:

        return render(request, 'studserviceapp/formazaispravkugresaka.html', greske_cele)


def maillist(request, username):
    if request.method == 'GET':
        if Nalog.objects.filter(username=username).exists():
            mejlovi = username + '@raf.rs'
            zaslanje = {'za_slanje': [], 'mejlovi': mejlovi}
            nalog = Nalog.objects.get(username=username)

            if nalog.uloga in ('sekretar', 'administrator'):
                zaslanje['prezime'] = username
                zaslanje['za_slanje'].append('svi')
                zaslanje['za_slanje'].append('racunarske nauke')
                zaslanje['za_slanje'].append('racunarsko inzenjerstvo')
                zaslanje['za_slanje'].append('racunarski dizajn')
                for p in Predmet.objects.all():
                    zaslanje['za_slanje'].append(str(p))

                for g in Grupa.objects.all():
                    zaslanje['za_slanje'].append(str(g))

                return render(request, 'studserviceapp/maillist.html', zaslanje)

            elif nalog.uloga == 'Nastavnik':
                ime = Nastavnik.objects.get(nalog=nalog).ime
                prezime = Nastavnik.objects.get(nalog=nalog).prezime
                zaslanje['ime'] = ime
                zaslanje['prezime'] = prezime

                for t in Termin.objects.all():
                    profa = t.nastavnik
                    predmet = t.predmet
                    grupe = t.grupe.all()
                    if profa.nalog.username == username:
                        if str(predmet) not in zaslanje['za_slanje']:
                            zaslanje['za_slanje'].append(str(predmet))
                        for g in grupe:
                            if str(g) not in zaslanje['za_slanje']:
                                zaslanje['za_slanje'].append(str(g))

                #print(zaslanje)
                return render(request, 'studserviceapp/maillist.html', zaslanje)
            else:
                return HttpResponse('Nema nista u bazi')
        else:
            return HttpResponse(' Greska????!')

    elif request.method == 'POST':
        if True:
            if request.POST.get('posalji'):
                checkbox = request.POST.get('checkbox')
                #print(checkbox)
                from1 = request.POST.get('from')
                #print(from1)
                subject = request.POST.get('subject')
                message = request.POST.get('text_area')
                #print(message)
                specific = request.POST.get('specific')
                #print(specific)
                attachments = None
                if request.FILES and request.FILES.get('attachment'):
                    attachments = [request.FILES.get('attachment')]

                send_gmail.create_and_send_message(from1, specific, subject, message, attachmentFile=None, cc=None)

                return HttpResponse('Mail je poslat')

def pocetna(request,username):

    nalog=Nalog.objects.get(username=username)
    if nalog.uloga == "Nastavnik":

        #raspored
        nastavnik = Nastavnik.objects.get(nalog=nalog)
        queryset = Termin.objects.filter(nastavnik=nastavnik)
        table = SimpleTable(queryset)
        table.exclude = ('raspored',)



        #obavestenje
        ob=Obavestenje.objects.all()
        brojac=len(ob)
        i=5
        queryset1=[]
        while i:
            #print(ob[brojac-1])
            i=i-1
            queryset1.append(ob[brojac-1])
            brojac = brojac - 1

        tableObavestenja=SimpleTable2(queryset1)
        tableObavestenja.exclude=('fajl')



        data = {'nalog': nalog, 'table': table,'table2': tableObavestenja}
        return render(request, 'studserviceapp/pocetna.html',data)
    elif nalog.uloga == "student":
        nalog=Nalog.objects.get(username=username)
        student = Student.objects.get(nalog_id=nalog.id)
        grupa = Student.grupa.through.objects.get(student_id=student.id)
        grupa = Grupa.objects.get(id=grupa.grupa_id)
        #print(grupa.oznaka_grupe)
        termin = Termin.grupe.through.objects.filter(grupa_id=grupa.id)  # je termin_grupa
        terms=[]
        for k in range(0, len(termin)):
            t = Termin.objects.get(id=termin[k].termin_id)  # je pravi termin
            #print(t)
            terms.append(t)
            #print('alo')
        table = SimpleTable(terms)
        table.exclude = ('raspored',)
        terms.clear()





        ob = Obavestenje.objects.all()
        brojac = len(ob)
        i = 5
        queryset1 = []
        while i:
            #print(ob[brojac - 1])
            i = i - 1
            queryset1.append(ob[brojac - 1])
            brojac = brojac - 1

        tableObavestenja = SimpleTable2(queryset1)
        tableObavestenja.exclude = ('fajl')

        data = {'nalog': nalog, 'table': table,'table2':tableObavestenja}
        return render(request, 'studserviceapp/pocetna.html', data)
    elif nalog.uloga == "administrator":
        queryset = Termin.objects.all()
        table = SimpleTable(queryset)
        table.exclude = ('raspored',)

        ob = Obavestenje.objects.all()
        brojac = len(ob)
        i = 5
        queryset1 = []
        while i:
            #print(ob[brojac - 1])
            i = i - 1
            queryset1.append(ob[brojac - 1])
            brojac = brojac - 1

        tableObavestenja = SimpleTable2(queryset1)
        tableObavestenja.exclude = ('fajl')

        data = {'nalog': nalog, 'table': table,'table2':tableObavestenja}
        return render(request, 'studserviceapp/pocetna.html', data)
    elif nalog.uloga == "sekretar":

        queryset = Termin.objects.all()
        table = SimpleTable(queryset)
        table.exclude = ('raspored',)

        ob = Obavestenje.objects.all()
        brojac = len(ob)
        i = 5
        queryset1 = []
        while i:
            #print(ob[brojac - 1])
            i = i - 1
            queryset1.append(ob[brojac - 1])
            brojac = brojac - 1

        tableObavestenja = SimpleTable2(queryset1)
        tableObavestenja.exclude = ('fajl')

        data = {'nalog': nalog, 'table': table,'table2':tableObavestenja}
        return render(request, 'studserviceapp/pocetna.html', data)