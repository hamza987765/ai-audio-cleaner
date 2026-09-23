import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "https://ai-audio-cleaner.onrender.com";

  static Future<Map<String, dynamic>> uploadVideo(File file) async {
    try {
      print("Uploading file: ${file.path}");

      var request = http.MultipartRequest(
        "POST",
        Uri.parse("$baseUrl/upload"),
      );

      request.files.add(
        await http.MultipartFile.fromPath(
          "file",
          file.path,
        ),
      );

      print("Sending request...");

      var response = await request.send();

      print("Status Code: ${response.statusCode}");

      var body = await response.stream.bytesToString();

      print("Response Body:");
      print(body);

      return jsonDecode(body);
    } catch (e) {
      print("UPLOAD ERROR:");
      print(e);
      rethrow;
    }
  }

  static Future<void> renderVideo(
    List<String> layers,
  ) async {
    await http.post(
      Uri.parse("$baseUrl/render"),
      headers: {
        "Content-Type": "application/json",
      },
      body: jsonEncode({
        "keep": layers,
      }),
    );
  }

  static Future<List<int>> downloadVideo() async {
    final response = await http.get(
      Uri.parse("$baseUrl/download"),
    );

    return response.bodyBytes;
  }
}
