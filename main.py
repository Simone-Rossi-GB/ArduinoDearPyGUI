import dearpygui.dearpygui as dpg
import json
import threading
import time
import serial
import signal
import sys
from queue import Queue

PORTA_SERIALE = 'COM6'
VELOCITA_TRASMISSIONE = 9600
INTERVALLO = 5
FILE_DATI = 'dati_sensori.jsonl'
TEMPERATURA_SOGLIA_MINIMA = 20
TEMPERATURA_SOGLIA_MASSIMA = 25
UMIDITA_SOGLIA_MINIMA = 30
UMIDITA_SOGLIA_MASSIMA = 60

tempi = []
temperature = []
umidita = []
file_lock = threading.Lock()

serie_temperatura = None
serie_umidita = None
indicatore_temperatura = None
indicatore_umidita = None


def gestisci_terminazione(signum, frame):
    with file_lock:
        with open(FILE_DATI, 'a', encoding='utf-8') as f:
            f.write('\n')
    sys.exit(0)


signal.signal(signal.SIGINT, gestisci_terminazione)
signal.signal(signal.SIGTERM, gestisci_terminazione)


def inizializza_file():
    try:
        with open(FILE_DATI, 'r+', encoding='utf-8') as f:
            linee = f.readlines()
            if linee and linee[-1].strip() != '':
                f.write('\n')
    except FileNotFoundError:
        with open(FILE_DATI, 'w', encoding='utf-8') as f:
            pass


def salva_dati(dati):
    with file_lock:
        with open(FILE_DATI, 'a', encoding='utf-8') as f:
            json.dump(dati, f)
            f.write('\n')
            f.flush()


def lettura_seriale(coda):
    inizializza_file()

    try:
        ser = serial.Serial(PORTA_SERIALE, VELOCITA_TRASMISSIONE, timeout=1)
    except Exception as e:
        print(f"Errore porta seriale: {e}")
        return

    while True:
        try:
            riga = ser.readline().decode().strip()
            if riga:
                try:
                    dati = json.loads(riga)
                    coda.put(dati)
                    salva_dati(dati)
                except json.JSONDecodeError:
                    print(f"Dati non validi: {riga}")
        except Exception as e:
            print(f"Errore: {e}")
            time.sleep(0.1)

    ser.close()

def crea_interfaccia():
    global serie_temperatura, serie_umidita, indicatore_temperatura, indicatore_umidita

    with dpg.window(label="Monitoraggio", width=1200, height=800):
        # Grafico Temperatura
        with dpg.plot(label="Temperatura", height=300, width=-1):
            dpg.add_plot_axis(
                dpg.mvXAxis,
                label="Tempo (s)",
                no_gridlines=False,
                no_tick_labels=False
            )
            asse_y = dpg.add_plot_axis(
                dpg.mvYAxis,
                label="°C",
                no_gridlines=False,
                no_tick_labels=False
            )
            serie_temperatura = dpg.add_line_series([], [], parent=asse_y)

        # Grafico Umidità
        with dpg.plot(label="Umidità", height=300, width=-1):
            dpg.add_plot_axis(
                dpg.mvXAxis,
                label="Tempo (s)",
                no_gridlines=False,
                no_tick_labels=False
            )
            asse_y = dpg.add_plot_axis(
                dpg.mvYAxis,
                label="%",
                no_gridlines=False,
                no_tick_labels=False
            )
            serie_umidita = dpg.add_line_series([], [], parent=asse_y)

        # Cerchi che indicano lo Stato
        with dpg.group(horizontal=True):
            with dpg.group():
                dpg.add_text("Temperatura:")
                with dpg.drawlist(width=100, height=100):
                    indicatore_temperatura = dpg.draw_circle((50, 50), 40, color=(255, 255, 0, 255))

            with dpg.group():
                dpg.add_text("Umidità:")
                with dpg.drawlist(width=100, height=100):
                    indicatore_umidita = dpg.draw_circle((50, 50), 40, color=(255, 255, 0, 255))

def aggiorna_indicatori(temperatura_valore, umidita_valore):
    # cerchi indicatori temperatura
    if temperatura_valore < TEMPERATURA_SOGLIA_MINIMA:
        dpg.configure_item(indicatore_temperatura, color=(255, 255, 0, 255))
    elif temperatura_valore > TEMPERATURA_SOGLIA_MASSIMA:
        dpg.configure_item(indicatore_temperatura, color=(255, 0, 0, 255))
    else:
        dpg.configure_item(indicatore_temperatura, color=(0, 255, 0, 255))

    # cerchi indicatori umidità
    if umidita_valore < UMIDITA_SOGLIA_MINIMA:
        dpg.configure_item(indicatore_umidita, color=(255, 255, 0, 255))
    elif umidita_valore > UMIDITA_SOGLIA_MASSIMA:
        dpg.configure_item(indicatore_umidita, color=(255, 0, 0, 255))
    else:
        dpg.configure_item(indicatore_umidita, color=(0, 255, 0, 255))

def main():
    coda = Queue()
    dpg.create_context()

    # Thread che legge i json dalla seriale
    threading.Thread(target=lettura_seriale, args=(coda,), daemon=True).start()

    # Creazione della interfaccia GUI
    crea_interfaccia()
    dpg.create_viewport(title='Termostato', width=1200, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    # Parte di programma in loop che aggiorna i dati
    while dpg.is_dearpygui_running():
        if not coda.empty():
            dati = coda.get()
            try:
                # Converti millisecondi in secondi
                tempo_secondi = dati['time'] / 1000
                tempi.append(tempo_secondi)
                temperature.append(dati['temp'])
                umidita.append(dati['humidity'])
                print(f"Time: {tempo_secondi:.1f}s - Temp: {dati['temp']}°C - Umidità: {dati['humidity']}%")

                dpg.configure_item(serie_temperatura, x=tempi, y=temperature)
                dpg.configure_item(serie_umidita, x=tempi, y=umidita)
                aggiorna_indicatori(dati['temp'], dati['humidity'])

            except KeyError as e:
                print(f"Chiave mancante: {e}")

        dpg.render_dearpygui_frame()

    # Aggiungi riga vuota ad ogni chiusura in modo tale che ricominci al riavvio dopo di essa
    with file_lock:
        with open(FILE_DATI, 'a', encoding='utf-8') as f:
            f.write('\n')
    dpg.destroy_context()

if __name__ == "__main__":
    main()
