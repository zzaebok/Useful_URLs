params = {
    'PAD':'<pad>',
    'UNK':'<unk>',
    'default_fasttext_path':'/content/drive/My Drive/Colab Notebooks/Movie Review/Word_Embedding/ko/ko.bin',
    'default_word_dict_pkl_path':'/content/drive/My Drive/Colab Notebooks/Movie Review/Pickle/word_dict.pkl',
    'default_word_emb_pkl_path':'/content/drive/My Drive/Colab Notebooks/Movie Review/Pickle/word_emb.pkl',
    'default_training_data_path':'/content/drive/My Drive/Colab Notebooks/Movie Review/Data/ratings_train.txt',
    'default_test_data_path':'/content/drive/My Drive/Colab Notebooks/Movie Review/Data/ratings_test.txt',
    'max_seq_length':40,
    'min_vocab_count':10,
    'word_emb_dim':200, #it should be matched with pre-trained word embedding dimension
    'batch_size':300,
    'learning_rate':0.01,
    'SAVER_DIR':'/content/drive/My Drive/Colab Notebooks/Movie Review/ckpt'
}