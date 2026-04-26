import 'package:flutter/material.dart';
import '../models/user.dart';
import '../services/api_service.dart';

class AuthProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();
  User? _currentUser;
  bool _isLoading = false;

  User? get currentUser => _currentUser;
  bool get isLoading => _isLoading;
  bool get isAuthenticated => _currentUser != null;

  Future<void> checkAuth() async {
    try {
      final token = await _apiService.getToken();
      if (token != null) {
        _currentUser = await _apiService.getCurrentUser();
        notifyListeners();
      }
    } catch (e) {
      // Token invalid or expired
    }
  }

  Future<void> register({
    required String email,
    required String password,
    String? fullName,
  }) async {
    _isLoading = true;
    notifyListeners();
    
    try {
      await _apiService.register(
        email: email,
        password: password,
        fullName: fullName,
      );
      await login(email: email, password: password);
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> login({
    required String email,
    required String password,
  }) async {
    _isLoading = true;
    notifyListeners();
    
    try {
      await _apiService.login(email: email, password: password);
      _currentUser = await _apiService.getCurrentUser();
      notifyListeners();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> logout() async {
    await _apiService.logout();
    _currentUser = null;
    notifyListeners();
  }
}
