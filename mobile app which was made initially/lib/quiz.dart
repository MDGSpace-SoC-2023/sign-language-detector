import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:tflite/tflite.dart';
import 'dart:math';

class quiz extends StatefulWidget {
  const quiz({Key? key}) : super(key: key);

  @override
  State<quiz> createState() => _QuizState();
}

List<String> words = ['thumbsup', 'thumbsdown', 'livelong', 'thankyou'];

class _QuizState extends State<quiz> {
  CameraImage? cameraImage;
  CameraController? cameraController;
  String output = "";
  List<CameraDescription>? cameras;

  String randomWord = words[Random().nextInt(words.length)];

  @override
  void initState() {
    super.initState();
    initializeCamera().then((_) {
      loadCamera();
    });
    loadModel();
  }

  Future<void> initializeCamera() async {
    cameras = await availableCameras();
  }

  void loadCamera() {
    if (cameras != null && cameras!.isNotEmpty) {
      cameraController = CameraController(cameras![0], ResolutionPreset.medium);
      cameraController!.initialize().then((_) {
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
  }

  runModel() async {
    if (cameraImage != null) {
      var predictions = await Tflite.runModelOnFrame(
        bytesList: cameraImage!.planes.map((plane) => plane.bytes).toList(),
        imageHeight: cameraImage!.height,
        imageWidth: cameraImage!.width,
        imageMean: 127.5,
        imageStd: 127.5,
        rotation: 90,
        numResults: 2,
        threshold: 0.1,
        asynch: true,
      );
      if (predictions != null && predictions.isNotEmpty) {
        setState(() {
          output = predictions[0]["label"] ?? "No label found";
        });
      }
    }
  }

  Future<void> loadModel() async {
    await Tflite.loadModel(
      model: "assets/detect.tflite",
      labels: "assets/labels.txt",
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: const Text(
          "QUIZ",
          style: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: <Widget>[
            Container(
              padding: const EdgeInsets.all(8.0),
              decoration:
                  BoxDecoration(border: Border.all(color: Colors.black)),
              child: Text(randomWord),
            ),
            Padding(
              padding: const EdgeInsets.all(20),
              child: SizedBox(
                height: MediaQuery.of(context).size.height * 0.7,
                width: MediaQuery.of(context).size.width,
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(
                      10.0), // Optional: Add border radius
                  child: cameraController != null &&
                          cameraController!.value.isInitialized
                      ? AspectRatio(
                          aspectRatio: cameraController!.value.aspectRatio,
                          child: CameraPreview(cameraController!),
                        )
                      : Container(),
                ),
              ),
            ),
            ElevatedButton(
              onPressed: () {
                runModel(); // Run model when the button is pressed
              },
              child: const Text('Capture and Match '),
            ),
            Padding(
              padding: EdgeInsets.all(20),
              child: output == randomWord
                  ? () {
                      setState(() {
                        randomWord = words[Random().nextInt(words.length)];
                      });
                      return Text("Correct");
                    }()
                  : Text("Incorrect"),
            ),
            SizedBox(height: 20), // Add some space at the bottom
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    cameraController?.dispose();
    super.dispose();
  }
}
