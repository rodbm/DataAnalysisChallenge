NIBO Danta Analyst Challenge - Level 2
==============

Quer saber o por que vale a pena trabalhar no nibo? Acesse [tech.nibo.com.br](https://tech.nibo.com.br)

## O desafio
Você deverá entregar uma tabela Cohort em conjunto com uma análise sobre os dados do problema. 

### Problema
Os contadores amam as soluções que o Nibo oferece. E, assim que nos conhecem, querem logo fechar contrato. Esse contrato geralmente é feito em lotes das empresas. Então é possível que um contador assine um contrato de 100 empresas e vá criando elas ao longo do tempo.

Para o Nibo, quanto mais rápido um contador consegue criar todas as empresas, melhor é o engajamento. Então queremos entender como anda a relação destes dados para tomar decisões sobre o que fazer na área de vendas e de produto. Será que os contadores estão criando todas as empresas? Quais informações podemos tirar a partir dos dados que temos?

Temos muitos dados vindos de várias fontes. Para este problema, temos dois arquivos com dados fictícios:

`SRC/AccountantContracts.json` Possui a lista de contadores (accountants) com o seu ID único (accountantId), data da assinatura do contrato (signDate), quantidade de empresas contratadas (signedOrganizationsCount) e data de quando o contrato foi cancelado, caso não seja mais cliente (cancelDate).

`SRC/CreatedOrganizations.sql` Possui a QUERY para inserir em um banco de dados a lista de todas as empresas criadas no sistema. Cada linha representa uma empresa com seu ID único (organizationId), o contador relacionado (accountantId), a data de criação (organizationCreateDate) e ainda possui a data de criação do próprio contador (accountantCreateDate), dado este que deveria estar no primeiro arquivo.   

### O que você deverá fazer
Você precisará criar uma análise Cohort que indique a taxa de criação de empresas ao longo de 12 meses desde a data de contratação do contador. Não sabe o que é Cohort? [Leia este artigo]((https://customersuccessbrasil.com/analise-cohort-um-grande-aliado-da-operacao-de-customer-success/)) e entenda.

Você também precisará desenvolver uma hipótese sobre se há ou não uma relação entre o engajamento dos contadores e o cancelamento do contrato. Fique livre para decidir como construir esta hipótese: poderá usar gráficos, criar textos de análise ou ser criativo :D

Você pode escolher como irá tratar os dados, onde e como os dados finais serão armazenados e também decidir qual ferramenta irá utilizar para apresentar o resultado da Cohort e a sua análise qualitativa.

Mesmo que você não finalize todos os problemas, nos envie o desafio. Mais do que o resultado final, queremos saber como você raciocinou para chegar à uma solução.

**Requisitos:**
- [ ] Escolha as ferramentas e técnicas que desejar. Menos Excel.
- [ ] Não utilize soluções prontas. Nós as conhecemos.
- [ ] Coloque todas os códigos/recursos utilizados, caso haja, na pasta `SRC`
- [ ] Escreva as instruções para visualizar ou rodar a solução em um arquivo `readme.md` dentro da pasta `SRC`

## Envio da solução
Você deverá criar um fork deste repositório, seguir as instruções e requisitos do problema, preencher o formulário "_about/Profile.md" e enviar para recruta.tech@nibo.com.br o link do seu fork.

Tenha capricho com o resultado final. Essa é a sua chance de entrar para o melhor time, na startup que mais cresce no Brasil.

**NIBO - Desenvolvimento de alta performance para geeks inquietos**

Boa sorte :D
