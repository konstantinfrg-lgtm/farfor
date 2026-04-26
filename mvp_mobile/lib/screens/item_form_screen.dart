import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../services/api_service.dart';

class ItemFormScreen extends StatefulWidget {
  const ItemFormScreen({super.key});

  @override
  State<ItemFormScreen> createState() => _ItemFormScreenState();
}

class _ItemFormScreenState extends State<ItemFormScreen> {
  final _api = ApiService();
  final _picker = ImagePicker();

  final _title = TextEditingController();
  final _manufacturer = TextEditingController();
  final _shapeAuthor = TextEditingController();
  final _paintingAuthor = TextEditingController();
  final _shapeName = TextEditingController();
  final _paintingName = TextEditingController();
  final _year = TextEditingController();
  final _period = TextEditingController();
  final _material = TextEditingController();
  final _condition = TextEditingController();
  final _size = TextEditingController();
  final _location = TextEditingController();
  final _comment = TextEditingController();

  bool _isPublic = false;
  bool _loading = false;
  final List<File> _photos = [];

  Future<void> _addFromCamera() async {
    final file = await _picker.pickImage(source: ImageSource.camera, imageQuality: 90);
    if (file != null) {
      setState(() => _photos.add(File(file.path)));
    }
  }

  Future<void> _addFromGallery() async {
    final files = await _picker.pickMultiImage(imageQuality: 90);
    setState(() => _photos.addAll(files.map((f) => File(f.path))));
  }

  Future<void> _save() async {
    setState(() => _loading = true);
    try {
      final photoUrls = <String>[];
      for (final file in _photos) {
        photoUrls.add(await _api.uploadPhoto(file));
      }

      await _api.createItem({
        'title': _title.text,
        'manufacturer': _manufacturer.text,
        'shape_author': _shapeAuthor.text,
        'painting_author': _paintingAuthor.text,
        'shape_name': _shapeName.text,
        'painting_name': _paintingName.text,
        'production_year': int.tryParse(_year.text),
        'period': _period.text,
        'material': _material.text,
        'condition': _condition.text,
        'size': _size.text,
        'location': _location.text,
        'comment': _comment.text,
        'is_public': _isPublic,
        'photo_urls': photoUrls,
      });

      if (!mounted) return;
      Navigator.of(context).pop();
    } catch (_) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Не удалось сохранить предмет')));
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Widget _field(String label, TextEditingController controller, {TextInputType? keyboard}) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: TextField(controller: controller, keyboardType: keyboard, decoration: InputDecoration(labelText: label)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Новый предмет')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Wrap(
            spacing: 8,
            children: [
              OutlinedButton.icon(onPressed: _addFromCamera, icon: const Icon(Icons.photo_camera), label: const Text('Сфотографировать')),
              OutlinedButton.icon(onPressed: _addFromGallery, icon: const Icon(Icons.photo_library), label: const Text('Из галереи')),
            ],
          ),
          const SizedBox(height: 8),
          Text('Выбрано фото: ${_photos.length}'),
          const SizedBox(height: 12),
          _field('Название предмета', _title),
          _field('Производитель', _manufacturer),
          _field('Автор формы', _shapeAuthor),
          _field('Автор росписи', _paintingAuthor),
          _field('Название формы', _shapeName),
          _field('Название росписи', _paintingName),
          _field('Год выпуска', _year, keyboard: TextInputType.number),
          _field('Период', _period),
          _field('Материал', _material),
          _field('Состояние', _condition),
          _field('Размер', _size),
          _field('Место нахождения / приобретения', _location),
          _field('Комментарий', _comment),
          SwitchListTile(
            title: const Text('Сделать предмет публичным'),
            value: _isPublic,
            onChanged: (value) => setState(() => _isPublic = value),
          ),
          const SizedBox(height: 8),
          FilledButton(onPressed: _loading ? null : _save, child: const Text('Сохранить в коллекцию')),
        ],
      ),
    );
  }
}
