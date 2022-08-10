class Transmissao:
    label: str
    url: str

    def __init__(self, transmissao: any) -> None:
        self.label = transmissao['label']
        self.url = transmissao['url']


class NextGame:
    partida_id: int
    clube_casa_id: int
    clube_casa_posicao: int
    clube_visitante_id: int
    aproveitamento_mandante: list[str]
    aproveitamento_visitante: list[str]
    clube_visitante_posicao: int
    partida_data: str
    timestamp: int
    local: str
    valida: bool
    placar_oficial_mandante: str
    placar_oficial_visitante: str
    status_transmissao_tr: str
    inicio_cronometro_tr: str
    periodo_tr: str
    transmissao: Transmissao

    def __init__(self, next_game: any) -> None:
        self.partida_id = next_game['partida_id']
        self.clube_casa_id = next_game['clube_casa_id']
        self.clube_casa_posicao = next_game['clube_casa_posicao']
        self.clube_visitante_id = next_game['clube_visitante_id']
        self.aproveitamento_mandante = next_game['aproveitamento_mandante']
        self.aproveitamento_visitante = next_game['aproveitamento_visitante']
        self.clube_visitante_posicao = next_game['clube_visitante_posicao']
        self.partida_data = next_game['partida_data']
        self.timestamp = next_game['timestamp']
        self.local = next_game['local']
        self.valida = next_game['valida']
        self.placar_oficial_mandante = next_game['placar_oficial_mandante']
        self.placar_oficial_visitante = next_game['placar_oficial_visitante']
        self.status_transmissao_tr = next_game['status_transmissao_tr']
        self.periodo_tr = next_game['periodo_tr']
        self.transmissao = Transmissao(next_game['transmissao'])
