"""Defines a question type and helper methods for it."""

_max_question_id = 0

class Question:
    """A question."""
    def __init__(self, question_text: str, answer_text: str = None, question_id: int = None):
        self.text = question_text
        self.answer = answer_text
        self._write_id(question_id)

    def is_answered(self):
        """True if the question has been provided an answer."""
        return self.answer is not None

    def to_dict(self) -> dict:
        """Creates a dictionary representation of this object."""
        return {
            "text": self.text,
            "id": self.id,
            "answer": self.answer
        }

    @staticmethod
    def from_dict(d: dict):
        """Builds a question from a dictionary."""
        return Question(
            question_text=d['text'],
            question_id=d['id'],
            answer_text=d['answer'] if 'answer' in d else None
        )

    def _write_id(self, question_id: int | None):
        """Assigns an ID to this question."""
        global _max_question_id

        # If no ID was provided, assign one in sequence.
        if question_id is None:
            self.id = _max_question_id + 1
            _max_question_id = self.id

        # If the id was provided, update _max_proposition_id if necessary.
        else:
            self.id = question_id
            if self.id > _max_question_id:
                _max_question_id = self.id


def from_questions_json_list(l: list) -> list:
    """Builds a list of questions from a list of JSON questions."""
    return [Question.from_dict(x) for x in l]