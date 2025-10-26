import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class ApiService extends ChangeNotifier {
  static const Duration lanTimeout = Duration(seconds: 5);
  static const Duration wanTimeout = Duration(seconds: 15);
  
  static final List<Map<String, dynamic>> candidateServers = [
    {'url': 'http://192.168.50.123:11434', 'timeout': lanTimeout, 'name': 'Local'},
    {'url': 'http://iaevolutionxm.asuscomm.com:11434', 'timeout': wanTimeout, 'name': 'DDNS'},
  ];

  String? _activeServerUrl;
  String? get activeServerUrl => _activeServerUrl;

  Future<void> findActiveServer() async {
    for (var server in candidateServers) {
      try {
        final response = await http
            .get(Uri.parse('${server['url']}/api/tags'))
            .timeout(server['timeout']);
        
        if (response.statusCode == 200) {
          _activeServerUrl = server['url'];
          notifyListeners();
          return;
        }
      } catch (e) {
        continue;
      }
    }
    throw Exception('No Ollama server available');
  }

  Future<Map<String, dynamic>> sendMessage(String model, List<Map<String, String>> messages) async {
    if (_activeServerUrl == null) {
      await findActiveServer();
    }

    final response = await http.post(
      Uri.parse('$_activeServerUrl/api/chat'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'model': model,
        'messages': messages,
        'stream': false,
      }),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to send message');
    }
  }
}
