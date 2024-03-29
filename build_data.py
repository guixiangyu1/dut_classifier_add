from model.config import Config
from model.data_utils import CoNLLDataset, get_vocabs, UNK, NUM, \
    get_glove_vocab, write_vocab, load_vocab, get_char_vocab, \
    export_trimmed_glove_vectors, get_processing_word, entity2vocab


def main():
    """Procedure to build data

    You MUST RUN this procedure. It iterates over the whole dataset (train,
    dev and test) and extract the vocabularies in terms of words, tags, and
    characters. Having built the vocabularies it writes them in a file. The
    writing of vocabulary in a file assigns an id (the line #) to each word.
    It then extract the relevant GloVe vectors and stores them in a np array
    such that the i-th entry corresponds to the i-th word in the vocabulary.


    Args:
        config: (instance of Config) has attributes like hyper-params...

    """
    # get config and processing of words
    config = Config(load=False)
    processing_word = get_processing_word(lowercase=True) # 把字符全部小写，数字替换成NUM

    # Generators
    dev   = CoNLLDataset(config.filename_dev, processing_word) # 创建一个生成器对象，每一次迭代产生tuple （words，tags）
    test  = CoNLLDataset(config.filename_test, processing_word) # 返回一句话（words），和标签tags
    train = CoNLLDataset(config.filename_train, processing_word)


    #进一步处理数据



    # Build Word and Tag vocab
    vocab_words, vocab_tags = get_vocabs([train, dev, test])   # word词表， tags表
    print(len(vocab_words))


    vocab_glove = get_glove_vocab(config.filename_glove)       # glove词表


    vocab = vocab_words & vocab_glove                          # & 求交集  set，都是集合
    vocab.add(UNK)
    vocab.add(NUM)                                             # 手动添加
    print("len of vocab without entity: ", len(vocab))

    # vocab_entity = entity2vocab(datasets=[train, dev, test])
    # vocab.update(vocab_entity)
    # vocab = entity2vocab(datasets=[train, dev], vocab=vocab)

    # Save vocab
    write_vocab(vocab, config.filename_words)
    write_vocab(vocab_tags, config.filename_tags)

    # Trim GloVe Vectors
    vocab = load_vocab(config.filename_words)    # 得到dict类型的vocab：{word:index}
    # 针对vocab，生成numpy的embedding文件，包含一个矩阵，对应词嵌入
    export_trimmed_glove_vectors(vocab, config.filename_glove,
                                config.filename_trimmed, config.dim_word)


    # Build and save char vocab   生成字母表, 这里没用到小写化的东西。只有文件本身。
    train = CoNLLDataset(config.filename_train)
    vocab_chars = get_char_vocab(train)
    write_vocab(vocab_chars, config.filename_chars)


if __name__ == "__main__":
    main()
