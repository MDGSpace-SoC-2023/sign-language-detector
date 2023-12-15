import 'package:flutter/material.dart';

import './home.dart';
import 'package:camera/camera.dart';

List<CameraDescription>? camera;

void main() async{
  WidgetsFlutterBinding.ensureInitialized();
  camera= await availableCameras();
  runApp(myapp());
}

class myapp extends StatelessWidget {
  const myapp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(primaryColor: Colors.black),
      debugShowCheckedModeBanner: false,
      home: const Home(),
    );
  }
}






