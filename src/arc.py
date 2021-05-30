class Arc():

  def __init__(self, vertex_1: int, vertex_2: int):
    self._vertex_1 = vertex_1
    self._vertex_2 = vertex_2

  def __hash__(self) -> int:
    pass  