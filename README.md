# Ferramenta de Validação de Schemas de Banco de Dados Relacionais (SQL)

## Objetivos
A ferramenta tem como objetivo possibilitar o usuário de escrever testes de validações para os Bancos de Dados SQL que sejam facilmente testáveis e reutilizáveis entre diferentes implementações de Bancos de Dado (Ex.: AS calidações funcionarem tanto para PostgreSQL e Oracle SQL)

## Motivação
Fez-se necessário que fossem desenvolvidos uma série de validações automatizadas para um padrão de banco de dados. A ferramenta escolhida foi a de implementar Custom Design Rules para o Oracle Datamodeler. Essa ferramenta, no entanto tinha muitos problemas:
 - A engine de Javascript utilizada pelo Datamodeler por padrão é a Oracle Nashorn, que além de não ter implementar toda a biblioteca padrão JS, está em vias de ser descontinuada.
 - A ferramente não é propriamente documentada. Sua única guia é apenas uma especificação da API escondida dentro das pastas do Datamodeler, fazendo com que muitas vezes quem estivesse com a missão de implementar as validações precisasse fazer inúmeras tentativas cegas para conseguir ter acesso aos dados que desejavam de uma entidade.
 - A falta de uma documentação própria não permitiu definir se certas entidades podiam ser diretamente validadas pela ferramenta, causando várias gambiarras ao longo do caminho - Por exemplo: Criar uma validações para uma tabela que na verdade valida todas as Restrições do Schema
 - Não havia um modo confiável de gerar testes e fazer debug das validações, uma vez que o único output possível eram as mensagens das validações que retornavam falso, não havendo um REPL que nos permitisse executar comandos como console.log(mais um agravante ao ponto anterior)

## Como utilizar
_Aviso: A seção a seguir é um esboço, baseado em uma solução provisória de execução do programa. Tudo que estiver aqui pode já estar desatualizado, e assim se manterá até o momento em que esse aviso for retirado_

Para utilizar a validação, crie um arquivo .py contendo no mínimo 4 funções:

 - adapter(): Retorna a interface implementada do banco de dados
 - validations(): Dict contendo as validações a serem feitas no schema
 - ignore_tables(): Lista contendo os nomes das tabelas, em string, no qual a validação é ignorada
 - export(): retorna uma string dizendo o formato de exportação (atualmente: CLI, CSV)

No momento, não há valores padrões, ou verificação de erros. Todas as funções devem ser implementadas corretamente para que o programa execute.

Execute, então, validate_schema.py com o módulo do arquivo como argumento (python validate_schema.py NOME_DO_ARQUIVO, se o arquivo for NOME_DO_ARQUIVO.py e estiver na pasta raiz). No momento, não há como especificar o caminho do arquivo.

O output é enviado para stdout, independente do formato em que é definido a exportação, mudando apenas a formatação da saída. Caso execute:

``` python validate_schema.py examples.config ```

O output será:

```
REPORT
==================================================
Tables:
==================================================
 + purchases
   + Table should start with "TBL_"
----------------------------------------
Functions:
==================================================
Procedures:
==================================================
Columns:
==================================================
 + tbl_product.product_name
   + varchar column should start with VC_
----------------------------------------
 + purchases.product_id
   + Since it' a foreign key, column should be named "PRODUCT_ID"
----------------------------------------
 + tbl_price_history.product_id
   + Since it' a foreign key, column should be named "PRODUCT_ID"
----------------------------------------
 + tbl_price_history.history_price
   + real column should start with RL_
----------------------------------------
Triggers:
==================================================
 + tbl_price_history.alter_product_price
   + Trigger name should start with "TG_"
----------------------------------------
Indexes:
==================================================
Constraints:
==================================================
```

## API das entidades do Schema
 ~ Em Construção ~
