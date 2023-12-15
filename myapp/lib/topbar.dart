import 'package:flutter/material.dart';

class Topbar extends StatelessWidget {
  const Topbar({Key? key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Sign Language Detector',
          style: TextStyle(
              color: Color.fromARGB(255, 0, 50, 126),
              fontWeight: FontWeight.bold),
        ),
        backgroundColor: Colors.blueAccent,
      ),
    );
  }
}