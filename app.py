from flask import Flask, render_template, request

app = Flask(__name__)

class Course:
    def __init__(self, name, start, end, lecturer):
        self.name = name
        self.start = start
        self.end = end
        self.lecturer = lecturer

class Classroom:
    def __init__(self, name):
        self.name = name
        self.schedule = []

class Lecturer:
    def __init__(self, name, available_hours):
        self.name = name
        self.available_hours = eval(available_hours)  # Convert string to list of tuples

def classroom_optimization(courses, classrooms, lecturers):
    optimized_classrooms = []

    for course in courses:
        assigned = False
        for lecturer in lecturers:
            if lecturer.name == course.lecturer:
                if any(course.start >= a[0] and course.end <= a[1] for a in lecturer.available_hours):
                    for classroom in classrooms:
                        if all(not (course.start < c.end and course.end > c.start) for c in classroom.schedule):
                            classroom.schedule.append(course)
                            assigned = True
                            break
                    if assigned:
                        break

    optimized_classrooms = [(classroom.name, classroom.schedule) for classroom in classrooms]
    return optimized_classrooms

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    try:
        courses = []
        classrooms = []
        lecturers = []

        course_names = request.form.getlist('course[]')
        start_times = request.form.getlist('start[]')
        end_times = request.form.getlist('end[]')
        lecturer_names = request.form.getlist('lecturer[]')
        
        for name, start, end, lecturer in zip(course_names, start_times, end_times, lecturer_names):
            courses.append(Course(name, int(start), int(end), lecturer))
        
        classroom_names = request.form.getlist('classroom[]')
        for name in classroom_names:
            classrooms.append(Classroom(name))
        
        lecturer_names = request.form.getlist('lecturer_name[]')
        lecturer_hours = request.form.getlist('lecturer_hours[]')
        for name, hours in zip(lecturer_names, lecturer_hours):
            lecturers.append(Lecturer(name, hours))

        optimized_classrooms = classroom_optimization(courses, classrooms, lecturers)
        return render_template('schedule.html', classrooms=optimized_classrooms)

    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
