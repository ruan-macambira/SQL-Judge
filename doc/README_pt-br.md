# SQL Judge, uma ferramenta de Validação de Schemas de Banco de Dados Relacionais (SQL)

## Objetivos

SQL Judge tem como bojetivo possibilitar a criação de validações do schema de bancos de dados relacionais que são facilmente testáveis e reutilizáveis entre diferentes implementações (Postgres, MariaDB, MySQL, etc.)

O primeiro é alcançado por fazer as validações funções de python que são executadas do jeito que são definidas, necessitando apenas que tais funções sejam marcadas com um decorator(que não altera em nada a execução desta), fazendo-a testável através de ferramentas padrão de testes unitários em python, como unittest e pytest

O segundo é alcançado utilizando um método independente da ferramenta, e provida pelo usuário de conseguir informações do banco de dados (ver [Desenvolvendo um adaptador de banco de Dados](#Desenvolvendo-um-adaptador-de-banco-de-Dados))

## Motivação
Fez-se necessário que fossem desenvolvidos uma série de validações automatizadas para um padrão de banco de dados. A ferramenta escolhida foi a de implementar Custom Design Rules para o Oracle Datamodeler. Essa ferramenta, no entanto tinha muitos problemas:
 - A engine de Javascript utilizada pelo Datamodeler por padrão é a Oracle Nashorn, que além de não ter implementar toda a biblioteca padrão JS, está em vias de ser descontinuada.
 - A ferramente não é propriamente documentada. Sua única guia é apenas uma especificação da API escondida dentro das pastas do Datamodeler, fazendo com que muitas vezes quem estivesse com a missão de implementar as validações precisasse fazer inúmeras tentativas cegas para conseguir ter acesso aos dados que desejavam de uma entidade.
 - A falta de uma documentação própria não permitiu definir se certas entidades podiam ser diretamente validadas pela ferramenta, causando várias gambiarras ao longo do caminho - Por exemplo: Criar uma validações para uma tabela que na verdade valida todas as Restrições do Schema
 - Não havia um modo confiável de gerar testes e fazer debug das validações, uma vez que o único output possível eram as mensagens das validações que retornavam falso, não havendo um REPL que nos permitisse executar comandos como console.log(mais um agravante ao ponto anterior)


## Instalação
 - Faça o clone do repositório
 - No terminal escreva ```python setup.py bdist_wheel```
 - Novamente no terminal ```pip install dist/[ARQUIVO_WHEEL].whl```, onde ARQUIVO_WHEEL é o nome do arquivo que foi criado na pasta dist/

## Como funciona
_TODO: escrever seção_

## Como utilizar
As configurações de utilização são passadas através de arquivos no formato JSON, que seguem o padrão abaixo:

```json
{
  "adapter": {
    "module": "adapter_module",
    "class": "AdapterClass",
    "params": ["posarg1"],
    "named_params": { "namedarg1": "value1"}
  },
  "validations": {
    "module": "validations_module"
  },
  "ignore_tables": ["ignored_table"],
  "export": {
    "format": "\"CLI\" or \"CSV\""
  }
}
```

**adapter**: Opções relacionadas ao Adaptador, i.e a classe que informa o dicionário de dados do schema, para montar o schema. Instruções de como criar um adaptador mais abaixo.

 - module *(obrigatório)*: Nome do módulo em que a classe do adaptador se encontra. *Planeja-se no futuro que o usuário possa passar um arquivo qualquer, que independa do sys.path do interpretador*
 - class *(obrigatório)*: Nome da classe do adaptador
 - params *(opcional)*: Lista de argumentos posicionais para serem enviadas ao construtor do adaptador
 - named_params *(opcionais)*: Hash com argumentos para serem enviados como argumentos nomeados ao construtor do adaptador

**validations**: Opções relacionadas às validações. Instruções de como criar as validações mais abaixo.
 - module *(obrigatório)*: Módulo em que as validações se encontra.

**ignore_tables** (*opcional, padrão:* []): Array com todas as tabelas no schema que serão ignoradas pelas validações

**export**: Formato de exportação do relatório. *No momento ele sempre exporta em stdout*
 - format (*opcional, possível: [CLI, CSV], padrão: CLI*)

É possível utilizar múltiplos arquivos de configuração. Se houver um conflito entre dois arquivos atribuem um valor para a mesma opção, a prioridade é do arquivo que foi especificado por último.

O output é enviado para stdout, independente do formato em que é definido a exportação, mudando apenas a formatação da saída. Caso execute:

``` cd examples; python -m sql_judge config.json special_config.json ```

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
A ferramenta de validação do Schema é meramente uma maneira de validar um schema de banco de dados SQL. Ele não possui nativamente uma maneira de se comunicar com um banco de Dados, ficando para o usuário a tarefa de providenciar um meio do programa obter o schema. O sistema não assume nada sobre a fonte dos dados, não precisando nem mesmo ser extraído de um banco de dados real. Contanto que ele implemente corretamente a interface do objeto, todas as entidades do schema hão de ser reproduzidas no sistema. Mais informações de como implementar um adaptador no arquivo contendo sua interface (sql_judge/adapter.py)

## Criando validações
O validador não possui nenhuma validação que ele execute por padrão. O usuário precisa, portanto, definir todas as validações em um único arquivo.

O validador não asssume que nenhuma função do módulo passado é uma validação, ele precisa ser explicitamente definido como tal através utilizando o *decorator* ```validates``` especificando o grupo de entidades no qual aquela validação ocorre. Ex.:

```python
from sql_judge import validates # Decorator que marca as funções

def not_a_validation(): # Validador não reconhece como uma validação
  pass

@validates('Tables') # Define que a função irá validar tabelas
def table_must_start_with_tbl(table):
  if table.name[0:4] == 'tbl_':
    return None # Válida
  return "Table must start with 'tbl_'" # Inválida
```

Cada função que é define uma validação precisa seguir algumas regras:
 - Precisa ser marcada com o decorator ```validates```, passando, como argumento, o grupo de entidades (Tables, Columns, Indexes, Constraints, Triggers, Functions, Procedures) no plural e com a primeira letra em maiúsculo;
 - Precisa possuir um, e apenas um, argumento, pelo qual a entidade será referenciada. É recomendado, mas não obrigatório, que o argumento possua o nome da entidade no qual ela valide;
 - Para que uma entidade seja considerada válida em uma dada validação, a validação executada na entidade deve retornar None;
 - Se uma validação retorna uma string, é considerada uma falha de validação, e o seu valor de retorno é utilizado como a mensagem explicando o porque da validação ter falhado, que será adicionado ao relatório.

## API das entidades do Schema
O montador de Schema tem suporte para as seguintes entidades de um banco de Dados do SQL:
 - Tabelas;
 - Funções;
 - Procedimentos;
 - Colunas;
 - Triggers;
 - Índices (atualmente ligado a colunas);
 - Restrições;
 - Sequências.

Está em planos para ter suporte:
 - Visões;
 - Visões Materializadas;

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
|Propriedade|Classe|Descrição                                                    |  
|-----------|------|-------------------------------------------------------------|  
|name       |str   |Nome da Entidade                                             |  
|-----------|------|-------------------------------------------------------------|  
|schema     |Schema| Objeto principal, do qual se pode acessar todas as entidades|  

### Table
|Propriedade|Classe      |Descrição                                                    |  
|-----------|------------|-------------------------------------------------------------|  
|columns    |List[Column]| Colunas da tabela                                           |  
|primary_key|Column      | Coluna da tabela na qual está a restrição de chave primária |  

### Propriedades Comuns a Column e Trigger(TableEntity)
|Propriedade|Classe|Descrição                   |  
|-----------|------|----------------------------|  
|table      |Table | Tabela associada à Entidade|  

### Column
|Propriedade|Classe          |Descrição                                              |  
|-----------|----------------|-------------------------------------------------------|  
|primary_key|bool            | True se é a chave primária. False, caso contrário     |  
|references |Table           | Tabela no qual esta coluna referencia, caso ela o faça|  
|indexes    |List[Index]     | Índice associado à coluna                             |  
|constraints|List[Constraint]| Restrições associadas à coluna                        |

### Propriedades Comuns a Index e Constraint(ColumnEntity)
|Propriedade|Classe|Descrição                  |  
|-----------|------|---------------------------|  
|column     |column|Coluna associada à entidade|
