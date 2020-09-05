from django import forms
from studserviceapp.models import TerminPolaganja
import django_tables2 as tables
from studserviceapp.models import Termin,Obavestenje,Nalog


class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()

class UnosKolokvijumaForm(forms.Form):
    nedelja = forms.ChoiceField(label='Broj kolokvijumske nedelje', choices=[(1, 'prva'), (2, 'druga'), (3, 'treca'), (4, 'cetvrta')])
    raspored = forms.FileField(label='Izaberite fajl sa rasporedom')

class SimpleTable(tables.Table):
    nastavnik = tables.Column(accessor='nastavnik.ime')
    prezime = tables.Column(accessor='nastavnik.prezime')
    class Meta:
        model = Termin
        sequence = ('id','nastavnik', 'prezime')

class SimpleTable2(tables.Table):
    postavio = tables.Column(accessor='postavio.username')
    class Meta:
        model = Obavestenje
        sequence = ('id','postavio')

