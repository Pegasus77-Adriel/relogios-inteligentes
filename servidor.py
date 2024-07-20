import socket
import itertools
import threading

def run_clock():
    # Inicializando horas, minutos e segundos
    hours = 0
    minutes = 0
    seconds = 0

    # Definindo um fator de atraso para simulação (ajuste conforme necessário)
    delay_factor = 1000000  # Ajuste conforme necessário para aproximar 1 segundo

    # Configurando o servidor UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("0.0.0.0", 12346))
    server_socket.settimeout(1)  # Timeout de 1 segundo para o recvfrom

    client_address = None

    def send_time():
        nonlocal client_address
        while True: #ass
            if client_address:
                time_message = f"{hours:02}:{minutes:02}:{seconds:02}"
                try:
                    server_socket.sendto(time_message.encode(), client_address)
                except ConnectionResetError:
                    client_address = None
                except Exception as e:
                   pass
            for _ in range(delay_factor):
                pass

    threading.Thread(target=send_time, daemon=True).start()

    for _ in itertools.count():
        try:
            data, address = server_socket.recvfrom(1024)
            if data.decode() == "heartbeat":
                client_address = address
        except socket.timeout:
            continue
        except ConnectionResetError:
            client_address = None
        except Exception as e:
            pass

        # Incrementar o contador de segundos
        seconds += 1

        # Verificar se o contador de segundos chegou a 60
        if seconds == 60:
            seconds = 0
            minutes += 1

            # Verificar se o contador de minutos chegou a 60
            if minutes == 60:
                minutes = 0
                hours += 1

                # Verificar se o contador de horas chegou a 24
                if hours == 24:
                    hours = 0
        print("\033c", end="")
        print(f"{hours:02}:{minutes:02}:{seconds:02}")
# Executar o relógio
run_clock()
