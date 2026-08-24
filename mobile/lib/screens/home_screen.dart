import 'dart:io';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';

import '../services/api_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  File? selectedVideo;

  List<String> layers = [];

  List<String> selectedLayers = [];

  bool processing = false;

  Future<void> pickVideo() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.video,
    );

    if (result == null) return;

    setState(() {
      selectedVideo = File(
        result.files.single.path!,
      );
    });
  }

  Future<void> uploadVideo() async {
    if (selectedVideo == null) return;

    setState(() {
      processing = true;
    });

    final response = await ApiService.uploadVideo(
      selectedVideo!,
    );

    setState(() {
      layers = List<String>.from(
        response["layers"],
      );

      selectedLayers = List<String>.from(
        response["layers"],
      );

      processing = false;
    });
  }

  Future<void> downloadVideo() async {
    final bytes = await ApiService.downloadVideo();

    final directory = await getApplicationDocumentsDirectory();

    final file = File(
      "${directory.path}/cleaned_video.mp4",
    );

    await file.writeAsBytes(bytes);

    if (!mounted) return;

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          "Saved to:\n${file.path}",
        ),
      ),
    );
  }

  Future<void> renderVideo() async {
    setState(() {
      processing = true;
    });

    await ApiService.renderVideo(
      selectedLayers,
    );

    await downloadVideo();

    setState(() {
      processing = false;
    });

    if (!mounted) return;

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text(
          "Video Rendered Successfully",
        ),
      ),
    );
  }

  IconData getLayerIcon(String layer) {
    if (layer.contains("Speech")) {
      return Icons.mic;
    }

    if (layer.contains("Music")) {
      return Icons.music_note;
    }

    if (layer.contains("Drums")) {
      return Icons.album;
    }

    if (layer.contains("Bass")) {
      return Icons.graphic_eq;
    }

    return Icons.audiotrack;
  }

  String getLayerDescription(String layer) {
    if (layer.contains("Speech")) {
      return "Human voices and dialogue";
    }

    if (layer.contains("Music")) {
      return "Music and melodies";
    }

    if (layer.contains("Drums")) {
      return "Percussion sounds";
    }

    if (layer.contains("Bass")) {
      return "Low-frequency instruments";
    }

    return "Audio layer";
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(
        0xFF0F172A,
      ),
      appBar: AppBar(
        backgroundColor: const Color(
          0xFF0F172A,
        ),
        elevation: 0,
        centerTitle: true,
        title: const Text(
          "AI Audio Cleaner",
          style: TextStyle(
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(
          20,
        ),
        child: Column(
          children: [
            const Icon(
              Icons.auto_awesome,
              size: 70,
              color: Colors.cyan,
            ),
            const SizedBox(
              height: 10,
            ),
            const Text(
              "Separate and Rebuild Audio Using AI",
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 18,
                color: Colors.white70,
              ),
            ),
            const SizedBox(
              height: 30,
            ),
            Container(
              padding: const EdgeInsets.all(
                20,
              ),
              decoration: BoxDecoration(
                color: const Color(
                  0xFF1E293B,
                ),
                borderRadius: BorderRadius.circular(
                  20,
                ),
              ),
              child: Column(
                children: [
                  const Row(
                    children: [
                      Icon(
                        Icons.video_file,
                        color: Colors.cyan,
                      ),
                      SizedBox(width: 10),
                      Text(
                        "Selected Video",
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(
                    height: 15,
                  ),
                  Text(
                    selectedVideo == null
                        ? "No video selected"
                        : selectedVideo!.path.split("\\").last,
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(
                    height: 20,
                  ),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      onPressed: pickVideo,
                      icon: const Icon(
                        Icons.upload_file,
                      ),
                      label: const Text(
                        "Choose Video",
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(
              height: 20,
            ),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: selectedVideo == null ? null : uploadVideo,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.all(
                    18,
                  ),
                ),
                child: const Text(
                  "Upload & Analyze",
                ),
              ),
            ),
            const SizedBox(
              height: 25,
            ),
            if (layers.isNotEmpty)
              Container(
                padding: const EdgeInsets.all(
                  20,
                ),
                decoration: BoxDecoration(
                  color: const Color(
                    0xFF1E293B,
                  ),
                  borderRadius: BorderRadius.circular(
                    20,
                  ),
                ),
                child: Column(
                  children: [
                    const Text(
                      "Audio Layers",
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(
                      height: 15,
                    ),
                    ...layers.map(
                      (layer) {
                        return SwitchListTile(
                          secondary: Icon(
                            getLayerIcon(
                              layer,
                            ),
                            color: Colors.cyan,
                          ),
                          title: Text(
                            layer.replaceAll(
                              ".wav",
                              "",
                            ),
                          ),
                          subtitle: Text(
                            getLayerDescription(
                              layer,
                            ),
                          ),
                          value: selectedLayers.contains(
                            layer,
                          ),
                          onChanged: (value) {
                            setState(
                              () {
                                if (value) {
                                  selectedLayers.add(
                                    layer,
                                  );
                                } else {
                                  selectedLayers.remove(
                                    layer,
                                  );
                                }
                              },
                            );
                          },
                        );
                      },
                    ),
                  ],
                ),
              ),
            const SizedBox(
              height: 25,
            ),
            if (layers.isNotEmpty)
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: renderVideo,
                  icon: const Icon(
                    Icons.movie,
                  ),
                  label: const Text(
                    "GENERATE VIDEO",
                  ),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.all(
                      20,
                    ),
                  ),
                ),
              ),
            if (processing)
              const Padding(
                padding: EdgeInsets.all(
                  30,
                ),
                child: CircularProgressIndicator(),
              ),
          ],
        ),
      ),
    );
  }
}
