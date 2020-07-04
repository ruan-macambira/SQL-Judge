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
 ~ Em Construção ~

## API das entidades do Schema
 ~ Em Construção ~
