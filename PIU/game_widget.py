from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor


class GameWidget(QWidget):
    def __init__(self, open_options_callback=None):
        super().__init__()
        self.open_options_callback = open_options_callback

        self.player_x = 400
        self.player_y = 550
        self.player_speed = 5


        self.bullets = []
        self.shoot_cooldown = 0


        self.keys_pressed = {
            "left": False,
            "right": False,
            "space": False
        }


        self.alien_rows = 5
        self.alien_cols = 10
        self.alien_speed = 3
        self.alien_direction = 1  # 1 = right, -1 = left

        self.aliens = []
        start_x = 60
        start_y = 60
        spacing_x = 60
        spacing_y = 45

        for row in range(self.alien_rows):
            for col in range(self.alien_cols):
                alien = {
                    "x": start_x + col * spacing_x,
                    "y": start_y + row * spacing_y,
                    "alive": True
                }
                self.aliens.append(alien)


        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)  # ~60 FPS

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)


    def game_loop(self):


        if self.keys_pressed["left"]:
            self.player_x -= self.player_speed
            if self.player_x < 20:
                self.player_x = 20

        if self.keys_pressed["right"]:
            self.player_x += self.player_speed
            if self.player_x > self.width() - 20:
                self.player_x = self.width() - 20

        # ----- SHOOTING -----
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.keys_pressed["space"] and self.shoot_cooldown == 0:
            self.shoot_bullet()
            self.shoot_cooldown = 10

        # ----- MOVE BULLETS -----
        for bullet in self.bullets:
            bullet["y"] -= 10

        self.bullets = [b for b in self.bullets if b["y"] > 0]

        # =====================================================
        #                   ALIEN MOVEMENT
        # =====================================================
        move_down = False

        for alien in self.aliens:
            if alien["alive"]:
                if alien["x"] >= self.width() - 40 and self.alien_direction == 1:
                    move_down = True
                if alien["x"] <= 20 and self.alien_direction == -1:
                    move_down = True

        for alien in self.aliens:
            if alien["alive"]:
                alien["x"] += self.alien_direction * self.alien_speed

        if move_down:
            self.alien_direction *= -1
            for alien in self.aliens:
                if alien["alive"]:
                    alien["y"] += 25

        # =====================================================
        #                   BULLET COLLISIONS
        # =====================================================
        for bullet in self.bullets:
            for alien in self.aliens:
                if alien["alive"]:
                    if (alien["x"] - 20 < bullet["x"] < alien["x"] + 20 and
                        alien["y"] - 20 < bullet["y"] < alien["y"] + 20):
                        alien["alive"] = False
                        bullet["y"] = -999  # remove bullet

        # Redraw everything
        self.update()

    # =====================================================
    #                        SHOOTING
    # =====================================================
    def shoot_bullet(self):
        self.bullets.append({
            "x": self.player_x,
            "y": self.player_y - 20
        })

    # =====================================================
    #                        DRAWING
    # =====================================================
    def paintEvent(self, event):
        painter = QPainter(self)

        # Background
        painter.fillRect(self.rect(), QColor("#000020"))

        # Player ship
        painter.setBrush(QColor("green"))
        painter.drawRect(self.player_x - 20, self.player_y - 10, 40, 20)

        # Bullets
        painter.setBrush(QColor("yellow"))
        for bullet in self.bullets:
            painter.drawRect(bullet["x"] - 2, bullet["y"], 4, 10)

        # Aliens
        painter.setBrush(QColor("#FF00FF"))
        for alien in self.aliens:
            if alien["alive"]:
                painter.drawRect(alien["x"] - 20, alien["y"] - 20, 40, 25)

    # =====================================================
    #                   KEYBOARD INPUT
    # =====================================================
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            self.keys_pressed["left"] = True
        elif event.key() == Qt.Key.Key_Right:
            self.keys_pressed["right"] = True
        elif event.key() == Qt.Key.Key_Space:
            self.keys_pressed["space"] = True
        elif event.key() == Qt.Key.Key_O:
            if self.open_options_callback:
                self.open_options_callback("game")

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            self.keys_pressed["left"] = False
        elif event.key() == Qt.Key.Key_Right:
            self.keys_pressed["right"] = False
        elif event.key() == Qt.Key.Key_Space:
            self.keys_pressed["space"] = False
