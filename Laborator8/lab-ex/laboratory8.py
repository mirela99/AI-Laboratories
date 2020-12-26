import re
import numpy as np
import pandas as pd
import gensim

from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def get_data_from_file():
        #load data from file
        filename = 'text.txt'
        file= open(filename, 'r')
        text =file.read()
        file.close()

        # split into sentences 
        from nltk import sent_tokenize
        sentences= sent_tokenize(text)
        # print(sentences[2])

        #split into words
        from nltk import word_tokenize
        tokens= word_tokenize(text)

        #convert to lower case
        tokens= [w.lower() for w in tokens]

        #remove all tokens that are not alphabetic
        words= [word for word in tokens if word.isalpha()]
        # print(words[:100])

        #stopwords
        from nltk.corpus import stopwords
        stop_words= set(stopwords.words('english'))
        words =[  w for w in words if not w in stop_words]
        return words

def generate_dictionary_data(text):
    put_index_to_word= dict()
    words=[]
    index_to_word = dict()
    corpus = []
    count = 0
    unique_words_count = 0
    
    for row in text:
        for word in row.split():
            word = word.lower()
            corpus.append(word)
            if put_index_to_word.get(word) == None:
                words.append(word)
                put_index_to_word.update ( {word : count})
                index_to_word.update ( {count : word })
                count  += 1
    unique_words_count = len(put_index_to_word)
    length_of_corpus = len(corpus)
    
    return put_index_to_word,index_to_word,corpus,unique_words_count,length_of_corpus, words

def get_one_hot_vectors(target_word,context_words,unique_words_count,put_index_to_word):
    
    #array of size = unique_words_count filled with zeros
    target_word_vector = np.zeros(unique_words_count)
    
    index_of_word_dictionary = put_index_to_word.get(target_word) 
    
    #Set the index to 1
    target_word_vector[index_of_word_dictionary] = 1
    context_word_vector = np.zeros(unique_words_count)
    for word in context_words:
        index_of_word_dictionary = put_index_to_word.get(word) 
        context_word_vector[index_of_word_dictionary] = 1
        
    return target_word_vector,context_word_vector

# funtion to generate training data
def generate_training_data(corpus,nb_of_words_to_consider_context,unique_words_count,put_index_to_word,length_of_corpus, sample=None):
    
    training_data =  []
    training_sample_words =  []
    for i,word in enumerate(corpus):

        index_target_word = i
        target_word = word
        context_words = []

        #when target word is the first word
        if i == 0:  
            context_words = [corpus[x] for x in range(i + 1 , nb_of_words_to_consider_context + 1)] 
        #when target word is the last word
        elif i == len(corpus)-1:
            context_words = [corpus[x] for x in range(length_of_corpus - 2 ,length_of_corpus -2 - nb_of_words_to_consider_context  , -1 )]

        #When target word is the middle word
        else:

            #Before the middle target word
            before_target_word_index = index_target_word - 1
            for x in range(before_target_word_index, before_target_word_index - nb_of_words_to_consider_context , -1):
                if x >=0:
                    context_words.extend([corpus[x]])

            #After the middle target word
            after_target_word_index = index_target_word + 1
            for x in range(after_target_word_index, after_target_word_index + nb_of_words_to_consider_context):
                if x < len(corpus):
                    context_words.extend([corpus[x]])


        target_word_vector,context_word_vector = get_one_hot_vectors(target_word,context_words,unique_words_count,put_index_to_word)
        training_data.append([target_word_vector,context_word_vector])    
        if sample is not None:
            training_sample_words.append([target_word,context_words]) 
        
    return training_data,training_sample_words

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def forward_prop(weight_inp_hidden,weight_hidden_output,target_word_vector):
    #Lab formula  
    hidden_layer = np.dot(weight_inp_hidden.T, target_word_vector)
    #lab formula
    u = np.dot(weight_hidden_output.T, hidden_layer)
    y_predicted = softmax(u)
    
    return y_predicted, hidden_layer, u


def backward_prop(weight_inp_hidden,weight_hidden_output,total_error, hidden_layer, target_word_vector,learning_rate):
    
    dl_weight_inp_hidden = np.outer(target_word_vector, np.dot(weight_hidden_output, total_error.T))
    dl_weight_hidden_output = np.outer(hidden_layer, total_error)
    
    # Update weights
    weight_inp_hidden = weight_inp_hidden - (learning_rate * dl_weight_inp_hidden)
    weight_hidden_output = weight_hidden_output - (learning_rate * dl_weight_hidden_output)
    
    return weight_inp_hidden,weight_hidden_output

def calculate_error(y_pred,context_words):
    
    total_error = [None] * len(y_pred)
    index_of_1_in_context_words = {}
    
    for index in np.where(context_words == 1)[0]:
        index_of_1_in_context_words.update ( {index : 'yes'} )
        
    number_of_1_in_context_vector = len(index_of_1_in_context_words)
    
    for i,value in enumerate(y_pred):
        
        if index_of_1_in_context_words.get(i) != None:
            total_error[i]= (value-1) + ( (number_of_1_in_context_vector -1) * value)
        else:
            total_error[i]= (number_of_1_in_context_vector * value)
            
            
    return  np.array(total_error) 

def calculate_loss(u,context):
    
    sum_1 = 0
    for index in np.where(context==1)[0]:
        sum_1 = sum_1 + u[index]
    
    sum_1 = -sum_1
    sum_2 = len(np.where(context==1)[0]) * np.log(np.sum(np.exp(u)))
    
    total_loss = sum_1 + sum_2
    return total_loss

def train(word_embedding_dimension,nb_of_words_to_consider_context,epochs,training_data,learning_rate,disp = 'no',interval=-1):
    
    weights_input_hidden = np.random.uniform(-1, 1, (unique_words_count, word_embedding_dimension))
    weights_hidden_output = np.random.uniform(-1, 1, (word_embedding_dimension, unique_words_count))
    weights_1 = []
    weights_2 = []
    
    for epoch in range(epochs):
        loss = 0

        for target,context in training_data:
            y_pred, hidden_layer, u = forward_prop(weights_input_hidden,weights_hidden_output,target)

            total_error = calculate_error(y_pred, context)

            weights_input_hidden,weights_hidden_output = backward_prop(
                weights_input_hidden,weights_hidden_output ,total_error, hidden_layer, target,learning_rate
            )

            loss_temp = calculate_loss(u,context)
            loss += loss_temp
        
        
        weights_1.append(weights_input_hidden)
        weights_2.append(weights_hidden_output)
        
        if disp == 'yes':
            if epoch ==0 or epoch % interval ==0 or epoch == epochs-1:
                print('Epoch: %s. Loss:%s' %(epoch,loss))
    return loss, weights_1, weights_2

def word2vec(word):
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw

def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]





#-------------------------------------------------------------------------------------------------------------------

text = get_data_from_file()
put_index_to_word,index_to_word,corpus,unique_words_count,length_of_corpus, words= generate_dictionary_data(text)
print('Number of unique words:' , unique_words_count)
print('put_index_to_word : ',put_index_to_word)
print('Length of corpus :',length_of_corpus)
#print('index_to_word : ',index_to_word)
#print('corpus:',corpus)
# print( 'Words vector: ', words)
# print('Lenght words vector ', len(words))
nb_of_words_to_consider_context = 1
epochs = 100
learning_rate = 0.01
loss_epoch = {}
training_data,training_sample_words = generate_training_data(corpus,nb_of_words_to_consider_context, unique_words_count,put_index_to_word,length_of_corpus, 'yes')
print('%s', len(training_data))

for i in range(len(training_data)):
    print('*' * 50)
    print('Target word:%s '%(training_sample_words[i][0]))
    print('Context word:%s '%(training_sample_words[i][1]))

print("Wait... it's training...")
word_embedding_dimension=1
loss, weights_1, weights_2 = train(word_embedding_dimension,nb_of_words_to_consider_context,epochs,training_data,learning_rate)

# print(epoch_loss, weights_1, weights_2)
# print('\n')
loss_epoch.update( {word_embedding_dimension: loss} )
print(loss_epoch)

#similarity
list_A = words
print("Enter a list of words to find similarity")
list_B=[]
for i in range (0, 3):
    x=input()
    list_B.append(x)

print(list_B)



threshold = 0.70     # if needed
print("All words most similar to the list from the text disctionary :")
for key in list_A:
    for word in list_B:
        try:
                res = cosdis(word2vec(word), word2vec(key))
                if res > threshold:
                    print(" {} with original word: {}".format(word, key))
        except IndexError:
                pass


