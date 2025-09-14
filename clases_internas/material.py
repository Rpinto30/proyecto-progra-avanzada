class DidacticMaterial:
    def __init__(self, description, max_points):
        self._max_points = max_points
        self._obteined_points = 0
        self._description = description
