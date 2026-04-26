import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../models/user.dart';
import '../models/item.dart';

class ApiService {
  // Замените на адрес вашего сервера
  static const String baseUrl = 'http://localhost:8000';
  
  final _storage = const FlutterSecureStorage();
  
  // ==================== AUTH ====================
  
  Future<Map<String, dynamic>> register({
    required String email,
    required String password,
    String? fullName,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'password': password,
        'full_name': fullName,
      }),
    );
    
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Ошибка регистрации: ${response.body}');
    }
  }
  
  Future<String> login({
    required String email,
    required String password,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: 'username=$email&password=$password',
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final token = data['access_token'];
      await _storage.write(key: 'auth_token', value: token);
      return token;
    } else {
      throw Exception('Ошибка входа: ${response.body}');
    }
  }
  
  Future<void> logout() async {
    await _storage.delete(key: 'auth_token');
  }
  
  Future<String?> getToken() async {
    return await _storage.read(key: 'auth_token');
  }
  
  Future<User> getCurrentUser() async {
    final token = await getToken();
    if (token == null) throw Exception('Не авторизован');
    
    final response = await http.get(
      Uri.parse('$baseUrl/auth/me'),
      headers: {'Authorization': 'Bearer $token'},
    );
    
    if (response.statusCode == 200) {
      return User.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Ошибка получения пользователя: ${response.body}');
    }
  }
  
  // ==================== ITEMS ====================
  
  Future<List<Item>> getItems({
    bool myCollection = false,
    String? search,
    String? manufacturer,
    String? authorForm,
    String? authorDecoration,
    String? formName,
    String? decorationName,
    String? period,
  }) async {
    final token = await getToken();
    if (token == null) throw Exception('Не авторизован');
    
    var uri = Uri.parse('$baseUrl/items').replace(queryParameters: {
      if (myCollection) 'my_collection': 'true',
      if (search != null) 'search': search,
      if (manufacturer != null) 'manufacturer': manufacturer,
      if (authorForm != null) 'author_form': authorForm,
      if (authorDecoration != null) 'author_decoration': authorDecoration,
      if (formName != null) 'form_name': formName,
      if (decorationName != null) 'decoration_name': decorationName,
      if (period != null) 'period': period,
    });
    
    final response = await http.get(
      uri,
      headers: {'Authorization': 'Bearer $token'},
    );
    
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((item) => Item.fromJson(item)).toList();
    } else {
      throw Exception('Ошибка получения предметов: ${response.body}');
    }
  }
  
  Future<Item> getItem(int itemId) async {
    final token = await getToken();
    if (token == null) throw Exception('Не авторизован');
    
    final response = await http.get(
      Uri.parse('$baseUrl/items/$itemId'),
      headers: {'Authorization': 'Bearer $token'},
    );
    
    if (response.statusCode == 200) {
      return Item.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Ошибка получения предмета: ${response.body}');
    }
  }
  
  Future<Item> createItem({
    Map<String, String?>? attributes,
    List<File>? photos,
    bool isPublic = false,
  }) async {
    final token = await getToken();
    if (token == null) throw Exception('Не авторизован');
    
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/items'),
    );
    
    request.headers['Authorization'] = 'Bearer $token';
    request.fields['is_public'] = isPublic.toString();
    
    if (attributes != null) {
      attributes.forEach((key, value) {
        if (value != null && value.isNotEmpty) {
          request.fields[key] = value;
        }
      });
    }
    
    if (photos != null) {
      for (var photo in photos) {
        request.files.add(await http.MultipartFile.fromPath(
          'photos',
          photo.path,
        ));
      }
    }
    
    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);
    
    if (response.statusCode == 200) {
      return Item.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Ошибка создания предмета: ${response.body}');
    }
  }
  
  Future<Item> updateItem({
    required int itemId,
    Map<String, String?>? attributes,
    List<File>? photos,
    bool? isPublic,
  }) async {
    final token = await getToken();
    if (token == null) throw Exception('Не авторизован');
    
    var request = http.MultipartRequest(
      'PUT',
      Uri.parse('$baseUrl/items/$itemId'),
    );
    
    request.headers['Authorization'] = 'Bearer $token';
    if (isPublic != null) {
      request.fields['is_public'] = isPublic.toString();
    }
    
    if (attributes != null) {
      attributes.forEach((key, value) {
        if (value != null) {
          request.fields[key] = value;
        }
      });
    }
    
    if (photos != null) {
      for (var photo in photos) {
        request.files.add(await http.MultipartFile.fromPath(
          'photos',
          photo.path,
        ));
      }
    }
    
    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);
    
    if (response.statusCode == 200) {
      return Item.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Ошибка обновления предмета: ${response.body}');
    }
  }
  
  Future<void> deleteItem(int itemId) async {
    final token = await getToken();
    if (token == null) throw Exception('Не авторизован');
    
    final response = await http.delete(
      Uri.parse('$baseUrl/items/$itemId'),
      headers: {'Authorization': 'Bearer $token'},
    );
    
    if (response.statusCode != 200) {
      throw Exception('Ошибка удаления предмета: ${response.body}');
    }
  }
  
  Future<void> deletePhoto(int itemId, int photoId) async {
    final token = await getToken();
    if (token == null) throw Exception('Не авторизован');
    
    final response = await http.delete(
      Uri.parse('$baseUrl/items/$itemId/photos/$photoId'),
      headers: {'Authorization': 'Bearer $token'},
    );
    
    if (response.statusCode != 200) {
      throw Exception('Ошибка удаления фото: ${response.body}');
    }
  }
  
  // ==================== PUBLIC ITEMS ====================
  
  Future<List<Item>> getPublicItems({
    String? search,
    String? manufacturer,
    String? authorForm,
    String? authorDecoration,
    String? formName,
    String? decorationName,
    String? period,
  }) async {
    var uri = Uri.parse('$baseUrl/public/items').replace(queryParameters: {
      if (search != null) 'search': search,
      if (manufacturer != null) 'manufacturer': manufacturer,
      if (authorForm != null) 'author_form': authorForm,
      if (authorDecoration != null) 'author_decoration': authorDecoration,
      if (formName != null) 'form_name': formName,
      if (decorationName != null) 'decoration_name': decorationName,
      if (period != null) 'period': period,
    });
    
    final response = await http.get(uri);
    
    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((item) => Item.fromJson(item)).toList();
    } else {
      throw Exception('Ошибка получения публичных предметов: ${response.body}');
    }
  }
}
