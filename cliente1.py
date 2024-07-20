import socket
import itertools
import threading
import time



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
                print("Erro: Conexão resetada pelo servidor.")
            except Exception as e:
                print(f"Erro ao enviar heartbeat: {e}")
            for _ in range(delay_factor // 10):  # Enviar heartbeat a cada 0,1 segundo
                pass

    threading.Thread(target=send_heartbeat, daemon=True).start()
    
    def adjust_clock(latency):
        nonlocal hours, minutes, seconds
        # Ajustar o relógio do cliente baseado na latência
        adjusted_seconds = seconds + latency
        adjusted_minutes = minutes + adjusted_seconds // 60
        adjusted_hours = hours + adjusted_minutes // 60
        seconds = int(adjusted_seconds % 60)
        minutes = int(adjusted_minutes % 60)
        hours = int(adjusted_hours % 24)

    def measure_latency():
        while True:
            try:
                start_time = time.time()
                client_socket.sendto("ping".encode(), server_address)
                data, _ = client_socket.recvfrom(1024)
                if data.decode() == "pong":
                    latency = (time.time() - start_time) / 2  # Latência de ida e volta dividida por 2
                    print(f"Latência: {latency * 1000:.2f} ms")
                    # Ajustar o relógio do cliente aqui, se necessário
                    adjust_clock(latency)
            except ConnectionResetError:
                print("Erro: Conexão resetada pelo servidor.")
            except Exception as e:
                print(f"Erro ao medir latência: {e}")
            time.sleep(1)  # Medir a latência a cada 1 segundo


    threading.Thread(target=measure_latency, daemon=True).start()
    
    def adjust_clock_based_on_server(server_hours, server_minutes, server_seconds):
        nonlocal hours, minutes, seconds
        # Calcular a diferença entre o tempo do servidor e o tempo do cliente
        client_total_seconds = hours * 3600 + minutes * 60 + seconds
        server_total_seconds = server_hours * 3600 + server_minutes * 60 + server_seconds
        difference = server_total_seconds - client_total_seconds
        
        # Ajustar o relógio do cliente
        if abs(difference) > 1:  # Sincronizar apenas se a diferença for maior que 1 segundo
            hours = server_hours
            minutes = server_minutes
            seconds = server_seconds
            print(f"{hours:02}:{minutes:02}:{seconds:02}")

    for _ in itertools.count():
        try:
            data, _ = client_socket.recvfrom(1024)
            server_time = data.decode().split(':')
            server_hours, server_minutes, server_seconds = map(int, server_time)
            
            # Ajustar o relógio do cliente baseado no horário do servidor
            adjust_clock_based_on_server(server_hours, server_minutes, server_seconds)

        except ConnectionResetError:
            print("Erro: Conexão resetada pelo servidor.")
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")

        # Limpar a tela (opcional)
        #print("\033c", end="")  # Para sistemas Unix-based
        # Para Windows, pode-se usar: os.system('cls') importando a biblioteca os
        #print("\033c", end="")
        # Exibir o tempo atual
        #print(f"{hours:02}:{minutes:02}:{seconds:02}")

        # Simulação de atraso
        for _ in range(delay_factor):
            pass


# Executar o relógio
run_clock()
