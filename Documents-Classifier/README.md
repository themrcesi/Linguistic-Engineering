# Document Classifier with Glossary

Document classifiers are based on categorizing a series of documents based on their characteristics. According to this definition, we can easily distinguish two types of document classifiers:
+ **Manual classifiers**: the texts are classified in a subject having been read by a person and making a logical classification of them. This is what happens, for example, in physical libraries, where the various documents, the books in this case, are distributed into categories manually.
+ **Automatic classifiers**: the texts are classified in a subject without a reading and understanding by a person. A computer program is in charge of obtaining a series of characteristics of the documents and classifying them based on these characteristics. We find here two types of automatic classifiers:
  + Document classifiers with glossary: they start from a set of key words, called glossary, as a reference. 
  + Document classifiers without glossary: grouping documents into categories based on similarity metrics.

In this directory you can find an implementation of a document classifier with glossary.

## Project structure

* In the subfolder ``/documents`` you will find the documents for each of the themes, as well as a file containing a list of *stopwords*.
* In the subfolder ``/keywords`` we are going to save the glossaries generated for each of the topics.
* In the last sub-folder, ``/src``, are the scripts that have been used to achieve the objectives. These are the two files that we see with the extension .ipynb.
* Finally, the document ``gabarre_documents_classifier.pdf``, which is the report of this project.

## Documents

In order to implement our classifier, documents from three different topics were selected. We decided to use as topics: health, politics and sports. So we finally collected 50 documents of each of the previously mentioned topics.

---

## Glossary creation

A 'glossary' is a catalog of words from the same discipline, the same field of study, the same work, etc., defined or commented upon.

Glossaries are a fundamental part of this project since they are the ones that will allow us to later classify each document in one category or another. Therefore, a correct classification of documents will depend on the good creation of glossaries.

### Methodology 

From the very beginning, our intention has been to automate the process of generating glossaries as much as possible. To achieve this automation, we have decided to extract the 100 most representative terms of each class in 3 different ways and then make the intersection two to two of these sets and finally perform a manual filtering of this aggregation to keep 30 words. Therefore, we managed to generate the glossaries in a semi-automatic process, all this done with only 15 documents from each class.

The process of creating glossaries is as follows:
+ Choose at random 15 documents from each class.
+ Extraction of the 100 most representative terms from each class in 3 different ways, eliminating the terms that appear in several classes because they are not representative of only one class.
  + Method 1: TF-IDF
  + Method 2: Already implemented terminology extractor using [Gensim](https://radimrehurek.com/gensim/).
  + Method 3: K-Means.
+ Aggregate these local glossaries in a single global glossary.
+ Filter manually this global glossary and keep the 30 terms that we consider most representative.

---

## Classifier

Once the glossaries for each category have been created, we can proceed to classify the documents in the test suite based on these glossaries. This requires the use of a document classifier. A multitude of algorithms have been used for this task: from traditional approaches using Logistic Regression to more modern approaches using Neural Networks.

For the purpose of this project, three different methods have been analyzed and implemented: Vector Space Model using TF-IDF, Wrod2Vec and a Bayesian Classifier.

### Vector Space Model using TF-IDF

The Vector Space Model is one of the three traditional models in the field of Information Retrieval along with the Boolean Model and the Probabilistic Model. This model presents an improvement over the Boolean model by allowing partial matches. Particularly, this model represents the documents by means of weight vectors. In our particular case, we will use the tf-idf metric for the vector weights. 

This model makes use of other concepts such as *dictionary* and *bag of words* which we will describe in the next two sections. In turn, to establish the similarities between documents, the cosine is used between the vectors.

In spite of how simple and old this model is, it is still one of the most popular ones today. This is why we have decided to use it in our document classification task. What we will do is calculate the similarity between the documents and each glossary by classifying each document to the glossary class that most closely resembles it. Again, for the implementation of this model we have used the *Gensim* library.

### Word2Vec

The second classifier we decided to try is one based also on the representation of words by vectors. Therefore, the whole procedure (calculating similarities, converting into probabilities, classifying the documents) will be exactly the same.

However, this time we will not use the tf-idf model to calculate the vectors. As a model we will use the famous 'Word2Vec' text created by Mikolov et al. (2013) that represents the words as *embeddings*. These *embeddings* are computed by means of a neural network.

### Bayesian Classifier

Within the automatic learning classification algorithms, the use of, among others, tSupport Vector Machine, k-Nearest Neighbor or Naïve Bayes stands out in the classification of texts. We are aware that for an automatic learning algorithm to work well and be reliable it is necessary to have a large dataset, of the order of 10,000 data. However, we wanted to test from the beginning how an automatic learning algorithm works.

We chose to use a Naïve Bayes classifier. This type of classifier is based on Bayes' naive assumption (or Naïve Bayes assumption), assuming that the predictor variables -in our case the words- are independent. That is, the appearance of a certain word in the text is not related to the appearance of any other word. This assumption is clearly false in the domain of text classification, however, it works very well in classification tasks. This paradox is explained in Friedman 1997.

These classifiers work by learning in training the conditional probability of each attribute (each word) given a class (health, sports or politics). Once trained, the classification is made by applying Bayes' rule to calculate the probability of each class according to the words in each document.





