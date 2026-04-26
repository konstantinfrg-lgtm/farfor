import 'package:flutter/material.dart';

import '../services/api_service.dart';
import 'collection_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _api = ApiService();
  final _email = TextEditingController();
  final _password = TextEditingController();
  final _username = TextEditingController();
  bool _isRegister = false;
  bool _loading = false;

  Future<void> _submit() async {
    setState(() => _loading = true);
    try {
      if (_isRegister) {
        await _api.register(email: _email.text.trim(), username: _username.text.trim(), password: _password.text);
      }
      await _api.login(email: _email.text.trim(), password: _password.text);
      if (!mounted) return;
      Navigator.of(context).pushReplacement(MaterialPageRoute(builder: (_) => const CollectionScreen()));
    } catch (_) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Ошибка авторизации')));
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Фарфор. Коллекция')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(controller: _email, decoration: const InputDecoration(labelText: 'Email')),
            if (_isRegister) TextField(controller: _username, decoration: const InputDecoration(labelText: 'Имя пользователя')),
            TextField(controller: _password, obscureText: true, decoration: const InputDecoration(labelText: 'Пароль')),
            const SizedBox(height: 16),
            FilledButton(onPressed: _loading ? null : _submit, child: Text(_isRegister ? 'Зарегистрироваться' : 'Войти')),
            TextButton(
              onPressed: () => setState(() => _isRegister = !_isRegister),
              child: Text(_isRegister ? 'У меня уже есть аккаунт' : 'Создать аккаунт'),
            ),
          ],
        ),
      ),
    );
  }
}
