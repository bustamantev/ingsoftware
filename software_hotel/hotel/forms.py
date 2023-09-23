from django import forms


class formularioReserva(forms.Form):
    fecha_entrada = forms.DateField(
        label='Fecha de entrada', 
        widget=forms.DateInput())
    fecha_salida = forms.DateField(
        label='Fecha de salida', 
        widget=forms.DateInput(attrs={'class': 'form-control'}))
    numero_huespedes = forms.ChoiceField(
        label='Cantidad de huespedes', 
        choices=[(0, 'Seleccione cantidad de huespedes'), 
                (1, '1'), 
                (2, '2'), 
                (3, '3'), 
                (4, '4')], 
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial=0)
    tipo_habitacion = forms.ChoiceField(
        label='Tipo de habitacion', 
        choices=[(0, 'Seleccione tipo de habitacion'),
                (1, 'Suite Executive'), 
                (2, 'Suite Executive'), 
                (3, 'Suite Premier'), 
                (4, 'Suite Premier con terraza')], 
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial=0)
