from django import forms
from .models import MilkJug, Photo, Manufacturer, Sculptor, Artist, Form, Painting


class MilkJugForm(forms.ModelForm):
    """Форма для создания/редактирования молочника"""
    
    class Meta:
        model = MilkJug
        fields = [
            'manufacturer', 'sculptor', 'artist', 'form', 'painting',
            'name', 'year', 'material', 'country', 'factory',
            'height', 'volume', 'condition', 'has_mark', 'mark_description',
            'source', 'comments', 'visibility', 'is_published'
        ]
        widgets = {
            'manufacturer': forms.Select(attrs={'class': 'form-control'}),
            'sculptor': forms.Select(attrs={'class': 'form-control'}),
            'artist': forms.Select(attrs={'class': 'form-control'}),
            'form': forms.Select(attrs={'class': 'form-control'}),
            'painting': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название предмета'}),
            'year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Год или период'}),
            'material': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Материал'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Страна'}),
            'factory': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Завод / фабрика'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'volume': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'has_mark': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'mark_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'source': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Источник поступления'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'visibility': forms.Select(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PhotoForm(forms.ModelForm):
    """Форма для загрузки фотографии"""
    
    class Meta:
        model = Photo
        fields = ['image', 'is_main', 'order']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class SearchForm(forms.Form):
    """Форма поиска по каталогу"""
    query = forms.CharField(
        required=False,
        label='Поиск',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию, производителю, скульптору...'
        })
    )


class FilterForm(forms.Form):
    """Форма фильтрации каталога"""
    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        empty_label='Все производители',
        label='Производитель',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sculptor = forms.ModelChoiceField(
        queryset=Sculptor.objects.all(),
        required=False,
        empty_label='Все скульпторы',
        label='Скульптор',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    artist = forms.ModelChoiceField(
        queryset=Artist.objects.all(),
        required=False,
        empty_label='Все художники',
        label='Художник',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    form = forms.ModelChoiceField(
        queryset=Form.objects.all(),
        required=False,
        empty_label='Все формы',
        label='Форма',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    painting = forms.ModelChoiceField(
        queryset=Painting.objects.all(),
        required=False,
        empty_label='Все росписи',
        label='Роспись',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    year_from = forms.CharField(
        required=False,
        label='Год от',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'От'})
    )
    year_to = forms.CharField(
        required=False,
        label='Год до',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'До'})
    )
    has_photos = forms.BooleanField(
        required=False,
        label='Только с фото',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
