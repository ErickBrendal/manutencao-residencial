# Manutenção Residencial — Douglas Santana

Landing page para divulgação dos serviços de manutenção residencial do Douglas Santana
(eletricista, pintor, montador e instalações) em Guarulhos/SP.

Feita para ser **compartilhada no WhatsApp**: quando o cliente preenche o formulário de
orçamento, é gerada automaticamente uma mensagem organizada que abre direto na conversa
do WhatsApp do Douglas — assim ele responde mais rápido e com mais profissionalismo.

## Arquivos

- `index.html` — a página inteira (HTML + CSS + JavaScript em um único arquivo).
- `og-image.png` — imagem de preview que aparece ao compartilhar o link no WhatsApp.
- `make_og.py` — script opcional que gera a imagem de preview.
- `vercel.json` — configuração do deploy na Vercel.

## Como alterar o número de WhatsApp

Abra o `index.html` e procure por:

```js
var WHATS_NUMBER = "5511948970819";
```

Troque pelo número desejado no formato internacional: `55` + DDD + número, sem espaços
ou símbolos. Ex.: `(11) 94897-0819` → `5511948970819`.

## Como adicionar fotos reais na galeria

1. Coloque as fotos (ex.: `foto1.jpg`) na mesma pasta do `index.html`.
2. Na seção da galeria, troque o bloco `<div class="gal-ph">...</div>` por:
   ```html
   <img src="foto1.jpg" alt="Descrição do serviço">
   ```

## Deploy

Site estático. Pode ser publicado na Vercel, Netlify, GitHub Pages ou qualquer
hospedagem de arquivos estáticos. Na Vercel, basta importar o repositório — não precisa
de build.
