// ************************************************************************
//                TCC GUSTAVO LENHARDT STEFFEN 2022/2023
//                            UFSM - CS
//                        CÓDIGO FINAL ESP32
// ************************************************************************

#include "EmonLib.h"             // Inclusão da biblioteca EmonLib

EnergyMonitor emon1;             // Criação da instância
EnergyMonitor emon2;             // Criação da instância
EnergyMonitor emon3;             // Criação da instância

#define pinRPM 5                 // Definição pino do sensor de velocideda
int RPM = 0;
volatile byte pulsosRPM = 0;
unsigned int PPV = 16;           // Número de aberturas do encoder

unsigned long tUL = 0;           // Tempo da Ultima Leitura

void contadorRPM(){
  pulsosRPM++;
}

void setup()
{
  Serial.begin(115200);
  
  emon1.voltage(14, 243, 3.4);  // Voltage: input pin, calibration, phase_shift
  emon1.current(12, 21.25);     // Current: input pin, calibration.
  
  emon2.voltage(25, 352, 0.5);  // Voltage: input pin, calibration, phase_shift
  emon2.current(26, 21.5);      // Current: input pin, calibration.

  emon3.voltage(34, 246, 3.4);  // Voltage: input pin, calibration, phase_shift
  emon3.current(35  , 20.2);    // Current: input pin, calibration.

  pinMode(pinRPM, INPUT);
  attachInterrupt(pinRPM, contadorRPM, FALLING);

  tUL = micros();
}

void loop()
{
  emon1.calcVI(100,150);        // Calculo das variáveis Emon1
  emon2.calcVI(100,150);        // Calculo das variáveis Emon2
  emon3.calcVI(100,150);        // Calculo das variáveis Emon3

if (emon1.Irms < 0.2 ){         // Zeramento das variáveis da Emon1 quando na há nada conectado
  emon1.Irms = 0;
  emon1.Vrms = 0;
  emon3.powerFactor = 0;
}

if (emon2.Irms < 0.2 ){         // Zeramento das variáveis da Emon2 quando na há nada conectado
  emon2.Irms = 0;
  emon2.Vrms = 0;
  emon3.powerFactor = 0;
}

if (emon3.Irms < 0.2 ){         // Zeramento das variáveis da Emon3 quando na há nada conectado
  emon3.Irms = 0;
  emon3.Vrms = 0;
  emon3.powerFactor = 0;
}

if (emon1.powerFactor > 1 ){    // Definindo valor máximo do fator de potência como 1
  emon1.powerFactor = 1;
}

if (emon2.powerFactor > 1 ){    // Definindo valor máximo do fator de potência como 1
  emon2.powerFactor = 1;
}

if (emon3.powerFactor > 1 ){    // Definindo valor máximo do fator de potência como 1
  emon3.powerFactor = 1;
}

  detachInterrupt(0);
  RPM = (60 * 1000 / PPV ) / (millis() - tUL) * pulsosRPM; // Calculo do RPM
  tUL = millis();
  pulsosRPM = 0;
  attachInterrupt(5, contadorRPM, RISING);

  Serial.printf(" %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f \n", RPM*1.0000, 
  emon1.realPower, emon1.apparentPower, emon1.Vrms, emon1.Irms, emon1.powerFactor,
  emon2.realPower, emon2.apparentPower, emon2.Vrms, emon2.Irms, emon2.powerFactor,
  emon3.realPower, emon3.apparentPower, emon3.Vrms, emon3.Irms, emon3.powerFactor); //Print dos valores via serial

}