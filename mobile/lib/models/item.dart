class Photo {
  final int id;
  final int itemId;
  final String filePath;
  final bool isMain;

  Photo({
    required this.id,
    required this.itemId,
    required this.filePath,
    required this.isMain,
  });

  factory Photo.fromJson(Map<String, dynamic> json) {
    return Photo(
      id: json['id'],
      itemId: json['item_id'],
      filePath: json['file_path'],
      isMain: json['is_main'] ?? false,
    );
  }
}

class Item {
  final int id;
  final int userId;
  final String? manufacturer;
  final String? authorForm;
  final String? authorDecoration;
  final String? formName;
  final String? decorationName;
  final String? yearIssue;
  final String? period;
  final String? material;
  final String? condition;
  final String? size;
  final String? location;
  final String? comment;
  final bool isPublic;
  final List<Photo> photos;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  Item({
    required this.id,
    required this.userId,
    this.manufacturer,
    this.authorForm,
    this.authorDecoration,
    this.formName,
    this.decorationName,
    this.yearIssue,
    this.period,
    this.material,
    this.condition,
    this.size,
    this.location,
    this.comment,
    this.isPublic = false,
    this.photos = const [],
    this.createdAt,
    this.updatedAt,
  });

  factory Item.fromJson(Map<String, dynamic> json) {
    List<Photo> photos = [];
    if (json['photos'] != null) {
      photos = (json['photos'] as List).map((p) => Photo.fromJson(p)).toList();
    }

    return Item(
      id: json['id'],
      userId: json['user_id'],
      manufacturer: json['manufacturer'],
      authorForm: json['author_form'],
      authorDecoration: json['author_decoration'],
      formName: json['form_name'],
      decorationName: json['decoration_name'],
      yearIssue: json['year_issue'],
      period: json['period'],
      material: json['material'],
      condition: json['condition'],
      size: json['size'],
      location: json['location'],
      comment: json['comment'],
      isPublic: json['is_public'] ?? false,
      photos: photos,
      createdAt: json['created_at'] != null ? DateTime.parse(json['created_at']) : null,
      updatedAt: json['updated_at'] != null ? DateTime.parse(json['updated_at']) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'manufacturer': manufacturer,
      'author_form': authorForm,
      'author_decoration': authorDecoration,
      'form_name': formName,
      'decoration_name': decorationName,
      'year_issue': yearIssue,
      'period': period,
      'material': material,
      'condition': condition,
      'size': size,
      'location': location,
      'comment': comment,
      'is_public': isPublic,
    };
  }
}
