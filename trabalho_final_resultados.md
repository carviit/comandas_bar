
CSI606-2024-02 - Remoto - Trabalho Final - Resultados  
Discente: Carlos Vitor Ferreira de moura

## Resumo

O trabalho final tem como objetivo desenvolver uma aplicação web para o gerenciamento de comandas em um bar. A aplicação permite a criação, acompanhamento e fechamento de comandas de clientes de forma eficiente, reduzindo erros e otimizando o atendimento. O sistema conta com um back-end para armazenamento de informações e um front-end intuitivo, facilitando a interação dos funcionários.

## 1. Funcionalidades implementadas

- **Cadastro e autenticação de funcionários:** Permite o acesso seguro ao sistema por meio de login.  
- **Abertura e fechamento de comandas:** Controle eficaz das comandas abertas e finalizadas.  
- **Adição e remoção de itens:** Edição dos pedidos em tempo real, com atualização automática do valor total da comanda.  
- **Listagem de comandas em aberto:** Dashboard intuitivo para consulta rápida das comandas ativas.  
- **Cálculo automático do valor total:** Somatória dos valores dos itens adicionados à comanda.  
- **Sistema de permissões:** Diferentes níveis de acesso para funcionários e gerentes.  
- **Histórico de pedidos:** Registro detalhado das transações realizadas.

## 2. Funcionalidades previstas e não implementadas

- **Integração com sistemas externos:** Conexão com sistemas de estoque e contabilidade para automatizar a gestão financeira e de suprimentos.  
- **Integração com meios de pagamento reais:** Implementação de gateways de pagamento para processamento de transações de forma automatizada.  
- **Suporte para aplicativos móveis:** Versões nativas para Android e iOS para facilitar o uso em tablets e smartphones.  
- **Recuperação de senha:** Implementação de funcionalidade para permitir que funcionários possam recuperar suas senhas em caso de esquecimento.

## 3. Outras funcionalidades implementadas

- **Interface responsiva e intuitiva:** Design focado na usabilidade para os funcionários, com modais para visualização de notas fiscais e gerenciamento de mesas.  
- **Comunicação via API REST:** Facilita a integração entre o front-end e o back-end, garantindo a consistência dos dados.  
- **Atualização dinâmica de produtos:** Permite alterar quantidades, atualizar ou remover produtos das comandas de forma prática.

## 4. Principais desafios e dificuldades

- **Integração entre tecnologias:** Conciliar o funcionamento do back-end com o front-end, garantindo uma comunicação eficaz via APIs REST.  
- **Segurança dos dados:** Implementação de um sistema de autenticação robusto e gerenciamento seguro das informações armazenadas.  
- **Desenvolvimento da interface:** Criação de uma experiência de usuário intuitiva e responsiva para facilitar o uso pelos funcionários.  
- **Gerenciamento de permissões:** Implementação de níveis de acesso que atendam às diferentes necessidades dos cargos (funcionários x gerentes).

## 5. Instruções para instalação e execução

1. **Clonar o repositório:** Faça o clone do projeto para sua máquina.  
2. **Instalar dependências:** Utilize o gerenciador de pacotes para instalar todas as dependências do back-end e front-end.  
3. **Configurar o banco de dados:** Configure o MySQL conforme as instruções fornecidas, garantindo a persistência das informações.  
4. **Executar a aplicação:** Inicie o servidor e acesse o sistema via navegador no endereço especificado.  
5. **Realizar cadastro:** Cadastre os funcionários para testar as funcionalidades de autenticação e gerenciamento de comandas.

## 6. Referências

- Documentação do Flask e SQLAlchemy.  
- Documentação do Bootstrap.  
