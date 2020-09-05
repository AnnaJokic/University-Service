import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studservice.settings")
import django
django.setup()

from studserviceapp.models import Semestar,Grupa,Nalog,Student

#4. STAVKA U SPECIFIKACIJI
semestar = Semestar(vrsta="neparni", skolska_godina_pocetak=2018, skolska_godina_kraj=2019)
if not Semestar.objects.filter(vrsta="neparni").exists():
    semestar.save()

if not Nalog.objects.filter(username ="ajokic17").exists():

    nalog_ajokic17 = Nalog(username="ajokic17", lozinka="53644773", uloga="student")
    nalog_ajokic17.save()
    grupa_302 = Grupa.objects.get(oznaka_grupe="302")
    student_ajokic17 = Student(ime="Ana", prezime="Jokic", broj_indeksa="77", godina_upisa=2016, smer="RN",nalog=nalog_ajokic17)

    student_ajokic17.save()
    student_ajokic17.grupa.add(grupa_302)

if not Nalog.objects.filter(username = "ikocic17").exists():

    nalog_ikocic17 = Nalog(username="ikocic17", lozinka="75262986", uloga="student")
    nalog_ikocic17.save()
    grupa_302 = Grupa.objects.get(oznaka_grupe = "302")
    student_ikocic17 = Student(ime="Irina", prezime="Kocic", broj_indeksa="61", godina_upisa=2016,smer="RN", nalog=nalog_ikocic17)

    student_ikocic17.save()
    student_ikocic17.grupa.add(grupa_302)

