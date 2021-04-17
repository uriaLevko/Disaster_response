import sys
import nltk
import pandas as pd
from sqlalchemy import create_engine
import re
from sklearn.metrics import classification_report
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np
from sklearn.datasets import make_multilabel_classification
from sklearn.multioutput import MultiOutputClassifier
from sklearn.neighbors import KNeighborsClassifier
nltk.download(['punkt', 'wordnet','stopwords', 'averaged_perceptron_tagger'])
    

def load_data(database_filepath):
    # load data from database
    engine = create_engine(f'sqlite:///{database_filepath}')
    df = pd.read_sql_table(database_filepath,engine)
    X = df['message']
    Y = df.iloc[:,4:]
    category_names = Y.columns
    for col in category_names:
        Y[col] = Y[col].apply(lambda x:1 if x>1 else x)
    return X,Y,category_names

def tokenize(text):
    text = re.sub(r'[^a-zA-Z0-9]',' ',text.lower().strip())
    tokens = word_tokenize(text)
    
    stop_words = stopwords.words("english")
    lemmatizer = WordNetLemmatizer()
    
     # lemmatize andremove stop words
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w not in stop_words]
#     tokens = [lemmatizer.lemmatize(w) for w in tokens]
    return tokens


def build_model():
    
    pipeline = Pipeline([
                    ('vect', CountVectorizer(tokenizer=tokenize)),
                    ('tfidf', TfidfTransformer()),
                ('clf', MultiOutputClassifier(RandomForestClassifier()))
        ])

    parameters = {
        'vect__max_df': (0.5, 1.0),
#         'vect__max_features': (None, 5000),
        'tfidf__use_idf': (True, False),
        'clf__estimator__n_estimators': [120],
        'clf__estimator__max_features': [6]
    }

    cv = GridSearchCV(pipeline, param_grid=parameters,cv=3)
    model = pipeline
    return cv


def evaluate_model(model, X_test, Y_test, category_names):
#     model = build_model()
#     model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = (y_pred == Y_test).mean()
    print(f'over all accuracy: {accuracy.mean()}\n')
#     print(f'Table of column accuracy:\n{accuracy}\n')
    print(classification_report(np.array(Y_test),y_pred))
#     for i,x in enumerate(category_names):
#         print(f'classification_report for "{x}" column\n')
#         print(classification_report(np.array(Y_test[x]),y_pred[:,i]))
#         print('----------------------------------------------------')
#     cols = list(accuracy[accuracy<0.85].index)
#     seri = accuracy[accuracy<0.85]
#     for col in cols:
#         acc = np.round(seri[col],decimals=2)
#         print(f'confusion_matrix - {col}({acc})\n{confusion_matrix(np.array(y_test.loc[:,col]),y_pred[:,int(y_test.columns.get_loc(col))])}\n')

def save_model(model, model_filepath):
    pd.to_pickle(model,model_filepath)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()