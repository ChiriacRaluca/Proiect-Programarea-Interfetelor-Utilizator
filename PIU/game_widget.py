
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QRectF, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPixmap, QFont

class GameWidget(QWidget):
    def __init__(self, open_options_callback=None, return_to_menu_callback=None):
        super().__init__()
        self.open_options_callback = open_options_callback
        self.return_to_menu_callback = return_to_menu_callback

        # Stare joc: "playing", "won", "lost"
        self.game_status = "playing"

        self.vieti = 3
        self.joc_activ = True
        self.invincibil = False
        self.score = 0

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

        self.alien_rows = 3
        self.alien_cols = 8
        self.alien_speed = 2
        self.alien_direction = 1
        self.alien_bullets = []
        self.alien_shoot_timer = 0
        self.alien_shoot_cooldown = 60

        self.init_aliens()

        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.player_sprite = QPixmap("assets/player.png")
        self.alien_sprite = QPixmap("assets/alien.png")
        self.img_inima = QPixmap("assets/heart.png")

        self.player_sprite = self.player_sprite.scaled(
            40, 40,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.alien_sprite = self.alien_sprite.scaled(40, 30)
        self.img_inima = self.img_inima.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)

    def init_aliens(self):
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

    def game_loop(self):
        # Dacă jocul NU e în desfășurare, oprim logica
        if self.game_status != "playing":
            return

        # ==================== PLAYER MOVEMENT ====================
        if self.keys_pressed["left"]:
            self.player_x = max(20, self.player_x - self.player_speed)
        if self.keys_pressed["right"]:
            self.player_x = min(self.width() - 20, self.player_x + self.player_speed)

        # ==================== PLAYER SHOOTING ====================
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.keys_pressed["space"] and self.shoot_cooldown == 0:
            self.shoot_bullet()
            self.shoot_cooldown = 15

        # ==================== BULLETS UPDATE ====================
        for bullet in self.bullets:
            bullet["y"] -= 10
        self.bullets = [b for b in self.bullets if b["y"] > 0]

        # ==================== ALIEN LOGIC ====================
        alive_aliens = [a for a in self.aliens if a["alive"]]

        # 1. VERIFICARE WIN (dacă nu mai sunt extratereștri)
        if not alive_aliens:
            self.game_status = "won"
            self.update()
            return

        move_down = False
        for alien in alive_aliens:
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
                    # 2. VERIFICARE LOSS (extratereștrii au ajuns jos)
                    if alien["y"] >= self.player_y - 20:
                        self.game_status = "lost"
                        self.update()
                        return

        # Alien Shooting
        self.alien_shoot_timer += 1
        if self.alien_shoot_timer >= self.alien_shoot_cooldown:
            self.alien_shoot()
            self.alien_shoot_timer = 0

        # Alien Bullets Move
        for bullet in self.alien_bullets:
            bullet["y"] += 6
        self.alien_bullets = [b for b in self.alien_bullets if b["y"] < self.height()]

        # ==================== COLLISIONS ====================


        for bullet in self.bullets:
            bullet_rect = QRectF(bullet["x"] - 2, bullet["y"], 4, 10)
            for alien in alive_aliens:
                alien_rect = QRectF(alien["x"] - 20, alien["y"] - 15, 40, 30)
                if bullet_rect.intersects(alien_rect):
                    alien["alive"] = False
                    bullet["y"] = -999
                    self.score += 100
                    print(f"Scor: {self.score}")

        player_hitbox = QRectF(self.player_x - 15, self.player_y - 15, 30, 30)

        for bullet in self.alien_bullets:
            bullet_rect = QRectF(bullet["x"], bullet["y"], 4, 12)

            if player_hitbox.intersects(bullet_rect):
                self.lovit_de_inamic()
                bullet["y"] = self.height() + 100
                if self.vieti <= 0:
                    return
        self.update()

    def restart_game(self):
        self.game_status = "playing"
        self.bullets = []
        self.alien_bullets = []
        self.player_x = 400
        self.init_aliens()
        # Timer-ul nu a fost oprit, dar logica era blocată de if
        self.update()

    def shoot_bullet(self):
        self.bullets.append({"x": self.player_x, "y": self.player_y - 20})

    def alien_shoot(self):
        import random
        alive_aliens = [a for a in self.aliens if a["alive"]]
        if alive_aliens:
            shooter = random.choice(alive_aliens)
            self.alien_bullets.append({"x": shooter["x"], "y": shooter["y"] + 20})

    def lovit_de_inamic(self):

        self.vieti -= 1
        print(f"Lovit! Au mai ramas {self.vieti} vieti.")

        if self.vieti <= 0:
            self.game_status = "lost"

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # 1. FUNDAL
        painter.fillRect(self.rect(), QColor("#000020"))

        # 2. ELEMENTE JOC
        # Player (îl desenăm mereu, ca să se vadă sub textul de Game Over)
        if self.game_status in ["playing", "lost", "won"]:
            painter.drawPixmap(int(self.player_x - 20), int(self.player_y - 20), self.player_sprite)

        # Gloanțe Player (Galben)
        painter.setBrush(QColor("yellow"))
        for bullet in self.bullets:
            painter.drawRect(int(bullet["x"] - 2), int(bullet["y"]), 4, 10)

        # Extratereștri
        for alien in self.aliens:
            if alien["alive"]:
                painter.drawPixmap(int(alien["x"] - 20), int(alien["y"] - 15), self.alien_sprite)

        # Gloanțe Aliens (Roșu)
        painter.setBrush(Qt.GlobalColor.red)
        for bullet in self.alien_bullets:
            painter.drawRect(int(bullet["x"]), int(bullet["y"]), 4, 12)

        # ==================== HUD (DATE JOC) ====================

        # A. VIEȚI (Stânga Sus)
        # Desenăm inimioarele
        for i in range(self.vieti):
            x = 10 + (i * 35)
            y = 10
            painter.drawPixmap(x, y, self.img_inima)

        # B. SCOR (Dreapta Sus) <--- NOU!
        font_hud = QFont("Courier New", 18, QFont.Weight.Bold)
        painter.setFont(font_hud)
        painter.setPen(QColor("white"))

        # Desenăm scorul la marginea din dreapta (scădem 200px din lățime ca să încapă)
        painter.drawText(self.width() - 200, 35, f"SCORE: {self.score}")

        # ==================== UI OVERLAYS (GAME OVER / WIN) ====================
        if self.game_status != "playing":
            # Fundal semi-transparent întunecat
            color = QColor(0, 0, 0, 200)
            painter.fillRect(self.rect(), color)

            # Configurare Font Titlu
            font_big = QFont("Courier New", 40, QFont.Weight.Bold)
            font_small = QFont("Courier New", 18)

            title_text = ""
            title_color = QColor("white")

            if self.game_status == "won":
                title_text = "VICTORY!"
                title_color = QColor("#00FF00")  # Verde
            elif self.game_status == "lost":
                title_text = "GAME OVER"
                title_color = QColor("#FF0000")  # Roșu

            # Desenare Titlu (Centrat)
            painter.setPen(title_color)
            painter.setFont(font_big)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, title_text)

            # Desenare Instrucțiuni (Centrat, sub titlu)
            painter.setPen(QColor("white"))
            painter.setFont(font_small)

            rect_instr = self.rect()
            rect_instr.setTop(rect_instr.top() + 100)  # Mutăm textul mai jos
            painter.drawText(rect_instr, Qt.AlignmentFlag.AlignCenter,
                             "PRESS [SPACE] TO RESTART\nPRESS [ESC] FOR MENU")

        painter.end()
    def keyPressEvent(self, event):
        # Comenzi valabile DOAR când jocul s-a terminat
        if self.game_status != "playing":
            if event.key() == Qt.Key.Key_Space:
                self.vieti=3
                self.score=0
                self.game_status = "playing"
                self.restart_game()
            elif event.key() == Qt.Key.Key_Escape:
                if self.return_to_menu_callback:
                    self.return_to_menu_callback()
            return  # Ieșim, nu mai procesăm mișcarea

        # Comenzi valabile în timpul jocului
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
