import Pyro4
import cv2
import threading

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class VideoServer:
    def __init__(self):
        self.videos = ["video1.mp4", "video2.mp4", "video3.mp4"]
        self.selected_video = None
        self.cap = None
        self.playing = False
        self.thread = None

    def list_videos(self):
        return self.videos

    def select_video(self, video_name):
        if video_name in self.videos:
            self.selected_video = video_name
            print(self.selected_video)
            return f"{video_name} selected"
        else:
            return "Video not found"

    def control_video(self, action):
        print(self.selected_video, action)
        if not self.selected_video:
            return "No video selected"
        
        if action == "play":
            if not self.playing:
                self.playing = True
                self.thread = threading.Thread(target=self.play_video)
                self.thread.start()
                print(self.playing)
            return f"Playing {self.selected_video}"
        elif action == "pause":
            self.playing = False
            return f"Pausing {self.selected_video}"
        elif action == "stop":
            self.playing = False
            if self.cap:
                self.cap.release()
            return f"Stopping {self.selected_video}"
        else:
            return "Invalid action"

    def play_video(self):
        self.cap = cv2.VideoCapture(self.selected_video)
        while self.playing and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            cv2.imshow('Video', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    Pyro4.Daemon.serveSimple(
        {
            VideoServer: "video.server"
        },
        host="localhost",
        port=9090,
        ns=False
    )
