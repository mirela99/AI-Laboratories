import nltk
import re
# nltk.download('punkt')
# nltk.download('stopwords')

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
        print(words)


get_data_from_file()



#----------------------------------------------------------------------------------------------------
# Input vector, returns nearest word(s)
# def cosine_similarity(word,weight,put_index_to_word,unique_words_count,index_to_word):
#     #Get the index of the word from the dictionary
#     index = put_index_to_word[word]
    
#     # #Get the correspondin weights for the word
#     # word_vector_1 = weight[index]

#     word_similarity = {}

#     for i in range(unique_words_count):
        
#         word_vector_2 = weight[i]
        
#         theta_sum = np.dot(word_vector_1, word_vector_2)
#         theta_den = np.linalg.norm(word_vector_1) * np.linalg.norm(word_vector_2)
#         theta = theta_sum / theta_den
        
#         word = index_to_word[i]
#         word_similarity[word] = theta
    
#     return word_similarity #words_sorted

# def print_similar_words(top_n_words,weight,msg,words_subset):
    
#     columns=[]
    
#     for i in range(0,len(words_subset)):
#         columns.append('similar:' +str(i+1) )
        
#     df = pd.DataFrame(columns=columns,index=words_subset)
#     df.head()
    
#     row = 0
#     for word in words_subset:
        
#         #Get the similarity matrix for the word: word
#         similarity_matrix = cosine_similarity(word,weight,put_index_to_word,unique_words_count,index_to_word)
#         col = 0
        
#         #Sort the top_n_words
#         words_sorted = dict(sorted(similarity_matrix.items(), key=lambda x: x[1], reverse=True)[1:top_n_words+1])
        
#         #Create a dataframe to display the similarity matrix
#         for similar_word,similarity_value in words_sorted.items():
#             df.iloc[row][col] = (similar_word,round(similarity_value,2))
#             col += 1
#         row += 1
#     styles = [dict(selector='caption', 
#     props=[('text-align', 'center'),('font-size', '20px'),('color', 'red')])] 
#     df = df.style.set_properties(**
#                        {'color': 'green','border-color': 'blue','font-size':'14px'}
#                       ).set_table_styles(styles).set_caption(msg)
#     return df

#--------------------------------------------------------------
