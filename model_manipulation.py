import fasttext
import heapq
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from underthesea import word_tokenize
from json import dumps
#cbow_model = fasttext.train_unsupervised('training_3.txt'.model='cbow')
#skipgram_model = fasttext.train_unsupervised('training_3.txt'.model='skipgram')

#model = fasttext.load_model("hanhchinhcong-model-200q.bin")
model = fasttext.load_model("model_5.bin")




# print(classification_model.predict(""))

# classification_model.save_model('saved_model_ptit.bin')


app = Flask(__name__)
api = Api(app)

class Questions(Resource):
    def post(self):
        s = request.form.getlist('question')[0] # nhan cau hoi 
        print(s)
        topic = model.predict(s,k=5)        #du doan topic
        tokens = word_tokenize(s)       # tach tu
        # print(topic)
        # print(tokens)
        # print(topic)
        token_list = []
        topics = [t for t in topic[0]]
        score = [t for t in topic[1]]
        largest_prob = heapq.nlargest(3,score)
        print("topics : ",topics)
        print("score:",score)
        print("largest prob:",largest_prob)
        largest_prob_index = []
        largest_prob_topics = []
        for each in score:
            if each in largest_prob[0:3] and score.index(each) not in largest_prob_index:
                largest_prob_index.append(score.index(each))
                # largest_prob_topics.append(topics[score.index(each)])
        # BAD CODE, refactor larter
        if(len(largest_prob_index) < 3):
            largest_prob_index.append(score.index(largest_prob[2],2))
        print("largest prob index",largest_prob_index)
        for each in largest_prob_index:
            largest_prob_topics.append(topics.pop(each))
        # if largest_prob[0] > largest_prob[1]:
        #     largest_prob_topics[1] = largest_prob_topics[0]
        # if largest_prob[1] > largest_prob[2]:
        #     largest_prob_topics[2] = largest_prob_topics[1]            
        for each in tokens:
            token_list.append(each)
        # print(largest_prob.astype(int))
        print("largest prob topics",largest_prob_topics)
        print("largest prob",largest_prob)
        r = {}
        for i in range(0,len(largest_prob_topics)):
            r['topic_'+str(i+1)] = dumps(largest_prob_topics[i]+":"+str(largest_prob[i]))
        r['tokens'] = dumps(token_list)
        print(r)
        result = r
        
        return result

api.add_resource(Questions,"/questions")

if __name__ == '__main__':
    app.run()
