import socket
import itertools
import threading
import time

# Cada relogio é um cliente e servidor ao mesmo tempo

def executar_relogio():
    # Inicializando horas, minutos e segundos
    horas = 0
    minutos = 0
    segundos = 0
    host = socket.gethostbyname(socket.gethostname())
    # Definindo um fator de atraso 
    fator_atraso = 10000000 
    # Configurando o servidor UDP
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_servidor.bind((host, 12346))
    socket_servidor.settimeout(1)  # Timeout de 1 segundo para o recvfrom

    endereco_cliente = None
    maior_horario = None  # Para armazenar o maior horário recebido

    # Configurando os endereços dos outros servidores para sincronização
    outros_servidores = [(host, 12347), (host, 12348)] #

    def enviar_horario():
        while True:
            mensagem_horario = f"time:{horas:02}:{minutos:02}:{segundos:02}"
            for servidor in outros_servidores:
                try:
                    socket_servidor.sendto(mensagem_horario.encode(), servidor)
                except Exception as e:
                    pass
            time.sleep(0.2)  # Envia o horário a cada 0,2 segundos

    threading.Thread(target=enviar_horario, daemon=True).start()

    def ping():
        nonlocal endereco_cliente, maior_horario
        for _ in itertools.count():
            try:
                dados, endereco = socket_servidor.recvfrom(1024)
                if dados.decode() == "ping":
                    socket_servidor.sendto("pong".encode(), endereco)
                elif dados.decode().startswith("time:"):
                    _, horas_servidor, minutos_servidor, segundos_servidor = dados.decode().split(":")
                    horario_servidor = (int(horas_servidor), int(minutos_servidor), int(segundos_servidor))
                    
                    if maior_horario is None or horario_servidor > maior_horario:
                        maior_horario = horario_servidor

            except socket.timeout:
                continue
            except ConnectionResetError:
                endereco_cliente = None
            except Exception as e:
                pass

    threading.Thread(target=ping, daemon=True).start()

    def medir_latencia(servidor):
        try:
            tempo_inicio = time.time()
            socket_servidor.sendto("ping".encode(), servidor)
            dados, _ = socket_servidor.recvfrom(1024)
            if dados.decode() == "pong":
                return (time.time() - tempo_inicio) / 2  # Latência de ida e volta dividida por 2
        except Exception as e:
            pass
        return None

    def ajustar_relogio_com_base_na_latencia_e_maior_horario():
        nonlocal horas, minutos, segundos, maior_horario
        while True:
            tempo_atual = horas * 3600 + minutos * 60 + segundos

            if maior_horario:
                horas_maior, minutos_maior, segundos_maior = maior_horario
                tempo_maior = horas_maior * 3600 + minutos_maior * 60 + segundos_maior
                
                # Ajustar o tempo local com base no maior horário recebido
                if tempo_maior > tempo_atual:
                    tempo_atual = tempo_maior

            # Adicionar latência ao tempo ajustado
            for servidor in outros_servidores:
                latencia = medir_latencia(servidor)
                if latencia is not None:
                    tempo_atual += latencia

            # Garantir que o horário local não regresse
            novo_horas = int(tempo_atual // 3600) % 24
            novo_minutos = int((tempo_atual % 3600) // 60)
            novo_segundos = int(tempo_atual % 60)

            if (novo_horas, novo_minutos, novo_segundos) > (horas, minutos, segundos):
                horas = novo_horas
                minutos = novo_minutos
                segundos = novo_segundos

            time.sleep(0.5)  # Ajusta a cada meio segundo

    # Inicia a thread para ajustar o relógio em paralelo
    threading.Thread(target=ajustar_relogio_com_base_na_latencia_e_maior_horario, daemon=True).start()

    resp = False
    while(resp == False):
         # Menu inicial da tela
        menu = input("Digite o atraso do incremento do relógio níveis ('1', '2', '3', '4', '5'):")
        
        if(menu == "3"):
            resp = True
        elif(menu == "1"):
            fator_atraso = fator_atraso/3
            resp = True
        elif(menu == "2"):
            fator_atraso = fator_atraso/2
            resp = True
        elif(menu == "4"): 
            fator_atraso = fator_atraso *2
            resp = True
        elif(menu == "5"):
            fator_atraso = fator_atraso *3
            resp = True
        else:
            print("Valor inválido por favor tente novamente!")
            time.sleep(3)
    # Incrementar o contador de segundos
    while True:
        segundos += 1
        if segundos == 60:
            segundos = 0
            minutos += 1
            if minutos == 60:
                minutos = 0
                horas += 1
                if horas == 24:
                    horas = 0
        # printandop o horário na tela
        print("\033c", end="")
        print(f"Horário:{horas:02}:{minutos:02}:{segundos:02}")

        for _ in range(int(fator_atraso)):
            pass
        
# Executar o relógio
executar_relogio()
