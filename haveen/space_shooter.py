import math
import random
import sys
from pathlib import Path
import pygame

try:
    import cv2  
except Exception:  
    cv2 = None

pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    pass  


WIDTH, HEIGHT = 900, 700
FPS = 60
MAX_LEVELS = 5

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
VIDEO_PATH = ASSETS_DIR / "backgrounds" / "background.mp4"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NAVY = (5, 8, 22)
PANEL = (10, 14, 38)
CYAN = (0, 240, 255)
PURPLE = (170, 70, 255)
RED = (255, 50, 70)
GREEN = (50, 255, 140)
AMBER = (255, 190, 40)
MAGENTA = (255, 60, 200)
TEAL = (0, 200, 170)
GREY = (100, 110, 135)
LGREY = (190, 200, 220)

IMAGE_FILES = {
    "player":           "player.jpg",
    "malware":          "malware.jpg",
    "ransomware":       "ransomware.jpg",
    "phishing_drone":   "phishing_drone.jpg",
    "rootkit_core":     "rootkit_core.jpg",
    "vpn":              "vpn.jpg",
    "yubikey":          "yubikey.jpg",
    "firewall":         "firewall.jpg",
    "antivirus":        "antivirus.jpg",
    "encryption":       "encryption.jpg",
    "data_packet":      "data_packet.jpg",
    "malicious_packet": "malicious_packet.jpg",
    "debris":           "debris.jpg",
    "glitch_burst":     "glitch_burst.jpg",
}


KEEP_ASPECT_RATIO = True          
IMAGE_SIZES = {
    "player":           (64, 64),
    "malware":          (56, 56),
    "ransomware":       (78, 66),
    "phishing_drone":   (54, 54),
    "rootkit_core":     (190, 150),
    "vpn":              (40, 40),
    "yubikey":          (40, 40),
    "firewall":         (40, 40),
    "antivirus":        (40, 40),
    "encryption":       (40, 40),
    "data_packet":      (14, 34),
    "malicious_packet": (16, 28),
    "debris":           (80, 80),
    "glitch_burst":     (96, 96),
}
HITBOX_SCALE = {
    "player": 0.50, "malware": 0.70, "ransomware": 0.75, "phishing_drone": 0.70,
    "rootkit_core": 0.65, "vpn": 0.90, "yubikey": 0.90, "firewall": 0.90,
    "antivirus": 0.90, "encryption": 0.90, "data_packet": 0.80,
    "malicious_packet": 0.70, "debris": 0.90, "glitch_burst": 1.0,
}
PLACEHOLDER_STYLE = {
    "player":           (CYAN, "YOU", "box"),
    "malware":          (RED, "MAL", "box"),
    "ransomware":       (PURPLE, "RAN", "box"),
    "phishing_drone":   (AMBER, "PHI", "circle"),
    "rootkit_core":     (RED, "ROOTKIT", "box"),
    "vpn":              (GREEN, "VPN", "circle"),
    "yubikey":          (CYAN, "KEY", "circle"),
    "firewall":         (AMBER, "FW", "circle"),
    "antivirus":        (MAGENTA, "AV", "circle"),
    "encryption":       (PURPLE, "ENC", "circle"),
    "data_packet":      (CYAN, "", "oval"),
    "malicious_packet": (RED, "", "oval"),
    "debris":           (GREY, "", "circle"),
    "glitch_burst":     (MAGENTA, "", "circle"),
}
PLAYER_LEVEL_TINT = True
PLAYER_TINTS = [(0, 0, 0), (0, 40, 35), (10, 45, 10), (50, 40, 0), (45, 10, 60)]
SFX_NAMES = [
    "player_shoot", "enemy_destroyed", "player_hit", "player_death",
    "powerup_collect", "bomb_activate", "shield_activate", "boss_warning",
    "boss_hit", "boss_defeated", "level_complete", "game_over", "button_click",
]
SFX_VOLUME = {"player_shoot": 0.25, "boss_hit": 0.35, "enemy_destroyed": 0.5}  
MUSIC_FILES = {
    "menu":     "music/menu_music.mp3",
    "gameplay": "music/gameplay_music.mp3",
    "boss":     "music/boss_music.mp3",
    "victory":  "music/victory_music.mp3",
}
MUSIC_VOLUME = 0.45
VIDEO_DIM = 110          
SCANLINES = True         
VPN_SECONDS = 5          
RAPID_SECONDS = 6        
SPREAD_SECONDS = 4       
MAX_LIVES, MAX_BOMBS, MAX_SHIELD = 5, 5, 5
GRID_EDGE_MARGIN = 40    
LEVELS = [
    dict(name="PERIMETER BREACH", color=CYAN,   boss="TROJAN LOADER",
         ship="BASE NODE",       ship_desc="Single encrypted packet"),
    dict(name="PACKET FLOOD",     color=TEAL,   boss="BOTNET HERDER",
         ship="PATCHED KERNEL",  ship_desc="Dual data cannons"),
    dict(name="ZERO DAY",         color=GREEN,  boss="ZERO-DAY WORM",
         ship="HARDENED NODE",   ship_desc="Triple packet spread"),
    dict(name="DARK WEB",         color=AMBER,  boss="DARKNET ROOTKIT",
         ship="SECURE ENCLAVE",  ship_desc="Quad packet stream"),
    dict(name="KERNEL PANIC",     color=PURPLE, boss="ROOTKIT CORE",
         ship="ZERO TRUST CORE", ship_desc="Five-way packet storm"),
]
LEVEL_SHOTS = {
    1: [(0, 0, 0, -16)],
    2: [(-7, 0, 0, -16), (7, 0, 0, -16)],
    3: [(0, 0, -3, -16), (0, 0, 0, -16), (0, 0, 3, -16)],
    4: [(-12, 0, 0, -16), (-4, 0, 0, -16), (4, 0, 0, -16), (12, 0, 0, -16)],
    5: [(0, 0, 0, -17), (0, 0, -3, -15), (0, 0, 3, -15), (0, 0, -6, -13), (0, 0, 6, -13)],
}
SPREAD_SHOTS = [(0, 0, -4, -16), (0, 0, 0, -16), (0, 0, 4, -16)]
RAPID_BONUS_SHOTS = [(-14, 8, 0, -14), (14, 8, 0, -14)]  

ENEMY_STATS = {  
    "malware":        dict(hp=1, score=100, bob=(0.07, 0.05, 3)),
    "ransomware":     dict(hp=3, score=300, bob=(0.05, 0.03, 2)),
    "phishing_drone": dict(hp=1, score=80,  bob=(0.09, 0.05, 4)),
}

POWERUPS = {  
    "vpn":        ("VPN", GREEN),
    "yubikey":    ("YUBIKEY", CYAN),
    "firewall":   ("FIREWALL", AMBER),
    "antivirus":  ("ANTIVIRUS", MAGENTA),
    "encryption": ("ENCRYPT", PURPLE),
}
FONT_HUGE = pygame.font.SysFont("consolas", 64, bold=True)
FONT_BIG = pygame.font.SysFont("consolas", 44, bold=True)
FONT_MID = pygame.font.SysFont("consolas", 28, bold=True)
FONT_SMALL = pygame.font.SysFont("consolas", 19)
FONT_TINY = pygame.font.SysFont("consolas", 14)
assets = None
audio = None
def pulse(base, amp, speed, t):
    """Smooth value that oscillates around `base` (clamped to 0-255)."""
    return max(0, min(255, int(base + amp * math.sin(speed * t))))


def lerp_color(c1, c2, t):
    return tuple(max(0, min(255, int(c1[i] + (c2[i] - c1[i]) * t))) for i in range(3))


def draw_text(surf, text, font, color, x, y, center=True, shadow=True):
    """Draw text at (x, y). `center=True` treats (x, y) as the centre point."""
    if shadow:
        shade = font.render(text, True, BLACK)
        pos = shade.get_rect(center=(x + 2, y + 2)) if center else (x + 2, y + 2)
        surf.blit(shade, pos)
    img = font.render(text, True, color)
    surf.blit(img, img.get_rect(center=(x, y)) if center else (x, y))


def draw_glitch_text(surf, text, font, cx, cy, ticks, color=CYAN):
    """Title text with a chromatic-aberration look that glitches now and then."""
    glitching = (ticks % 150) < 8
    spread = random.randint(4, 10) if glitching else 2
    for dx, col in ((-spread, MAGENTA), (spread, CYAN)):
        jitter = random.randint(-3, 3) if glitching else 0
        img = font.render(text, True, col)
        surf.blit(img, img.get_rect(center=(cx + dx, cy + jitter)))
    img = font.render(text, True, WHITE if glitching else color)
    surf.blit(img, img.get_rect(center=(cx, cy)))


def draw_panel(surf, rect, border, fill=PANEL, radius=10, width=2):
    pygame.draw.rect(surf, fill, rect, border_radius=radius)
    pygame.draw.rect(surf, border, rect, width, border_radius=radius)


def draw_bar(surf, x, y, w, h, fraction, color, label):
    fraction = max(0.0, min(1.0, fraction))
    pygame.draw.rect(surf, (20, 24, 50), (x, y, w, h), border_radius=4)
    pygame.draw.rect(surf, color, (x, y, int(w * fraction), h), border_radius=4)
    pygame.draw.rect(surf, color, (x, y, w, h), 1, border_radius=4)
    draw_text(surf, label, FONT_TINY, color, x + w // 2, y - 9, shadow=False)


def blit_centered(surf, image, x, y):
    surf.blit(image, image.get_rect(center=(int(x), int(y))))


def glitch_slices(surf, count=6):
    """Shift a few horizontal strips sideways for a quick glitch effect."""
    frame = surf.copy()
    for _ in range(count):
        y = random.randint(0, HEIGHT - 30)
        h = random.randint(4, 24)
        dx = random.randint(-30, 30)
        strip = pygame.Rect(0, y, WIDTH, h)
        surf.blit(frame, (dx, y), strip)


def make_scanlines():
    layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for y in range(0, HEIGHT, 3):
        pygame.draw.line(layer, (0, 0, 0, 45), (0, y), (WIDTH, y))
    return layer
def fit_image(image, size):
    """Scale an image to `size` (keeping aspect ratio if KEEP_ASPECT_RATIO)."""
    width, height = image.get_size()
    if KEEP_ASPECT_RATIO:
        factor = min(size[0] / width, size[1] / height)
        size = (max(1, int(width * factor)), max(1, int(height * factor)))
    size = (max(1, int(size[0])), max(1, int(size[1])))
    return pygame.transform.smoothscale(image, size)


def make_placeholder(name, size):
    """Simple stand-in sprite used when an image file is missing."""
    color, label, shape = PLACEHOLDER_STYLE.get(name, (GREY, "?", "box"))
    surf = pygame.Surface(size, pygame.SRCALPHA)
    rect = surf.get_rect()
    fill = color + (110,)
    if shape == "oval":
        pygame.draw.ellipse(surf, fill, rect)
        pygame.draw.ellipse(surf, color, rect, 2)
    elif shape == "circle":
        pygame.draw.ellipse(surf, fill, rect)
        pygame.draw.ellipse(surf, color, rect, 2)
    else:
        pygame.draw.rect(surf, fill, rect, border_radius=8)
        pygame.draw.rect(surf, color, rect, 2, border_radius=8)
    if label:
        text = FONT_TINY.render(label, True, WHITE)
        surf.blit(text, text.get_rect(center=rect.center))
    return surf


class Assets:
    """Loads every image once and hands out ready-to-draw surfaces."""

    def __init__(self):
        self.raw = {}        
        self.images = {}     
        self.hitboxes = {}   
        self.missing = []
        self._scaled_cache = {}

        for name, relative_path in IMAGE_FILES.items():
            self._load_image(name, ASSETS_DIR / relative_path)
        base = self.images["player"]
        self.player_variants = [self._tint(base, PLAYER_TINTS[i]) for i in range(MAX_LEVELS)]

    def _load_image(self, name, path):
        size = IMAGE_SIZES[name]
        try:
            raw = pygame.image.load(str(path)).convert_alpha()
        except (pygame.error, FileNotFoundError, OSError):
            self.missing.append(str(path.relative_to(BASE_DIR)))
            raw = make_placeholder(name, size)
        self.raw[name] = raw
        self.images[name] = fit_image(raw, size)
        w, h = self.images[name].get_size()
        factor = HITBOX_SCALE.get(name, 0.8)
        self.hitboxes[name] = (max(2, w * factor), max(2, h * factor))

    @staticmethod
    def _tint(image, tint):
        if not PLAYER_LEVEL_TINT or tint == (0, 0, 0):
            return image
        tinted = image.copy()
        tinted.fill(tint + (0,), special_flags=pygame.BLEND_RGBA_ADD)
        return tinted

    def scaled(self, name, size):
        """Cached copy of an image at a custom size (HUD icons, debris, ...)."""
        key = (name, int(size[0]), int(size[1]))
        if key not in self._scaled_cache:
            self._scaled_cache[key] = fit_image(self.raw[name], size)
        return self._scaled_cache[key]


class Audio:
    """Loads sound effects + music. Missing files simply stay silent."""

    def __init__(self):
        self.enabled = pygame.mixer.get_init() is not None
        self.muted = False
        self.sfx = {}
        self.music_paths = {}
        self.current_music = None
        self.missing = []
        for name in SFX_NAMES:
            path = ASSETS_DIR / "audio" / f"{name}.mp3"
            if not path.exists():
                self.missing.append(str(path.relative_to(BASE_DIR)))
            elif self.enabled:
                try:
                    sound = pygame.mixer.Sound(str(path))
                    sound.set_volume(SFX_VOLUME.get(name, 0.7))
                    self.sfx[name] = sound
                except pygame.error:
                    self.missing.append(str(path.relative_to(BASE_DIR)))
        for name, relative_path in MUSIC_FILES.items():
            path = ASSETS_DIR / "audio" / relative_path
            if path.exists():
                self.music_paths[name] = path
            else:
                self.missing.append(str(path.relative_to(BASE_DIR)))

    def play_sfx(self, name):
        if self.enabled and not self.muted and name in self.sfx:
            self.sfx[name].play()

    def play_music(self, name):
        if not self.enabled or name == self.current_music:
            return
        self.current_music = name
        path = self.music_paths.get(name)
        if path is None:
            pygame.mixer.music.stop()
            return
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.set_volume(0 if self.muted else MUSIC_VOLUME)
            pygame.mixer.music.play(-1)
        except pygame.error:
            self.current_music = None

    def stop_music(self):
        if self.enabled:
            pygame.mixer.music.stop()
        self.current_music = None

    def toggle_mute(self):
        self.muted = not self.muted
        if self.enabled:
            pygame.mixer.music.set_volume(0 if self.muted else MUSIC_VOLUME)
class VideoBackground:
    """Plays assets/backgrounds/background.mp4 in a loop using OpenCV."""

    def __init__(self, path):
        self.capture = None
        self.frame = None
        self.fps = 30.0
        self.timer = 0.0
        self.dim = pygame.Surface((WIDTH, HEIGHT))
        self.dim.fill((0, 0, 12))
        self.dim.set_alpha(VIDEO_DIM)
        if cv2 is None or not path.exists():
            return
        try:
            capture = cv2.VideoCapture(str(path))
            if capture.isOpened():
                fps = capture.get(cv2.CAP_PROP_FPS)
                self.fps = fps if fps and fps > 1 else 30.0
                self.capture = capture
                if not self._read_frame():
                    self._disable()
            else:
                capture.release()
        except Exception:
            self._disable()

    @property
    def available(self):
        return self.capture is not None and self.frame is not None

    def _disable(self):
        if self.capture is not None:
            try:
                self.capture.release()
            except Exception:
                pass
        self.capture = None
        self.frame = None

    def _read_frame(self):
        """Read the next frame (looping at the end). Returns False on failure."""
        try:
            ok, bgr = self.capture.read()
            if not ok:  
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ok, bgr = self.capture.read()
                if not ok:
                    return False
            bgr = cv2.resize(bgr, (WIDTH, HEIGHT))
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            self.frame = pygame.image.frombuffer(rgb.tobytes(), (WIDTH, HEIGHT), "RGB").convert()
            return True
        except Exception:
            return False

    def update(self, dt_ms):
        if self.capture is None:
            return
        self.timer += dt_ms
        frame_time = 1000.0 / self.fps
        if self.timer >= frame_time:
            self.timer = min(self.timer - frame_time, frame_time)
            if not self._read_frame():
                self._disable()  

    def draw(self, surf):
        surf.blit(self.frame, (0, 0))
        surf.blit(self.dim, (0, 0))


class CyberBackground:
    """Fallback: perspective grid + falling hex digits."""

    def __init__(self):
        self.offset = 0.0
        self.glyphs = []
        for char in "0123456789ABCDEF":
            for color, alpha in ((CYAN, 70), (CYAN, 140), (PURPLE, 100)):
                img = FONT_TINY.render(char, True, color)
                img.set_alpha(alpha)
                self.glyphs.append(img)
        self.bits = [
            dict(x=random.randint(0, WIDTH), y=random.randint(0, HEIGHT),
                 speed=random.uniform(0.6, 3.0), glyph=random.choice(self.glyphs))
            for _ in range(90)
        ]

    def update(self, dt_ms):
        self.offset = (self.offset + 0.012) % 1.0
        for bit in self.bits:
            bit["y"] += bit["speed"]
            if bit["y"] > HEIGHT:
                bit["y"] = -10
                bit["x"] = random.randint(0, WIDTH)

    def draw(self, surf):
        surf.fill(NAVY)
        horizon = int(HEIGHT * 0.5)
        grid_color = (40, 20, 90)
        for i in range(-12, 13):
            pygame.draw.line(surf, grid_color, (WIDTH // 2, horizon), (WIDTH // 2 + i * 110, HEIGHT), 1)
        for k in range(10):
            t = ((k + self.offset) / 10) % 1.0
            y = int(horizon + (HEIGHT - horizon) * t * t)
            pygame.draw.line(surf, grid_color, (0, y), (WIDTH, y), 1)
        pygame.draw.line(surf, PURPLE, (0, horizon), (WIDTH, horizon), 1)
        for bit in self.bits:
            surf.blit(bit["glyph"], (int(bit["x"]), int(bit["y"])))


class Background:
    """Uses the video when it works, otherwise the animated fallback."""

    def __init__(self, video_path):
        self.video = VideoBackground(video_path)
        self.fallback = CyberBackground()

    def update(self, dt_ms):
        if self.video.available:
            self.video.update(dt_ms)
        if not self.video.available:
            self.fallback.update(dt_ms)

    def draw(self, surf):
        if self.video.available:
            self.video.draw(surf)
        else:
            self.fallback.draw(surf)
class Entity:
    """Anything with a centre position, a sprite and a hitbox."""
    image_key = None

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.active = True

    @property
    def image(self):
        return assets.images[self.image_key]

    @property
    def rect(self):
        w, h = assets.hitboxes[self.image_key]
        return pygame.Rect(int(self.x - w / 2), int(self.y - h / 2), int(w), int(h))

    def draw(self, surf, ticks=0):
        blit_centered(surf, self.image, self.x, self.y)


class Player(Entity):
    SPEED = 6
    image_key = "player"

    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT - 80)
        self.lives = 3
        self.score = 0
        self.bombs = 2
        self.level = 1
        self.rapid = 0         
        self.spread = 0        
        self.vpn = 0           
        self.invincible = 0    
        self.shield_hp = 0     
        self.shoot_cd = 0

    @property
    def image(self):
        return assets.player_variants[min(self.level, MAX_LEVELS) - 1]

    @property
    def invulnerable(self):
        return self.invincible > 0 or self.vpn > 0

    def reset_for_level(self):
        self.lives = max(self.lives, 3)
        self.bombs = min(self.bombs + 1, MAX_BOMBS)
        self.rapid = self.spread = self.vpn = self.invincible = self.shoot_cd = 0
        self.shield_hp = 0
        self.x, self.y = WIDTH / 2, HEIGHT - 80

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.SPEED
        half_w, half_h = self.image.get_width() // 2, self.image.get_height() // 2
        self.x = max(half_w, min(WIDTH - half_w, self.x))
        self.y = max(48 + half_h, min(HEIGHT - half_h, self.y))
        for timer in ("rapid", "spread", "vpn", "invincible", "shoot_cd"):
            if getattr(self, timer) > 0:
                setattr(self, timer, getattr(self, timer) - 1)

    def can_shoot(self):
        if self.shoot_cd == 0:
            self.shoot_cd = 7 if self.rapid > 0 else 18
            return True
        return False

    def fire(self):
        """Return the list of PlayerBullets for the current level / power-ups."""
        nose_y = self.y - self.image.get_height() / 2
        pattern = SPREAD_SHOTS if self.spread > 0 else LEVEL_SHOTS[min(self.level, MAX_LEVELS)]
        shots = list(pattern)
        if self.rapid > 0 and self.level < 3:
            shots += RAPID_BONUS_SHOTS
        return [PlayerBullet(self.x + dx, nose_y + dy, vx, vy) for dx, dy, vx, vy in shots]

    def hit(self):
        """Take a hit. Returns True if the player is out of lives."""
        if self.invulnerable:
            return False
        if self.shield_hp > 0:
            self.shield_hp -= 1
            self.invincible = 90
            return False
        self.lives -= 1
        self.invincible = 330
        return self.lives <= 0

    def draw(self, surf, ticks=0):
        radius = int(max(self.image.get_size()) * 0.62)
        if self.vpn > 0:
            pygame.draw.circle(surf, GREEN, (int(self.x), int(self.y)), radius + 6, 2)
            pygame.draw.circle(surf, (0, pulse(150, 90, 0.2, ticks), 70), (int(self.x), int(self.y)), radius + 2, 1)
        if self.shield_hp > 0:
            ring = (0, pulse(180, 75, 0.1, ticks), pulse(220, 35, 0.15, ticks))
            pygame.draw.circle(surf, ring, (int(self.x), int(self.y)), radius + int(3 * math.sin(0.1 * ticks)), 3)
        blinking = self.invincible > 0 and self.vpn == 0 and (self.invincible // 5) % 2
        if not blinking:
            blit_centered(surf, self.image, self.x, self.y)


class PlayerBullet(Entity):
    """Encrypted data packet."""
    image_key = "data_packet"

    def __init__(self, x, y, vx=0, vy=-16):
        super().__init__(x, y)
        self.vx, self.vy = vx, vy
        angle = math.degrees(math.atan2(-vx, -vy))  
        base = assets.images[self.image_key]
        self.sprite = pygame.transform.rotate(base, angle) if abs(angle) > 1 else base

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.y < -10 or self.x < -10 or self.x > WIDTH + 10:
            self.active = False

    def draw(self, surf, ticks=0):
        blit_centered(surf, self.sprite, self.x, self.y)


class EnemyBullet(Entity):
    """Malicious data packet."""
    image_key = "malicious_packet"

    def __init__(self, x, y, vx=0, vy=6):
        super().__init__(x, y)
        self.vx, self.vy = vx, vy
        angle = math.degrees(math.atan2(vx, vy))  
        base = assets.images[self.image_key]
        self.sprite = pygame.transform.rotate(base, angle) if abs(angle) > 1 else base

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.y > HEIGHT + 10 or self.y < -60 or self.x < -20 or self.x > WIDTH + 20:
            self.active = False

    def draw(self, surf, ticks=0):
        blit_centered(surf, self.sprite, self.x, self.y)


class Enemy(Entity):
    """kind: 'malware' (grid shooter), 'ransomware' (tanky 3-way), 'phishing_drone' (aimed)."""

    def __init__(self, x, y, kind, level):
        super().__init__(x, y)
        self.kind = kind
        self.image_key = kind
        stats = ENEMY_STATS[kind]
        self.hp = stats["hp"] + level // 2
        self.max_hp = self.hp
        self.score_value = stats["score"]
        self.bob = stats["bob"]
        self.shoot_cd = random.randint(114, 329)
        self.shoot_rate = max(82, 326 - level * 12)
        self.entry_y = random.randint(60, 140) if kind == "phishing_drone" else None

    def update(self):
        if self.entry_y is not None and self.y < self.entry_y:
            self.y += 2.5

    def draw(self, surf, ticks=0):
        speed, x_factor, amplitude = self.bob
        bob = math.sin(ticks * speed + self.x * x_factor) * amplitude
        blit_centered(surf, self.image, self.x, self.y + bob)
        if self.kind == "ransomware" and self.hp > 1:  
            top = self.y - self.image.get_height() / 2 - 8
            for i in range(self.hp):
                pygame.draw.circle(surf, RED, (int(self.x) - (self.hp - 1) * 5 + i * 10, int(top)), 4)

    def shoot(self, player, level):
        muzzle = self.y + self.image.get_height() * 0.35
        if self.kind == "malware":
            return [EnemyBullet(self.x, muzzle, 0, 5 + level * 0.4)]
        if self.kind == "ransomware":
            speed = 4 + level * 0.3
            return [EnemyBullet(self.x, muzzle, vx, speed) for vx in (-2, 0, 2)]
        dx, dy = player.x - self.x, player.y - self.y
        dist = math.hypot(dx, dy) or 1
        speed = 5 + level * 0.3
        return [EnemyBullet(self.x, muzzle, dx / dist * speed, dy / dist * speed)]


class Boss(Entity):
    """Rootkit / Malware Core - one at the end of every level."""
    image_key = "rootkit_core"

    def __init__(self, level):
        super().__init__(WIDTH / 2, 180)
        self.level = level
        self.max_hp = 40 + level * 20
        self.hp = self.max_hp
        self.phase = 1
        self.move_t = 0
        self.shoot_cd = 0
        self.pattern = 0
        self.name = LEVELS[level - 1]["boss"]

    @property
    def hp_frac(self):
        return max(0, self.hp / self.max_hp)

    def update(self):
        self.move_t += 0.015
        self.x = WIDTH / 2 + math.sin(self.move_t) * 260
        self.y = 160 + math.sin(self.move_t * 0.7) * 40
        if self.hp_frac < 0.5:
            self.phase = 2
        if self.hp_frac < 0.25:
            self.phase = 3
        if self.shoot_cd > 0:
            self.shoot_cd -= 1

    def can_shoot(self):
        if self.shoot_cd == 0:
            self.shoot_cd = max(40, 112 - self.level * 4 - self.phase * 8)
            return True
        return False

    def shoot(self, player):
        bullets = []
        bx, by = self.x, self.y + self.image.get_height() * 0.35
        dx, dy = player.x - bx, player.y - by
        dist = math.hypot(dx, dy) or 1
        speed = 6 + self.level * 0.5
        self.pattern = (self.pattern + 1) % 4
        if self.pattern == 0:      
            bullets.append(EnemyBullet(bx, by, dx / dist * speed, dy / dist * speed))
        elif self.pattern == 1:    
            for i in range(5):
                a = math.atan2(dy, dx) + math.radians(-40 + i * 20)
                bullets.append(EnemyBullet(bx, by, math.cos(a) * speed, math.sin(a) * speed))
        elif self.pattern == 2:    
            count = 8 if self.phase >= 2 else 0
            for i in range(count):
                a = math.radians(i * 360 // count)
                bullets.append(EnemyBullet(bx, by, math.cos(a) * 4, math.sin(a) * 4))
        else:                      
            for vx in (-3, 0, 3):
                bullets.append(EnemyBullet(bx - vx * 8, by, vx, speed))
        return bullets

    def draw(self, surf, ticks=0):
        shake = random.randint(-2, 2) if self.phase == 3 else 0  
        blit_centered(surf, self.image, self.x + shake, self.y)
        bar_w = 140
        bar_x = int(self.x) - bar_w // 2
        bar_y = int(self.y - self.image.get_height() / 2 - 22)
        pygame.draw.rect(surf, (60, 0, 10), (bar_x, bar_y, bar_w, 12), border_radius=6)
        pygame.draw.rect(surf, RED, (bar_x, bar_y, int(bar_w * self.hp_frac), 12), border_radius=6)
        pygame.draw.rect(surf, WHITE, (bar_x, bar_y, bar_w, 12), 2, border_radius=6)
        draw_text(surf, self.name, FONT_TINY, RED, self.x, bar_y - 10, shadow=False)


class Debris(Entity):
    """Corrupted data fragment (the old asteroid)."""
    image_key = "debris"

    def __init__(self):
        super().__init__(random.randint(30, WIDTH - 30), -30)
        self.vy = random.uniform(1.5, 3.5)
        self.vx = random.uniform(-1.0, 1.0)
        self.radius = random.randint(18, 40)
        self.angle = random.uniform(0, math.pi * 2)
        self.spin = random.uniform(-0.03, 0.03)
        self.hp = max(1, self.radius // 15)
        self.base = assets.scaled("debris", (self.radius * 2, self.radius * 2))

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.angle += self.spin
        if self.y > HEIGHT + 60:
            self.active = False

    def draw(self, surf, ticks=0):
        blit_centered(surf, pygame.transform.rotate(self.base, math.degrees(self.angle)), self.x, self.y)


class Explosion:
    """Glitch burst that grows and fades over 20 frames."""
    DURATION = 20

    def __init__(self, x, y, big=False):
        self.x, self.y, self.big, self.frame = x, y, big, 0

    @property
    def done(self):
        return self.frame >= self.DURATION

    def update(self):
        self.frame += 1

    def draw(self, surf, ticks=0):
        t = self.frame / self.DURATION
        size = int(max(8, 90 * (0.3 + t) * (1.9 if self.big else 1.0)))
        image = fit_image(assets.raw["glitch_burst"], (size, size))
        image = pygame.transform.rotate(image, self.frame * 18)
        image.set_alpha(int(255 * (1 - t)))
        blit_centered(surf, image, self.x, self.y)


class Powerup(Entity):
    KINDS = list(POWERUPS)

    def __init__(self, x, y):
        super().__init__(x, y)
        self.kind = random.choice(self.KINDS)
        self.image_key = self.kind
        self.vy = 1.8

    def update(self):
        self.y += self.vy
        if self.y > HEIGHT + 30:
            self.active = False

    def draw(self, surf, ticks=0):
        name, color = POWERUPS[self.kind]
        pygame.draw.circle(surf, color, (int(self.x), int(self.y)), pulse(24, 3, 0.15, ticks), 2)
        blit_centered(surf, self.image, self.x, self.y)
        draw_text(surf, name, FONT_TINY, color, self.x, self.y + 30)
def build_level(level):
    """Grid of malware (+ ransomware on top row from level 3) and phishing drones."""
    enemies = []
    rows = min(2 + level, 5)
    cols = min(5 + level, 10)
    x_gap = min(80, (WIDTH - 80) // max(cols, 1))
    x0 = (WIDTH - x_gap * (cols - 1)) // 2
    for r in range(rows):
        for c in range(cols):
            kind = "ransomware" if (r == 0 and level >= 3) else "malware"
            enemies.append(Enemy(x0 + c * x_gap, 90 + r * 70, kind, level))
    if level >= 2:
        for _ in range(level * 2):
            enemies.append(Enemy(random.randint(60, WIDTH - 60), random.randint(-200, -60), "phishing_drone", level))
    return enemies
def draw_hud(surf, player, level, ticks):
    pygame.draw.rect(surf, (6, 8, 24), (0, 0, WIDTH, 48))
    pygame.draw.line(surf, CYAN, (0, 48), (WIDTH, 48), 1)
    draw_text(surf, f"SCORE {player.score:,}", FONT_SMALL, AMBER, 12, 14, center=False)
    draw_text(surf, f"LEVEL {level} // {LEVELS[level - 1]['name']}", FONT_SMALL, CYAN, WIDTH // 2, 25)
    icon = assets.scaled("player", (26, 26))
    for i in range(player.lives):
        surf.blit(icon, (WIDTH - 36 - i * 32, 11))
    bomb_icon = assets.scaled("antivirus", (22, 22))
    surf.blit(bomb_icon, (10, HEIGHT - 30))
    draw_text(surf, f"x{player.bombs}  [B]", FONT_SMALL, MAGENTA, 38, HEIGHT - 28, center=False)
    bars = []
    if player.rapid > 0:
        bars.append(("ENCRYPT", player.rapid / (FPS * RAPID_SECONDS), PURPLE))
    if player.vpn > 0:
        bars.append(("VPN", player.vpn / (FPS * VPN_SECONDS), GREEN))
    if player.spread > 0:
        bars.append(("SPREAD", player.spread / (FPS * SPREAD_SECONDS), AMBER))
    for i, (label, fraction, color) in enumerate(bars):
        draw_bar(surf, 190 + i * 140, HEIGHT - 16, 120, 8, fraction, color, label)
    if player.shield_hp > 0:  
        draw_text(surf, "SHIELD", FONT_TINY, CYAN, WIDTH - 110, HEIGHT - 26, shadow=False)
        for i in range(player.shield_hp):
            pygame.draw.rect(surf, CYAN, (WIDTH - 170 + i * 22, HEIGHT - 18, 18, 8), border_radius=2)
class LevelSession:
    def __init__(self, level, player):
        self.level = level
        self.player = player
        self.enemies = build_level(level)
        self.p_bullets = []
        self.e_bullets = []
        self.debris = []
        self.explosions = []
        self.powerups = []
        self.boss = None
        self.boss_spawned = False
        self.direction = 1
        self.move_timer = 0
        self.base_speed = 2.2 + level * 1.0
        self.debris_timer = random.randint(40, 100)
        self.ticks = 0
        self.banner_timer = 0      
        self.clear_timer = 0       
        self.boss_hit_cooldown = 0
        self.flash_color = RED
        self.flash_timer = 0
        self.flash_surface = pygame.Surface((WIDTH, HEIGHT))
    def _flash(self, color, frames=12):
        self.flash_color, self.flash_timer = color, frames

    def _damage_player(self):
        """Apply a hit to the player. Returns True if the player died."""
        shielded = self.player.shield_hp > 0
        dead = self.player.hit()
        self._flash(CYAN if shielded else RED)
        audio.play_sfx("player_death" if dead else "player_hit")
        return dead

    def _kill_enemy(self, enemy, from_bomb=False):
        enemy.active = False
        self.player.score += enemy.score_value * self.level
        self.explosions.append(Explosion(enemy.x, enemy.y))
        audio.play_sfx("enemy_destroyed")
        if not from_bomb and random.random() < 0.18:
            self.powerups.append(Powerup(enemy.x, enemy.y))

    def _damage_boss(self, amount):
        boss = self.boss
        if not boss or not boss.active:
            return
        boss.hp -= amount
        if boss.hp > 0:
            if self.boss_hit_cooldown <= 0:
                audio.play_sfx("boss_hit")
                self.boss_hit_cooldown = 8
            return
        boss.active = False
        self.player.score += 2000 * self.level
        for dx, dy in ((0, 0), (-40, 20), (40, -10)):
            self.explosions.append(Explosion(boss.x + dx, boss.y + dy, True))
        self.powerups.append(Powerup(boss.x, boss.y))
        self.e_bullets.clear()
        self.clear_timer = FPS  
        audio.play_sfx("boss_defeated")

    def _apply_powerup(self, kind):
        p = self.player
        if kind == "vpn":
            p.vpn = FPS * VPN_SECONDS
        elif kind == "yubikey":
            p.shield_hp = max(p.shield_hp, 3)
        elif kind == "firewall":
            p.lives = min(MAX_LIVES, p.lives + 1)
            p.shield_hp = min(MAX_SHIELD, p.shield_hp + 1)
        elif kind == "antivirus":
            p.bombs = min(MAX_BOMBS, p.bombs + 1)
            self.e_bullets.clear()
            self._flash(MAGENTA, 8)
        elif kind == "encryption":
            p.rapid = FPS * RAPID_SECONDS
            p.spread = max(p.spread, FPS * SPREAD_SECONDS)
        audio.play_sfx("powerup_collect")
        if kind in ("vpn", "yubikey", "firewall"):
            audio.play_sfx("shield_activate")
    def use_bomb(self):
        """B key: purge hostile packets, damage every enemy, hurt the boss."""
        p = self.player
        if p.bombs <= 0:
            return
        p.bombs -= 1
        audio.play_sfx("bomb_activate")
        self._flash(CYAN, 14)
        self.e_bullets.clear()
        self.explosions.append(Explosion(WIDTH / 2, HEIGHT / 2, True))
        for enemy in self.enemies:
            if enemy.active:
                enemy.hp -= 2
                if enemy.hp <= 0:
                    self._kill_enemy(enemy, from_bomb=True)
        for piece in self.debris:
            self.explosions.append(Explosion(piece.x, piece.y))
        self.debris.clear()
        self._damage_boss(10)
    def update(self, keys):
        """Advance one frame. Returns None, 'dead' or 'clear'."""
        self.ticks += 1
        p = self.player
        p.update(keys)
        if keys[pygame.K_SPACE] and p.can_shoot():
            self.p_bullets += p.fire()
            audio.play_sfx("player_shoot")
        if self.boss_hit_cooldown > 0:
            self.boss_hit_cooldown -= 1
        if self.banner_timer > 0:
            self.banner_timer -= 1

        steps = (self._update_enemies, self._update_boss, self._update_debris,
                 self._update_player_bullets, self._update_enemy_bullets, self._update_powerups)
        for step in steps:
            if step() == "dead":
                return "dead"

        for explosion in self.explosions:
            explosion.update()
        self.explosions = [e for e in self.explosions if not e.done]
        if self.flash_timer > 0:
            self.flash_timer -= 1

        if self.clear_timer > 0:
            self.clear_timer -= 1
            if self.clear_timer == 0:
                return "clear"
        return None

    def _update_enemies(self):
        living = [e for e in self.enemies if e.active]
        for enemy in living:
            enemy.update()
        self.move_timer += 1
        defeated = len(self.enemies) - len(living)
        interval = max(1, 8 - self.level - defeated // 4)
        if self.move_timer >= interval:
            self.move_timer = 0
            if living:
                step = self.base_speed * self.direction
                if any(not GRID_EDGE_MARGIN <= e.x + step <= WIDTH - GRID_EDGE_MARGIN for e in living):
                    self.direction *= -1
                    for enemy in living:
                        enemy.y += 18
                        if enemy.y > HEIGHT - 100:
                            return "dead"  
                for enemy in living:
                    enemy.x += self.base_speed * self.direction
        for enemy in living:
            enemy.shoot_cd -= 1
            if enemy.shoot_cd <= 0 and enemy.y > 20:
                enemy.shoot_cd = enemy.shoot_rate
                self.e_bullets += enemy.shoot(self.player, self.level)
        return None

    def _update_boss(self):
        living = any(e.active for e in self.enemies)
        if not living and not self.boss_spawned:
            self.boss_spawned = True
            self.boss = Boss(self.level)
            self.banner_timer = int(FPS * 2.5)
            audio.play_sfx("boss_warning")
            audio.play_music("boss")
        boss = self.boss
        if boss and boss.active:
            boss.update()
            if boss.can_shoot():
                self.e_bullets += boss.shoot(self.player)
            if boss.rect.colliderect(self.player.rect) and not self.player.invulnerable:
                if self._damage_player():
                    return "dead"
        return None

    def _update_debris(self):
        p = self.player
        self.debris_timer -= 1
        if self.debris_timer <= 0:
            self.debris_timer = random.randint(max(20, 90 - self.level * 10), max(40, 160 - self.level * 12))
            self.debris.append(Debris())
        for piece in self.debris:
            piece.update()
            if piece.active and piece.rect.colliderect(p.rect):
                piece.hp -= 1
                if piece.hp <= 0:
                    piece.active = False
                    self.explosions.append(Explosion(piece.x, piece.y))
                if not p.invulnerable and self._damage_player():
                    return "dead"
        self.debris = [d for d in self.debris if d.active]
        return None

    def _update_player_bullets(self):
        for bullet in self.p_bullets:
            bullet.update()
        for bullet in self.p_bullets:
            if not bullet.active:
                continue
            for enemy in self.enemies:
                if enemy.active and bullet.rect.colliderect(enemy.rect):
                    enemy.hp -= 1
                    bullet.active = False
                    if enemy.hp <= 0:
                        self._kill_enemy(enemy)
                    break
            boss = self.boss
            if bullet.active and boss and boss.active and bullet.rect.colliderect(boss.rect):
                bullet.active = False
                self._damage_boss(1)
            if bullet.active:
                for piece in self.debris:
                    if piece.active and bullet.rect.colliderect(piece.rect):
                        piece.hp -= 1
                        bullet.active = False
                        if piece.hp <= 0:
                            piece.active = False
                            self.explosions.append(Explosion(piece.x, piece.y))
                            self.player.score += 50
                        break
        self.p_bullets = [b for b in self.p_bullets if b.active]
        return None

    def _update_enemy_bullets(self):
        p = self.player
        for bullet in self.e_bullets:
            bullet.update()
            if bullet.active and bullet.rect.colliderect(p.rect):
                bullet.active = False  
                if not p.invulnerable:
                    self.explosions.append(Explosion(p.x, p.y))
                    if self._damage_player():
                        return "dead"
        self.e_bullets = [b for b in self.e_bullets if b.active]
        return None

    def _update_powerups(self):
        for item in self.powerups:
            item.update()
            if item.active and item.rect.colliderect(self.player.rect):
                item.active = False
                self._apply_powerup(item.kind)
        self.powerups = [i for i in self.powerups if i.active]
        return None
    def draw(self, surf):
        t = self.ticks
        for piece in self.debris:
            piece.draw(surf, t)
        for enemy in self.enemies:
            if enemy.active:
                enemy.draw(surf, t)
        if self.boss and self.boss.active:
            self.boss.draw(surf, t)
        for group in (self.e_bullets, self.p_bullets, self.explosions, self.powerups):
            for obj in group:
                obj.draw(surf, t)
        self.player.draw(surf, t)

        if self.flash_timer > 0:  
            self.flash_surface.fill(self.flash_color)
            self.flash_surface.set_alpha(int(110 * self.flash_timer / 12))
            surf.blit(self.flash_surface, (0, 0))

        draw_hud(surf, self.player, self.level, t)

        if self.banner_timer > 0 and self.boss:
            color = (255, pulse(60, 60, 0.4, t), 60)
            draw_text(surf, f"!! {self.boss.name} DETECTED !!", FONT_MID, color, WIDTH // 2, 110)
        elif self.boss and self.boss.active and self.boss.hp_frac < 0.3:
            color = (255, pulse(0, 255, 0.25, t), 0)
            draw_text(surf, "!! ROOTKIT ENRAGED !!", FONT_SMALL, color, WIDTH // 2, HEIGHT - 60)
def scr_title(surf, ticks, unlocked, menu_items):
    draw_glitch_text(surf, "PACKET STORM", FONT_HUGE, WIDTH // 2, 56, ticks)
    draw_text(surf, "//  CYBER DEFENSE PROTOCOL  //", FONT_SMALL, PURPLE, WIDTH // 2, 106)
    pygame.draw.line(surf, GREY, (60, 126), (WIDTH - 60, 126), 1)
    lw, lh, gap = 130, 58, 14
    x0 = (WIDTH - (5 * lw + 4 * gap)) // 2
    ly = 138
    for i, info in enumerate(LEVELS):
        number = i + 1
        lx = x0 + i * (lw + gap)
        locked = number > unlocked
        color = GREY if locked else info["color"]
        fill = (14, 16, 40) if locked else lerp_color((10, 24, 60), info["color"], 0.18)
        draw_panel(surf, (lx, ly, lw, lh), color, fill)
        draw_text(surf, f"LV{number}", FONT_SMALL, color, lx + lw // 2, ly + 14)
        words = info["name"].split()
        draw_text(surf, words[0], FONT_TINY, GREY if locked else WHITE, lx + lw // 2, ly + 34)
        draw_text(surf, words[1] if len(words) > 1 else "", FONT_TINY, GREY if locked else LGREY, lx + lw // 2, ly + 48)
        if locked:
            pygame.draw.rect(surf, GREY, (lx + lw // 2 - 7, ly + lh - 20, 14, 12), border_radius=3)
            pygame.draw.circle(surf, GREY, (lx + lw // 2, ly + lh - 22), 6, 2)
        if i < 4:
            ax, ay = lx + lw + 2, ly + lh // 2
            arrow = info["color"] if number < unlocked else GREY
            pygame.draw.line(surf, arrow, (ax, ay), (ax + gap - 4, ay), 2)
            pygame.draw.polygon(surf, arrow, [(ax + gap - 4, ay - 4), (ax + gap, ay), (ax + gap - 4, ay + 4)])
    menu_top = ly + lh + 18
    pygame.draw.line(surf, GREY, (60, menu_top - 6), (WIDTH - 60, menu_top - 6), 1)
    row = 42
    draw_panel(surf, (WIDTH // 2 - 200, menu_top - 4, 400, len(menu_items) * row + 16), PURPLE)
    for idx, (label, color, _action) in enumerate(menu_items):
        draw_text(surf, f"{idx + 1} - {label}", FONT_SMALL, color, WIDTH // 2, menu_top + 8 + idx * row)

    pygame.draw.line(surf, GREY, (60, HEIGHT - 44), (WIDTH - 60, HEIGHT - 44), 1)
    draw_text(surf, "WASD / Arrows = Move  |  Space = Shoot  |  B = Bomb  |  P = Pause  |  M = Mute",
              FONT_TINY, GREY, WIDTH // 2, HEIGHT - 26)


def scr_instructions(surf):
    draw_text(surf, "INSTRUCTIONS", FONT_MID, CYAN, WIDTH // 2, 45)
    rows = [  
        ("MOVE", "WASD or Arrow Keys", None),
        ("SHOOT", "SPACE - hold to stream encrypted data packets", "data_packet"),
        ("BOMB", "B key - purge all hostile packets, damage every threat", "antivirus"),
        ("VPN", "Invincible for 5 seconds", "vpn"),
        ("YUBIKEY", "Activates a shield that absorbs 3 hits", "yubikey"),
        ("FIREWALL", "+1 life and +1 shield layer", "firewall"),
        ("ANTIVIRUS", "+1 bomb and purges all hostile packets", "antivirus"),
        ("ENCRYPTION", "Rapid fire for 6s + triple spread for 4s", "encryption"),
        ("SCORING", "Malware=100  Ransomware=300  Phishing=80  Boss=2000 (x level)", None),
        ("LEVELS", "5 levels - a Rootkit boss guards the end of each one", None),
        ("GOAL", "Neutralise every threat. Don't let them reach your network!", None),
    ]
    for i, (label, desc, icon) in enumerate(rows):
        y = 85 + i * 50
        draw_panel(surf, (55, y, WIDTH - 110, 42), (40, 50, 100), radius=6, width=1)
        if icon:
            blit_centered(surf, assets.scaled(icon, (30, 30)), 85, y + 21)
        draw_text(surf, label, FONT_TINY, AMBER, 115, y + 5, center=False, shadow=False)
        draw_text(surf, desc, FONT_TINY, LGREY, 115, y + 22, center=False, shadow=False)
    draw_text(surf, "ENTER - back to menu", FONT_SMALL, GREY, WIDTH // 2, HEIGHT - 28)


def scr_levelclear(surf, level, score, ticks):
    info = LEVELS[level - 1]
    color = (pulse(80, 175, 0.08, ticks), 255, pulse(130, 120, 0.06, ticks))
    draw_text(surf, f"LEVEL {level} SECURED", FONT_BIG, color, WIDTH // 2, 190)
    draw_text(surf, f"{info['boss']} neutralised", FONT_SMALL, LGREY, WIDTH // 2, 240)
    draw_text(surf, f"Score: {score:,}", FONT_MID, AMBER, WIDTH // 2, 290)

    next_level = level + 1
    if next_level <= MAX_LEVELS:
        nxt = LEVELS[next_level - 1]
        draw_text(surf, "SYSTEM UPGRADED!", FONT_MID, nxt["color"], WIDTH // 2, 355)
        draw_text(surf, nxt["ship"], FONT_SMALL, WHITE, WIDTH // 2, 400)
        draw_text(surf, nxt["ship_desc"], FONT_TINY, LGREY, WIDTH // 2, 430)
        draw_text(surf, "Lives restored to 3 minimum  |  +1 Bomb  |  Position reset",
                  FONT_TINY, GREEN, WIDTH // 2, 458)
        preview = assets.player_variants[next_level - 1]
        blit_centered(surf, preview, WIDTH // 2, 540)
    draw_text(surf, "ENTER - next level", FONT_SMALL, CYAN, WIDTH // 2, HEIGHT - 30)


def scr_bosswarn(surf, ticks, level):
    info = LEVELS[level - 1]
    color = (255, pulse(0, 255, 0.2, ticks), 0)
    draw_text(surf, "WARNING!", FONT_HUGE, color, WIDTH // 2, 240)
    draw_text(surf, "INTRUSION DETECTED", FONT_MID, RED, WIDTH // 2, 330)
    draw_text(surf, f"LEVEL {level}: {info['name']}", FONT_SMALL, info["color"], WIDTH // 2, 385)
    draw_text(surf, f"Boss signature: {info['boss']}", FONT_SMALL, LGREY, WIDTH // 2, 415)
    draw_text(surf, "Prepare yourself...", FONT_SMALL, GREY, WIDTH // 2, 455)
    if ticks % 20 < 8:
        glitch_slices(surf, 5)


def scr_gameover(surf, score, high, ticks):
    color = (pulse(200, 55, 0.1, ticks), 40, 60)
    draw_text(surf, "SYSTEM COMPROMISED", FONT_BIG, color, WIDTH // 2, 220)
    draw_text(surf, "GAME OVER", FONT_MID, RED, WIDTH // 2, 275)
    draw_text(surf, f"Score:      {score:,}", FONT_MID, AMBER, WIDTH // 2, 340)
    draw_text(surf, f"High Score: {high:,}", FONT_MID, CYAN, WIDTH // 2, 390)
    draw_text(surf, "ENTER - menu", FONT_SMALL, CYAN, WIDTH // 2, 470)
    if ticks % 45 < 5:
        glitch_slices(surf, 4)


def scr_victory(surf, score, ticks):
    color = (50, pulse(220, 35, 0.1, ticks), pulse(140, 60, 0.07, ticks))
    draw_glitch_text(surf, "NETWORK SECURED!", FONT_BIG, WIDTH // 2, 220, ticks, color)
    draw_text(surf, "All threats neutralised", FONT_SMALL, LGREY, WIDTH // 2, 280)
    draw_text(surf, f"Final Score: {score:,}", FONT_MID, AMBER, WIDTH // 2, 340)
    draw_text(surf, "ENTER - menu", FONT_SMALL, CYAN, WIDTH // 2, 430)


def scr_highscores(surf, scores):
    draw_text(surf, "HIGH SCORES", FONT_MID, AMBER, WIDTH // 2, 60)
    if not scores:
        draw_text(surf, "No scores yet!", FONT_SMALL, GREY, WIDTH // 2, 300)
    else:
        colors = [AMBER, CYAN, LGREY]
        for i, value in enumerate(scores[:10]):
            draw_text(surf, f"#{i + 1:02d}   {value:,}", FONT_SMALL, colors[min(i, 2)], WIDTH // 2, 130 + i * 44)
    draw_text(surf, "ENTER - menu", FONT_SMALL, GREY, WIDTH // 2, HEIGHT - 40)
MUSIC_FOR_STATE = {
    "title": "menu", "instructions": "menu", "highscores": "menu", "levelclear": "menu",
    "bosswarn": "gameplay", "playing": "gameplay", "victory": "victory",
}


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.background = Background(VIDEO_PATH)
        self.scanlines = make_scanlines() if SCANLINES else None
        self.high_scores = []
        self.unlocked_level = 1
        self.player = None
        self.level = 1
        self.session = None
        self.paused = False
        self.warn_timer = 0
        self.ticks = 0
        self.state = "title"
        self.set_state("title")
    def set_state(self, state):
        self.state = state
        music = MUSIC_FOR_STATE.get(state)
        if music:
            audio.play_music(music)
        else:
            audio.stop_music()
        if state == "bosswarn":
            audio.play_sfx("boss_warning")
        elif state == "levelclear":
            audio.play_sfx("level_complete")

    def start_run(self, level):
        self.player = Player()
        self.level = self.player.level = level
        self.start_level()

    def start_level(self):
        self.session = LevelSession(self.level, self.player)
        self.paused = False
        self.set_state("playing")

    def next_level(self):
        self.level += 1
        self.player.level = self.level
        self.unlocked_level = max(self.unlocked_level, self.level)
        self.player.reset_for_level()
        self.warn_timer = FPS * 3
        self.set_state("bosswarn")

    def record_score(self):
        self.high_scores.append(self.player.score)
        self.high_scores.sort(reverse=True)

    def finish_run(self, result):
        if result == "clear":
            if self.level >= MAX_LEVELS:
                self.record_score()
                self.unlocked_level = max(self.unlocked_level, self.level)
                self.set_state("victory")
            else:
                self.set_state("levelclear")
        elif result == "dead":
            self.record_score()
            self.set_state("gameover")
            audio.play_sfx("game_over")
        elif result == "quit":
            self.record_score()
            self.set_state("title")

    def quit(self):
        pygame.quit()
        sys.exit()
    def title_menu(self):
        """List of (label, colour, action). Number keys pick the matching row."""
        scores = ("HIGH SCORES", AMBER, lambda: self.set_state("highscores"))
        help_ = ("INSTRUCTIONS", CYAN, lambda: self.set_state("instructions"))
        leave = ("QUIT", RED, self.quit)
        if self.unlocked_level == 1:
            return [("START GAME", GREEN, lambda: self.start_run(1)), scores, help_, leave]
        return [
            ("NEW GAME  (Level 1)", GREEN, lambda: self.start_run(1)),
            (f"CONTINUE  (Level {self.unlocked_level})", CYAN, lambda: self.start_run(self.unlocked_level)),
            scores, help_, leave,
        ]
    def handle_keydown(self, key):
        if key == pygame.K_m:
            audio.toggle_mute()
            return
        state = self.state
        if state == "title":
            menu = self.title_menu()
            index = key - pygame.K_1
            if key == pygame.K_ESCAPE:
                self.quit()
            elif 0 <= index < len(menu):
                audio.play_sfx("button_click")
                menu[index][2]()
        elif state in ("instructions", "highscores"):
            if key in (pygame.K_RETURN, pygame.K_ESCAPE):
                audio.play_sfx("button_click")
                self.set_state("title")
        elif state == "levelclear":
            if key == pygame.K_RETURN:
                audio.play_sfx("button_click")
                self.next_level()
        elif state in ("gameover", "victory"):
            if key == pygame.K_RETURN:
                audio.play_sfx("button_click")
                self.set_state("title")
        elif state == "playing":
            if key == pygame.K_q:
                self.finish_run("quit")
            elif key == pygame.K_p:
                self.paused = not self.paused
            elif key == pygame.K_b and not self.paused:
                self.session.use_bomb()
    def update(self, dt):
        self.ticks += 1
        self.background.update(dt)
        if self.state == "bosswarn":
            self.warn_timer -= 1
            if self.warn_timer <= 0:
                self.start_level()
        elif self.state == "playing" and not self.paused:
            result = self.session.update(pygame.key.get_pressed())
            if result:
                self.finish_run(result)

    def draw(self):
        screen, state, t = self.screen, self.state, self.ticks
        self.background.draw(screen)
        if state == "title":
            scr_title(screen, t, self.unlocked_level, self.title_menu())
        elif state == "instructions":
            scr_instructions(screen)
        elif state == "highscores":
            scr_highscores(screen, self.high_scores)
        elif state == "levelclear":
            scr_levelclear(screen, self.level, self.player.score, t)
        elif state == "bosswarn":
            scr_bosswarn(screen, t, self.level)
        elif state == "gameover":
            scr_gameover(screen, self.player.score, self.high_scores[0] if self.high_scores else 0, t)
        elif state == "victory":
            scr_victory(screen, self.player.score, t)
        elif state == "playing":
            self.session.draw(screen)
            if self.paused:
                draw_text(screen, "PAUSED", FONT_BIG, CYAN, WIDTH // 2, HEIGHT // 2)
                draw_text(screen, "P - resume   |   Q - quit to menu", FONT_SMALL, LGREY, WIDTH // 2, HEIGHT // 2 + 50)
        if self.scanlines:
            screen.blit(self.scanlines, (0, 0))
        pygame.display.flip()

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event.key)
            self.update(dt)
            self.draw()
def create_game():
    """Create the window, load every asset, and return a ready Game."""
    global assets, audio
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PACKET STORM")
    assets = Assets()
    audio = Audio()
    game = Game(screen)

    if assets.missing:
        print(f"[PACKET STORM] {len(assets.missing)} image(s) missing - placeholders used:")
        for name in assets.missing:
            print("   ", name)
    if audio.missing:
        print(f"[PACKET STORM] {len(audio.missing)} audio file(s) missing - those sounds are silent.")
    if not game.background.video.available:
        reason = "OpenCV (cv2) not installed" if cv2 is None else "background.mp4 missing or unreadable"
        print(f"[PACKET STORM] Video background unavailable ({reason}) - using animated fallback.")
    return game


def main():
    create_game().run()


if __name__ == "__main__":
    main()