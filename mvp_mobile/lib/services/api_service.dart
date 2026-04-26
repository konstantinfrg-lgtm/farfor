import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../models/item.dart';

class ApiService {
  ApiService()
      : _dio = Dio(BaseOptions(baseUrl: _baseUrl)),
        _storage = const FlutterSecureStorage();

  static const String _baseUrl = 'http://10.0.2.2:8000/api';
  final Dio _dio;
  final FlutterSecureStorage _storage;

  Future<void> register({required String email, required String username, required String password}) async {
    await _dio.post('/auth/register', data: {'email': email, 'username': username, 'password': password});
  }

  Future<void> login({required String email, required String password}) async {
    final response = await _dio.post('/auth/login', data: {'email': email, 'password': password});
    await _storage.write(key: 'token', value: response.data['access_token'] as String);
  }

  Future<List<Item>> myItems({String? query}) async {
    final token = await _storage.read(key: 'token');
    final response = await _dio.get(
      '/items/me',
      queryParameters: {'q': query},
      options: Options(headers: {'Authorization': 'Bearer $token'}),
    );
    return (response.data as List<dynamic>).map((it) => Item.fromJson(it as Map<String, dynamic>)).toList();
  }

  Future<String> uploadPhoto(File file) async {
    final token = await _storage.read(key: 'token');
    final formData = FormData.fromMap({
      'file': await MultipartFile.fromFile(file.path, filename: file.uri.pathSegments.last),
    });
    final response = await _dio.post(
      '/items/upload',
      data: formData,
      options: Options(headers: {'Authorization': 'Bearer $token'}),
    );
    return response.data['url'] as String;
  }

  Future<void> createItem(Map<String, dynamic> payload) async {
    final token = await _storage.read(key: 'token');
    await _dio.post('/items', data: payload, options: Options(headers: {'Authorization': 'Bearer $token'}));
  }
}
