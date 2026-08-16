# Configuração de Abertura Padrão de Markdown em Modo Preview

## 1. Contexto e Objetivo
Configurar o editor Antigravity (IDE) para que arquivos `.md` (Markdown) abram por padrão diretamente no modo visualizador renderizado (`vscode.markdown.preview.editor`) em vez do modo código-fonte texto puro.

## 2. Alterações Realizadas
Adicionada a propriedade `workbench.editorAssociations` aos arquivos de configuração de usuário do Antigravity:

- `~/.config/Antigravity IDE/User/settings.json`
- `~/.config/Antigravity/User/settings.json`

### Estrutura Adicionada
```json
"workbench.editorAssociations": {
  "*.md": "vscode.markdown.preview.editor"
}
```

## 3. Como Reverter ou Abrir como Código
- Para abrir o código-fonte de um arquivo `.md` pontualmente: clique com o botão direito no arquivo na barra lateral e selecione **"Abrir com..."** -> **"Editor de Texto"** (ou use `Ctrl+K V` para alternar/abrir lado a lado).
- Para desfazer o comportamento padrão: remova a chave `"*.md": "vscode.markdown.preview.editor"` de `workbench.editorAssociations` nas configurações do usuário.
