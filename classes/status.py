class Status:
    nome: str
    id: int

    def __init__(self, status: any) -> None:
        self.nome = status['nome']
        self.id = status['id']
