from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load association rules
rules = pd.read_hdf('rules.h5', key='df')
print('loaded')

all_groceries = set()
for itemset in rules['antecedents']:
    all_groceries.update(itemset)
groceries=list(all_groceries)
groceries.sort()

@app.route('/')
def index():
    return render_template('index.html', groceries=groceries)

# Recommendation function
def recommend_items(selected_items):
    recommended_items = set()
    for item in selected_items:

        print("Processing item:", item,type(rules['antecedents'] ),type(item),rules['antecedents'] == (item))
        # print(rules[rules['antecedents'] == set(item)]['consequents'])
        recommendations = rules[rules['antecedents'] == {item}]['consequents']
        recommended_items.update(recommendations)
    return recommended_items

@app.route('/home')
def index1():
    return render_template('index.html',groceries=groceries)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    selected_items = request.form.getlist('grocery')
    print(selected_items)
    recommendations = recommend_items(selected_items)
    print(recommendations)
    if len(recommendations)>0:
        return render_template('result.html', recommendations=recommendations)
    else:
        return render_template('error.html')
if __name__ == '__main__':
    app.run(debug=True)
