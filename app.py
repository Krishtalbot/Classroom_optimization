from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Class:
    def __init__(self, start, end):
        self.start = start
        self.end = end

def classroom_optimization(classes):
    sorted_classes = sorted(classes, key=lambda x: x.end)
    selected_classes = [sorted_classes[0]]
    for i in range(1, len(sorted_classes)):
        if sorted_classes[i].start >= selected_classes[-1].end:
            selected_classes.append(sorted_classes[i])
    return selected_classes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    start_times = request.form.getlist('start[]')
    end_times = request.form.getlist('end[]')
    classes = [Class(int(start), int(end)) for start, end in zip(start_times, end_times)]
    optimized_schedule = classroom_optimization(classes)
    return render_template('schedule.html', schedule=optimized_schedule)

if __name__ == '__main__':
    app.run(debug=True)
