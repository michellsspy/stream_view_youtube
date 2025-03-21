import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from stem.control import Controller
from fake_useragent import UserAgent

# Configurações
YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v=YZC4l6vVyPA"  # URL do vídeo
TOR_CONTROL_PORT = 9051  # Porta do Tor
TOR_PASSWORD = ""  # Defina no torrc

# Função para resetar o IP via Tor
def renew_tor_ip():
    try:
        with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
            controller.authenticate(password=TOR_PASSWORD)
            controller.signal("NEWNYM")
            time.sleep(10)  # Espera um tempo para o novo IP ser ativado
            print("Novo IP Tor gerado.")
    except Exception as e:
        print(f"Erro ao renovar IP Tor: {e}")

# Função para criar perfil aleatório
def create_random_profile():
    names = ["Alex", "Jordan", "Taylor", "Casey", "Riley", "Sam", "Jamie"]
    surnames = ["Smith", "Johnson", "Brown", "Taylor", "Anderson", "Lee"]
    return f"{random.choice(names)} {random.choice(surnames)}"

# Configurações do Selenium
def get_driver():
    options = Options()
    options.add_argument("--headless")  # Se quiser ver o navegador, remova essa linha
    options.add_argument("--proxy-server=socks5h://127.0.0.1:9050")  # Conexão via Tor
    options.add_argument(f"user-agent={UserAgent().random}")  # User-Agent aleatório

    # Tenta definir o caminho do Firefox (caso necessário)
    options.binary_location = "/usr/bin/firefox"  # Ajuste se o Firefox estiver em outro local

    try:
        driver = webdriver.Firefox(options=options)
        return driver
    except Exception as e:
        print(f"Erro ao iniciar o navegador: {e}")
        return None

# Função principal
def watch_video():
    profile = create_random_profile()
    print(f"Usando perfil: {profile}")

    driver = get_driver()
    if not driver:
        print("Navegador não pôde ser iniciado. Pulando esta execução...")
        return

    driver.get(YOUTUBE_VIDEO_URL)

    # Aguarda o carregamento da página
    time.sleep(random.randint(5, 10))

    # Simula o clique no vídeo para evitar pausas automáticas
    try:
        video_element = driver.find_element(By.TAG_NAME, "video")
        video_element.click()
        print("Vídeo iniciado.")
    except Exception:
        print("Não foi possível clicar no vídeo (possível autoplay ativado).")

    # Assiste ao vídeo por um tempo aleatório
    watch_time = random.randint(30, 120)  # Tempo de exibição
    print(f"Assistindo ao vídeo por {watch_time} segundos...")
    time.sleep(watch_time)

    # Tenta curtir o vídeo
    try:
        like_button = driver.find_element(By.XPATH, '//button[@aria-label="Curtir"]')
        like_button.click()
        print("Vídeo curtido com sucesso!")
    except Exception as e:
        print(f"Erro ao tentar curtir o vídeo: {e}")

    # Fecha o navegador
    driver.quit()

    # Renova o IP para a próxima interação
    renew_tor_ip()

# Executa o processo em loop
while True:
    watch_video()
    wait_time = random.randint(60, 180)  # Espera entre 1 e 3 minutos
    print(f"Aguardando {wait_time} segundos antes da próxima iteração...\n")
    time.sleep(wait_time)
