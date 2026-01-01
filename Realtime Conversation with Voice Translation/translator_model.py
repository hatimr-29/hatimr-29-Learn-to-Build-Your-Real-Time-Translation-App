# translator_model.py
import math

class NearestNeighborTranslator:
    """
    Simple ML-style translator using Nearest Neighbor:
    - Training data: parallel sentence pairs
    - Vectorization: Bag-of-words
    - Prediction: Cosine similarity
    """

    def __init__(self, src_sentences, tgt_sentences):
        assert len(src_sentences) == len(tgt_sentences), "Training data mismatch."

        self.src_sentences = [s.lower() for s in src_sentences]
        self.tgt_sentences = tgt_sentences

        # Build vocabulary
        vocab = set()
        for s in self.src_sentences:
            for w in s.split():
                vocab.add(w)

        self.vocab = sorted(list(vocab))
        self.word_index = {w: i for i, w in enumerate(self.vocab)}

        # Precompute training vectors
        self.src_vectors = [self.vectorize(s) for s in self.src_sentences]

    def vectorize(self, sentence: str):
        vec = [0] * len(self.vocab)
        for w in sentence.lower().split():
            if w in self.word_index:
                vec[self.word_index[w]] += 1
        return vec

    @staticmethod
    def cosine_similarity(v1, v2):
        dot = sum(a*b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a*a for a in v1))
        norm2 = math.sqrt(sum(b*b for b in v2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def translate(self, sentence: str):
        sentence = sentence.strip()
        if not sentence:
            return "[No input detected]"

        vec = self.vectorize(sentence)

        best_idx = None
        best_score = -1.0

        for i, ref_vec in enumerate(self.src_vectors):
            score = self.cosine_similarity(vec, ref_vec)
            if score > best_score:
                best_score = score
                best_idx = i

        if best_idx is None or best_score <= 0.0:
            return "[No close translation found]"
        
        return self.tgt_sentences[best_idx]
