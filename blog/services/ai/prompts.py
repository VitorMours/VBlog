
class BlogPrompts:
  @staticmethod
  def summarize(content: str) -> str:
    return f"""
      Você é um editor profissional de jornal.

      Crie UM ÚNICO título para o post abaixo.

      Regras:
      - máximo 150 caracteres
      - deve refletir a ideia central do texto
      - retorne SOMENTE o título
      - não explique nada
      - não liste opções
      - não use aspas

      Texto:
      {content}
    """

  @staticmethod
  def improve(content: str) -> str:
    return f"""
    Reescreva esse blog da maneira menos robotica e mais humana possivel, de 
    forma que ainda assim, corrija os elementos de gramática impostos pela lingua
    portuguesa, e que mantenha as ideias, elesmentos, e conteúdos do texto. Produzindo 
    no final apenas uma revisao ortográfica praticamente
    {content}
    """