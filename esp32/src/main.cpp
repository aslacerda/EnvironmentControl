#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include "secrets.h"

WebServer server(80);

const int pinLM35 = 34;
const int pinLDR = 35;

static const int adcSamples = 16;
static const float adcMaxRaw = 4095.0f;
static const bool ldrInverted = false;

uint16_t ldrObservedMin = 4095;
uint16_t ldrObservedMax = 0;

uint32_t readAverageMilliVolts(uint8_t pin, int samples) {
  uint32_t sum = 0;
  for (int i = 0; i < samples; i++) {
    sum += analogReadMilliVolts(pin);
    delayMicroseconds(200);
  }
  return sum / samples;
}

uint16_t readAverageRaw(uint8_t pin, int samples) {
  uint32_t sum = 0;
  for (int i = 0; i < samples; i++) {
    sum += analogRead(pin);
    delayMicroseconds(200);
  }
  return static_cast<uint16_t>(sum / samples);
}

void handleStatus() {
  uint32_t startedAt = millis();
  const char* method = "UNKNOWN";
  if (server.method() == HTTP_GET) {
    method = "GET";
  } else if (server.method() == HTTP_POST) {
    method = "POST";
  } else if (server.method() == HTTP_PUT) {
    method = "PUT";
  } else if (server.method() == HTTP_DELETE) {
    method = "DELETE";
  }

  IPAddress remote = server.client().remoteIP();
  Serial.printf("[HTTP] %s /status solicitado por %u.%u.%u.%u\n", method, remote[0], remote[1], remote[2], remote[3]);

  // LM35: leitura calibrada em mV e média para reduzir ruído.
  uint32_t lm35mV = readAverageMilliVolts(pinLM35, adcSamples);
  float tempC = lm35mV / 10.0f;

  // LDR: média em leitura bruta e percentual configurável (invertido ou não).
  uint16_t rawLuz = readAverageRaw(pinLDR, adcSamples);
  uint32_t ldrmV = readAverageMilliVolts(pinLDR, adcSamples);
  float tensao = ldrmV / 1000.0f;

  ldrObservedMin = min(ldrObservedMin, rawLuz);
  ldrObservedMax = max(ldrObservedMax, rawLuz);

  float normRaw = rawLuz / adcMaxRaw;
  if (ldrInverted) {
    normRaw = 1.0f - normRaw;
  }
  float luzPercent = constrain(normRaw * 100.0f, 0.0f, 100.0f);

  // Se houver faixa observada suficiente, usa autoescala para dar mais sensibilidade.
  if (ldrObservedMax > (ldrObservedMin + 20)) {
    float normAuto = (rawLuz - ldrObservedMin) / float(ldrObservedMax - ldrObservedMin);
    if (ldrInverted) {
      normAuto = 1.0f - normAuto;
    }
    luzPercent = constrain(normAuto * 100.0f, 0.0f, 100.0f);
  }

  // Criando a resposta JSON para a ferramenta da IA
  String json = "{";
  json += "\"temperatura\":" + String(tempC, 1) + ",";
  json += "\"luminosidade\":" + String(luzPercent, 1) + ",";
  json += "\"rawLuz\":" + String(rawLuz) + ",";
  json += "\"tensao\":" + String(tensao, 3) + ",";
  json += "\"ldrMin\":" + String(ldrObservedMin) + ",";
  json += "\"ldrMax\":" + String(ldrObservedMax);
  json += "}";

  server.send(200, "application/json", json);
  Serial.println("[HTTP] Resposta enviada: " + json);
  Serial.printf("[HTTP] Tempo de processamento: %lu ms\n", millis() - startedAt);
}

void setup() {
  Serial.begin(115200);

  analogReadResolution(12);
  // LM35 normalmente fica abaixo de 1.1V; 0dB melhora resolução nessa faixa.
  analogSetPinAttenuation(pinLM35, ADC_0db);
  // LDR em divisor costuma ocupar faixa maior; 11dB amplia a leitura até ~3.3V.
  analogSetPinAttenuation(pinLDR, ADC_11db);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nConectado!");
  Serial.print("IP para a Tool da IA: http://");
  Serial.println(WiFi.localIP());

  server.on("/status", handleStatus);
  server.begin();
}

void loop() {
  server.handleClient();
}