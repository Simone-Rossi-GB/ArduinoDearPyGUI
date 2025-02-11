# ArduinoDearPyGUI
un progetto scolastico a gruppi volto a migliorare le capacità degli stuudenti nell'apprendimento autonomo tramite datasheet e documentazioni. I codici creati permettono il rilevamento di temperatura e umidità che verranno poi inviati al programma python tramite la seriale e infine mostrati sui grafici in finestra grazie alla libreria DearpyGUI.

Il progetto è stato portato avanti tramite l'utilizzo e lo studio dei datasheet per lo schermo LCD I2C, per il DHT11 e tramite la documentazione della libreria DearpyGUI accessibile e visualizzabile all'indirizzo https://dearpygui.readthedocs.io/en/latest/index.html, più precisamente per i grafici https://dearpygui.readthedocs.io/en/latest/documentation/plots.html.

Sono subentrate difficoltà come:
  - Aggiornamento dei dati sui grafici;
  - Comunicazione tra Thread, processi e programmi;
  - informazioni non visualizzate sullo schermo LCD I2C;
  - Ottenimento di un tempo preciso che veniva in ritardo a causa delle tante istruzioni da eseguire. (Il rilevamento e l'aggiornamento non avvengono precisamente ogni 5 secondi).

ATTENZIONE: Si informa che sono stati usate IA come DeepSeek e CahtGPT per una coprensione di eccezioni, errori e parti di codice nella documentazione non compresi completamente.

Gruppo: Rossi Simone, Grassi Francesco e Viola Filippo.
