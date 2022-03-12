from numpy import number
from app.models import CourseGroup, Course, Unit, SubUnit, School, Subject, Topic
from app import db

course_groups = {
    (1, "Advanced Placement (AP)"),
    (2, "International Baccalaureate (IB)"),
    (3, "Cambridge AS & A Level"),
}

subjects_and_courses= {
    "English (Language Arts)" : {
        1 : [
            'AP English Language and Composition',
            'AP English Literature and Composition'
        ],
        2 : [
            'Language A: Literature',
            'Language A: Language and Literature',
            'Literature and Performance'
        ],
        3 : [
            'English - Language - 9093',
            'English - Language and Literature (AS Level only) - 8695',
            'English - Literature - 9695',
            'English General Paper (AS Level only) - 8021'
        ]
    },
    "Math" : {
        1 : [
            'AP Calculus AB',
            'AP Calculus BC',
            'AP Statistics'
        ],
        2 : [
            'Mathematics: Applications and interpretation',
            'Mathematics: Analysis and approaches',
        ],
        3 : [
            'Mathematics - 9709',
            'Mathematics - Further - 9231',
        ]
    },
    # "Social Studies" : {
    #     1 : [

    #     ],
    #     2 : [

    #     ],
    #     3 : [
            
    #     ]
    # },
    "Sciences" : {
        1 : [
            'AP Biology',
            'AP Chemistry',
            'AP Computer Science A',
            'AP Computer Science Principles',
            'AP Environmental Science',
            'AP Physics 1: Algebra-Based',
            'AP Physics 2: Algebra-Based',
            'AP Physics C: Electricity and Magnetism',
            'AP Physics C: Mechanics'
        ],
        2 : [
            'Biology',
            'Chemistry',
            'Computer Science',
            'Design Technology',
            'Environmental Systems and Societies',
            'Physics',
            'Sports, Exercise, and Health Science'
        ],
        3 : [
            'Biology - 9700',
            'Chemistry - 9701',
            'Environmental Management (AS only) - 8291',
            'Marine Science - 9693',
            'Physics - 9702',
            'Computer Science - 9608',
            'Computer Science - 9618 (from 2021)',
            'Design & Technology - 9705'
        ]
    },
    # "Computer Science and Information Technology" : {
    #     1 : [

    #     ],
    #     2 : [

    #     ],
    #     3 : [
            
    #     ]
    # },
    # "Foreign Language" : {
    #     1 : [

    #     ],
    #     2 : [

    #     ],
    #     3 : [
            
    #     ]
    # },
    # "Performing Arts" : {
    #     1 : [

    #     ],
    #     2 : [

    #     ],
    #     3 : [
            
    #     ]
    # },
    # "Visual Arts" : {
    #     1 : [

    #     ],
    #     2 : [

    #     ],
    #     3 : [
            
    #     ]
    # },
    # "Physical Education" : {
    #     1 : [

    #     ],
    #     2 : [

    #     ],
    #     3 : [
            
    #     ]
    # },
    # "Business" : {
    #     1 : [

    #     ],
    #     2 : [

    #     ],
    #     3 : [
            
    #     ]
    # },
}

courses_and_units = {
    'AP Calculus AB' : {
        1: "Limits and Continuity",
        2: "Differentiation: Definition and Fundamental Properties",
        3: "Differentiation: Composite, Implicit, and Inverse Functions",
        4: "Contextual Applications of Differentiation",
        5: "Analytical Applications of Differentiation",
        6: "Integration and Accumulation of Change",
        7: "Differential Equations",
        8: "Applications of Integration"
    },
    'AP Calculus BC': {
        1: "Limits and Continuity",
        2: "Differentiation: Definition and Fundamental Properties",
        3: "Differentiation: Composite, Implicit, and Inverse Functions",
        4: "Contextual Applications of Differentiation",
        5: "Analytical Applications of Differentiation",
        6: "Integration and Accumulation of Change",
        7: "Differential Equations",
        8: "Applications of Integration",
        9: "Parametric Equations, Polar Coordinates, and Vector-Valued Functions",
        10: "Infinite Sequences and Series"
    },
    'AP Statistics': {
        1: "Exploring One-Variable Data",
        2: "Exploring Two-Variable Data",
        3: "Collecting Data",
        4: "Probability, Random Variables, and Probability Distributions",
        5: "Sampling Distributions",
        6: "Inference for Categorical Data: Proportions",
        7: "Inference for Quantitative Data: Means",
        8: "Inference for Categorical Data: Chi-Square",
        9: "Inference for Quantitative Data: Slopes"
    },
}

def add_course_groups(id_group_list):
    for id, course_group in id_group_list:
        existing_course = CourseGroup.query.filter_by(name=course_group).first()
        if existing_course is None:
            new_group = CourseGroup(id=id, name=course_group)
            db.session.add(new_group)
            db.session.commit()

def add_courses_by_subject(subjects_and_courses):
    for subject_name, id_courses in subjects_and_courses.items():
        existing_subject = Subject.query.filter_by(name=subject_name).first()
        if existing_subject is None:
            new_subject = Subject(name=subject_name)
            db.session.add(new_subject)
            db.session.commit()
            subject_id = new_subject.id
        else:
            subject_id = existing_subject.id
        for group_id, courses in id_courses.items():
            for course_name in courses:
                existing_course = Course.query.filter_by(name=course_name).first()
                if existing_course is None:
                    new_course = Course(
                        name=course_name,
                        course_group_id=group_id,
                        subject_id=subject_id
                    )
                    db.session.add(new_course)
                    db.session.commit()

def add_units_by_course(courses_and_units):
    for course_name, units_info in courses_and_units.items():
        course = Course.query.filter_by(name=course_name).first()
        course_id = course.id
        for unit_num, unit_name in units_info.items():
            existing_unit = Unit.query.filter_by(number=unit_num, course_id=course_id).first()
            if existing_unit is None:
                new_unit = Unit(
                    number=unit_num,
                    name=unit_name,
                    course_id=course_id
                )
                db.session.add(new_unit)
            else:
                existing_unit.name = unit_name
    db.session.commit()


add_course_groups(course_groups)
add_courses_by_subject(subjects_and_courses)
add_units_by_course(courses_and_units)