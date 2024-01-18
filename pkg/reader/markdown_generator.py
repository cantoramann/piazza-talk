import os

class MarkdownGenerator():
    def __init__(self):
        print('MarkdownGenerator initialized')

    def generate_markdown(self, raw_dir, post_data):
        with open(os.path.join(raw_dir, f"post_{post_data.post_id}.txt"), 'w') as file:
            file.write('# Title:' + post_data.post_title + '\n')
            file.write('## Post type: ' + post_data.post_type + '\n')
            
            if post_data.post_type == 'question':
                file.write('\n## Question:\n```' + post_data.post_main_thread + '```\n')
            else:
                file.write('\n## Note:\n```' + post_data.post_main_thread + '```\n')
                
            if post_data.post_answer != None:    
                file.write('\n## Answer:\n')            
                if post_data.post_answer[0] == 'instructor_answer':
                    file.write('### Answerer: instructor\n')
                elif post_data.post_answer[0] == 'student_answer':
                    file.write('### Answerer: student\n')
                file.write('\n### Answer Data:\n```' + post_data.post_answer[1] + '```\n')

            if post_data.post_followups != None:
                file.write('\n## Followups:\n')
                for followup in post_data.post_followups:
                    if followup == None:
                        continue
                    file.write(followup + '\n')