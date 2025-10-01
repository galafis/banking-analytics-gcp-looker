# Guia de Contribuição

Bem-vindo ao projeto Banking Analytics Dashboard! Agradecemos seu interesse em contribuir.

Para garantir uma colaboração eficiente e manter a qualidade do código, por favor, siga as diretrizes abaixo.

## Como Contribuir

### 1. Faça um Fork do Repositório

Primeiro, faça um fork deste repositório para sua conta GitHub. Isso criará uma cópia do projeto onde você poderá fazer suas alterações.

### 2. Clone o Repositório Forkado

Clone o seu fork para sua máquina local:

```bash
git clone https://github.com/yourusername/banking-analytics-gcp-looker.git
cd banking-analytics-gcp-looker
```

Substitua `yourusername` pelo seu nome de usuário do GitHub.

### 3. Crie uma Branch

Crie uma nova branch para suas alterações. Use um nome descritivo para a branch, como `feature/nova-funcionalidade` ou `bugfix/correcao-erro-x`.

```bash
git checkout -b feature/sua-nova-feature
```

### 4. Faça Suas Alterações

Implemente suas alterações ou adicione novas funcionalidades. Certifique-se de:

*   **Seguir o estilo de código existente**: Mantenha a consistência com o código já presente no projeto.
*   **Escrever testes**: Se suas alterações adicionarem novas funcionalidades ou corrigirem bugs, inclua testes relevantes para garantir que tudo funcione como esperado.
*   **Atualizar a documentação**: Se suas alterações afetarem a funcionalidade ou a forma como o projeto é usado, atualize o `README.md` e outros arquivos de documentação conforme necessário.

### 5. Teste Suas Alterações

Antes de enviar suas alterações, execute os testes existentes e quaisquer novos testes que você tenha adicionado para garantir que nada foi quebrado:

```bash
pytest tests/
```

### 6. Commite Suas Alterações

Commite suas alterações com uma mensagem clara e concisa. Uma boa mensagem de commit deve explicar o que foi feito e por que foi feito.

```bash
git add .
git commit -m "feat: Adiciona nova funcionalidade X" # ou "fix: Corrige bug Y"
```

### 7. Envie Suas Alterações para o GitHub

Envie suas alterações para o seu repositório forkado no GitHub:

```bash
git push origin feature/sua-nova-feature
```

### 8. Abra um Pull Request (PR)

Finalmente, abra um Pull Request (PR) do seu repositório forkado para a branch `main` do repositório original. Certifique-se de:

*   **Fornecer uma descrição detalhada**: Explique o propósito do seu PR, as alterações que você fez e quaisquer considerações importantes.
*   **Referenciar issues**: Se o seu PR resolver uma issue existente, mencione-a na descrição (ex: `Closes #123`).
*   **Responder a comentários**: Esteja preparado para discutir suas alterações e fazer ajustes com base no feedback dos mantenedores.

## Padrões de Código

*   **Python**: Siga as diretrizes do [PEP 8](https://www.python.org/dev/peps/pep-0008/).
*   **Documentação**: Comentários claros e docstrings para funções e classes.

## Reportando Bugs

Se você encontrar um bug, por favor, abra uma issue no GitHub e forneça o máximo de detalhes possível, incluindo:

*   Uma descrição clara e concisa do bug.
*   Passos para reproduzir o comportamento.
*   O comportamento esperado.
*   O comportamento real.
*   Sua configuração (sistema operacional, versão do Python, etc.).

## Sugestões de Funcionalidades

Para sugerir uma nova funcionalidade, abra uma issue no GitHub e descreva sua ideia. Explique por que você acha que seria uma boa adição ao projeto e como ela se encaixaria na arquitetura existente.

Obrigado por sua contribuição!
