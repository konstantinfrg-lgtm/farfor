import 'package:flutter/material.dart';
import 'dart:io';
import 'package:photo_view/photo_view.dart';
import 'package:photo_view/photo_view_gallery.dart';
import '../services/api_service.dart';
import '../models/item.dart';

class ItemDetailScreen extends StatefulWidget {
  final Item item;

  const ItemDetailScreen({super.key, required this.item});

  @override
  State<ItemDetailScreen> createState() => _ItemDetailScreenState();
}

class _ItemDetailScreenState extends State<ItemDetailScreen> {
  final ApiService _apiService = ApiService();
  late Item _item;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _item = widget.item;
  }

  Future<void> _deleteItem() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Удаление предмета'),
        content: const Text('Вы действительно хотите удалить этот предмет? Это действие нельзя отменить.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Отмена'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Удалить'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      setState(() => _isLoading = true);
      try {
        await _apiService.deleteItem(_item.id);
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Предмет удален')),
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
  }

  Future<void> _toggleVisibility() async {
    try {
      final updatedItem = await _apiService.updateItem(
        itemId: _item.id,
        isPublic: !_item.isPublic,
      );
      setState(() => _item = updatedItem);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              _item.isPublic ? 'Предмет теперь публичный' : 'Предмет теперь приватный',
            ),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Ошибка: $e')),
        );
      }
    }
  }

  void _viewPhotos(int index) {
    if (_item.photos.isEmpty) return;

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => PhotoGalleryScreen(photos: _item.photos, initialIndex: index),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Предмет'),
        actions: [
          IconButton(
            icon: Icon(_item.isPublic ? Icons.public : Icons.lock),
            tooltip: _item.isPublic ? 'Публичный' : 'Приватный',
            onPressed: _toggleVisibility,
          ),
          PopupMenuButton<String>(
            onSelected: (value) {
              if (value == 'delete') _deleteItem();
            },
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'delete',
                child: Row(
                  children: [
                    Icon(Icons.delete, color: Colors.red),
                    SizedBox(width: 8),
                    Text('Удалить', style: TextStyle(color: Colors.red)),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // Photos
                if (_item.photos.isNotEmpty)
                  SizedBox(
                    height: 300,
                    child: PageView.builder(
                      itemCount: _item.photos.length,
                      itemBuilder: (context, index) {
                        final photo = _item.photos[index];
                        return GestureDetector(
                          onTap: () => _viewPhotos(index),
                          child: Hero(
                            tag: 'photo_${photo.id}',
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(12),
                              child: Image.network(
                                '${ApiService.baseUrl}/${photo.filePath}',
                                fit: BoxFit.cover,
                                errorBuilder: (_, __, ___) => Container(
                                  color: Colors.grey[200],
                                  child: const Icon(Icons.broken_image),
                                ),
                              ),
                            ),
                          ),
                        );
                      },
                    ),
                  )
                else
                  Container(
                    height: 200,
                    decoration: BoxDecoration(
                      color: Colors.grey[200],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.image_not_supported, size: 48, color: Colors.grey),
                        SizedBox(height: 8),
                        Text('Нет фотографий', style: TextStyle(color: Colors.grey)),
                      ],
                    ),
                  ),

                if (_item.photos.length > 1) ...[
                  const SizedBox(height: 8),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: List.generate(
                      _item.photos.length,
                      (index) => Container(
                        margin: const EdgeInsets.symmetric(horizontal: 4),
                        width: 8,
                        height: 8,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: index == 0 ? Theme.of(context).primaryColor : Colors.grey[300],
                        ),
                      ),
                    ),
                  ),
                ],

                const SizedBox(height: 24),

                // Status chip
                Row(
                  children: [
                    Chip(
                      avatar: Icon(
                        _item.isPublic ? Icons.public : Icons.lock,
                        size: 18,
                        color: _item.isPublic ? Colors.green : Colors.grey,
                      ),
                      label: Text(_item.isPublic ? 'Публичный' : 'Приватный'),
                      backgroundColor: _item.isPublic ? Colors.green[50] : Colors.grey[200],
                    ),
                    const SizedBox(width: 8),
                    if (_item.photos.isNotEmpty)
                      Chip(
                        avatar: const Icon(Icons.photo, size: 18),
                        label: Text('${_item.photos.length} фото'),
                      ),
                  ],
                ),

                const SizedBox(height: 24),

                // Info sections
                _buildInfoSection(
                  'Основная информация',
                  [
                    if (_item.formName != null) _buildInfoRow('Название формы', _item.formName!),
                    if (_item.decorationName != null) _buildInfoRow('Название росписи', _item.decorationName!),
                    if (_item.manufacturer != null) _buildInfoRow('Производитель', _item.manufacturer!),
                    if (_item.authorForm != null) _buildInfoRow('Автор формы', _item.authorForm!),
                    if (_item.authorDecoration != null) _buildInfoRow('Автор росписи', _item.authorDecoration!),
                  ],
                ),

                const SizedBox(height: 16),

                _buildInfoSection(
                  'Детали',
                  [
                    if (_item.yearIssue != null) _buildInfoRow('Год выпуска', _item.yearIssue!),
                    if (_item.period != null) _buildInfoRow('Период', _item.period!),
                    if (_item.material != null) _buildInfoRow('Материал', _item.material!),
                    if (_item.condition != null) _buildInfoRow('Состояние', _item.condition!),
                    if (_item.size != null) _buildInfoRow('Размер', _item.size!),
                    if (_item.location != null) _buildInfoRow('Место', _item.location!),
                  ],
                ),

                if (_item.comment != null && _item.comment!.isNotEmpty) ...[
                  const SizedBox(height: 16),
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Комментарий',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: Color(0xFF5D4037),
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(_item.comment!),
                        ],
                      ),
                    ),
                  ),
                ],
              ],
            ),
    );
  }

  Widget _buildInfoSection(String title, List<Widget> children) {
    if (children.isEmpty) return const SizedBox.shrink();

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: Color(0xFF5D4037),
              ),
            ),
            const Divider(),
            ...children,
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 140,
            child: Text(
              '$label:',
              style: TextStyle(color: Colors.grey[600]),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(fontWeight: FontWeight.w500),
            ),
          ),
        ],
      ),
    );
  }
}

class PhotoGalleryScreen extends StatelessWidget {
  final List<dynamic> photos;
  final int initialIndex;

  const PhotoGalleryScreen({super.key, required this.photos, this.initialIndex = 0});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: Colors.black,
        leading: IconButton(
          icon: const Icon(Icons.close, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: PhotoViewGallery.builder(
        scrollDirection: Axis.horizontal,
        builder: (context, index) {
          final photo = photos[index];
          return PhotoViewGalleryPageOptions(
            imageProvider: NetworkImage('${ApiService.baseUrl}/${photo['file_path'] ?? photo.filePath}'),
            initialScale: PhotoViewComputedScale.contained,
            heroAttributes: PhotoViewHeroAttributes(tag: 'photo_${photo['id'] ?? photo.id}'),
          );
        },
        itemCount: photos.length,
        loadingBuilder: (context, event) => const Center(
          child: CircularProgressIndicator(color: Colors.white),
        ),
        pageController: PageController(initialPage: initialIndex),
      ),
    );
  }
}
