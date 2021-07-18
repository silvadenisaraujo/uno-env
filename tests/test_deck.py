from uno_env.deck import generate_shuffled_deck


def test_shuffle_deck():
    deck = generate_shuffled_deck()
    assert len(deck) == 108
