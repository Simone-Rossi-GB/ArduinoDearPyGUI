# ArduinoDearPyGUI
Un progetto scolastico a gruppi volto a migliorare le capacità degli studenti nell'apprendimento autonomo tramite datasheet e documentazioni. I codici creati permettono il rilevamento di temperatura e umidità che verranno poi inviati al programma python tramite la seriale e infine mostrati sui grafici in finestra grazie alla libreria DearpyGUI.

Per il salvataggio dei json è necessario avere nella cartella del progetto un file jsonl. Il codice è stato scritto in modo tale da salvare ogni json ricevuto dalla seriale su ogni riga del file jsonl e in caso di chiusura del programma è previsto l'inserimento di una riga vuota dove il programma inizia a salvare di nuovo (dopo la riga vuota) in caso di riavvio.

Il progetto è stato portato avanti tramite l'utilizzo e lo studio dei datasheet per lo schermo LCD I2C, per il DHT11 e tramite la documentazione della libreria DearpyGUI accessibile e visualizzabile all'indirizzo https://dearpygui.readthedocs.io/en/latest/index.html, più precisamente per i grafici https://dearpygui.readthedocs.io/en/latest/documentation/plots.html.

Sono subentrate difficoltà come:
  - Aggiornamento dei dati sui grafici;
  - Comunicazione tra Thread, processi e programmi;
  - informazioni non visualizzate sullo schermo LCD I2C;
  - Ottenimento di un tempo preciso che veniva in ritardo a causa delle tante istruzioni da eseguire. (Il rilevamento e l'aggiornamento non avvengono precisamente ogni 5 secondi).

Problemi ancora non risolti: inserimento di intervalli da 5 negli assi x e y della temperatura e un intervallo di 20 all'asse y dell'umidità.

ATTENZIONE: Si informa che sono stati usate IA come DeepSeek e ChatGPT per una comprensione maggiore di eccezioni, errori e parti di codice nella documentazione non compresi completamente.

Gruppo: Rossi Simone, Grassi Francesco e Viola Filippo.
