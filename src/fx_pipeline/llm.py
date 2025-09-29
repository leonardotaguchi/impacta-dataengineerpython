import openai
import structlog
from .config import settings

log = structlog.get_logger()
openai.api_key = settings.OPENAI_API_KEY

PROMPT_TEMPLATE = '''
Você é um analista financeiro. Abaixo estão métricas agregadas das cotações do dia {date} para base {base}:
{summary}

Gere:
1) Um resumo executivo curto (2-3 frases).
2) Top 5 moedas com maior valorização frente a {base} no período.
3) Observações sobre volatilidade e riscos.
4) Sugestões para o time de negócios (linguagem simples).

Responda em português.
'''

def generate_insight(summary_text, date, base):
    prompt = PROMPT_TEMPLATE.format(date=date, base=base, summary=summary_text)
    log.info("llm.request", date=date)
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":"Você é um assistente analítico."},
                  {"role":"user","content":prompt}],
        max_tokens=500,
        temperature=0.3
    )
    text = resp["choices"][0]["message"]["content"]
    log.info("llm.response_len", length=len(text))
    return text
