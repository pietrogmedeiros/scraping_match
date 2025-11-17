# 🚀 DEPLOY VERCEL - INSTRUÇÕES FINAIS

## Status Atual
- ✅ Código pronto no GitHub: https://github.com/pietrogmedeiros/scraping_match
- ✅ Arquivo `vercel.json` configurado
- ✅ Arquivo `.env` com variáveis
- ✅ API testada localmente (5/6 testes)
- ✅ Todos os arquivos committed

## Próximos Passos para Deploy

### Option 1: Via Dashboard Vercel (Recomendado)

1. Acesse: https://vercel.com/dashboard
2. Clique em "Add New" → "Project"
3. Selecione "Import Git Repository"
4. Escolha: `pietrogmedeiros/scraping_match`
5. Clique "Import"
6. Em "Environment Variables", adicione:
   - `API_TOKEN` = `seu_token_secreto_super_seguro_aqui`
   - `PORT` = `8000`
7. Clique "Deploy"

**Resultado:** Projeto deployado em ~2-3 minutos

### Option 2: Via CLI (Vercel CLI)

```bash
cd /Users/pietro_medeiros/Downloads/scrapping-match-1P
vercel --prod
```

Será solicitado:
- Nome do projeto: `scraping-match`
- Selecionar team (padrão)
- Depois responder "yes" para usar `vercel.json`

## Depois do Deploy

1. Aguarde conclusão (builds podem levar 5-10 min)
2. Você receberá uma URL como: `https://scraping-match.vercel.app`
3. Teste a API:
   ```bash
   curl https://scraping-match.vercel.app/status
   ```

4. Para testar scraping com token:
   ```bash
   curl -X POST https://scraping-match.vercel.app/scrape \
     -H "Authorization: Bearer seu_token_secreto_super_seguro_aqui" \
     -H "Content-Type: application/json" \
     -d '{"url":"https://www.mercadolivre.com.br/...", "capturar_screenshots": false}'
   ```

## URLs Importantes

- 📊 Dashboard: https://vercel.com/dashboard
- 🔗 Repositório: https://github.com/pietrogmedeiros/scraping_match
- 📖 Docs API: http://localhost:8000/docs (local)
- 🧪 Testes: `python test_api.py`

## Troubleshooting

Se o deploy falhar:

1. Verifique logs no Vercel Dashboard
2. Certifique-se que API_TOKEN está configurada
3. Verifique se Python 3.11 é suportado
4. Consulte: https://vercel.com/docs/build-output-api/v3

---

**Última atualização:** 17 de novembro de 2025
**Status:** 🟢 Pronto para deploy
