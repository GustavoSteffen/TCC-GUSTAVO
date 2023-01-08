// ************************************************************************
//                TCC GUSTAVO LENHARDT STEFFEN 2022/2023
//                            UFSM - CS
//                        CÓDIGO MEDIÇÃO DE VELOCIDADE
// ************************************************************************

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
  
  pinMode(pinRPM, INPUT);
  attachInterrupt(pinRPM, contadorRPM, FALLING);

  tUL = micros();
}

void loop()
{
  detachInterrupt(0);
  RPM = (60 * 1000 / PPV ) / (millis() - tUL) * pulsosRPM; // Calculo do RPM
  tUL = millis();
  pulsosRPM = 0;
  attachInterrupt(5, contadorRPM, RISING);

  Serial.println(RPM);
}