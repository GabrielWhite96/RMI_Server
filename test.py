import vlc
import time

# Caminho para o vídeo que você deseja testar
video_path = "C:\\Users\\gabri\\Documents\\GitHub\\RMI_Server\\Server\\video1.mp4"

# Cria uma instância VLC
instance = vlc.Instance()

# Cria um media player
player = instance.media_player_new()

# Cria um media VLC a partir do caminho do vídeo
media = instance.media_new(video_path)

# Anexa o media ao media player
player.set_media(media)

# Reproduz o vídeo
player.play()

# Duração de espera para permitir que o vídeo comece a ser reproduzido
time.sleep(5)  # Espera 5 segundos

# Aguarda até que o vídeo termine (ou você pode parar manualmente)
while player.is_playing():
    time.sleep(1)

# Para o player ao final da reprodução
player.stop()
