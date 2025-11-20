import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton,
                             QLabel, QVBoxLayout, QHBoxLayout, QFrame, QSlider)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase
from game_widget import GameWidget

class SpaceInvadersMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_screen = "menu"
        self.sound_volume = 50
        self.music_volume = 50
        self.setup_fonts()
        self.init_ui()

    def setup_fonts(self):


        from pathlib import Path


        jackpot_path = Path(r"D:\Downloads\master_droid\Master Droid.ttf")
        if jackpot_path.exists():
            jackpot_id = QFontDatabase.addApplicationFont(str(jackpot_path))
            families = QFontDatabase.applicationFontFamilies(jackpot_id)
            if families:
                self.jackpot_font_name = families[0]
                print(f" Font Jackpot încărcat: {self.jackpot_font_name}")
            else:
                print("Master Droid.ttf incarcat, dar nu s-au gasit familii — fallback la Courier New")
                self.jackpot_font_name = "Courier New"
        else:
            print(" Font Jackpot.ttf nu a fost găsit!")
            self.jackpot_font_name = "Courier New"


        arcade_path = Path(r"D:\Downloads\arcade_quest\Arcade Quest.ttf")
        if arcade_path.exists():
            arcade_id = QFontDatabase.addApplicationFont(str(arcade_path))
            families = QFontDatabase.applicationFontFamilies(arcade_id)
            if families:
                self.retro_font_name = families[0]
                print(f"Font Arcade Quest incarcat: {self.retro_font_name}")
            else:
                print("⚠️ Arcade Quest.ttf incarcat, dar fara familii — fallback la Courier New")
                self.retro_font_name = "Courier New"
        else:
            print("❌ Font Arcade Quest.ttf nu a fost gasit!")
            self.retro_font_name = "Courier New"

    def init_ui(self):

        self.setWindowTitle("Space Invaders")
        self.setFixedSize(800, 600)
        self.setStyleSheet("""
                   QMainWindow {
                       background: qlineargradient(
                           x1:0, y1:0, x2:0, y2:1,
                           stop:0 #000000,
                           stop:0.5 #131D36,
                           stop:1 #0D2C52
                       );
                   }
               """)


        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)


        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.central_widget.setLayout(self.main_layout)


        self.show_main_menu()

    def clear_layout(self):

        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_main_menu(self):

        self.clear_layout()
        self.current_screen = "menu"


        menu_container = QWidget()
        menu_layout = QVBoxLayout()
        menu_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_layout.setSpacing(30)
        menu_container.setLayout(menu_layout)





        subtitle = QLabel("SPACE<br>INVADERS")
        subtitle_font = QFont(self.jackpot_font_name)
        subtitle_font.setPointSize(30)
        subtitle.setFont(subtitle_font)

        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            color: #C309EF;
            margin-top: px;
            padding: 0px ;
        """)
        subtitle.setTextFormat(Qt.TextFormat.RichText)  # 🔥 Important!
        subtitle.setMinimumHeight(20)
        menu_layout.addWidget(subtitle)

        menu_layout.addSpacing(10)


        button_style = f"""
            QPushButton {{
                background-color: #00ff00;
                color: #000000;
                font-size: 28px;
                font-weight: bold;
                font-family: '{self.retro_font_name}';
                border: 3px solid #00ff00;
                border-radius: 10px;
                padding: 20px 60px;
                min-width: 300px;
            }}
            QPushButton:hover {{
                background-color: #000000;
                color: #00ff00;
                border: 3px solid #00ff00;
            }}
            QPushButton:pressed {{
                background-color: #00cc00;
                color: #000000;
            }}
        """


        btn_start = QPushButton("▶ START")
        btn_start.setStyleSheet(button_style)
        btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_start.clicked.connect(self.start_game)
        menu_layout.addWidget(btn_start, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_options = QPushButton("⚙ OPTIONS")
        btn_options.setStyleSheet(button_style)
        btn_options.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_options.clicked.connect(self.show_options)
        menu_layout.addWidget(btn_options, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_exit = QPushButton("❌ EXIT")
        btn_exit.setStyleSheet(button_style.replace("#00ff00", "#ff0000"))
        btn_exit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_exit.clicked.connect(self.close)
        menu_layout.addWidget(btn_exit, alignment=Qt.AlignmentFlag.AlignCenter)

        menu_layout.addStretch()


        footer = QLabel("Space Invaders | © 2025")
        footer.setStyleSheet(f"""
            color: #666666;
            font-size: 14px;
            font-family: '{self.retro_font_name}';
            padding: 20px;
        """)
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_layout.addWidget(footer)

        self.main_layout.addWidget(menu_container)

    def show_options(self):

        self.clear_layout()
        self.current_screen = "options"


        options_container = QWidget()
        options_layout = QVBoxLayout()
        options_layout.setContentsMargins(50, 30, 50, 30)
        options_layout.setSpacing(20)
        options_container.setLayout(options_layout)


        title = QLabel("⚙ OPTIONS")
        title.setStyleSheet(f"""
            color: #00ff00;
            font-size: 48px;
            font-weight: bold;
            font-family: '{self.retro_font_name}';
            padding: 20px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        options_layout.addWidget(title)

        options_layout.addSpacing(30)


        settings_frame = QFrame()
        settings_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border: 2px solid #00ff00;
                border-radius: 10px;
                padding: 30px;
            }
        """)
        settings_layout = QVBoxLayout()
        settings_layout.setSpacing(40)
        settings_frame.setLayout(settings_layout)


        sound_label = QLabel("🔊 SOUND EFFECTS")
        sound_label.setStyleSheet(f"""
            color: #00ff00;
            font-size: 24px;
            font-family: '{self.retro_font_name}';
            font-weight: bold;
        """)
        settings_layout.addWidget(sound_label)

        sound_slider_layout = QHBoxLayout()

        self.sound_slider = QSlider(Qt.Orientation.Horizontal)
        self.sound_slider.setMinimum(0)
        self.sound_slider.setMaximum(100)
        self.sound_slider.setValue(self.sound_volume)
        self.sound_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #333333;
                height: 10px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: #00ff00;
                width: 20px;
                height: 20px;
                margin: -5px 0;
                border-radius: 10px;
            }
            QSlider::sub-page:horizontal {
                background: #00ff00;
                border-radius: 5px;
            }
        """)
        self.sound_slider.valueChanged.connect(self.update_sound_volume)

        self.sound_value_label = QLabel(f"{self.sound_volume}%")
        self.sound_value_label.setStyleSheet(f"""
            color: #ffffff;
            font-size: 20px;
            font-family: '{self.retro_font_name}';
            font-weight: bold;
            min-width: 60px;
        """)
        self.sound_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sound_slider_layout.addWidget(self.sound_slider)
        sound_slider_layout.addWidget(self.sound_value_label)
        settings_layout.addLayout(sound_slider_layout)

        # --- MUSIC ---
        music_label = QLabel("🎵 MUSIC")
        music_label.setStyleSheet(f"""
            color: #00ff00;
            font-size: 24px;
            font-family: '{self.retro_font_name}';
            font-weight: bold;
        """)
        settings_layout.addWidget(music_label)

        music_slider_layout = QHBoxLayout()

        self.music_slider = QSlider(Qt.Orientation.Horizontal)
        self.music_slider.setMinimum(0)
        self.music_slider.setMaximum(100)
        self.music_slider.setValue(self.music_volume)
        self.music_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #333333;
                height: 10px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: #00ff00;
                width: 20px;
                height: 20px;
                margin: -5px 0;
                border-radius: 10px;
            }
            QSlider::sub-page:horizontal {
                background: #00ff00;
                border-radius: 5px;
            }
        """)
        self.music_slider.valueChanged.connect(self.update_music_volume)

        self.music_value_label = QLabel(f"{self.music_volume}%")
        self.music_value_label.setStyleSheet(f"""
            color: #ffffff;
            font-size: 20px;
            font-family: '{self.retro_font_name}';
            font-weight: bold;
            min-width: 60px;
        """)
        self.music_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        music_slider_layout.addWidget(self.music_slider)
        music_slider_layout.addWidget(self.music_value_label)
        settings_layout.addLayout(music_slider_layout)

        options_layout.addWidget(settings_frame)
        options_layout.addStretch()

        # Buton back
        btn_back = QPushButton("← BACK TO MENU")
        btn_back.setStyleSheet(f"""
            QPushButton {{
                background-color: #00ff00;
                color: #000000;
                font-size: 24px;
                font-weight: bold;
                font-family: '{self.retro_font_name}';
                border: 3px solid #00ff00;
                border-radius: 10px;
                padding: 15px 40px;
            }}
            QPushButton:hover {{
                background-color: #000000;
                color: #00ff00;
            }}
        """)
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(self.show_main_menu)
        options_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(options_container)

    def update_sound_volume(self, value):
        """Actualizează volumul sunetelor"""
        self.sound_volume = value
        self.sound_value_label.setText(f"{value}%")
        print(f"Sound volume: {value}%")

    def update_music_volume(self, value):
        """Actualizează volumul muzicii"""
        self.music_volume = value
        self.music_value_label.setText(f"{value}%")
        print(f"Music volume: {value}%")

    def start_game(self):

        self.clear_layout()
        self.current_screen = "game"

        game = GameWidget()
        self.main_layout.addWidget(game)
        game.setFocus()


def main():
    app = QApplication(sys.argv)
    window = SpaceInvadersMenu()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()