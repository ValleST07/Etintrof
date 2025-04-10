import random

def generate_map(width=50, height=50):
    # Create empty map filled with floors (0)
    game_map = [[0 for _ in range(width)] for _ in range(height)]
    
    # Add border walls
    for x in range(width):
        game_map[0][x] = 1  # Top border
        game_map[height-1][x] = 1  # Bottom border
    for y in range(height):
        game_map[y][0] = 1  # Left border
        game_map[y][width-1] = 1  # Right border
    
    # Add random walls
    for _ in range(random.randint(50, 100)):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        game_map[y][x] = 1
        
        # Sometimes make wall clusters
        if random.random() > 0.7:
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < width-1 and 0 < ny < height-1:
                    game_map[ny][nx] = 1
    
    # Add water features
    for _ in range(random.randint(5, 10)):
        # Start a water feature
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        size = random.randint(3, 8)
        
        for _ in range(size):
            game_map[y][x] = 2
            # Random walk to expand water
            dx, dy = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
            x = max(1, min(width-2, x + dx))
            y = max(1, min(height-2, y + dy))
    
    return game_map

# Generate and print a sample map
map_data = generate_map()
for row in map_data:
    print(' '.join(str(cell) for cell in row))