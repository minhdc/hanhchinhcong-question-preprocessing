import fasttext
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
        topic = model.predict(s)        #du doan topic
        tokens = word_tokenize(s)       # tach tu
        print(topic[0][0])
        print(tokens)
        token_list = []
        for each in tokens:
            token_list.append(each)
        result = {"topic":topic[0][0],"tokens":dumps(token_list)}
        
        return result

api.add_resource(Questions,"/questions")

if __name__ == '__main__':
    app.run()
