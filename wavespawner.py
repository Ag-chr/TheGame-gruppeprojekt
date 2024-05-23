import random
import math
import pygame

def spawn_enemy_around_island(main, enemy_type):
    map_radius = 25*16*main.scale
    angle = random.uniform(0, 2 * math.pi)
    x = main.maps[1].map_w / 2 + map_radius * math.cos(angle)
    y = main.maps[1].map_h / 2 + map_radius * math.sin(angle)


    new_enemy = enemy_type(main, main.player, main.maps[1].map_w, main.maps[1].map_h,
                           "Levels/MainLevel_Collision enemy.csv")
    new_enemy.x = x
    new_enemy.y = y
    new_enemy.sværhed(main.wave_number)
    main.enemies.append(new_enemy)




class WaveManager:
    def __init__(self, main, wave_config):
        self.main = main
        self.wave_config = wave_config
        self.current_wave = 0
        self.time_spawn = 0
        self.enemies_spawned = 0
        self.wave_active = False

    def start_waves(self):
        self.current_wave = 0
        self.time_spawn = 0
        self.enemies_spawned = 0
        self.wave_active = True
        self.main.wave_number = 1
        self.main.show_text = True
        self.main.wave_text_timer = pygame.time.get_ticks()


    def start_next_wave(self):
        self.current_wave = (self.current_wave + 1) % len(self.wave_config)  # Loop tilbage til starten af wave config
        self.time_spawn = 0
        self.enemies_spawned = 0
        self.wave_active = True
        self.main.wave_number += 1
        self.main.show_text = True
        self.main.wave_text_timer = pygame.time.get_ticks()

    def update(self):
        if self.wave_active:
            current_wave_config = self.wave_config[self.current_wave]
            self.time_spawn += self.main.clock.get_time() / 1000

            if self.enemies_spawned < current_wave_config['base_count'] + self.main.wave_number:
                if self.time_spawn >= current_wave_config['interval']:
                    # Vælg en tilfældig fjende fra wave_config
                    enemy_type = random.choice([cfg['type'] for cfg in self.wave_config])
                    spawn_enemy_around_island(self.main, enemy_type)
                    self.enemies_spawned += 1
                    self.time_spawn = 0

            # Tjekker om enemies er død
            if self.enemies_spawned >= current_wave_config['base_count'] + self.main.wave_number:
                if all(enemy.dead for enemy in self.main.enemies):
                    self.wave_active = False
                    self.main.show_text = True
                    self.main.wave_text_timer = pygame.time.get_ticks()
                    # Starter efter lidt tid en ny wave
                    pygame.time.set_timer(pygame.USEREVENT, 1500)

    def handle_event(self, event):
        if event.type == pygame.USEREVENT:
            self.start_next_wave()
            pygame.time.set_timer(pygame.USEREVENT, 0)  # stopper timeren

