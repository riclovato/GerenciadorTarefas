# Casos de Uso

1. Adicionar Tarefa
   - Ator: Usu�rio
   - Fluxo principal:
     1. Usu�rio seleciona "Adicionar Nova Tarefa"
     2. Sistema exibe formul�rio de nova tarefa
     3. Usu�rio preenche t�tulo, descri��o, data de vencimento e prioridade
     4. Usu�rio confirma a adi��o
     5. Sistema valida os dados
     6. Sistema adiciona a tarefa ao banco de dados
     7. Sistema atualiza a lista de tarefas

2. Visualizar Tarefas
   - Ator: Usu�rio
   - Fluxo principal:
     1. Usu�rio abre o aplicativo
     2. Sistema exibe lista de tarefas existentes

3. Marcar Tarefa como Conclu�da
   - Ator: Usu�rio
   - Fluxo principal:
     1. Usu�rio seleciona uma tarefa na lista
     2. Usu�rio marca a op��o "Conclu�da"
     3. Sistema atualiza o status da tarefa no banco de dados
     4. Sistema atualiza a exibi��o da tarefa na lista

4. Editar Tarefa
   - Ator: Usu�rio
   - Fluxo principal:
     1. Usu�rio seleciona uma tarefa na lista
     2. Usu�rio escolhe a op��o "Editar"
     3. Sistema exibe formul�rio com dados atuais da tarefa
     4. Usu�rio modifica os campos desejados
     5. Usu�rio confirma as altera��es
     6. Sistema valida os dados
     7. Sistema atualiza a tarefa no banco de dados
     8. Sistema atualiza a exibi��o da tarefa na lista

5. Excluir Tarefa
   - Ator: Usu�rio
   - Fluxo principal:
     1. Usu�rio seleciona uma tarefa na lista
     2. Usu�rio escolhe a op��o "Excluir"
     3. Sistema pede confirma��o
     4. Usu�rio confirma a exclus�o
     5. Sistema remove a tarefa do banco de dados
     6. Sistema atualiza a lista de tarefas

6. Filtrar Tarefas
   - Ator: Usu�rio
   - Fluxo principal:
     1. Usu�rio seleciona op��es de filtro (status, prioridade ou data)
     2. Sistema aplica o filtro � lista de tarefas
     3. Sistema exibe a lista de tarefas filtrada