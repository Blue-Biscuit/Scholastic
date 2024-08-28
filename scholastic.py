"""Stores propositions, so that you can have a well-examined belief system."""
import proposition
import question
import json
import random

DATA_FILE_NAME = 'user_data.json'



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


def random_question(tokens: list[str], questions: list[question.Question]):
    """Prints a random question."""
    to_select = questions
    unanswered = 'unanswered' in tokens

    if unanswered:
        to_select = [x for x in to_select if not x.is_answered()]

    if len(to_select) == 0:
        print('No questions to select.')
    else:
        random_choice = random.choice(to_select)
        print(f'{random_choice.id} {random_choice.text}')


def parse_command(line: str, propositions: list[proposition.Proposition], questions: list[question.Question]):
    """Dispatches commands."""
    tokens = line.split()
    if len(tokens) == 0:
        return
    elif tokens[0] == 'new':
        if len(tokens) == 1:
            print('Must provide an argument to new: proposition or question')
            return
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
            return
        elif len(tokens) == 2:
            print('Which?')
            return

        try:
            idx = int(tokens[2])
        except ValueError:
            print('Must specify an integer index.')
            return

        if tokens[1] == 'proposition':
            delete_proposition(idx, propositions)
        elif tokens[1] == 'question':
            delete_question(idx, questions)
    elif tokens[0] == 'random':
        if len(tokens) == 1:
            print('Random what? (proposition or question)')
            return
        random_type = tokens[1]
        if random_type == 'proposition':
            if len(propositions) == 0:
                print('No propositions from which to select.')
            else:
                random_proposition = random.choice(propositions)
                print(f'{random_proposition.id}: {random_proposition.text}')
        elif random_type == 'question':
            random_question(tokens[2:], questions)
    elif tokens[0] == 'print':
        print(' '.join(tokens[1:]))


def run_startup_code(config: dict, propositions: list[proposition.Proposition], questions: list[question.Question]):
    startup = config['startup_code']
    for line in startup:
        parse_command(line, propositions, questions)


def do_startup(config: dict, propositions: list, questions: list):
    print('Scholastic. 2024.')
    print()
    run_startup_code(config, propositions, questions)


def main():
    propositions, questions = load_json_userdata(DATA_FILE_NAME)
    with open('config.json', 'r') as c_f:
        config = json.load(c_f)

    do_startup(config, propositions, questions)

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
