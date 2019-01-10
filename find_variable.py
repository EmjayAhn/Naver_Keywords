from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import pandas as pd
import pickle
import requests, json
# system module 추가
# arguement 를 받을 수 있음
import sys

# file 경로
import os


def fine_accuracy(alpha):

    # 기사 데이터 프레임 로드
    
    # path 설정
    path = os.path.dirname(os.path.realpath(__file__))
    print(path)
    article_df = pd.read_pickle("{}/article_2016-06-01.plk".format(path))

    # 테스트 데이터와 트레인 데이터 분리
    X_train, X_test, y_train, y_test = train_test_split(article_df.content, article_df.category, test_size=0.1, random_state=1)

    # vectorizer와 classification algorithm 설정
    clf = Pipeline([
        ('vect', TfidfVectorizer()), 
        ('clf', MultinomialNB(alpha=alpha)) 
    ])

    # 모델 생성
    model = clf.fit(X_train, y_train) 

    # 테스트 데이터 예측 결과 출력
    y_pred = model.predict(X_test)

    # 정확도 확인
    result = accuracy_score(y_test, y_pred)
    send_slack("alpha:{}, accuracy:{}".format(alpha, result))
    return result

def send_slack(msg, channel="#chatbot_tutorial", username="model_bot" ):
    webhook_URL = "https://hooks.slack.com/services/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"
    payload = {
        "channel": channel,
        "username": username,
        "icon_emoji": ":provision:",
        "text": msg,
    }
    response = requests.post(
        webhook_URL,
        data = json.dumps(payload),
    )

# 변수값 설정
# alphas = [0.1, 0.01, 0.001]
# for alpha in alphas:
#    print(alpha, fine_accuracy(alpha))

#변수값 설정
alpha = float(sys.argv[1])
accuracy = fine_accuracy(alpha)
print(alpha, accuracy)


