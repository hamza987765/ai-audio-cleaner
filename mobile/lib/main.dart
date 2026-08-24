import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const AudioCleanerApp());
}

class AudioCleanerApp extends StatelessWidget {
  const AudioCleanerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'AI Audio Cleaner',
      theme: ThemeData(
        brightness: Brightness.dark,
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}
