def vlog(message, level=1):
    if log_level >= level:
        print(message, flush=True)

def set_v_lvl(level):
    global log_level
    log_level = level

def build_letter_dict(coords):
    vlog('Enter button coords: {}'.format(coords))
    letter_dict = {}

    rel_coords = (coords[0] + 60, coords[1])
    for l in 'zxcvbnm':
        letter_dict[l] = rel_coords
        vlog('Added \'{}\' to dict with coords {}'.format(l, rel_coords), 3)
        rel_coords = (rel_coords[0] + 50, rel_coords[1])

    rel_coords = (rel_coords[0], rel_coords[1] - 65)
    for l in 'lkjhgfdsa':
        letter_dict[l] = rel_coords
        vlog('Added \'{}\' to dict with coords {}'.format(l, rel_coords), 3)
        rel_coords = (rel_coords[0] - 50, rel_coords[1])

    rel_coords = (rel_coords[0] + 30, rel_coords[1] - 65)
    for l in 'qwertyuiop':
        letter_dict[l] = rel_coords
        vlog('Added \'{}\' to letter dict with coords {}'.format(l, rel_coords), 3)
        rel_coords = (rel_coords[0] + 50, rel_coords[1])

    vlog(letter_dict, 4)
    return letter_dict

def build_board_dict(coords):
    vlog('Top left space coords: {}'.format(coords))
    board_dict = {}

    count = 0
    rel_coords = (coords[0], coords[1])
    for r in range(6):
        for c in range(5):
            board_dict[count] = rel_coords
            vlog('Added \'{}\' to board dict with coords {}'.format(count, rel_coords), 3)
            rel_coords = (rel_coords[0] + 67, rel_coords[1])
            count += 1
        rel_coords = (coords[0], rel_coords[1] + 67)

    vlog(board_dict, 4)
    return board_dict