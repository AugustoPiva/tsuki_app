from flatpickr import DatePickerInput
from django import forms
from .models import Pedidos
from datetime import datetime,date
#
class FormularioNuevoPedido(forms.ModelForm):
    class Meta:
        model = Pedidos
        fields =  ['fecha','nombre_cliente','comentario']
        widgets = {
            'fecha': DatePickerInput()
        }

class Fecha(forms.Form):
    dia= forms.DateField(widget=DatePickerInput())
    # options={"dateFormat":""}
