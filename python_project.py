import pygame
import random  # For random landing pad position

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 600
gravity_level = 0
gravity_values = [
    0.0154,  # Moon
    0.0352,  # Mercury
    0.0354,  # Mars
    0.0843,  # Venus
    0.0933,  # Earth
    0.0826,  # Uranus
    0.099,  # saturn
    0.11,  # neptune
]
background_images = [
    pygame.transform.scale(pygame.image.load("assets/placeholder_background.webp"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/placeholder_2.jpg"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/placeholder_3.jpg"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("assets/placeholder_4.webp"), (WIDTH, HEIGHT)),
]

planet_names = [
    "Moon", "Mercury", "Mars", "Venus", "Earth",
    "Uranus", "Neptune", "Saturn", "Jupiter"
]
g = gravity_values[min(gravity_level, len(gravity_values) - 1)]
angle = 0
thrust = -0.15  # Thrust power
fuel_max = 100  # Maximum fuel
horizontal_speed = 2  # Speed for left/right movement
landing_pad_y = HEIGHT - 20  # Fixed vertical position for landing pad
landing_pad_width = 100  # Width of the landing pad
rocket_img = pygame.image.load("assets/rocket.png.webp")
rocket_img = pygame.transform.scale(rocket_img, (40, 60))
thrust_img = pygame.image.load("assets/thruster.png")
thrust_img = pygame.transform.scale(thrust_img, (40, 20))
thrust_img = pygame.transform.flip(thrust_img, False, True)
celestial_bodies = [
    {"name": "Moon", "fact": "The Moon has no atmosphere, which means there’s no weather!"},
    {"name": "Mercury", "fact": "Mercury is the closest planet to the Sun but not the hottest."},
    {"name": "Mars", "fact": "Mars has the tallest volcano in the solar system: Olympus Mons."},
    {"name": "Venus", "fact": "A day on Venus is longer than its year."},
    {"name": "Earth", "fact": "Earth is the only planet known to support life."},
    {"name": "Uranus", "fact": "Uranus rotates on its side, making its seasons extreme."},
    {"name": "Saturn", "fact": "Saturn’s rings are made mostly of ice particles."},
    {"name": "Neptune", "fact": "Neptune has the fastest winds in the solar system — over 1,300 mph!"}
]

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
pad_size_level = 0  # Tracks the landing pad shrinkage level
pad_move_level = 1  # Tracks landing pad movement level
pad_speed = 0.5  # Starting speed of the pad's movement (slower speed)
pad_range = 50  # Starting range of the pad's oscillation (how far it moves left and right)
pad_direction = 1  # Direction of the pad's movement (1 for right, -1 for left)
successful_landings = 0  # Tracks the number of successful landings for progression
pad_center_x = random.randint(50, WIDTH - landing_pad_width - 50)  # Starting center position of the pad

def reset_game(reset_difficulty=False):
    """Resets game variables for a new attempt. Optionally resets difficulty."""
    global current_background, rocket, velocity_y, angle, velocity_x, fuel_remaining, landed, crashed, landing_pad_x, landing_pad_width, g, gravity_level, pad_size_level, pad_move_level, pad_speed, pad_direction, pad_range, successful_landings, pad_center_x
    
    if reset_difficulty:
        angle = 0
        gravity_level = 0
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
    current_background = background_images[successful_landings % len(background_images)]

    landed = False
    crashed = False
    g = gravity_values[min(gravity_level, len(gravity_values) - 1)]
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

def wrap_text(text, font, max_width):
    """Wraps text into multiple lines based on the max width."""
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

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

def show_loading_screen(show_controls=False):
    """Displays the loading screen with a fun fact and optional controls."""
    screen.fill(BLACK)
    font = pygame.font.Font(None, 28)

    current_body = celestial_bodies[min(successful_landings, len(celestial_bodies) - 1)]
    name_text = font.render(f"Approaching: {current_body['name']}", True, WHITE)
    screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2 - 100))

    # Wrap the fact text to fit within the screen
    wrapped_lines = wrap_text(current_body['fact'], font, WIDTH - 40)
    for i, line in enumerate(wrapped_lines):
        line_surface = font.render(line, True, WHITE)
        screen.blit(line_surface, (WIDTH // 2 - line_surface.get_width() // 2, HEIGHT // 2 - 60 + i * 30))

    if show_controls:
        control_font = pygame.font.Font(None, 24)
        controls = [
            "Controls:",
            "← → : Move Left/Right",
            "Space: Thrust",
            "R: Retry if you crash"
        ]
        for i, text in enumerate(controls):
            control_text = control_font.render(text, True, WHITE)
            screen.blit(control_text, (WIDTH // 2 - control_text.get_width() // 2, HEIGHT - 120 + i * 25))
       

    pygame.display.flip()
    pygame.time.wait(4000)

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
show_loading_screen(show_controls=True)

# Initialize the first level
reset_game()
# Main game loop
running = True
while running:
    
    screen.blit(current_background, (0, 0))



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
            fuel_remaining -= 0.25  # Small fuel usage for horizontal movement
            angle = 15
        elif keys[pygame.K_RIGHT] and fuel_remaining > 0:
            velocity_x = horizontal_speed  # Move right
            fuel_remaining -= 0.25
            angle = -15
        else:
            velocity_x = 0  # Stop horizontal movement when no key is pressed
            angle = 0

        velocity_y += g  # Apply gravity
        rocket.y += velocity_y  # Update vertical position
        rocket.x += velocity_x  # Update horizontal position

        # Prevent the rocket from moving off-screen
        rocket.x = max(0, min(WIDTH - rocket.width, rocket.x))

        # Check landing
        if rocket.bottom >= landing_pad_y:
            if landing_pad_x <= rocket.x <= landing_pad_x + landing_pad_width - rocket.width:
                if velocity_y > 8:  # Too fast = crash
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
     show_loading_screen()  # ⬅️ This is the new fun fact screen

     reset_game()  # Then reset and move to the next planet


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
    rotated_rocket = pygame.transform.rotate(rocket_img, angle)
    rotated_rect = rotated_rocket.get_rect(center=rocket.center)
    screen.blit(rotated_rocket, rotated_rect.topleft)

    if keys[pygame.K_SPACE] and fuel_remaining > 0:
        rotated_thrust = pygame.transform.rotate(thrust_img, angle)
        thrust_rect = rotated_thrust.get_rect(center=(rocket.centerx, rocket.bottom))
        screen.blit(rotated_thrust, thrust_rect.topleft) 
    pygame.draw.rect(screen, WHITE, (landing_pad_x, landing_pad_y, landing_pad_width, 10))  # Landing pad
    # Display status text
    font = pygame.font.Font(None, 24)
    fuel_text = font.render(f"Fuel: {fuel_remaining}", True, WHITE)
    screen.blit(fuel_text, (10, 10))

    # Display difficulty progression
    font = pygame.font.Font(None, 24)
    current_planet = planet_names[min(gravity_level, len(planet_names) - 1)]
    planet_text = font.render(f"Celestial body: {current_planet}", True, WHITE)
    screen.blit(planet_text, (10, 35))

    pygame.display.flip()
    clock.tick(30)  # Maintain frame rate

pygame.quit()
