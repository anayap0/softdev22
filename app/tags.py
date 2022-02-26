from app.models import User, Post, School, \
    CourseGroup, Course, Unit, SubUnit, Subject, Topic, \
        SchoolTag, CourseGroupTag, CourseTag, UnitTag, SubUnitTag, SubjectTag, TopicTag
from app import db

group_classes = {
    'school': School,
    'course_group': CourseGroup,
    'course': Course,
    'unit': Unit,
    'subunit': SubUnit,
    'subject': Subject,
    'topic': Topic
}

group_colors = {
    'school': '#FFC09F',
    'course_group': '#FFEE93',
    'course': '#E8DFF5',
    'unit': '#ADF7B6',
    'subunit': '#C1D3FE',
    'subject': 'D1D1D1',
    'topic': '#FCF5C7'
}

def get_tag_choices(group_classes):
    tags = []
    for group_name, model in group_classes.items():
        rows = model.query.all()
        for row in rows:
            tags.append(('{}:{}'.format(group_name, row.id), row.name))
    return tags

def write_tag_choice(tag_value, post_id, commit=True):
    table, row_id = tag_value.split(":")
    row_id = int(row_id)
    new_item = None
    match table:
        case 'school':
            new_item = SchoolTag(post_id=post_id, school_id=row_id)
        case 'course_group': 
            new_item = CourseGroupTag(post_id=post_id, course_group_id=row_id)
        case 'course': 
            new_item = CourseTag(post_id=post_id, course_id=row_id)
        case 'unit':
            new_item = UnitTag(post_id=post_id, unit_id=row_id)
        case 'subunit':
            new_item = SubUnitTag(post_id=post_id, subunit_id=row_id)
        case 'subject':
            new_item = SubjectTag(post_id=post_id, subject_id=row_id)
        case 'topic':
            new_item = TopicTag(post_id=post_id, topic_id=row_id)
    if new_item is not None:
        db.session.add(new_item)
        if commit:
            db.session.commit()

def write_tag_choices(post_id, tag_values, commit=True):
    for tv in tag_values:
        write_tag_choice(tv, post_id, commit)
    if commit:
        db.session.commit()
        
def get_all_tags_as_map(group_classes):
    tags = {} # format: 'group': [(item_id, name)]
    for group_name, model in group_classes.items():
        rows = model.query.all()
        tags[group_name] = [(row.id, row.name) for row in rows]
    

def get_all_tags_as_list():
    tags = []
    for group_name, model in group_classes.items():
        rows = model.query.all()
        for row in rows:
            tags.append({
                'table': group_name,
                'id': row.id,
                'name': row.name
            })
    return tags