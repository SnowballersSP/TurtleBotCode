def plow_driveway(width, height):
    path = []

    # Step 1: Plow top row left to right
    for x in range(width):
        path.append((x, 0))  # Top row

    # Step 2: Return to start (right to left)
    for x in reversed(range(width)):
        path.append((x, 0))  # Back to top-left

    # Step 3: Start plowing each column, top to bottom, back to top, move right
    for col in range(width):
        # Plow down the column
        for row in range(1, height):
            path.append((col, row))

        # Move back up
        for row in reversed(range(1, height)):
            path.append((col, row - 1))

        # If not the last column, shift right on top row to next column
        if col < width - 1:
            path.append((col + 1, 0))

    return path


# Parameters
width = 5
height = 8

# Simulate
path = plow_driveway(width, height)

# Show path
for step, (x, y) in enumerate(path):
    print(f"Step {step + 1}: Plowing at ({x}, {y})")
