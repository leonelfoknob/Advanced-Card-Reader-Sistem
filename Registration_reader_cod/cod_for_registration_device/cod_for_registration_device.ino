#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9
#define SS_PIN 10

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("Waiting for card...");
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  String cardID = "";
  for (int i = mfrc522.uid.size - 1; i >= 0; i--) {
    if (mfrc522.uid.uidByte[i] < 0x10) {
      cardID += "0";
    }
    cardID += String(mfrc522.uid.uidByte[i], HEX);
  }

  cardID.toUpperCase();
  Serial.println(cardID); // Send card ID to the serial monitor

  delay(1000); // Wait before scanning again
}
