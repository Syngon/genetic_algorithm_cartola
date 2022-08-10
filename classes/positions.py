class Position:
    id: int
    nome: str
    abreviacao: str

    def __init__(self, position: any) -> None:
        self.id = position['id']
        self.nome = position['nome']
        self.abreviacao = position['abreviacao']
