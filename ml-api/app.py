from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index() -> str:
    match request.method:
        case 'GET':
            # Display the form
            return render_template('test_models.html')
        case 'POST':
            # Get form details
            question = request.form.get("question")
            answer = request.form.get("answer")
            candidate_answer = request.form.get("candidate_answer")

            return render_template('test/test_models.html')
        

if __name__ == "__main__":
    app.run()

