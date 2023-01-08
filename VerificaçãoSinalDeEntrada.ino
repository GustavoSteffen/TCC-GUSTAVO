// ************************************************************************
//                TCC GUSTAVO LENHARDT STEFFEN 2022/2023
//                            UFSM - CS
//              CÓDIGO PARA VERIFICAÇÃO DO SINAL DE ENTRADA
// ************************************************************************

#define pin_entrada 5              // Definição do pino de entrada

int X = 0;

void setup() {
  pinMode(pin_entrada, INPUT);     // Definição como um pino de entrada
  Serial.begin(115200);            // Início da comunição serial

}

void loop() {
  X = analogRead(pin_entrada);
  Serial.println(X);
  
}