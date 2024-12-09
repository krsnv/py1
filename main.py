from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QSlider,
    QFileDialog,
    QWidget,
    QHBoxLayout,
    QStatusBar,
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hexlet Study Video Player")
        self.setGeometry(100, 100, 800, 600)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()

        self.play_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        self.open_button = QPushButton("Open")
        self.fullscreen_button = QPushButton("Fullscreen")
        self.increase_speed_button = QPushButton("Speed +")
        self.decrease_speed_button = QPushButton("Speed -")
        self.reset_speed_button = QPushButton("Reset Speed")
        self.mute_button = QPushButton("Mute")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        control_layout_1 = QHBoxLayout()
        control_layout_1.addWidget(self.play_button)
        control_layout_1.addWidget(self.stop_button)
        control_layout_1.addWidget(self.open_button)
        control_layout_1.addWidget(self.fullscreen_button)

        control_layout_2 = QHBoxLayout()
        control_layout_2.addWidget(self.decrease_speed_button)
        control_layout_2.addWidget(self.increase_speed_button)
        control_layout_2.addWidget(self.reset_speed_button)
        control_layout_2.addWidget(self.mute_button)
        control_layout_2.addWidget(self.volume_slider)

        control_layout_3 = QHBoxLayout()
        control_layout_3.addWidget(self.position_slider)

        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addLayout(control_layout_1)
        layout.addLayout(control_layout_2)
        layout.addLayout(control_layout_3)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.media_player.setVideoOutput(self.video_widget)

        self.play_button.clicked.connect(self.toggle_play)
        self.stop_button.clicked.connect(self.stop)
        self.open_button.clicked.connect(self.open_file)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        self.increase_speed_button.clicked.connect(self.increase_speed)
        self.decrease_speed_button.clicked.connect(self.decrease_speed)
        self.reset_speed_button.clicked.connect(self.reset_speed)
        self.mute_button.clicked.connect(self.toggle_mute)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)
        self.media_player.stateChanged.connect(self.update_buttons)

        self.is_muted = False

    def toggle_play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def stop(self):
        self.media_player.stop()

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv)"
        )
        if file_name:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
            self.media_player.play()
            self.status_bar.showMessage(f"Playing: {file_name}")

    def set_position(self, position):
        self.media_player.setPosition(position)

    def update_position(self, position):
        self.position_slider.setValue(position)

    def update_duration(self, duration):
        self.position_slider.setRange(0, duration)

    def update_buttons(self, state):
        if state == QMediaPlayer.PlayingState:
            self.play_button.setText("Pause")
        else:
            self.play_button.setText("Play")

    def toggle_fullscreen(self):
        if self.video_widget.isFullScreen():
            self.video_widget.setFullScreen(False)
        else:
            self.video_widget.setFullScreen(True)
            self.video_widget.keyPressEvent = self.exit_fullscreen

    def exit_fullscreen(self, event):
        if event.key() == Qt.Key_Escape:
            self.video_widget.setFullScreen(False)

    def increase_speed(self):
        current_rate = self.media_player.playbackRate()
        new_rate = current_rate + 0.1
        self.media_player.setPlaybackRate(new_rate)
        self.status_bar.showMessage(f"Playback Speed: {new_rate:.1f}x")

    def decrease_speed(self):
        current_rate = self.media_player.playbackRate()
        new_rate = max(current_rate - 0.1, 0.1)
        self.media_player.setPlaybackRate(new_rate)
        self.status_bar.showMessage(f"Playback Speed: {new_rate:.1f}x")

    def reset_speed(self):
        self.media_player.setPlaybackRate(1.0)
        self.status_bar.showMessage("Playback Speed: 1.0x")

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        self.media_player.setMuted(self.is_muted)
        if self.is_muted:
            self.mute_button.setText("Unmute")
        else:
            self.mute_button.setText("Mute")

    def set_volume(self, volume):
        self.media_player.setVolume(volume)


if __name__ == "__main__":
    app = QApplication([])
    player = VideoPlayer()
    player.show()
    app.exec_()
