import Pyro4
import threading
import vlc

@Pyro4.expose
# @Pyro4.behavior(instance_mode="single")
class VideoServer:
    def __init__(self):
        self.videos = ["video1.mp4", "video2.mp4", "video3.mp4"]
        self.selected_video = None
        self.playing = False
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.thread = None

    def list_videos(self):
        return self.videos

    def select_video(self, video_name):
        if video_name in self.videos:
            self.selected_video = video_name
            media = self.instance.media_new(f"C:\\Users\\gabri\\Documents\\GitHub\\RMI_Server\\Server\\{video_name}")
            self.player.set_media(media)
            return f"{video_name} selected"
        else:
            return "Video not found"

    def control_video(self, action):
        if not self.selected_video:
            return "No video selected"
        else:
            if action == "play":
                if not self.playing:
                    self.playing = True
                    self.thread = threading.Thread(target=self.play_video)
                    self.thread.start()
                if self.playing:
                    self.player.pause()
                return f"Playing {self.selected_video}"
            elif action == "pause":
                if self.playing:
                    self.player.pause()
                return f"Pausing {self.selected_video}"
            elif action == "stop":
                if self.playing:
                    self.player.stop()
                    self.playing = False
                return f"Stopping {self.selected_video}"
            else:
                return "Invalid action"

    def play_video(self):
        self.player.set_fullscreen(True)
        self.player.play()
        while self.playing:
            pass  # Loop to keep the thread alive while video is playing
        self.player.stop()
        self.playing = False

if __name__ == "__main__":
    Pyro4.Daemon.serveSimple(
        {
            VideoServer: "video.server"
        },
        host="0.0.0.0",
        port=9090,
        ns=False
    )
