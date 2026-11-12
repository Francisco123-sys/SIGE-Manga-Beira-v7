# Sistema Integrado de Gestão Escolar (SIGE) - Escola Secundária da Manga (Beira - Sofala)

## Novas Melhorias Implementadas:
1. **Bancos & Carteiras Móveis:** Seletor obrigatório com **Banco BCI, Millennium BIM, Standard Bank, M-Pesa e e-Mola**.
2. **Validação Estrita de Referência (9 Dígitos):** Aceita exclusivamente 9 dígitos numéricos (`\d{9}`), bloqueando duplicações e caracteres inválidos.
3. **Datas Distintas no Pagamento:** Regista tanto a **Data em que o Depósito foi Efectuado** quanto a **Data do Registo no Sistema**.
4. **Matrícula Condicionada ao Pagamento:** No ato de inscrição de novos alunos, após os dados pessoais, o sistema exige o lançamento do pagamento/talão antes de gravar o aluno na base de dados (exceto alunos oficialmente isentos).
5. **Exportação de Listas Oficiais em `.DOC`:** Botão por turma para descarregar documento Word com o **Emblema da República de Moçambique**, cabeçalho da **Escola Secundária da Manga**, **Classe, Turma, Período (Manhã/Tarde/Noite) e Curso (Diurno, Nocturno ou À Distância)**.