class Item {
  Item({
    required this.id,
    required this.title,
    required this.manufacturer,
    required this.isPublic,
    required this.photoUrls,
    this.material,
    this.period,
    this.location,
    this.comment,
  });

  final int id;
  final String title;
  final String manufacturer;
  final bool isPublic;
  final List<String> photoUrls;
  final String? material;
  final String? period;
  final String? location;
  final String? comment;

  factory Item.fromJson(Map<String, dynamic> json) {
    final photos = (json['photos'] as List<dynamic>? ?? [])
        .map((p) => p['url'] as String)
        .toList();

    return Item(
      id: json['id'] as int,
      title: json['title'] as String,
      manufacturer: json['manufacturer'] as String,
      isPublic: json['is_public'] as bool? ?? false,
      photoUrls: photos,
      material: json['material'] as String?,
      period: json['period'] as String?,
      location: json['location'] as String?,
      comment: json['comment'] as String?,
    );
  }
}
