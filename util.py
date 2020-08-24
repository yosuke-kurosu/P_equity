# =================
import itertools
import collections
# =================

rank_to_num = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}
rank_list = list(rank_to_num)
suit_list = ['s', 'd', 'c', 'h']
player_num = 2


def rank_of_seven_card(seven_card_list):
    five_card_list = itertools.combinations(seven_card_list, 5)
    best_rank_num = max(rank_of_five_card(five_card) for five_card in five_card_list)
    return best_rank_num


def rank_of_five_card(card_list):
    ranks = [rank_to_num[c[0]] for c in card_list]
    num_cnt = collections.Counter(ranks)
    num_cnt = sorted(num_cnt.items(), key=lambda x: x[1] * 10 + x[0], reverse=True)
    suits = [c[1] for c in card_list]
    is_flush = len(set(suits)) == 1
    high = sum([item[0] * 10 ** (4 - i) for i, item in enumerate(num_cnt)])

    if len(num_cnt) == 2:
        if num_cnt[0][1] == 4:
            rank_num = 8  # four of a kind
        else:
            rank_num = 6  # full house
    elif len(num_cnt) == 3:
        if num_cnt[0][1] == 3:
            rank_num = 4  # three of a kind
        else:
            rank_num = 3  # two pair
    elif len(num_cnt) == 4:
        rank_num = 2  # one pair
    else:
        is_straight = (num_cnt[0][0] - num_cnt[4][0] == 4) or (num_cnt[0][0] == 14 and num_cnt[1][0] == 5) # 13枚のポーカーに書き直す
        if num_cnt[0][0] == 14 and num_cnt[1][0] == 5: 
            high = 54321 # five high flush
        if is_flush and is_straight:
            rank_num = 9  # straight flush
        elif is_flush:
            rank_num = 7  # flush
        elif is_straight:
            rank_num = 5  # straight
        else:
            rank_num = 1  # high card
    rank_num = rank_num * 10 ** 6 + high # Aが14（1桁→2桁）になるのでrank補正を5桁→6桁に修正
    return rank_num


def run(hole_cards, flop=None):
    """
    input:
        holecards()     
    output:
        equity()
    """
    # デッキは毎回初期化する必要あり
    deck = [r + s for r in rank_list for s in suit_list]
    # hollcardをデッキから削除
    deck.remove(hole_cards[0][0])
    deck.remove(hole_cards[0][1])
    deck.remove(hole_cards[1][0])
    deck.remove(hole_cards[1][1])
    boards = list(itertools.combinations(deck, 5))
    if flop != None:  # if flopでok
        boards = [board for board in boards if len(set(flop) & set(board))==len(flop)]
    else:
        pass
    player_win = [0] * player_num
    for board in boards:
        player_rank = [rank_of_seven_card(board + hole_cards[player]) for player in range(player_num)]
        winning_player = [player_rank[player] == max(player_rank) for player in range(player_num)]
        winning_cnt = sum(winning_player)
        player_win = [player_win[player] + winning_player[player] / winning_cnt for player in range(player_num)]
    return [player_win[player] / len(boards) for player in range(player_num)]
