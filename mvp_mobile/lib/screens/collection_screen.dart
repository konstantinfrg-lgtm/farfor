import 'package:flutter/material.dart';

import '../models/item.dart';
import '../services/api_service.dart';
import '../widgets/item_card.dart';
import 'item_form_screen.dart';

class CollectionScreen extends StatefulWidget {
  const CollectionScreen({super.key});

  @override
  State<CollectionScreen> createState() => _CollectionScreenState();
}

class _CollectionScreenState extends State<CollectionScreen> {
  final _api = ApiService();
  final _search = TextEditingController();
  List<Item> _items = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _loading = true);
    try {
      final items = await _api.myItems(query: _search.text.trim().isEmpty ? null : _search.text.trim());
      setState(() => _items = items);
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Моя коллекция')),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
          await Navigator.of(context).push(MaterialPageRoute(builder: (_) => const ItemFormScreen()));
          _load();
        },
        label: const Text('Добавить предмет'),
        icon: const Icon(Icons.add_a_photo_outlined),
      ),
      body: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          children: [
            TextField(
              controller: _search,
              decoration: InputDecoration(
                labelText: 'Поиск по коллекции',
                suffixIcon: IconButton(icon: const Icon(Icons.search), onPressed: _load),
              ),
            ),
            const SizedBox(height: 8),
            Expanded(
              child: _loading
                  ? const Center(child: CircularProgressIndicator())
                  : ListView.builder(
                      itemCount: _items.length,
                      itemBuilder: (context, index) => ItemCard(item: _items[index]),
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
