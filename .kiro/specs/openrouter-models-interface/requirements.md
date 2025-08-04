# Requirements Document

## Introduction

Esta funcionalidade permitirá aos usuários visualizar e filtrar todos os modelos disponíveis do OpenRouter na interface do Agno Builder. Os usuários poderão filtrar modelos por empresa (OpenAI, Google, Anthropic, etc.), separar modelos gratuitos dos pagos, e selecionar facilmente o modelo desejado para seus agentes.

## Requirements

### Requirement 1

**User Story:** Como um usuário do Agno Builder, eu quero visualizar todos os modelos disponíveis do OpenRouter, para que eu possa escolher o modelo mais adequado para minha aplicação.

#### Acceptance Criteria

1. WHEN o usuário seleciona "OpenRouter" como provedor THEN o sistema SHALL exibir uma lista completa de modelos disponíveis
2. WHEN a lista de modelos é carregada THEN o sistema SHALL mostrar informações básicas de cada modelo (nome, empresa, se é gratuito/pago)
3. IF a API do OpenRouter não estiver disponível THEN o sistema SHALL exibir uma lista de modelos em cache/fallback

### Requirement 2

**User Story:** Como um usuário do Agno Builder, eu quero filtrar modelos por empresa (OpenAI, Google, Anthropic, etc.), para que eu possa encontrar rapidamente modelos de um provedor específico.

#### Acceptance Criteria

1. WHEN o usuário acessa a seleção de modelos OpenRouter THEN o sistema SHALL exibir um dropdown com todas as empresas disponíveis
2. WHEN o usuário seleciona uma empresa no dropdown THEN o sistema SHALL filtrar a lista mostrando apenas modelos dessa empresa
3. WHEN o usuário seleciona "Todas" no dropdown THEN o sistema SHALL mostrar todos os modelos disponíveis
4. IF uma empresa não tiver modelos disponíveis THEN ela SHALL NOT aparecer no dropdown

### Requirement 3

**User Story:** Como um usuário do Agno Builder, eu quero separar modelos gratuitos dos pagos usando um checkbox, para que eu possa controlar meus custos de uso.

#### Acceptance Criteria

1. WHEN o usuário acessa a seleção de modelos OpenRouter THEN o sistema SHALL exibir checkboxes para "Mostrar apenas gratuitos" e "Mostrar apenas pagos"
2. WHEN o usuário marca "Mostrar apenas gratuitos" THEN o sistema SHALL filtrar mostrando apenas modelos gratuitos
3. WHEN o usuário marca "Mostrar apenas pagos" THEN o sistema SHALL filtrar mostrando apenas modelos pagos
4. WHEN ambos os checkboxes estão desmarcados THEN o sistema SHALL mostrar todos os modelos
5. WHEN ambos os checkboxes estão marcados THEN o sistema SHALL mostrar todos os modelos

### Requirement 4

**User Story:** Como um usuário do Agno Builder, eu quero ver indicadores visuais claros sobre quais modelos são gratuitos, para que eu possa identificar rapidamente as opções sem custo.

#### Acceptance Criteria

1. WHEN um modelo é gratuito THEN o sistema SHALL exibir um ícone verde ou badge "GRATUITO"
2. WHEN um modelo é pago THEN o sistema SHALL exibir um ícone laranja ou badge "PAGO"
3. WHEN possível THEN o sistema SHALL exibir informações de preço para modelos pagos
4. IF informações de preço não estiverem disponíveis THEN o sistema SHALL exibir "Consulte openrouter.ai"

### Requirement 5

**User Story:** Como um usuário do Agno Builder, eu quero que a lista de modelos seja carregada rapidamente, para que eu tenha uma experiência fluida na interface.

#### Acceptance Criteria

1. WHEN o usuário seleciona OpenRouter THEN o sistema SHALL carregar a lista de modelos em menos de 3 segundos
2. WHEN a lista está carregando THEN o sistema SHALL exibir um indicador de loading
3. IF o carregamento falhar THEN o sistema SHALL exibir uma mensagem de erro e uma lista de modelos em fallback
4. WHEN a lista é carregada com sucesso THEN o sistema SHALL cachear os dados por 1 hora

### Requirement 6

**User Story:** Como um usuário do Agno Builder, eu quero buscar modelos por nome, para que eu possa encontrar rapidamente um modelo específico.

#### Acceptance Criteria

1. WHEN o usuário acessa a seleção de modelos OpenRouter THEN o sistema SHALL exibir uma caixa de busca
2. WHEN o usuário digita na caixa de busca THEN o sistema SHALL filtrar modelos em tempo real baseado no nome
3. WHEN a busca não retorna resultados THEN o sistema SHALL exibir "Nenhum modelo encontrado"
4. WHEN o usuário limpa a busca THEN o sistema SHALL mostrar todos os modelos novamente