from scipy import spatial


def distance(embeddings, word, reference):
	return spatial.distance.cosine(embeddings[word], embeddings[reference])


def closest_words(embeddings, reference):
	return sorted(embeddings.keys(), key=lambda w: distance(embeddings, w, reference))


def goodness(embeddings, word, targets, bad):
	if word in targets + bad: return -float('inf')
	return sum([distance(embeddings, word, b) for b in bad]) - 4.0 * sum([distance(embeddings, word, t) for t in targets])


# Maximize distance from answers words, minimize distance from bad words
def minimax(embeddings, word, target, bad):
	if word in target + bad: return -float('inf')
	return min([distance(embeddings, word, b) for b in bad]) - max([distance(embeddings, word, t) for t in target])
