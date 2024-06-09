import random
import math
import pygame
from enemy import Sprinter, Tank, Boss

def spawn_enemy_around_island(main, enemy_type):
    map_radius = 25*16*main.scale
    angle = random.uniform(0, 2 * math.pi)
    x = main.maps[1].map_w / 2 + map_radius * math.cos(angle)
    y = main.maps[1].map_h / 2 + map_radius * math.sin(angle)

    new_enemy = enemy_type(main, main.player, main.maps[1].map_w, main.maps[1].map_h,"Levels/MainLevel_Collision enemy.csv")
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
        self.enemies_per_wave = 5
        self.increase = 3
        self.boss_spawned = False

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
        if self.main.wave_number > 1:
            self.enemies_per_wave += self.increase + 2
        self.main.show_text = True
        self.main.wave_text_timer = pygame.time.get_ticks()

    def enemies_dead(self):
        for enemy in self.main.enemies:
            if isinstance(enemy, Sprinter) or isinstance(enemy, Tank):
                return False
        return True

    def all_enemies_dead(self):
        return all(enemy.dead for enemy in self.main.enemies)

    def boss_dead(self):
        for enemy in self.main.enemies:
            if isinstance(enemy, Boss):
                return True
        return False

    def update(self):
        if self.wave_active:
            current_wave_config = self.wave_config[self.current_wave]
            self.time_spawn += self.main.clock.get_time() / 1000

            if self.enemies_spawned < self.enemies_per_wave:
                if self.time_spawn >= current_wave_config['interval']:
                    # Vælg en tilfældig fjende fra wave_config
                    enemy_type = random.choice([cfg['type'] for cfg in self.wave_config])
                    spawn_enemy_around_island(self.main, enemy_type)
                    self.enemies_spawned += 1
                    self.time_spawn = 0


            # Tjekker om alle enemies er døde
            if self.enemies_spawned >= self.enemies_per_wave:
                if self.all_enemies_dead():
                    if self.main.wave_number % 3 == 0 and self.all_enemies_dead():
                        if not self.boss_spawned:
                            spawn_enemy_around_island(self.main, Boss)
                            self.boss_spawned = True

                    # Tjekker om bossen er død
                    if not self.boss_dead():
                        self.wave_active = False
                        self.main.show_text = True
                        self.main.wave_text_timer = pygame.time.get_ticks()
                        # Starter efter lidt tid en ny wave
                        pygame.time.set_timer(pygame.USEREVENT, 1500)

    def handle_event(self, event):
        if event.type == pygame.USEREVENT:
            self.start_next_wave()
            pygame.time.set_timer(pygame.USEREVENT, 0)  # stopper timeren

