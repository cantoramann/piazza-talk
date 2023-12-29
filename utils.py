
# question, note, poll etc
def parse_post_type(post):
    if post['type'] == 'question' or post['type'] == 'note':
        return post['type']
    return None

def parse_post_main_content(post):
    return post['history'][0]['content']

def parse_post_title(post):
    return post['history'][0]['subject']

def parse_post_tags(post):
    return post['tags']

# instructor answer
def parse_answer(post):
    if post['type'] != 'question':
        return None
    
    for child in post['children']:
        if child['type'] == 'i_answer':
            return ('instructor_answer', child['history'][0]['content'])
        elif child['type'] == 's_answer':
            return ('student_answer', child['history'][0]['content'])

def parse_followups(post):
    if post['type'] != 'question':
        return None
    
    followups = []
    for child in post['children']:
        if child['type'] == 'followup':
            followups.append(child['subject'])

            for child_feedback in child['children']:
                followups.append(child_feedback['subject'])
    
    return followups

def parse_post_privacy(post):
    return post['status']