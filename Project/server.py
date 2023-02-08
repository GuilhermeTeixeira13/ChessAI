import socket, threading
import os, sys
import time
from datetime import datetime

time_out = 9999

moves_without_eat_to_draw = 9999


def pos1_to_pos2(x):
    row = x // 8
    col = x % 8
    return [row, col]


def pos2_to_pos1(x2):
    return x2[0] * 8 + x2[1]


def get_positions_directions(state, piece, p2, directions):
    ret = []
    for d in directions:
        for r in range(1, d[1] + 1):
            if d[0] == 'N':
                if p2[0] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1]])] == 'z':
                    ret.append([p2[0] - r, p2[1]])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1]])]) - ord(piece)) > 16:
                    ret.append([p2[0] - r, p2[1]])
                break

            if d[0] == 'S':
                if p2[0] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1]])] == 'z':
                    ret.append([p2[0] + r, p2[1]])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1]])]) - ord(piece)) > 16:
                    ret.append([p2[0] + r, p2[1]])
                break
            if d[0] == 'W':
                if p2[1] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0], p2[1] - r])] == 'z':
                    ret.append([p2[0], p2[1] - r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0], p2[1] - r])]) - ord(piece)) > 16:
                    ret.append([p2[0], p2[1] - r])
                break
            if d[0] == 'E':
                if p2[1] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0], p2[1] + r])] == 'z':
                    ret.append([p2[0], p2[1] + r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0], p2[1] + r])]) - ord(piece)) > 16:
                    ret.append([p2[0], p2[1] + r])
                break
            if d[0] == 'NE':
                if p2[0] - r < 0 or p2[1] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1] + r])] == 'z':
                    ret.append([p2[0] - r, p2[1] + r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] + r])]) - ord(piece)) > 16:
                    ret.append([p2[0] - r, p2[1] + r])
                break
            if d[0] == 'SW':
                if p2[0] + r > 7 or p2[1] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1] - r])] == 'z':
                    ret.append([p2[0] + r, p2[1] - r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] - r])]) - ord(piece)) > 16:
                    ret.append([p2[0] + r, p2[1] - r])
                break
            if d[0] == 'NW':
                if p2[0] - r < 0 or p2[1] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1] - r])] == 'z':
                    ret.append([p2[0] - r, p2[1] - r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] - r])]) - ord(piece)) > 16:
                    ret.append([p2[0] - r, p2[1] - r])
                break
            if d[0] == 'SE':
                if p2[0] + r > 7 or p2[1] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1] + r])] == 'z':
                    ret.append([p2[0] + r, p2[1] + r])
                    continue

                if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] + r])]) - ord(piece)) > 16:
                    ret.append([p2[0] + r, p2[1] + r])
                break
            if d[0] == 'PS':
                if p2[0] + r > 7:
                    break
                if state[pos2_to_pos1([p2[0] + r, p2[1]])] == 'z':
                    ret.append([p2[0] + r, p2[1]])
                continue
            if d[0] == 'PN':
                if p2[0] - r < 0:
                    break
                if state[pos2_to_pos1([p2[0] - r, p2[1]])] == 'z':
                    ret.append([p2[0] - r, p2[1]])
                continue
            if d[0] == 'PS2':
                if p2[0] + r <= 7 or p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] + r, p2[1] + 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] + 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] + r, p2[1] + 1])

                if p2[0] + r <= 7 or p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] + r, p2[1] - 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] + r, p2[1] - 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] + r, p2[1] - 1])
                continue
            if d[0] == 'PN2':
                if p2[0] - r >= 0 or p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] - r, p2[1] + 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] + 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] - r, p2[1] + 1])

                if p2[0] - r >= 0 or p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] - r, p2[1] - 1])] != 'z':
                        if abs(ord(state[pos2_to_pos1([p2[0] - r, p2[1] - 1])]) - ord(piece)) > 16:
                            ret.append([p2[0] - r, p2[1] - 1])
                continue
            if d[0] == 'H':
                if p2[0] - 2 >= 0 and p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] - 2, p2[1] - 1])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] - 2, p2[1] - 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 2, p2[1] - 1])

                if p2[0] - 2 >= 0 and p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] - 2, p2[1] + 1])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] - 2, p2[1] + 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 2, p2[1] + 1])

                if p2[0] - 1 >= 0 and p2[1] + 2 <= 7:
                    if state[pos2_to_pos1([p2[0] - 1, p2[1] + 2])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] - 1, p2[1] + 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 1, p2[1] + 2])

                if p2[0] + 1 <= 7 and p2[1] + 2 <= 7:
                    if state[pos2_to_pos1([p2[0] + 1, p2[1] + 2])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] + 1, p2[1] + 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 1, p2[1] + 2])

                if p2[0] + 2 <= 7 and p2[1] + 1 <= 7:
                    if state[pos2_to_pos1([p2[0] + 2, p2[1] + 1])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] + 2, p2[1] + 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 2, p2[1] + 1])

                if p2[0] + 2 <= 7 and p2[1] - 1 >= 0:
                    if state[pos2_to_pos1([p2[0] + 2, p2[1] - 1])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] + 2, p2[1] - 1])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 2, p2[1] - 1])

                if p2[0] + 1 <= 7 and p2[1] - 2 >= 0:
                    if state[pos2_to_pos1([p2[0] + 1, p2[1] - 2])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] + 1, p2[1] - 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] + 1, p2[1] - 2])

                if p2[0] - 1 >= 0 and p2[1] - 2 >= 0:
                    if state[pos2_to_pos1([p2[0] - 1, p2[1] - 2])] == 'z' or abs(
                            ord(state[pos2_to_pos1([p2[0] - 1, p2[1] - 2])]) - ord(piece)) > 16:
                        ret.append([p2[0] - 1, p2[1] - 2])
    return ret


def get_available_positions(state, p2, piece):
    ret = []
    if piece in ('a', 'h', 'A', 'H'):  # Tower
        aux = get_positions_directions(state, piece, p2, [['N', 7], ['S', 7], ['W', 7], ['E', 7]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('c', 'f', 'C', 'F'):  # Bishop
        aux = get_positions_directions(state, piece, p2, [['NE', 7], ['SE', 7], ['NW', 7], ['SW', 7]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('d', 'D'):  # Queen
        aux = get_positions_directions(state, piece, p2,
                                       [['N', 7], ['S', 7], ['W', 7], ['E', 7], ['NE', 7], ['SE', 7], ['NW', 7],
                                        ['SW', 7]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('e', 'E'):  # King
        aux = get_positions_directions(state, piece, p2,
                                       [['N', 1], ['S', 1], ['W', 1], ['E', 1], ['NE', 1], ['SE', 1], ['NW', 1],
                                        ['SW', 1]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if piece in ('b', 'g', 'B', 'G'):  # Horse
        aux = get_positions_directions(state, piece, p2, [['H', 1]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    # Pawn
    if ord('i') <= ord(piece) <= ord('p'):
        if p2[0] == 1:
            aux = get_positions_directions(state, piece, p2, [['PS', 2]])
            if len(aux) > 0:
                ret.extend(aux)
        else:
            aux = get_positions_directions(state, piece, p2, [['PS', 1]])
            if len(aux) > 0:
                ret.extend(aux)
        aux = get_positions_directions(state, piece, p2, [['PS2', 1]])
        if len(aux) > 0:
            ret.extend(aux)
        return ret

    if ord('I') <= ord(piece) <= ord('P'):
        if p2[0] == 6:
            aux = get_positions_directions(state, piece, p2, [['PN', 2]])
            if len(aux) > 0:
                ret.extend(aux)
        else:
            aux = get_positions_directions(state, piece, p2, [['PN', 1]])
            if len(aux) > 0:
                ret.extend(aux)
        aux = get_positions_directions(state, piece, p2, [['PN2', 1]])
        if len(aux) > 0:
            ret.extend(aux)
    return ret


def sucessor_states(state, player):
    ret = []

    for x in range(ord('a') - player * 32, ord('p') - player * 32 + 1):

        p = state.find(chr(x))
        if p < 0:
            continue
        p2 = pos1_to_pos2(p)

        pos_available = get_available_positions(state, p2, chr(x))
        # print('%c - Tot %d' % (chr(x), len(pos_available)))

        for a in pos_available:
            state_aux = list('%s' % state)
            state_aux[p] = 'z'
            if ord('i') <= x <= ord('p') and a[0] == 7:
                state_aux[pos2_to_pos1(a)] = 'd'
            elif ord('I') <= x <= ord('P') and a[0] == 0:
                state_aux[pos2_to_pos1(a)] = 'D'
            else:
                state_aux[pos2_to_pos1(a)] = chr(x)
            ret.append(''.join(state_aux))

    return ret


def valid_move(prev, cur, player):
    suc = sucessor_states(prev, player)
    for s in suc:
        if s == cur:
            return True

    return False


def check_winner(cur_state):
    if cur_state.find('e') < 0:
        return 1
    if cur_state.find('E') < 0:
        return 0
    return 2


def pieces_eaten(prev_state, cur_state):
    for c in prev_state:
        if cur_state.find(c) < 0:
            return True
    return False


# #####################################################################################################################
# PRINT Board

pieces = ''.join(chr(9812 + x) for x in range(12))
pieces = u' ' + pieces[:6][::-1] + pieces[6:]
allbox = ''.join(chr(9472 + x) for x in range(200))
box = [allbox[i] for i in (2, 0, 12, 16, 20, 24, 44, 52, 28, 36, 60)]
(vbar, hbar, ul, ur, ll, lr, nt, st, wt, et, plus) = box

h3 = hbar * 3

# useful constant unicode strings to draw the square borders

topline = ul + (h3 + nt) * 7 + h3 + ur
midline = wt + (h3 + plus) * 7 + h3 + et
botline = ll + (h3 + st) * 7 + h3 + lr

tpl = u' {0} ' + vbar


def inter(*args):
    """Return a unicode string with a line of the chessboard.

    args are 8 integers with the values
        0 : empty square
        1, 2, 3, 4, 5, 6: white pawn, knight, bishop, rook, queen, king
        -1, -2, -3, -4, -5, -6: same black pieces
    """
    assert len(args) == 8
    return vbar + u''.join((tpl.format(pieces[a]) for a in args))


print
pieces
print
' '.join(box)
print

start_position = (
        [
            (-4, -2, -3, -5, -6, -3, -2, -4),
            (-1,) * 8,
        ] +
        [(0,) * 8] * 4 +
        [
            (1,) * 8,
            (4, 2, 3, 5, 6, 3, 2, 4),
        ]
)


def _game(position):
    yield topline
    yield inter(*position[0])
    for row in position[1:]:
        yield midline
        yield inter(*row)
    yield botline


game = lambda squares: "\n".join(_game(squares))
game.__doc__ = "Return the chessboard as a string for a given position."


def print_board(prev, cur, idx, nick):
    # print('print_board()_%s_...' % cur)
    state_show = []
    for r in range(0, 8):
        row = []
        for c in range(0, 8):
            if cur[pos2_to_pos1([r, c])] == 'z':
                row.append(0)

            if cur[pos2_to_pos1([r, c])] == 'a':
                row.append(-4)
            if cur[pos2_to_pos1([r, c])] == 'b':
                row.append(-2)
            if cur[pos2_to_pos1([r, c])] == 'c':
                row.append(-3)
            if cur[pos2_to_pos1([r, c])] == 'd':
                row.append(-5)
            if cur[pos2_to_pos1([r, c])] == 'e':
                row.append(-6)
            if cur[pos2_to_pos1([r, c])] == 'f':
                row.append(-3)
            if cur[pos2_to_pos1([r, c])] == 'g':
                row.append(-2)
            if cur[pos2_to_pos1([r, c])] == 'h':
                row.append(-4)
            if ord('i') <= ord(cur[pos2_to_pos1([r, c])]) <= ord('p'):
                row.append(-1)

            if cur[pos2_to_pos1([r, c])] == 'A':
                row.append(4)
            if cur[pos2_to_pos1([r, c])] == 'B':
                row.append(2)
            if cur[pos2_to_pos1([r, c])] == 'C':
                row.append(3)
            if cur[pos2_to_pos1([r, c])] == 'D':
                row.append(5)
            if cur[pos2_to_pos1([r, c])] == 'E':
                row.append(6)
            if cur[pos2_to_pos1([r, c])] == 'F':
                row.append(3)
            if cur[pos2_to_pos1([r, c])] == 'G':
                row.append(2)
            if cur[pos2_to_pos1([r, c])] == 'H':
                row.append(4)
            if ord('I') <= ord(cur[pos2_to_pos1([r, c])]) <= ord('P'):
                row.append(1)
        state_show.append(tuple(row))

    ret = game(state_show) + '\n'

    if prev is None:
        return ret
    # print('before description...')
    ret = ret + description_move(prev, cur, idx, nick)
    # print('after description...')

    return ret


def get_description_piece(piece):
    if ord(piece) < 97:
        ret = 'Black '
    else:
        ret = 'White '
    if piece.lower() in ('a', 'h'):
        ret = ret + 'Tower'
    elif piece.lower() in ('b', 'g'):
        ret = ret + 'Horse'
    elif piece.lower() in ('c', 'f'):
        ret = ret + 'Bishop'
    elif piece.lower() == 'd':
        ret = ret + 'Queen'
    elif piece.lower() == 'e':
        ret = ret + 'King'
    else:
        ret = ret + 'Pawn'
    return ret


def description_move(prev, cur, idx, nick):
    # print('description_move()')
    ret = 'Move [%d - %s]: ' % (idx, nick)

    cur_blank = [i for i, ltr in enumerate(cur) if ltr == 'z']
    prev_not_blank = [i for i, ltr in enumerate(prev) if ltr != 'z']
    # print(cur_blank)
    # print(prev_not_blank)
    moved = list(set(cur_blank) & set(prev_not_blank))
    # print(moved)
    moved = moved[0]

    desc_piece = get_description_piece(prev[moved])

    fr = pos1_to_pos2(moved)
    to = pos1_to_pos2(cur.find(prev[moved]))
    # print(fr)
    # print(to)

    ret = ret + desc_piece + ' (%d, %d) --> (%d, %d)' % (fr[0], fr[1], to[0], to[1])
    if prev[pos2_to_pos1(to)] != 'z':
        desc_piece = get_description_piece(prev[pos2_to_pos1(to)])
        ret = ret + ' eaten ' + desc_piece
    return ret


# #####################################################################################################################


host = sys.argv[1]  # LocalHost
port = int(sys.argv[2])  # Choosing unreserved port
colors = ['White', 'Black']

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket initialization
server.bind((host, port))  # binding host and port to socket
server.listen()

client_0, address_0 = server.accept()
nick_0 = client_0.recv(1024).decode('ascii')

client_1, address_1 = server.accept()
nick_1 = client_1.recv(1024).decode('ascii')

nicks = [nick_0, nick_1]
clients = [client_0, client_1]

cur_state = 'abcdefghijklmnopzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzIJKMNLOPABCDEFGH'

date_time_file = os.path.join(
    '%s' % nick_0 + '_' + '%s' % nick_1 + '_' + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + '_log.txt')

file_out = open(date_time_file, "a+")

print('%s' % print_board(None, cur_state, 0, None))

idx_move = 0
moves_without_eat = 0
while True:

    try:
        # print('>>[%d] move %d - %s should play. Sending state_%s_' % (idx_move, idx_move % 2, nicks[idx_move % 2], cur_state))
        clients[idx_move % 2].send(cur_state.encode('ascii'))
        prev_state = '%s' % cur_state
        while True:
            clients[idx_move % 2].settimeout(time_out)
            cur_state = clients[idx_move % 2].recv(1024).decode('ascii')
            if len(cur_state) > 0:
                break
        # print('Received state_%s_' % cur_state)

        valid_mv = valid_move(prev_state, cur_state, idx_move % 2)
        # print('Valid %d' % valid_mv)
        if not valid_mv:
            file_out.write('%s\n' % description_move(prev_state, cur_state, idx_move, nicks[idx_move % 2]))
            print('%s' % description_move(prev_state, cur_state, idx_move, nicks[idx_move % 2]))
            print('Invalid move by %d - %s. Player %d - %s wins. Game finished. ' % (
            idx_move % 2, nicks[idx_move % 2], 1 - (idx_move % 2), nicks[1 - (idx_move % 2)]))
            file_out.write('Invalid move by %d - %s. Player %d - %s wins. Game finished. ' % (
            idx_move % 2, nicks[idx_move % 2], 1 - (idx_move % 2), nicks[1 - (idx_move % 2)]))
            break
        # print('printing board...')
        board = print_board(prev_state, cur_state, idx_move, nicks[idx_move % 2])
        print('%s' % board)

        # Antes -> file_out.write('%s\n' % print_board(prev_state, cur_state, idx_move, nicks[idx_move % 2]) -> Explodia aqui e entrava no Except
        file_out.write('%s\n' % description_move(prev_state, cur_state, idx_move, nicks[idx_move % 2]))

        # print('Evaluating finish')
        finish = check_winner(cur_state)
        # print('Evaluated finish %d' % finish)

        if finish < 2:
            print('Player %d - %s: %s wins. Game finished. ' % (finish, nicks[finish], colors[finish]))
            file_out.write('Player %d - %s: %s wins. Game finished. ' % (finish, nicks[finish], colors[finish]))
            break

        eat = pieces_eaten(prev_state, cur_state)
        if not eat:
            moves_without_eat += 1
        else:
            moves_without_eat = 0
        if moves_without_eat >= moves_without_eat_to_draw:
            print('%d consecutives without eaten pieces. %s - %s Draw. Game finished. ' % (
            moves_without_eat, nicks[0], nicks[1]))
            file_out.write('%d consecutives without eaten pieces. %s - %s Draw. Game finished. ' % (
            moves_without_eat, nicks[0], nicks[1]))
            break

        idx_move += 1
        time.sleep(0.1)
        # print('Done...')
    except:
        print('Timeout by %d - %s: %s. Player %d - %s: %s wins. Game finished. ' % (
        idx_move % 2, nicks[idx_move % 2], colors[idx_move % 2], 1 - (idx_move % 2), nicks[1 - (idx_move % 2)],
        colors[1 - (idx_move % 2)]))
        file_out.write('Timeout by %d - %s: %s. Player %d - %s: %s wins. Game finished. ' % (
        idx_move % 2, nicks[idx_move % 2], colors[idx_move % 2], 1 - (idx_move % 2), nicks[1 - (idx_move % 2)],
        colors[1 - (idx_move % 2)]))
        break

file_out.close()