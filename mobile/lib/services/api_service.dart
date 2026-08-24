import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "http://10.0.2.2:8000";

  static Future<Map<String, dynamic>> uploadVideo(File file) async {
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

    var response = await request.send();

    var body = await response.stream.bytesToString();

    return jsonDecode(body);
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
