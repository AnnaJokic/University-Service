from django.urls import path
from . import views

urlpatterns = [
    path('pocetna/<str:username>', views.pocetna, name='pocetna'),
    path('timetable/<str:username>', views.timetableforuser, name='timetableforuser'),
    path('nastavnik_details/<str:username>', views.nastavnik_details, name='nastavnik_details'),
    path('nastavnici/', views.nastavnici_template, name='nastavnici'),
    path('unosobavestenja/<str:user>', views.unos_obavestenja_form, name='unosobavestenja'),
    path('saveobavestenje/', views.save_obavestenje, name='saveobavestenje'),
    path('unosgrupe', views.napravi_grupu, name='napravi_grupu'),
    path('izmenagrupe/<str:oznaka_grupe>',views.izmena_grupe,name='izmena_grupe'),
    path('izborgrupe/<str:username>', views.izbor_grupe, name='izbor_grupe'),
    path('pregledgrupa', views.pregled_grupa, name='pregled_grupa'),
    path('detaljigrupe/<str:grupa>', views.detalji_grupe, name='detalji_grupe'),
    path('detaljistudenta/<str:username>', views.detalji_studenta, name='detalji_studenta'),
    path('grupeprofesora/<str:username>', views.grupe_profesora, name='grupeprofesora'),
    path('grupeprofesora/detalji/<str:oznaka_grupe>', views.grupe_profesora_detalji, name='grupeprofesoradetalji'),
    path('grupeprofesora/detalji/slika/<str:username>', views.grupe_profesora_slika, name='grupeprofesoraslika'),
    path('unoskolokvijuma/', views.unos_kolokvijuma, name='unoskolokvijuma'),
    path('unoskolokvijuma/izvestajgresaka/', views.izvestaj_gresaka, name='izvestajgresaka'),
    path('formazaispravkugresaka/', views.forma_za_ispravku_gresaka, name='formazaispravkugresaka'),
    path('maillist/<str:username>', views.maillist, name='maillist')

]

