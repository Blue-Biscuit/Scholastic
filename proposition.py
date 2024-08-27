"""Defines data structures used for the Scholastic project."""

_max_proposition_id = 0
"""The largest proposition ID assigned by the program, used to assign new IDs."""

class Proposition:
    """A proposition."""
    def __init__(self, proposition_text: str, proposition_id: int = None):
        self.text = proposition_text

        self._write_id(proposition_id)

    def to_dict(self) -> dict:
        """Creates a dictionary representation of this object."""
        return {
            "text": self.text,
            "id": self.id
        }

    @staticmethod
    def from_dict(d: dict):
        """Builds a proposition from a dictionary."""
        return Proposition(d['text'], d['id'])

    def _write_id(self, proposition_id: int | None):
        """Assigns an ID to this proposition."""
        global _max_proposition_id

        # If no ID was provided, assign one in sequence.
        if proposition_id is None:
            self.id = _max_proposition_id + 1
            _max_proposition_id = self.id

        # If the id was provided, update _max_proposition_id if necessary.
        else:
            self.id = proposition_id
            if self.id > _max_proposition_id:
                _max_proposition_id = self.id


def from_propositions_json_list(l: list) -> list:
    """Builds a list of propositions from a list of JSON propositions."""
    return [Proposition.from_dict(x) for x in l]