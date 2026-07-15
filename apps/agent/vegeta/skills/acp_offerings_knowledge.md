# ACP Offerings — Schema & Estrutura (VEGETA)

## Schema correto para importar offerings (web UI)

O dialog "Import Agent Offerings" em app.virtuals.io usa o formato **openclaw-acp**.
O campo de preço é `priceV2` como objeto aninhado.

```json
{
  "jobs": [
    {
      "name": "offeringNameCamelCase",
      "description": "Descrição do job — 10 a 500 chars.",
      "priceV2": {
        "type": "fixed",
        "value": 0.05
      },
      "slaMinutes": 30,
      "requiredFunds": false,
      "requirement": "O que o cliente deve fornecer para este job.",
      "deliverable": "O que o VEGETA entrega — formato e conteúdo."
    }
  ]
}
```

## NÃO usar (causa erro "Missing or invalid 'price' field")

```
❌ "price": 0.05
❌ "priceValue": 0.05
❌ "priceType": "fixed"
```

## Resources

```json
{
  "resources": [
    {
      "name": "get_resource_name",
      "description": "O que este endpoint retorna.",
      "url": "https://api.example.com/endpoint",
      "params": {"type": "object", "required": [], "properties": {}}
    }
  ]
}
```

## Configuração VEGETA

- Agent ID: `019ec5ec-4b48-750d-894a-7f1fedebb988`
- Wallet: `0xe09f40114af6c78788a8003da127c49c56158584`
- XDG config: `~/.config/acp-vegeta`
- Chain: Base mainnet (8453)
- Ficheiros: `ops/import_vegeta_jobs_40.json`, `ops/import_vegeta_resources_37.json`

## CLI

```bash
export XDG_CONFIG_HOME=~/.config/acp-vegeta
acp agent use --agent-id 019ec5ec-4b48-750d-894a-7f1fedebb988
acp offering create --name "jobName" --price-type fixed --price-value 0.05 --sla-minutes 30 ...
acp resource create --name "res_name" --url "https://..." --description "..."
```

## Fonte

`github.com/Virtual-Protocol/openclaw-acp` → `src/lib/api.ts` → `interface JobOfferingData`
Confirmado funcional — 40 offerings importadas com sucesso em Junho 2026.
