from db.database import Wordbook


def generate_phrase_url(id: int) -> str:
    wb = Wordbook()
    phrase = []
    for pos, pw in zip(wb.wordbook_PoS, wb.wordbook_lens):
        phrase.append(wb.wordbook[pos][id % pw].capitalize())
        id //= pw

    return ''.join(phrase)