from flask import Blueprint, jsonify, request
from app.game.ai_player import AIPlayer
from app.game.deck import Deck
from app.game.player import Player

bp = Blueprint('routes', __name__)

players = []
current_deck = Deck()

@bp.route('/start_game', methods=['POST'])
def start_game():
    global players, current_deck
    data = request.form
    player_name = data.get('player_name')
    
    # Сброс текущей игры
    current_deck = Deck()
    players = [Player(player_name), AIPlayer("AI")]

    deal_cards()
    return jsonify({"success": True})

def deal_cards():
    # Раздача случайных карт игрокам
    for player in players:
        player.hand = current_deck.draw(13)  # По 13 карт на игрока

@bp.route('/game_state', methods=['GET'])
def game_state():
    state = {
        "players": [{"name": player.name, "hand": [str(card) for card in player.hand]} for player in players],
        "current_card": str(current_deck.cards[-1]) if current_deck.cards else None
    }
    return jsonify(state)

@bp.route('/make_move', methods=['POST'])
def make_move():
    player_name = request.form['player_name']
    card = request.form['card']
    position = request.form['position']

    for player in players:
        if player.name == player_name:
            player.place_card(card, position)
            return jsonify({"success": True})

    return jsonify({"success": False})

@bp.route('/ai_move', methods=['GET'])
def ai_move():
    ai_player = next(p for p in players if isinstance(p, AIPlayer))
    decision = ai_player.make_decision()
    ai_player.place_card(decision['card'], decision['position'])

    return jsonify({"success": True, "decision": decision})
