# Hardware - Circuito ESP32 + LM35 + LDR GL5528

## Pinagem

| Componente | Pino ESP32 | Descrição |
|-----------|-----------|-----------|
| LM35 (Temperatura) | GPIO 34 (ADC1_CH6) | Sensor analógico de temperatura |
| LDR GL5528 (Luz) | GPIO 35 (ADC1_CH7) | Sensor analógico de luminosidade |
| GND | GND | Terra comum |
| 3.3V | 3.3V | Alimentação positiva |

## LM35 - Sensor de Temperatura

- **Tipo**: Sensor analógico de temperatura linear
- **Saída**: 10mV por °C (0V = 0°C, 0.33V = 33°C)
- **Faixa**: -40°C a +125°C
- **Resolução (ADC 12-bit ESP32)**: ~0.08°C
- **Atenuação**: ADC_0db (0-1.1V recomendado)

### Cálculo
```
Temperatura (°C) = (leitura_mV / 10)
```

## LDR GL5528 - Sensor de Luminosidade

- **Tipo**: Light Dependent Resistor (resistência variável com luz)
- **Resistência no escuro**: ~1MΩ
- **Resistência com luz intensa**: ~5kΩ
- **Espectralmente sensível**: 400-700nm (visível)
- **Montagem**: Divisor de tensão com resistor de pull-down

### Configuração (Divisor de Tensão)
```
3.3V
  |
  +--- LDR
  |
  +--- GPIO 35 (ADC)
  |
  +--- Resistor ~10kΩ (pull-down)
  |
 GND
```

## Montagem no Protoboard

1. **LM35**: Conectar os 3 pinos (Vin, Vout, GND) - Vout para GPIO 34
2. **LDR**: Formar divisor de tensão - saída para GPIO 35
3. **Jumpers**: Seguir cores padrão (vermelho=3.3V, preto=GND)
4. **Capacitores**: Opcional capacitor de 0.1µF entre 3.3V e GND próximo ao ESP32 para estabilidade

## Foto do Circuito

Adicione uma foto do seu protoboard aqui (arquivo: `circuito.jpg`).

## Calibração

O firmware faz autoescala do LDR observando min/max ao longo do tempo.  
Para forçar recalibração: reiniciar o ESP32 após expor a LDR a diferentes condições de iluminação.
