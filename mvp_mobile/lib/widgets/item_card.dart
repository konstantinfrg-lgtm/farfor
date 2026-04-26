import 'package:flutter/material.dart';

import '../models/item.dart';

class ItemCard extends StatelessWidget {
  const ItemCard({super.key, required this.item});

  final Item item;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (item.photoUrls.isNotEmpty)
              ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: Image.network(
                  item.photoUrls.first,
                  height: 180,
                  width: double.infinity,
                  fit: BoxFit.cover,
                ),
              ),
            const SizedBox(height: 8),
            Text(item.title, style: Theme.of(context).textTheme.titleMedium),
            Text('Производитель: ${item.manufacturer}'),
            if (item.material != null) Text('Материал: ${item.material}'),
            if (item.period != null) Text('Период: ${item.period}'),
            Text(item.isPublic ? 'Публичный предмет' : 'Приватный предмет'),
          ],
        ),
      ),
    );
  }
}
