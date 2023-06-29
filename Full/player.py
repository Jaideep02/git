import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
import requests
from io import BytesIO
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSlider
from PyQt5 import QtCore, QtGui
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import Qt, QPropertyAnimation


# Spotify credentials and user settings
SPOTIFY_CLIENT_ID = "72195189e3ed4d4fae47d7adc10b901f"
SPOTIFY_CLIENT_SECRET = "cec4abb69b5f48d5ad62ca40d5afffaf"
SCOPE = "user-modify-playback-state user-read-playback-state"

# Create the Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri='http://localhost:8888/callback',
                                               scope=SCOPE))


class SpotifyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Spotify Widget")
        self.setStyleSheet("background-color: #F0F0F0;")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create the label for the song name
        self.song_label = QLabel(self)
        self.song_label.setStyleSheet("font: 14pt Forte; font-weight: bold; border-radius: 10px; background-color: rgba(255, 255, 255, 0.5); padding: 10px; text-align: center;")
        self.layout.addWidget(self.song_label)

        # Create the album image label
        self.album_image_label = QLabel(self)
        self.album_image_label.setMinimumSize(200, 200)
        self.layout.addWidget(self.album_image_label)

        # Create the position slider and labels
        self.slider_layout = QHBoxLayout()
        self.layout.addLayout(self.slider_layout)

        self.current_time_label = QLabel(self)
        self.current_time_label.setStyleSheet("font: 10pt; color: #666666;")
        self.slider_layout.addWidget(self.current_time_label)

        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 100)
        self.position_slider.sliderMoved.connect(self.seek_to_position)
        self.slider_layout.addWidget(self.position_slider)

        self.duration_label = QLabel(self)
        self.duration_label.setStyleSheet("font: 10pt; color: #666666;")
        self.slider_layout.addWidget(self.duration_label)

        # Create a layout for the buttons
        self.buttons_layout = QHBoxLayout()
        self.layout.addLayout(self.buttons_layout)

        # Create the previous track button
        self.previous_button = QPushButton(self)
        self.previous_button.setFixedSize(64, 64)
        self.previous_button.setStyleSheet("border: none; border-radius: 20px;background-color: rgba(255, 255, 255, 0.15);")
        previous_icon = QSvgWidget("prev.svg", self)
        self.previous_button_layout = QHBoxLayout(self.previous_button)
        self.previous_button_layout.addWidget(previous_icon)
        self.previous_button_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.previous_button.clicked.connect(self.play_previous_song)
        self.buttons_layout.addWidget(self.previous_button)

        # Create the pause/play button
        self.pause_button = QPushButton(self)
        self.pause_button.setFixedSize(64, 64)
        self.pause_button.setStyleSheet("border: none; border-radius: 20px; background-color: rgba(255, 255, 255, 0.15);")
        pause_icon = QSvgWidget("pause.svg", self)
        play_icon = QSvgWidget("play.svg", self)
        self.pause_button_layout = QHBoxLayout(self.pause_button)
        self.pause_button_layout.addWidget(pause_icon)
        self.pause_button_layout.addWidget(play_icon)
        self.pause_button_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.pause_button.clicked.connect(self.toggle_playback)
        self.buttons_layout.addWidget(self.pause_button)

        # Create the next track button
        self.next_button = QPushButton(self)
        self.next_button.setFixedSize(64, 64)
        self.next_button.setStyleSheet("border: none; border-radius: 20px;background-color: rgba(255, 255, 255, 0.15);")
        next_icon = QSvgWidget("next.svg", self)
        self.next_button_layout = QHBoxLayout(self.next_button)
        self.next_button_layout.addWidget(next_icon)
        self.next_button_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.next_button.clicked.connect(self.play_next_song)
        self.buttons_layout.addWidget(self.next_button)

        # Start the widget by updating the UI
        self.update_widget()

    def update_widget(self):
        # Get the currently playing track information
        current_track = sp.currently_playing()

        if current_track is not None and current_track["is_playing"]:
            song_name = current_track["item"]["name"]
            self.song_label.setText(song_name)

            progress = current_track["progress_ms"]
            duration = current_track["item"]["duration_ms"]
            progress_percentage = (progress / duration) * 100
            self.position_slider.setValue(int(progress_percentage))

            # Retrieve the album artwork and display it
            album_image_url = current_track["item"]["album"]["images"][0]["url"]
            response = requests.get(album_image_url)
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            album_image_qimage = QtGui.QImage(image.tobytes(), image.width, image.height, QtGui.QImage.Format_RGB888)
            album_image_pixmap = QtGui.QPixmap.fromImage(album_image_qimage)

            # Set the album image as the pixmap for the label
            self.album_image_label.setPixmap(album_image_pixmap)
            self.album_image_label.setScaledContents(True)

            # Set the background color of the window to match the dominant color of the album image
            dominant_color = image.getpixel((0, 0))
            background_color = QtGui.QColor(*dominant_color)
            self.setStyleSheet(f"background-color: {background_color.name()};")

            # Update the pause/play button icon based on the playback state
            self.update_pause_play_icon(current_track["is_playing"])

            # Update the current time and duration labels
            current_time = self.format_time(progress)
            duration_time = self.format_time(duration)
            self.current_time_label.setText(current_time)
            self.duration_label.setText(duration_time)

        else:
            self.song_label.setText("No song is currently playing")
            self.position_slider.setValue(0)
            self.album_image_label.clear()
            self.setStyleSheet("background-color: #2f2e2e;")  # Set default background color

            self.update_pause_play_icon(False)

        # Schedule the next update after a short delay
        QtCore.QTimer.singleShot(10, self.update_widget)

    def play_previous_song(self):
        sp.previous_track()

    def play_next_song(self):
        sp.next_track()

    def toggle_playback(self):
        current_track = sp.currently_playing()
        if current_track is not None:
            is_playing = current_track["is_playing"]
            if is_playing:
                sp.pause_playback()
            else:
                sp.start_playback()

            # Animate the pause/play button
            self.animate_pause_play_icon(not is_playing)

    def seek_to_position(self, position):
        current_track = sp.currently_playing()
        if current_track is not None:
            duration = current_track["item"]["duration_ms"]
            target_position = (position / 100) * duration
            sp.seek_track(int(target_position))

    def format_time(self, milliseconds):
        seconds = int((milliseconds / 1000) % 60)
        minutes = int((milliseconds / (1000 * 60)) % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def update_pause_play_icon(self, is_playing):
        if is_playing:
            self.pause_button.setStyleSheet("border: none; border-radius: 20px; background-color: rgba(255, 255, 255, 0.15);")
        else:
            self.pause_button.setStyleSheet("border: none; border-radius: 20px; background-color: rgba(255, 255, 255, 0.15);")

    def animate_pause_play_icon(self, is_playing):
        animation = QPropertyAnimation(self.pause_button, b"geometry")
        animation.setDuration(200)
        animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)

        if is_playing:
            start_geometry = QtCore.QRect(18, 18, 28, 28)
            end_geometry = QtCore.QRect(20, 20, 24, 24)
        else:
            start_geometry = QtCore.QRect(20, 20, 24, 24)
            end_geometry = QtCore.QRect(18, 18, 28, 28)

        animation.setStartValue(start_geometry)
        animation.setEndValue(end_geometry)
        animation.start(QPropertyAnimation.DeleteWhenStopped)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    spotify_widget = SpotifyWidget()
    spotify_widget.show()
    sys.exit(app.exec_())
