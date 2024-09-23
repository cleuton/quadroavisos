import os, sys
# Caminho para o diretório raiz do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from typing import List
from database.db_quadro import obter_quadro
from database.db_mensagens import listar_mensagens_desc
from database.modelo import Usuario, Quadro, Mensagem
import logging

logger = logging.getLogger("backend")

def paginar_mensagens_quadro(idUsuarioLogado: int, idQuadroDesejado: int, pagina: int, mensagens_por_pagina: int) -> List[Mensagem]:
    flog = f"{__file__}::paginar_mensagens_quadro;"
    try:
        quadro = obter_quadro(idQuadroDesejado, idUsuarioLogado)
        qtde_mensagens = quadro.qtde_mensagens
        inicial = (pagina - 1) * mensagens_por_pagina
        final = inicial + mensagens_por_pagina
        if final > qtde_mensagens:
            return []
        return listar_mensagens_desc(idQuadroDesejado, inicial, mensagens_por_pagina, idUsuarioLogado)
    except ValueError as ve:
        mensagem = f"Erro ao obter quadro {idQuadroDesejado} pelo usuário {idUsuarioLogado}: {ve}"
        logger.error(f"{flog}{mensagem}")
        raise



