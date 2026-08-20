# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Byte-Pair Encoding (BPE) Primitive
Description: Implements the foundational subword tokenization algorithm used by GPT,
             iteratively merging the most frequent adjacent character pairs.
"""
import re
from collections import defaultdict


class BPEEngine:
    @staticmethod
    def get_vocab_frequencies(text_corpus: list[str]) -> dict:
        vocab = defaultdict(int)
        for word in text_corpus:
            # Split word into characters with a space, append ending token '</w>'
            chars = " ".join(list(word)) + " </w>"
            vocab[chars] += 1
        return vocab

    @staticmethod
    def get_pair_stats(vocab: dict) -> dict:
        pairs = defaultdict(int)
        for word, freq in vocab.items():
            symbols = word.split()
            for i in range(len(symbols) - 1):
                pairs[symbols[i], symbols[i+1]] += freq
        return pairs

    @staticmethod
    def merge_vocab(best_pair: tuple, v_in: dict) -> dict:
        v_out = {}
        # Create regex to match the exact pair separated by a space
        bigram = re.escape(' '.join(best_pair))
        p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
        
        replacement = ''.join(best_pair)
        for word in v_in:
            w_out = p.sub(replacement, word)
            v_out[w_out] = v_in[word]
        return v_out

    @classmethod
    def run_bpe_training(cls, corpus: list[str], num_merges: int) -> dict:
        vocab = cls.get_vocab_frequencies(corpus)
        for i in range(num_merges):
            pairs = cls.get_pair_stats(vocab)
            if not pairs:
                break
            # Find the most frequent adjacent pair
            best = max(pairs, key=pairs.get)
            vocab = cls.merge_vocab(best, vocab)
        return vocab


if __name__ == "__main__":
    # Small corpus with repetitive subword 'est'
    training_data = ["lowest", "lowest", "lowest", "lowest", "lowest", "newer", "newer", "wider", "wider"]
    
    # Run 3 BPE Merges
    final_vocab = BPEEngine.run_bpe_training(training_data, num_merges=3)
    
    # By observing the data, 'e' and 's' are highly frequent together, then 'es' and 't'
    # After 3 merges, we expect 'est</w>' to be merged into a single token block.
    vocab_keys = list(final_vocab.keys())
    
    # Assert compression occurred
    assert any("est</w>" in k for k in vocab_keys)
    
    print(f"[TASK 01 PASSED] BPE Tokenizer executed 3 merges successfully.\nFinal Vocab States: {vocab_keys}")