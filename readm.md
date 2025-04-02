# **CSI606-2024-02 - Remoto - Proposta de Trabalho Final**

## *Discente: Carlos Vitor Ferreira de Moura*

### Resumo

O trabalho final tem como objetivo desenvolver uma aplicação web para o gerenciamento de comandas em um bar. A aplicação permitirá a criação, acompanhamento e fechamento de comandas de clientes de forma eficiente, reduzindo erros e otimizando o atendimento. O sistema contará com um back-end para armazenar as informações e um front-end intuitivo para facilitar a interação dos funcionários do bar.

A aplicação será desenvolvida utilizando a tecnologia moderna **Python Flask**. O banco de dados escolhido será **MySQL**, garantindo persistência e confiabilidade das informações. A comunicação entre front-end e back-end será feita por meio de APIs REST.

### 1. Tema 

O tema deste trabalho é o desenvolvimento de um sistema de gerenciamento de comandas para um bar. O sistema permitirá que os funcionários realizem a abertura de comandas, adicionem pedidos, consultem o consumo dos clientes e realizem o fechamento e pagamento de cada comanda.

### 2. Escopo

O projeto terá as seguintes funcionalidades principais:

- **Cadastro e autenticação de funcionários**
- **Abertura e fechamento de comandas**: Controle de comandas abertas e finalizadas.
- **Adição e remoção de itens nas comandas**: Permissão para edição de pedidos em tempo real.
- **Listagem de comandas em aberto**: Dashboard intuitivo para consulta rápida.
- **Cálculo automático do valor total da comanda**
- **Sistema de permissões**: Diferentes níveis de acesso para funcionários e gerentes.
- **Histórico de pedidos**: Registro detalhado das transações realizadas.

### 3. Restrições

- O sistema não incluirá integração com sistemas externos de estoque ou contabilidade.
- O pagamento será simulado e não haverá integração com meios de pagamento reais.
- A aplicação será desenvolvida apenas para web, sem suporte a aplicativos móveis neste momento.
- O design será focado na usabilidade para funcionários e não para clientes finais.
- O suporte a múltiplos idiomas não será implementado nesta versão inicial.
- A autenticação será implementada apenas para os funcionários, sem acesso de clientes.

### 4. Protótipo

Protótipos para as seguintes páginas vão ser elaborados e podem ser encontrados no GitHub:

- **Tela de Login**: Autenticação dos funcionários com suporte a recuperação de senha.
- **Dashboard**: Visão geral das comandas em aberto, pedidos em andamento e estatísticas básicas.
- **Página de Comandas**: Listagem de todas as comandas abertas e possibilidade de adicionar/remover itens com atualização em tempo real.
- **Tela de Pagamento**: Finalização e fechamento da comanda, incluindo opções de desconto e taxa de serviço.
- **Relatórios**: Visualização de estatísticas sobre vendas.
- **Gestão de Funcionários**: Tela exclusiva para gerentes adicionarem ou removerem funcionários do sistema.

Os protótipos podem ser acessados em:

### 5. Referências
