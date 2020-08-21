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

## Desenvolvendo um adaptador de banco de Dados
A ferramenta de validação do Schema é meramente uma maneira de validar um schema de banco de dados SQL. Ele não possui nativamente uma maneira de se comunicar com um banco de Dados, ficando para o usuário a tarefa de providenciar um meio do programa obter o schema. Para isso, a função adapter() dentro do arquivo de configuração deve conter uma instância de um objeto adaptador, que implementa corretamente a interface presente em validate_schema/adapter.py. O sistema não assume nada sobre a fonte dos dados, não precisando nem mesmo ser extraído de um banco de dados real. Contanto que ele implemente corretamente a interface do objeto, todas as entidades do schema hão de ser reproduzidas no sistema. Mais informações de como implementar um adaptador no arquivo contendo sua interface (validate_schema/adapter.py)


## API das entidades do Schema
O montador de Schema tem suporte para as seguintes entidades de um banco de Dados do SQL:
 - Tabela;
 - Função;
 - Procedimento;
 - Coluna;
 - Trigger;
 - Índice (atualmente ligado a colunas);
 - Restrição.

Está em planos para ter suporte:
 - Visões;
 - Visões Materializadas;
 - Sequências.

Cada Entidade do schema possui suas propriedades próprias (especificadas abaixo), bem como as relações que esta possui com outras entidades. Por Exemplo, a Entidade tabela possui acesso às colunas que lhe pertencem, bastando apenas que seja utilizadas ```table.columns```, sendo ```table``` o objeto que representaria a tabela em questão. Todas as propriedades das entidades são definidas como properties do objeto, portanto devem ser invocadas apenas pelo seu nome, sem utilizar a sintaxe de invocação de método, i.e ao invés de utilizar ```entity.name()```, utilizar ```entity.name```. Essa regra vale para todas as propriedades apresentadas abaixo.

### Schema
|Propriedade|Classe            |Descrição                       |  
|-----------|------------------|--------------------------------|  
|tables*    |List[Table]       |Tabelas do Schema               |  
|functions* |List[SchemaEntity]|Funções do Schema               |  
|procedures*|List[SchemaEntity]|Procedimentos do Schema         |  
|triggers   |List[Trigger]     |Triggers das Tabelas do Schema  |  
|indexes    |List[Index]       |Índices das colunas do Schema   |  
|constraints|List[Constraint]  |Restrições das colunas do Schema|  

### Propriedades Comuns a Todas as Entidades (Entity)
|Propriedade|Classe|Descrição         |  
|-----------|------|------------------|  
|name       |str   |Nome da Entidade  |  

### Propriedades Comuns a Table, Function e Procedure(SchemaEntity)
|Propriedade|Classe|Descrição                                                    |  
|-----------|------|-------------------------------------------------------------|  
|schema     |Schema| Objeto principal, do qual se pode acessar todas as entidades|  

### Table
|Propriedade|Classe      |Descrição                                                    |  
|-----------|------------|-------------------------------------------------------------|  
|columns*   |List[Column]| Colunas da tabela                                           |  
|primary_key|Column      | Coluna da tabela na qual está a restrição de chave primária |  


### Function
Não possui propriedades além das que compartilha com SchemaEntity

### Procedure
Não possui propriedades além das que compartilha com SchemaEntity

### Propriedades Comuns a Column e Trigger(TableEntity)
|Propriedade|Classe|Descrição                   |  
|-----------|------|----------------------------|  
|table      |Table | Tabela associada à Entidade|  

### Trigger
|Propriedade|Classe|Descrição                                           |  
|-----------|------|----------------------------------------------------|  
|hook       |str   | Momento de ativação da trigger (ex.: BEFORE UPDATE)|


### Column
|Propriedade|Classe          |Descrição                                              |  
|-----------|----------------|-------------------------------------------------------|  
|index*     |Index           | Índice associado à coluna                             |  
|constraints|List[Constraint]| Restrições associadas à coluna                        |  
|references |Table           | Tabela no qual esta coluna referencia, caso ela o faça|  
|type       |str             | Tipo de valor presente na coluna (ex.: NUMBER, TEXT)  |
|primary_key|bool            | True se é a chave primária. False, caso contrário     |

### Propriedades Comuns a Index e Constraint(ColumnEntity)
|Propriedade|Classe|Descrição                  |  
|-----------|------|---------------------------|  
|column     |column|Coluna associada à entidade|

### Index
|Propriedade|Classe|Descrição                                                   |  
|-----------|------|------------------------------------------------------------|
|unique     |bool  | True se for um index que está ligado a uma restrição unique|

### Constraint
|Propriedade|Classe|Descrição                                                    |  
|-----------|------|-------------------------------------------------------------|  
|type       |str   | O tipo da restrição da coluna (Ex.: UNIQUE, NOT NULL, CHECK)|  


 \*Propriedades marcadas com um asterisco(*) são, no momento atual, elementos diretamente acessáveis, podendo portanto ter seu valor alterado. Recomenda-se cuidado quando for se utilizar dessas propriedades, pois reescrevê-las afetará as validações seguintes. Isso está planejado pra ser consertado em um futuro próximo.