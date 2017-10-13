from soy.utils import DoublespaceLineCorpus
from soy.nlp.extractors import KeywordExtractor
from soy.nlp.tokenizer import LTokenizer

corpus = DoublespaceLineCorpus(fname, iter_sent = True)
word_extractor = KeywordExtractor(corpus, min_count = 10)
words = word_extractor.extract()
scores = {w:s.cohesion_forward for w, s in words.items()}
tokenizer = LTokenizer(scores=scores)
tokenizer.tokenize("이게 잘 될지 모르겠네요.")