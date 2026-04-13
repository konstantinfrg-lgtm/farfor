from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import MilkJug, Photo
from .forms import MilkJugForm, PhotoForm, FilterForm


def home(request):
    """Главная страница"""
    recent_items = MilkJug.objects.filter(
        is_published=True,
        visibility='public'
    ).select_related('manufacturer', 'form', 'painting')[:6]
    
    context = {
        'recent_items': recent_items,
    }
    return render(request, 'catalog/home.html', context)


def get_visible_milk_jugs(user):
    """Получает видимые молочники для пользователя"""
    if user.is_authenticated:
        # Показываем публичные, для зарегистрированных, и свои приватные
        return MilkJug.objects.filter(
            Q(visibility='public') |
            Q(visibility='registered') |
            Q(owner=user)
        ).filter(is_published=True)
    else:
        # Для гостей только публичные
        return MilkJug.objects.filter(
            visibility='public',
            is_published=True
        )


def apply_filters(queryset, filter_form):
    """Применяет фильтры к queryset"""
    if not filter_form.is_valid():
        return queryset
    
    data = filter_form.cleaned_data
    
    if data.get('manufacturer'):
        queryset = queryset.filter(manufacturer=data['manufacturer'])
    if data.get('sculptor'):
        queryset = queryset.filter(sculptor=data['sculptor'])
    if data.get('artist'):
        queryset = queryset.filter(artist=data['artist'])
    if data.get('form'):
        queryset = queryset.filter(form=data['form'])
    if data.get('painting'):
        queryset = queryset.filter(painting=data['painting'])
    if data.get('year_from'):
        queryset = queryset.filter(year__gte=data['year_from'])
    if data.get('year_to'):
        queryset = queryset.filter(year__lte=data['year_to'])
    if data.get('has_photos'):
        queryset = queryset.annotate(photo_count=Count('photos')).filter(photo_count__gt=0)
    
    return queryset


def apply_search(queryset, query):
    """Применяет поиск к queryset"""
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(manufacturer__name__icontains=query) |
            Q(sculptor__name__icontains=query) |
            Q(artist__name__icontains=query) |
            Q(form__name__icontains=query) |
            Q(painting__name__icontains=query) |
            Q(comments__icontains=query)
        )
    return queryset


def collection_list(request):
    """Список коллекции (по умолчанию - все доступные пользователю)"""
    queryset = get_visible_milk_jugs(request.user)
    
    filter_form = FilterForm(request.GET)
    queryset = apply_filters(queryset, filter_form)
    
    search_query = request.GET.get('q', '')
    queryset = apply_search(queryset, search_query)
    
    # Сортировка
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['name', 'year', 'manufacturer__name', 'created_at', '-created_at']:
        queryset = queryset.order_by(sort_by)
    
    # Пагинация
    paginator = Paginator(queryset.select_related('manufacturer', 'form', 'painting').prefetch_related('photos'), 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'search_query': search_query,
        'sort_by': sort_by,
        'mode': 'all',
    }
    return render(request, 'catalog/collection_list.html', context)


@login_required
def my_collection(request):
    """Личная коллекция пользователя"""
    queryset = MilkJug.objects.filter(owner=request.user)
    
    filter_form = FilterForm(request.GET)
    queryset = apply_filters(queryset, filter_form)
    
    search_query = request.GET.get('q', '')
    queryset = apply_search(queryset, search_query)
    
    # Сортировка
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['name', 'year', 'manufacturer__name', 'created_at', '-created_at']:
        queryset = queryset.order_by(sort_by)
    
    # Пагинация
    paginator = Paginator(queryset.select_related('manufacturer', 'form', 'painting').prefetch_related('photos'), 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'search_query': search_query,
        'sort_by': sort_by,
        'mode': 'my',
    }
    return render(request, 'catalog/collection_list.html', context)


def all_collection(request):
    """Все публичные коллекции"""
    queryset = MilkJug.objects.filter(visibility='public', is_published=True)
    
    filter_form = FilterForm(request.GET)
    queryset = apply_filters(queryset, filter_form)
    
    search_query = request.GET.get('q', '')
    queryset = apply_search(queryset, search_query)
    
    # Сортировка
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['name', 'year', 'manufacturer__name', 'created_at', '-created_at']:
        queryset = queryset.order_by(sort_by)
    
    # Пагинация
    paginator = Paginator(queryset.select_related('manufacturer', 'form', 'painting', 'owner').prefetch_related('photos'), 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'search_query': search_query,
        'sort_by': sort_by,
        'mode': 'all_public',
    }
    return render(request, 'catalog/collection_list.html', context)


def milk_jug_detail(request, pk):
    """Детальный просмотр молочника"""
    milk_jug = get_object_or_404(
        MilkJug.objects.select_related('manufacturer', 'sculptor', 'artist', 'form', 'painting', 'owner'),
        pk=pk
    )
    
    # Проверка прав доступа
    if milk_jug.visibility == 'private' and milk_jug.owner != request.user:
        if not request.user.is_staff:
            messages.error(request, 'У вас нет доступа к этому предмету')
            return redirect('catalog:collection_list')
    
    if milk_jug.visibility == 'registered' and not request.user.is_authenticated:
        messages.error(request, 'Просмотр доступен только для зарегистрированных пользователей')
        return redirect('accounts:login')
    
    photos = milk_jug.photos.all()
    main_photo = photos.filter(is_main=True).first() or photos.first()
    
    context = {
        'milk_jug': milk_jug,
        'photos': photos,
        'main_photo': main_photo,
    }
    return render(request, 'catalog/milk_jug_detail.html', context)


@login_required
def milk_jug_create(request):
    """Создание нового молочника"""
    if request.method == 'POST':
        form = MilkJugForm(request.POST)
        if form.is_valid():
            milk_jug = form.save(commit=False)
            milk_jug.owner = request.user
            milk_jug.save()
            messages.success(request, 'Молочник успешно добавлен!')
            return redirect('catalog:milk_jug_detail', pk=milk_jug.pk)
    else:
        form = MilkJugForm()
    
    context = {'form': form, 'title': 'Добавить молочник'}
    return render(request, 'catalog/milk_jug_form.html', context)


@login_required
def milk_jug_update(request, pk):
    """Редактирование молочника"""
    milk_jug = get_object_or_404(MilkJug, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = MilkJugForm(request.POST, instance=milk_jug)
        if form.is_valid():
            form.save()
            messages.success(request, 'Молочник успешно обновлен!')
            return redirect('catalog:milk_jug_detail', pk=milk_jug.pk)
    else:
        form = MilkJugForm(instance=milk_jug)
    
    context = {'form': form, 'title': 'Редактировать молочник', 'milk_jug': milk_jug}
    return render(request, 'catalog/milk_jug_form.html', context)


@login_required
def milk_jug_delete(request, pk):
    """Удаление молочника"""
    milk_jug = get_object_or_404(MilkJug, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        milk_jug.delete()
        messages.success(request, 'Молочник успешно удален!')
        return redirect('catalog:my_collection')
    
    context = {'milk_jug': milk_jug}
    return render(request, 'catalog/milk_jug_confirm_delete.html', context)


@login_required
def photo_upload(request, pk):
    """Загрузка фотографии для молочника"""
    milk_jug = get_object_or_404(MilkJug, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.milk_jug = milk_jug
            photo.save()
            messages.success(request, 'Фотография успешно загружена!')
            return redirect('catalog:milk_jug_detail', pk=milk_jug.pk)
    else:
        form = PhotoForm()
    
    context = {'form': form, 'milk_jug': milk_jug}
    return render(request, 'catalog/photo_upload.html', context)


@login_required
def photo_delete(request, pk, photo_id):
    """Удаление фотографии"""
    milk_jug = get_object_or_404(MilkJug, pk=pk, owner=request.user)
    photo = get_object_or_404(Photo, pk=photo_id, milk_jug=milk_jug)
    
    if request.method == 'POST':
        photo.delete()
        messages.success(request, 'Фотография успешно удалена!')
        return redirect('catalog:milk_jug_detail', pk=milk_jug.pk)
    
    context = {'milk_jug': milk_jug, 'photo': photo}
    return render(request, 'catalog/photo_confirm_delete.html', context)


@login_required
def photo_set_main(request, pk, photo_id):
    """Установка фотографии как главной"""
    milk_jug = get_object_or_404(MilkJug, pk=pk, owner=request.user)
    photo = get_object_or_404(Photo, pk=photo_id, milk_jug=milk_jug)
    
    photo.is_main = True
    photo.save()
    
    messages.success(request, 'Фотография установлена как главная!')
    return redirect('catalog:milk_jug_detail', pk=milk_jug.pk)
