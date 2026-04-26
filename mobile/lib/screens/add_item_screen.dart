import 'package:flutter/material.dart';
import 'dart:io';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';
import '../models/item.dart';

class AddItemScreen extends StatefulWidget {
  const AddItemScreen({super.key});

  @override
  State<AddItemScreen> createState() => _AddItemScreenState();
}

class _AddItemScreenState extends State<AddItemScreen> {
  final _formKey = GlobalKey<FormState>();
  final ApiService _apiService = ApiService();
  final ImagePicker _picker = ImagePicker();

  // Controllers for form fields
  final _manufacturerController = TextEditingController();
  final _authorFormController = TextEditingController();
  final _authorDecorationController = TextEditingController();
  final _formNameController = TextEditingController();
  final _decorationNameController = TextEditingController();
  final _yearIssueController = TextEditingController();
  final _periodController = TextEditingController();
  final _materialController = TextEditingController();
  final _conditionController = TextEditingController();
  final _sizeController = TextEditingController();
  final _locationController = TextEditingController();
  final _commentController = TextEditingController();

  List<File> _photos = [];
  bool _isPublic = false;
  bool _isLoading = false;

  @override
  void dispose() {
    _manufacturerController.dispose();
    _authorFormController.dispose();
    _authorDecorationController.dispose();
    _formNameController.dispose();
    _decorationNameController.dispose();
    _yearIssueController.dispose();
    _periodController.dispose();
    _materialController.dispose();
    _conditionController.dispose();
    _sizeController.dispose();
    _locationController.dispose();
    _commentController.dispose();
    super.dispose();
  }

  Future<void> _pickImages(ImageSource source) async {
    try {
      final pickedFiles = await _picker.pickMultiImage(source: source);
      if (pickedFiles != null) {
        setState(() {
          _photos.addAll(pickedFiles.map((f) => File(f.path)).toList());
        });
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Ошибка выбора фото: $e')),
        );
      }
    }
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    try {
      final attributes = <String, String?>{
        'manufacturer': _manufacturerController.text.trim(),
        'author_form': _authorFormController.text.trim(),
        'author_decoration': _authorDecorationController.text.trim(),
        'form_name': _formNameController.text.trim(),
        'decoration_name': _decorationNameController.text.trim(),
        'year_issue': _yearIssueController.text.trim(),
        'period': _periodController.text.trim(),
        'material': _materialController.text.trim(),
        'condition': _conditionController.text.trim(),
        'size': _sizeController.text.trim(),
        'location': _locationController.text.trim(),
        'comment': _commentController.text.trim(),
      };

      await _apiService.createItem(
        attributes: attributes,
        photos: _photos.isNotEmpty ? _photos : null,
        isPublic: _isPublic,
      );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Предмет успешно добавлен!')),
        );
        Navigator.pop(context);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Ошибка: $e')),
        );
      }
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Добавить предмет'),
        actions: [
          TextButton(
            onPressed: _isLoading ? null : _submit,
            child: _isLoading
                ? const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Text('Сохранить'),
          ),
        ],
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // Photo section
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Фотографии',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 12),
                    if (_photos.isEmpty)
                      Center(
                        child: Column(
                          children: [
                            Icon(Icons.add_photo_alternate_outlined,
                                size: 48, color: Colors.grey[400]),
                            const SizedBox(height: 8),
                            Text(
                              'Нет фотографий',
                              style: TextStyle(color: Colors.grey[600]),
                            ),
                          ],
                        ),
                      )
                    else
                      SizedBox(
                        height: 100,
                        child: ListView.builder(
                          scrollDirection: Axis.horizontal,
                          itemCount: _photos.length,
                          itemBuilder: (context, index) {
                            return Stack(
                              margin: const EdgeInsets.only(right: 8),
                              children: [
                                ClipRRect(
                                  borderRadius: BorderRadius.circular(8),
                                  child: Image.file(
                                    _photos[index],
                                    height: 100,
                                    width: 100,
                                    fit: BoxFit.cover,
                                  ),
                                ),
                                Positioned(
                                  top: 4,
                                  right: 4,
                                  child: IconButton(
                                    icon: const CircleAvatar(
                                      backgroundColor: Colors.red,
                                      radius: 12,
                                      child: Icon(Icons.close,
                                          size: 14, color: Colors.white),
                                    ),
                                    onPressed: () {
                                      setState(() => _photos.removeAt(index));
                                    },
                                  ),
                                ),
                              ],
                            );
                          },
                        ),
                      ),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        ElevatedButton.icon(
                          onPressed: () => _pickImages(ImageSource.camera),
                          icon: const Icon(Icons.camera_alt),
                          label: const Text('Камера'),
                        ),
                        const SizedBox(width: 8),
                        ElevatedButton.icon(
                          onPressed: () => _pickImages(ImageSource.gallery),
                          icon: const Icon(Icons.photo_library),
                          label: const Text('Галерея'),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 16),

            // Main info
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Основная информация',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: _formNameController,
                      decoration: const InputDecoration(
                        labelText: 'Название формы',
                        prefixIcon: Icon(Icons.category),
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: _decorationNameController,
                      decoration: const InputDecoration(
                        labelText: 'Название росписи',
                        prefixIcon: Icon(Icons.palette),
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: _manufacturerController,
                      decoration: const InputDecoration(
                        labelText: 'Производитель',
                        prefixIcon: Icon(Icons.business),
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: _authorFormController,
                      decoration: const InputDecoration(
                        labelText: 'Автор формы',
                        prefixIcon: Icon(Icons.person),
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: _authorDecorationController,
                      decoration: const InputDecoration(
                        labelText: 'Автор росписи',
                        prefixIcon: Icon(Icons.brush),
                      ),
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 16),

            // Details
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Детали',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),
                    Row(
                      children: [
                        Expanded(
                          child: TextFormField(
                            controller: _yearIssueController,
                            decoration: const InputDecoration(
                              labelText: 'Год выпуска',
                              prefixIcon: Icon(Icons.calendar_today),
                            ),
                            keyboardType: TextInputType.number,
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: TextFormField(
                            controller: _periodController,
                            decoration: const InputDecoration(
                              labelText: 'Период',
                              prefixIcon: Icon(Icons.date_range),
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: _materialController,
                      decoration: const InputDecoration(
                        labelText: 'Материал',
                        prefixIcon: Icon(Icons.science),
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: _conditionController,
                      decoration: const InputDecoration(
                        labelText: 'Состояние',
                        prefixIcon: Icon(Icons.info_outline),
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: _sizeController,
                      decoration: const InputDecoration(
                        labelText: 'Размер',
                        prefixIcon: Icons.straighten,
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: _locationController,
                      decoration: const InputDecoration(
                        labelText: 'Место нахождения/приобретения',
                        prefixIcon: Icon(Icons.location_on_outlined),
                      ),
                      maxLines: 2,
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: _commentController,
                      decoration: const InputDecoration(
                        labelText: 'Комментарий',
                        prefixIcon: Icon(Icons.comment_outlined),
                      ),
                      maxLines: 3,
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 16),

            // Visibility
            Card(
              child: ListTile(
                leading: Icon(_isPublic ? Icons.public : Icons.lock),
                title: const Text('Видимость'),
                subtitle: Text(
                  _isPublic ? 'Публичный предмет' : 'Только для вас',
                ),
                trailing: Switch(
                  value: _isPublic,
                  onChanged: (value) => setState(() => _isPublic = value),
                ),
              ),
            ),

            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }
}
