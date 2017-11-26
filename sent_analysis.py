from afinn import Afinn
import numpy as np
from open_data import get_text_reviews_and_id
afinn = Afinn()
print(afinn.score('you look beautiful'))

reviews, ids_reviews = get_text_reviews_and_id()
scores = []
scores_1 = []
for review in reviews:

    scores.append(afinn.score(review))
    if afinn.score(review)>0:
        scores_1.append(1)
    elif afinn.score(review)<0:
        scores_1.append(-1)
    else:
        scores_1.append(0)
