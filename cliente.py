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

    # Configurando o cliente UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(("0.0.0.0", 12345))
    server_address = ("localhost", 12346)

    def send_heartbeat():
        while True:
            try:
                client_socket.sendto("heartbeat".encode(), server_address)
            except ConnectionResetError:
                pass
            except Exception as e:
                print(f"Erro ao enviar heartbeat: {e}")
            for _ in range(delay_factor // 10):  # Enviar heartbeat a cada 0,1 segundo
                pass

    threading.Thread(target=send_heartbeat, daemon=True).start()

    for _ in itertools.count():
        try:
            data, _ = client_socket.recvfrom(1024)
            time_message = data.decode()
            hours, minutes, seconds = map(int, time_message.split(':'))
        except ConnectionResetError:
            print("Erro: Conexão resetada pelo servidor.")
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")

        # Limpar a tela (opcional)
        print("\033c", end="")  # Para sistemas Unix-based
        # Para Windows, pode-se usar: os.system('cls') importando a biblioteca os

        # Exibir o tempo atual
        print(f"{hours:02}:{minutes:02}:{seconds:02}")

        # Simulação de atraso
        for _ in range(delay_factor):
            pass
        
# Executar o relógio
run_clock()
