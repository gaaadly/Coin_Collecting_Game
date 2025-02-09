import pygame
from random import randint

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Collect and Destroy!")

# Load images
coin = pygame.image.load("coin.png")
monster = pygame.image.load("monster.png")
robot = pygame.image.load("robot.png")
robot2 = pygame.image.load("robot2.png")
rules_book = pygame.image.load("rules.png")
clock = pygame.time.Clock()

# Constants
num_coins = 10
num_monsters = 7
robot_speed = 5
jump_height = 80
jump_duration = 20  # Frames
acceleration = 0.001

# Fonts
font = pygame.font.Font(None, 36)

# Functions
def draw_text(text, x, y, color=(200, 200, 200)):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def game_over_screen(player1_score, player2_score, num_players):
    screen.fill((0, 0, 0))
    draw_text("GAME OVER", width // 2 - 100, height // 2 - 70, (255, 0, 0))

    if num_players == 2:
        draw_text(f"Player 1 Score: {player1_score}", width // 2 - 120, height // 2 - 20, (200, 200, 200))
        draw_text(f"Player 2 Score: {player2_score}", width // 2 - 120, height // 2 + 20, (200, 200, 200))
    else:
        draw_text(f"Player 1 Score: {player1_score}", width // 2 - 120, height // 2 - 20, (200, 200, 200))

    draw_text("Press R to Restart or ESC to Exit", width // 2 - 150, height // 2 + 70, (200, 200, 200))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    pygame.quit()
                    exit()
                if event.key == pygame.K_r:  # Restart game
                    main()  # Restart the game loop

def mode_selection_screen():
    screen.fill((20, 20, 20))
    draw_text("Choose Mode:", width // 2 - 100, height // 2 - 70, (200, 200, 200))
    draw_text("One Player (Press 1)", width // 2 - 120, height // 2 - 20, (200, 200, 200))
    draw_text("Two Players (Press 2)", width // 2 - 120, height // 2 + 20, (200, 200, 200))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2

def rules_screen():
    rules_img = pygame.image.load("rules.png")  # Load the image
    screen.fill((0, 0, 0))
    screen.blit(rules_img, (0, 0))  # Display the rules image
    pygame.display.flip()

    # Wait for key press to continue
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False  # Continue to the game

# Mode Selection



def main():
    fall_speed = 2
    num_players = mode_selection_screen()
    rules_screen()
# Players
    players = [
        {"x": width // 4, "y": height - robot.get_height(), "base_y": height - robot.get_height(), "to_left": False, "to_right": False, "is_jumping": False, "jump_frame_count": 0, "score": 0, "alive": True},
        {"x": 3 * width // 4, "y": height - robot.get_height(), "base_y": height - robot.get_height(), "to_left": False, "to_right": False, "is_jumping": False, "jump_frame_count": 0, "score": 0, "alive": True},
    ]

    if num_players == 1:
        players = players[:1]

    # Coins
    coins = []
    for _ in range(num_coins):
        coins.append([randint(0, width - coin.get_width()), randint(-1000, -50)])

    # Monsters
    monsters = []
    for _ in range(num_monsters):
        monsters.append([randint(0, width - monster.get_width()), randint(-1000, -50)])

    # Game Loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    players[0]["to_left"] = True
                if event.key == pygame.K_RIGHT:
                    players[0]["to_right"] = True
                if event.key == pygame.K_SPACE and players[0]["alive"] and not players[0]["is_jumping"]:
                    players[0]["is_jumping"] = True
                    players[0]["jump_frame_count"] = 0

                if num_players == 2:
                    if event.key == pygame.K_a:
                        players[1]["to_left"] = True
                    if event.key == pygame.K_d:
                        players[1]["to_right"] = True
                    if event.key == pygame.K_w and players[1]["alive"] and not players[1]["is_jumping"]:
                        players[1]["is_jumping"] = True
                        players[1]["jump_frame_count"] = 0

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    players[0]["to_left"] = False
                if event.key == pygame.K_RIGHT:
                    players[0]["to_right"] = False

                if num_players == 2:
                    if event.key == pygame.K_a:
                        players[1]["to_left"] = False
                    if event.key == pygame.K_d:
                        players[1]["to_right"] = False

        # Update players
        for player in players:
            if not player["alive"]:
                continue

            # Move left/right
            if player["to_left"] and player["x"] > 0:
                player["x"] -= robot_speed
            if player["to_right"] and player["x"] < width - robot.get_width():
                player["x"] += robot_speed

            # Handle jumping
            if player["is_jumping"]:
                player["jump_frame_count"] += 1
                player["y"] = player["base_y"] - jump_height * (1 - (player["jump_frame_count"] / jump_duration) ** 2)
                if player["jump_frame_count"] >= jump_duration:
                    player["is_jumping"] = False
                    player["y"] = player["base_y"]

        # Move coins
        for coin_pos in coins:
            coin_pos[1] += fall_speed
            for player in players:
                if player["alive"] and (
                    coin_pos[0] < player["x"] + robot.get_width()
                    and coin_pos[0] + coin.get_width() > player["x"]
                    and coin_pos[1] + coin.get_height() > player["y"]
                ):
                    coin_pos[0] = randint(0, width - coin.get_width())
                    coin_pos[1] = randint(-1000, -50)
                    player["score"] += 1
            if coin_pos[1] > height:
                coin_pos[0] = randint(0, width - coin.get_width())
                coin_pos[1] = randint(-1000, -50)

        # Move monsters
        for monster_pos in monsters:
            monster_pos[1] += fall_speed
            for player in players:
                if player["alive"] and (
                    monster_pos[0] < player["x"] + robot.get_width()
                    and monster_pos[0] + monster.get_width() > player["x"]
                    and monster_pos[1] + monster.get_height() > player["y"]
                ):
                    if player["is_jumping"]:  # Destroy monster if jumping
                        monster_pos[0] = randint(0, width - monster.get_width())
                        monster_pos[1] = randint(-1000, -50)
                        player["score"] += 2
                    else:  # Player dies
                        player["alive"] = False

            if monster_pos[1] > height:
                monster_pos[0] = randint(0, width - monster.get_width())
                monster_pos[1] = randint(-1000, -50)

        fall_speed += acceleration

        # Check if game over
        if all(not player["alive"] for player in players):
            running = False

        # Draw everything
        screen.fill((100, 100, 100))
        for coin_pos in coins:
            screen.blit(coin, (coin_pos[0], coin_pos[1]))
        for monster_pos in monsters:
            screen.blit(monster, (monster_pos[0], monster_pos[1]))

        for i in range(len(players)):
            if players[i]["alive"] and i == 0:
                screen.blit(robot, (players[i]["x"], players[i]["y"]))
            elif players[i]["alive"] and i == 1:
                screen.blit(robot2, (players[i]["x"], players[i]["y"]))

        draw_text(f"P1 Score: {players[0]['score']}", 10, 10)
        if num_players == 2:
            draw_text(f"P2 Score: {players[1]['score']}", width - 150, 10)

        pygame.display.flip()
        clock.tick(60)

# Show game over screen
    game_over_screen(players[0]["score"], players[1]["score"] if num_players == 2 else 0, num_players)

main()