# Análise das Violações SOLID

## 1. SRP - Princípio da Responsabilidade Única
**Violação**: A classe ProcessadorDePedidos faz tudo - processa pedido, faz pagamento e envia notificação. Deveria ter uma responsabilidade só.

## 2. OCP - Princípio Aberto/Fechado  
**Violação**: Para adicionar novo método de pagamento (como Pix), preciso modificar a classe principal. Deveria ser extensível sem modificar.

## 3. LSP - Princípio da Substituição de Liskov
**Violação**: Não tem hierarquia de classes, então não tem como substituir comportamentos.

## 4. ISP - Princípio da Segregação de Interface
**Violação**: Não tem interfaces. Se tivesse, provavelmente seria uma interface grande com métodos que não são usados por todos.

## 5. DIP - Princípio da Inversão de Dependência
**Violação**: A classe principal depende diretamente das implementações concretas dos pagamentos, não de abstrações.