import random
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Link do vídeo que deseja assistir
video_url = "https://www.youtube.com/watch?v=YZC4l6vVyPA"

# Número de visualizações simultâneas desejadas
num_simultaneous_views = 5  # Por exemplo, 5 abas assistindo ao mesmo tempo

# Função para assistir ao vídeo em uma instância do navegador
def watch_video():
    print(f"📺 Iniciando nova visualização simultânea...")

    # Configuração do navegador
    chrome_options = Options()
    chrome_options.add_argument("--incognito")  # Modo anônimo
    chrome_options.add_argument("--mute-audio")  # Mutar áudio
    chrome_options.add_argument("--headless")   # Roda sem interface (opcional)

    # Inicializa o ChromeDriver usando o webdriver_manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Acessa o vídeo
    driver.get(video_url)
    print(f"📄 Título da página: {driver.title}")
    print(f"🔗 URL atual: {driver.current_url}")

    # Tempo aleatório para assistir ao vídeo (entre 30s e 58s)
    watch_time = random.randint(30, 900)
    print(f"⏳ Assistindo ao vídeo por {watch_time} segundos...")
    time.sleep(watch_time)

    # Fecha o navegador
    driver.quit()
    print(f"✅ Visualização simultânea concluída.")

# Cria e inicia as threads para visualizações simultâneas
threads = []
for _ in range(num_simultaneous_views):
    thread = threading.Thread(target=watch_video)
    threads.append(thread)
    thread.start()

# Aguarda todas as threads terminarem
for thread in threads:
    thread.join()

print("🎉 Todas as visualizações simultâneas concluídas!")