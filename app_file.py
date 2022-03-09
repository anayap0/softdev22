from app import app, db
from app.models import User, Post, School, Comment
from app.models import User, Post, PostVote, School, \
    CourseGroup, Course, Unit, SubUnit, Subject, Topic, \
        CourseGroupTag, CourseTag, UnitTag, SubUnitTag, SubjectTag


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'PostVote': PostVote,
        'School': School,
        'CourseGroup': CourseGroup,
        'Course': Course,
        'Unit': Unit,
        'SubUnit': SubUnit,
        'Subject': Subject,
        'Topic': Topic,
        'CourseGroupTag': CourseGroupTag,
        'CourseTag': CourseTag,
        'UnitTag': UnitTag,
        'SubUnitTag': SubUnitTag,
        'SubjectTag': SubjectTag,
    }