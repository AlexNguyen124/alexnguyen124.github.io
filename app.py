from flask import Flask, render_template, request
import os
import ast
import jiggybase_utils as jbu

app = Flask(__name__)

# Get company names an id
companies = jbu.collection_doc_names_id()
# Get question list
with open('questions.txt') as file:
    questions = [line.rstrip() for line in file]
# Get template file
with open('template.txt', 'r') as file:
    template = file.read()

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_company = ''
    selected_question = ''
    company_name = ''
    prompt = ''
    response = ''

    if request.method == 'POST':
        selected_company = request.form.get('company')
        selected_question = request.form.get('question')
        qnumber = int(selected_question[:2])
        company_name = os.path.splitext(ast.literal_eval(selected_company)[0])[0]
        prompt_response = jbu.submit_prompt(template,company_name,qnumber)
        prompt = prompt_response[0]
        response = prompt_response[1]
    return render_template('index.html',
                           companies=companies,
                           questions=questions,
                           selected_company=selected_company,
                           selected_question=selected_question,
                           company_name=company_name,
                           prompt=prompt,
                           response=response)

if __name__ == '__main__':
    app.run(debug=True)