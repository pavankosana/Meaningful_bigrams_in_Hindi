# Meaningful_bigrams_in_Hindi
If a paragraph of Hindi words were given as input in this program, then if returns the meaningful bigrams in the given text.

The initial part of the code is used to train a model for pos_tagger and bigram_tagger.
In the Dataset folder, the two available text files are datasets for training and testing 
the pos_tagger and bigram_tagger.

The assumption of this project is that the bigrams in hindi are always in either of given format.
i.e., all the bigrams would be Noun + Verb, Adjective + verb, Adjective + Noun,
Adverb + Noun, Adverb + Verb, Noun + Noun.

In the corpus folder the two text files are tested to find the meaningful bigrams according to assumption.

Finally, when we found the results are satisfactory we deployed the model using flask.
The web interface's code is written in index.html file which should be placed in templates folder while using the code.
When we run this model, it prompts the text (may be words, paragraphs, sentences) 
and pos_tagger is used to find the combination of all adjacent words and chooses the meaningful bigrams
as those which are either of above said forms. And the result is printed out at the bottom part of html.


--------------Updated Part----------
inltk library is to be installed for finding similarity between hindi words.
so,
iNLTK has a dependency on PyTorch 1.3.1, hence you have to install that first:
pip install torch==1.3.1+cpu -f https://download.pytorch.org/whl/torch_stable.html

You can then install iNLTK using pip:
pip install inltk

all these are updated in the .ipynb file. One can directly run the file in colab.

The dataset consists of 20,000 words and comparing the given dataset with all these 20,000 words
for every iteration for cosine similarity is too heavy for my computer processor(might take more than 3 hours).
so for the demonistration purpose only 20 words are considered for getting cosine similarity.

word_s = bi_wordsss[:20] in sim_words_in_dataset_inputtext(inp,bi_wordsss),
selects the number of words to be used in dataset for comparing.(adjust it accordingly)

To run the code:
The files in the 'Example Inputs' folders can be used to test run the code and deployed flask application.
Steps to run the code:
1) Open the ipynb file in jupyter/pycharm/googleColab.
2)Adjust the paths in the code according to your system.
3)run the code and open the deployed flask application.
