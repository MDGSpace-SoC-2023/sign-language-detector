import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:myapp/main.dart';
import 'package:tflite/tflite.dart';
import './navbar.dart';
import 'dart:math';

class quiz extends StatefulWidget {
  const quiz({super.key});

  @override
  State<quiz> createState() => _quizState();
}

List<String> words = ['thumbsup', 'thumbsdown', 'livelong', 'thankyou'];

class _quizState extends State<quiz> {
  CameraImage? cameraImage;
  CameraController? cameraController;
  String output = " ";

  String randomWord = words[Random().nextInt(words.length)];
  @override
  void initState() {
    super.initState();
    loadModel();
    loadCamera();
  }

  loadCamera() {
    cameraController = CameraController(camera![0], ResolutionPreset.medium);
    cameraController!.initialize().then((value) {
      if (!mounted) {
        return;
      } else {
        setState(() {
          cameraController!.startImageStream((imageStream) {
            cameraImage = imageStream;
          });
        });
      }
    });
  }

  runModel(String path) async {
    var output = await Tflite.runModelOnImage(
      path: path,
      imageMean: 127.5,
      imageStd: 127.5,
      numResults: 2,
      threshold: 0.1,
      asynch: true,
    );
    return output;
  }

  loadModel() async {
    await Tflite.loadModel(
      model: "assets/detect.tflite",
      labels: "assets/label.txt",
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
      ),
      body: Column(
        children: <Widget>[
          Container(
            padding: const EdgeInsets.all(8.0),
            decoration: BoxDecoration(border: Border.all(color: Colors.black)),
            child: Text(randomWord),
          ),
          Padding(
            padding: const EdgeInsets.all(20),
            child: SizedBox(
              height: MediaQuery.of(context).size.height * 0.7,
              width: MediaQuery.of(context).size.width,
              child: !cameraController!.value.isInitialized
                  ? Container()
                  : AspectRatio(
                      aspectRatio: cameraController!.value.aspectRatio,
                      child: CameraPreview(cameraController!),
                    ),
            ),
          ),
          ElevatedButton(
            onPressed: () async {
              // Capture the image
              if (cameraController != null) {
                // Capture the image
                final XFile image = await cameraController!.takePicture();
                // Load the tflite model
                await Tflite.loadModel(
                  model: "assets/model.tflite",
                  labels: "assets/labels.txt",
                );
                // Run the model on the image
                var output = await runModel(image.path);
                // Check if the output matches the random word
                if (output[0]["label"] == randomWord) {
                  // If it matches, generate a new random word
                  setState(() {
                    randomWord = words[Random().nextInt(words.length)];
                  });
                }
              }
              ;
            },
            child: const Text('Capture and Match'),
          ),
          const Navbar()
        ],
      ),
    );
  }
}
