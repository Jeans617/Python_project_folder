import pygame
import random  # For random landing pad position

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 600
g = 0.05  # placeholder gravity level, need to change to simulate gravity on various planets
thrust = -0.15  # Thrust power
fuel_max = 100  # Maximum fuel
horizontal_speed = 2  # Speed for left/right movement
landing_pad_y = HEIGHT - 20  # Fixed vertical position for landing pad
landing_pad_width = 100  # Width of the landing pad

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Landing Simulator")

# Clock for frame rate control
clock = pygame.time.Clock()

# Difficulty progression variables (initialized globally)
gravity_level = 0  # Tracks gravity increase level
pad_size_level = 0  # Tracks the landing pad shrinkage level
pad_move_level = 1  # Tracks landing pad movement level
pad_speed = 0.5  # Starting speed of the pad's movement (slower speed)
pad_range = 50  # Starting range of the pad's oscillation (how far it moves left and right)
pad_direction = 1  # Direction of the pad's movement (1 for right, -1 for left)
successful_landings = 0  # Tracks the number of successful landings for progression
pad_center_x = random.randint(50, WIDTH - landing_pad_width - 50)  # Starting center position of the pad

def reset_game(reset_difficulty=False):
    """Resets game variables for a new attempt. Optionally resets difficulty."""
    global rocket, velocity_y, velocity_x, fuel_remaining, landed, crashed, landing_pad_x, landing_pad_width, g, gravity_level, pad_size_level, pad_move_level, pad_speed, pad_direction, pad_range, successful_landings, pad_center_x
    
    if reset_difficulty:
        gravity_level = 0  # Reset gravity progression
        pad_size_level = 0  # Reset pad size progression
        pad_move_level = 1  # Reset pad movement progression
        landing_pad_width = 100  # Reset landing pad width to initial value
        pad_speed = 0.5  # Reset pad movement speed
        pad_range = 50  # Reset pad movement range
        pad_center_x = random.randint(50, WIDTH - landing_pad_width - 50)  # Reset the pad center position
        successful_landings = 0  # Reset successful landing counter
    
    rocket = pygame.Rect(WIDTH // 2 - 20, 100, 40, 60)
    velocity_y = 0
    velocity_x = 0
    fuel_remaining = fuel_max
    landed = False
    crashed = False
   
    g = 0.05 + gravity_level * 0.01  # Increase gravity with each level
    landing_pad_x = pad_center_x - landing_pad_width // 2  # Center the landing pad initially at the specified center position
    landing_pad_width = max(50, landing_pad_width - pad_size_level  * 5)  # Shrink the pad based on difficulty

    # If the landing pad moves, initialize the movement logic
    if pad_move_level > 1:  # Pad movement starts at level 1
        # Adjust the speed and range based on the number of successful landings
        if successful_landings >= 3:  # Start moving after 3 successful landings
            pad_speed = 0.5  # Start with a slower speed
            pad_range = 50  # Smaller movement range at the start
        if successful_landings >= 6:
            pad_speed = 0.7  # Increase speed slightly
            pad_range = 80  # Increase range
        if successful_landings >= 9:
            pad_speed = 1.0  # Increase speed further
            pad_range = 100  # Increase range further
        if successful_landings >= 12:
            pad_speed = 1.2  # Speed increases
            pad_range = 150  # Further increase range

def move_pad():
    """Oscillates the landing pad back and forth based on the difficulty level."""
    global landing_pad_x, pad_speed, pad_direction, pad_range, pad_center_x
    
    # Move the pad back and forth by modifying its x position with pad_speed
    landing_pad_x += pad_speed * pad_direction  # Move the pad by the speed value in the current direction
    
    # Reverse direction when the pad hits the left or right limit
    if landing_pad_x <= pad_center_x - pad_range or landing_pad_x + landing_pad_width >= pad_center_x + pad_range:
        pad_direction *= -1  # Reverse direction

    # Keep the landing pad within the movement bounds
    landing_pad_x = max(pad_center_x - pad_range, min(pad_center_x + pad_range - landing_pad_width, landing_pad_x))

# Initialize game variables
reset_game()

# Show start screen and wait for key press
def show_start_screen():
    """Displays the start screen with instructions."""
    font = pygame.font.Font(None, 28)  # Smaller font size
    message = font.render("Rocket Landing Simulator: Press any key to start", True, WHITE)
    screen.fill(BLACK)
    message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center the message
    screen.blit(message, message_rect)
    pygame.display.flip()

start_screen = True
while start_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            start_screen = False  # Exit start screen when any key is pressed

    show_start_screen()
    clock.tick(30)

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:  # Reset game if "R" is pressed
        reset_game()

    if not landed and not crashed:
        if keys[pygame.K_SPACE] and fuel_remaining > 0:
            velocity_y += thrust  # Apply thrust
            fuel_remaining -= 1

        if keys[pygame.K_LEFT] and fuel_remaining > 0:
            velocity_x = -horizontal_speed  # Move left
            fuel_remaining -= 0.5  # Small fuel usage for horizontal movement
        elif keys[pygame.K_RIGHT] and fuel_remaining > 0:
            velocity_x = horizontal_speed  # Move right
            fuel_remaining -= 0.5
        else:
            velocity_x = 0  # Stop horizontal movement when no key is pressed

        velocity_y += g  # Apply gravity
        rocket.y += velocity_y  # Update vertical position
        rocket.x += velocity_x  # Update horizontal position

        # Prevent the rocket from moving off-screen
        rocket.x = max(0, min(WIDTH - rocket.width, rocket.x))

        # Check landing
        if rocket.bottom >= landing_pad_y:
            if landing_pad_x <= rocket.x <= landing_pad_x + landing_pad_width - rocket.width:
                if velocity_y > 5:  # Too fast = crash
                    crashed = True
                else:
                    landed = True  # Safe landing
                    successful_landings += 1  # Increment successful landing count
                    gravity_level += 1  # Increment successful gravity landing counter
                    pad_size_level += 1  # Increment successful pad shrink counter
                    if successful_landings % 3 == 0:  # After every 3 successful landings, increase pad movement difficulty
                        pad_move_level += 1
            else:
                crashed = True  # Missed the pad = crash
            
            rocket.bottom = landing_pad_y
            velocity_y = 0

    # If landed, show the "Next Level" message
    if landed:
        font = pygame.font.Font(None, 24)
        status = font.render("Next Level! Preparing...", True, GREEN)
        screen.blit(status, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()

        # Wait for a moment before resetting for next level (show for 2 seconds)
        pygame.time.wait(2000)

        # After the message, reset game state for the next level
        reset_game()

    # Display the crash message before resetting
    if crashed:
        font = pygame.font.Font(None, 24)
        status = font.render("Crash! Press 'R' to retry.", True, RED)
        screen.blit(status, (WIDTH // 2 - 80, HEIGHT // 2))
        pygame.display.flip()  # Show the crash message before resetting

        # Wait for user to press 'R' to reset after crash
        while not keys[pygame.K_r]:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(30)

        reset_game(reset_difficulty=True)  # Reset game state after pressing 'R', but reset difficulty

    # Move the landing pad if pad_move_level is greater than 0
    if pad_move_level > 1:
        move_pad()

    # Draw rocket and landing pad
    pygame.draw.rect(screen, WHITE, rocket)
    pygame.draw.rect(screen, WHITE, (landing_pad_x, landing_pad_y, landing_pad_width, 10))  # Landing pad

    # Display status text
    font = pygame.font.Font(None, 24)
    fuel_text = font.render(f"Fuel: {fuel_remaining}", True, WHITE)
    screen.blit(fuel_text, (10, 10))

    # Display difficulty progression
    font = pygame.font.Font(None, 24)
    difficulty_text = font.render(f"Difficulty: Level {pad_move_level}", True, WHITE)
    screen.blit(difficulty_text, (WIDTH - 150, 10))

    pygame.display.flip()
    clock.tick(30)  # Maintain frame rate

pygame.quit()
