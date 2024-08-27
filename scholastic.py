"""Stores propositions, so that you can have a well-examined belief system."""
import proposition
import question
import json

DATA_FILE_NAME = 'user_data.json'

def do_startup():
    print('Scholastic. 2024.')
    print()


def load_json_userdata(filename: str) -> (list[proposition.Proposition], list[question.Question]):
    with open(filename, 'r') as f:
        user_data = json.load(f)

    propositions = proposition.from_propositions_json_list(user_data['propositions'])
    questions = question.from_questions_json_list(user_data['questions'])

    return propositions, questions


def write_json_userdata(filename: str, propositions: list[proposition.Proposition], questions: list[question.Question]):
    with open(filename, 'w') as f:
        json.dump(
            {
                "propositions": [x.to_dict() for x in propositions],
                "questions": [x.to_dict() for x in questions]
            },
            f
        )


def new_proposition(propositions: list[proposition.Proposition]):
    """Wizard to build a new proposition."""
    text = input('text >> ')
    propositions.append(proposition.Proposition(text))


def new_question(questions: list[question.Question]):
    """Wizard to build a new question."""
    text = input('text >> ')
    questions.append(question.Question(text))


def delete_question(idx: int, questions: list[question.Question]):
    """Deletes the given question from out of the list."""
    to_del = -1
    for i, q in enumerate(questions):
        if idx == q.id:
            to_del = i

    if to_del == -1:
        print(f'Invalid id: {to_del}')
    else:
        del questions[to_del]


def delete_proposition(idx: int, propositions: list[proposition.Proposition]):
    """Deletes the given proposition from out of the list."""
    to_del = -1
    for i, p in enumerate(propositions):
        if idx == p.id:
            to_del = i

    if to_del == -1:
        print(f'Invalid id: {to_del}')
    else:
        del propositions[to_del]


def parse_command(line: str, propositions: list[proposition.Proposition], questions: list[question.Question]):
    """Dispatches commands."""
    tokens = line.split()
    if len(tokens) == 0:
        return
    elif tokens[0] == 'new':
        if len(tokens) == 1:
            print('Must provide an argument to new: proposition or question')
        elif tokens[1] == 'proposition':
            new_proposition(propositions)
        elif tokens[1] == 'question':
            new_question(questions)
    elif tokens[0] == 'list':
        if len(tokens) == 1 or tokens[1] == 'propositions':
            for p in propositions:
                print(f'{p.id}: {p.text}')
        elif tokens[1] == 'questions':
            for q in questions:
                print(f'{q.id}: {q.text}')
    elif tokens[0] == 'delete':
        if len(tokens) == 1:
            print('Must provide argument: proposition or question')
        elif len(tokens) == 2:
            print('Which?')

        try:
            idx = int(tokens[2])
        except ValueError:
            print('Must specify an integer index.')
            return

        if tokens[1] == 'proposition':
            delete_proposition(idx, propositions)
        elif tokens[1] == 'question':
            delete_question(idx, questions)



def main():
    propositions, questions = load_json_userdata(DATA_FILE_NAME)
    do_startup()

    running = True
    while running:
        line = input('>> ').strip()

        if line.lower() == 'exit':
            running = False
        else:
            parse_command(line, propositions, questions)

    write_json_userdata(DATA_FILE_NAME, propositions, questions)

if __name__ == '__main__':
    main()
