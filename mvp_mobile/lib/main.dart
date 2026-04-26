import 'package:flutter/material.dart';

import 'screens/login_screen.dart';

void main() {
  runApp(const FarforApp());
}

class FarforApp extends StatelessWidget {
  const FarforApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Фарфор. Коллекция',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF7C8A7A),
          surface: const Color(0xFFF5F2EA),
        ),
        scaffoldBackgroundColor: const Color(0xFFF8F6F1),
        appBarTheme: const AppBarTheme(centerTitle: true),
      ),
      home: const LoginScreen(),
    );
  }
}
