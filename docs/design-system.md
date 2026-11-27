# Sistema de design (proposta inicial)

Estado: proposta, a validar antes da Fase 3. O que está marcado como "decisão em aberto" fica por fechar.

## Direção

Editorial, educativa, contemporânea e sofisticada. A interface deve transmitir inteligência, confiança, clareza, rigor académico, acessibilidade, concentração e credibilidade. A clareza pedagógica vem sempre antes da aparência.

## O que evitamos

Gradientes azuis e roxos, fundos escuros com brilho neon, glassmorphism usado em todo o lado, botões excessivamente brilhantes, cartões repetidos em todas as secções (e três colunas de cartões por defeito), ícones decorativos em círculos coloridos, ilustrações 3D genéricas, emojis no lugar de ícones funcionais, animações exageradas, texto comercial vazio e dashboards que parecem templates de SaaS. Inter e Roboto não são usados por defeito.

## Cores

O verde é a única cor de destaque principal. Os contrastes foram calculados com a fórmula da WCAG 2.x (mínimo AA: 4,5:1 para texto normal e 3:1 para texto grande e elementos de interface).

| Papel | Valor | Contraste e uso |
|---|---|---|
| Fundo | `#F7F6F2` | fundo das páginas |
| Superfície | `#FFFFFF` | zonas elevadas: formulários e painéis |
| Texto principal | `#202824` | 13,97:1 no fundo e 15,10:1 na superfície |
| Texto secundário | `#66716B` | 4,69:1 no fundo e 5,07:1 na superfície (não usar mais claro) |
| Destaque | `#176B55` | links e botões: 5,94:1 no fundo; texto branco sobre ele 6,42:1 |
| Destaque suave | `#E8F1EC` | fundos de realce; o texto principal sobre ele tem 13,11:1 |
| Borda | `#DFE4DF` | divisórias discretas (1,19:1 no fundo) |
| Aviso | `#B7791F` | ver regra abaixo |
| Erro | `#B54747` | 5,31:1 na superfície e 4,91:1 no fundo |

Regras que decorrem da verificação:

- O aviso tem 3,64:1 na superfície e 3,37:1 no fundo. Passa para ícones e texto grande, mas falha para texto pequeno. As mensagens de aviso usam o texto principal, com o amarelo só no ícone ou numa barra lateral.
- A borda é clara de mais para delimitar campos de formulário, porque a WCAG pede 3:1 para componentes de interface. Os campos usam o texto secundário como contorno.
- A cor nunca é a única forma de transmitir informação: erro e sucesso levam também texto ou ícone.
- O sucesso reutiliza o verde de destaque, porque a paleta não tem uma cor própria para isso.

## Tipografia

- Interface e texto corrido: Plus Jakarta Sans. Títulos editoriais selecionados: Instrument Serif.
- Fallbacks locais: fontes do sistema (sem serifa e com serifa), para o site funcionar sem as fontes externas.
- Alojadas no próprio servidor, em ficheiros woff2 do subconjunto latino e com a licença ao lado (ver [ADR 0010](adr/0010-fontes-alojadas-no-servidor.md)).
- Corpo de texto com 16px no mínimo, altura de linha 1,5 e linhas de leitura até cerca de 70 caracteres.
- Fórmulas matemáticas: KaTeX, com apresentação própria e legível (decisão final na Fase 5).

## Espaçamento, forma e movimento

- Espaçamento em múltiplos de 4px: 4, 8, 12, 16, 24, 32, 48, 64 e 96.
- Raios de borda: 4px (pequeno), 8px (médio) e 12px (grande), e nenhum outro.
- Bordas finas de 1px e sombras muito subtis.
- Interações discretas de 150 a 200 ms, a respeitar `prefers-reduced-motion`.

## Layout

Alternar listas, divisórias, colunas e layouts assimétricos: nem tudo é cartão. Espaço em branco generoso. Primeiro o telemóvel, com páginas leves para equipamentos modestos e ligações lentas.

## Estados e acessibilidade

- Todos os elementos interativos têm estados de hover, foco visível, ativo, desativado, a carregar, sucesso e erro.
- Foco: contorno de 2px na cor de destaque, com 2px de afastamento.
- Alvos de toque com 44x44px no mínimo.
- Navegação completa por teclado e HTML semântico.

## Tokens (proposta)

```css
:root {
  --cor-fundo: #f7f6f2;
  --cor-superficie: #ffffff;
  --cor-texto: #202824;
  --cor-texto-suave: #66716b;
  --cor-destaque: #176b55;
  --cor-destaque-suave: #e8f1ec;
  --cor-borda: #dfe4df;
  --cor-aviso: #b7791f;
  --cor-erro: #b54747;

  --espaco-1: 4px;
  --espaco-2: 8px;
  --espaco-3: 12px;
  --espaco-4: 16px;
  --espaco-6: 24px;
  --espaco-8: 32px;
  --espaco-12: 48px;
  --espaco-16: 64px;
  --espaco-24: 96px;

  --raio-pequeno: 4px;
  --raio-medio: 8px;
  --raio-grande: 12px;
  --sombra-suave: 0 1px 2px rgba(32, 40, 36, 0.06);
  --duracao-curta: 150ms;
  --duracao-media: 200ms;

  --fonte-interface: "Plus Jakarta Sans", system-ui, sans-serif;
  --fonte-editorial: "Instrument Serif", Georgia, serif;
}
```

## Por fazer antes da Fase 3

- Referências visuais escolhidas pelo dono do projeto: extrair princípios de hierarquia, densidade e espaçamento, sem copiar interfaces.
- Validar os [fluxos e wireframes](fluxos-e-wireframes.md) das páginas principais.
