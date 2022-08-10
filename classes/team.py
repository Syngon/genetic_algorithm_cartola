class Escudos:
    img60x40: str
    img45x45: str
    img30x30: str

    def __init__(self, escudos: any) -> None:
        self.img60x40 = escudos['60x40']
        self.img45x45 = escudos['45x45']
        self.img30x30 = escudos['30x30']


class Team:
    id: int
    nome: str
    abreviacao: str
    escudos: Escudos
    nome_fantasia: str

    def __init__(self, team: any) -> None:
        self.id = team['id']
        self.nome = team['nome']
        self.abreviacao = team['abreviacao']
        self.escudos = team['escudos']
        self.nome_fantasia = team['nome_fantasia']
