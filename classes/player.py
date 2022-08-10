class Scout:
    __scout: any

    a: int
    ca: int
    ds: int
    fc: int
    fd: int
    ff: int
    fs: int
    ft: int
    g: int
    i: int
    pi: int

    def __init__(self, scout: any) -> None:
        self.__scout = scout
        self.put_scout_data_in_attributes()

    def put_scout_data_in_attributes(self) -> None:
        for item in self.__scout:
            setattr(self, item, self.__scout[item] or None)


class Player:
    scout: Scout
    atleta_id: int
    rodada_id: int
    clube_id: int
    posicao_id: int
    pontus_num: float
    preco_num: float
    variacao_num: float
    media_num: float
    jogos_num: int
    minimo_para_valorizar: float
    slug: str
    apelido: str
    nome: str
    foto: str

    def __init__(self, player: any):
        self.atleta_id = player['atleta_id']
        self.rodada_id = player['rodada_id']
        self.clube_id = player['clube_id']
        self.posicao_id = player['posicao_id']
        self.pontus_num = player['pontos_num']
        self.preco_num = player['preco_num']
        self.variacao_num = player['variacao_num']
        self.media_num = player['media_num']
        self.jogos_num = player['jogos_num']
        self.minimo_para_valorizar = player['minimo_para_valorizar']
        self.slug = player['slug']
        self.apelido = player['apelido']
        self.nome = player['nome']
        self.foto = player['foto']
        self.scout = Scout(player['scout'])
