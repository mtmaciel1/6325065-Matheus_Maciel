# sistema_refatorado.py

from abc import ABC, abstractmethod
from typing import Dict, List

# =============================================
# ABSTRAÇÕES (DIP - Dependency Inversion Principle)
# =============================================

class MetodoPagamento(ABC):
    """Interface para métodos de pagamento"""
    
    @abstractmethod
    def processar_pagamento(self, pedido: Dict) -> bool:
        pass

class Notificador(ABC):
    """Interface para métodos de notificação"""
    
    @abstractmethod
    def enviar_notificacao(self, pedido: Dict) -> bool:
        pass

# =============================================
# IMPLEMENTAÇÕES DE PAGAMENTO (OCP - Open/Closed Principle)
# =============================================

class PagamentoCartaoCredito(MetodoPagamento):
    def processar_pagamento(self, pedido: Dict) -> bool:
        print(f"Pagando R$ {pedido['valor']:.2f} com cartão de crédito...")
        # Lógica específica para pagamento com cartão
        return True

class PagamentoBoleto(MetodoPagamento):
    def processar_pagamento(self, pedido: Dict) -> bool:
        print(f"Gerando boleto no valor de R$ {pedido['valor']:.2f}...")
        # Lógica específica para pagamento com boleto
        return True

class PagamentoPix(MetodoPagamento):
    def processar_pagamento(self, pedido: Dict) -> bool:
        print(f"Processando pagamento Pix no valor de R$ {pedido['valor']:.2f}...")
        # Lógica específica para pagamento com Pix
        print("QR Code gerado! Pagamento processado via Pix.")
        return True

# =============================================
# IMPLEMENTAÇÕES DE NOTIFICAÇÃO (OCP - Open/Closed Principle)
# =============================================

class NotificadorEmail(Notificador):
    def enviar_notificacao(self, pedido: Dict) -> bool:
        print(f"Enviando e-mail de confirmação para {pedido['cliente_email']}...")
        # Lógica para enviar e-mail
        return True

class NotificadorSMS(Notificador):
    def enviar_notificacao(self, pedido: Dict) -> bool:
        print(f"Enviando SMS de confirmação para o telefone do pedido #{pedido['id']}...")
        # Lógica para enviar SMS
        return True

# =============================================
# PROCESSADOR DE PEDIDOS REFATORADO (SRP - Single Responsibility Principle)
# =============================================

class ProcessadorDePedidos:
    """Agora esta classe tem uma única responsabilidade: orquestrar o processamento do pedido"""
    
    def __init__(self, metodo_pagamento: MetodoPagamento, notificadores: List[Notificador]):
        # DIP - Dependemos de abstrações, não de implementações concretas
        self.metodo_pagamento = metodo_pagamento
        self.notificadores = notificadores
    
    def processar(self, pedido: Dict) -> bool:
        try:
            # 1. Lógica de processamento do pedido (SRP - única responsabilidade)
            print(f"Processando o pedido #{pedido['id']} no valor de R$ {pedido['valor']:.2f}...")
            
            # 2. Processar pagamento (delegado para a classe especializada)
            if not self.metodo_pagamento.processar_pagamento(pedido):
                print("Falha no processamento do pagamento!")
                return False
            
            # 3. Enviar notificações (delegado para as classes especializadas)
            for notificador in self.notificadores:
                notificador.enviar_notificacao(pedido)
            
            # 4. Finalização
            pedido['status'] = 'concluido'
            print("Pedido concluído!")
            return True
            
        except Exception as e:
            print(f"Erro ao processar pedido: {e}")
            return False

# =============================================
# FÁBRICA PARA CRIAR PROCESSADORES 
# =============================================

class FabricaProcessadores:
    """Factory para criar diferentes configurações de processadores"""
    
    @staticmethod
    def criar_processador_cartao_email():
        return ProcessadorDePedidos(
            metodo_pagamento=PagamentoCartaoCredito(),
            notificadores=[NotificadorEmail()]
        )
    
    @staticmethod
    def criar_processador_boleto_email():
        return ProcessadorDePedidos(
            metodo_pagamento=PagamentoBoleto(),
            notificadores=[NotificadorEmail()]
        )
    
    @staticmethod
    def criar_processador_pix_sms_email():
        return ProcessadorDePedidos(
            metodo_pagamento=PagamentoPix(),
            notificadores=[NotificadorSMS(), NotificadorEmail()]
        )

# =============================================
# EXEMPLO DE USO
# =============================================

if __name__ == "__main__":
    # Criando pedidos de exemplo
    pedido1 = {
        'id': 123,
        'valor': 150.75,
        'cliente_email': 'cliente@exemplo.com',
        'status': 'pendente'
    }
    
    pedido2 = {
        'id': 456,
        'valor': 299.90,
        'cliente_email': 'outro@exemplo.com',
        'status': 'pendente'
    }
    
    pedido3 = {
        'id': 789,
        'valor': 89.50,
        'cliente_email': 'cliente3@exemplo.com',
        'status': 'pendente'
    }

    print("=== PROCESSAMENTO COM CARTÃO + EMAIL ===")
    processador1 = FabricaProcessadores.criar_processador_cartao_email()
    processador1.processar(pedido1)

    print("\n" + "="*50)
    print("=== PROCESSAMENTO COM BOLETO + EMAIL ===")
    processador2 = FabricaProcessadores.criar_processador_boleto_email()
    processador2.processar(pedido2)

    print("\n" + "="*50)
    print("=== PROCESSAMENTO COM PIX + SMS + EMAIL (BÔNUS) ===")
    processador3 = FabricaProcessadores.criar_processador_pix_sms_email()
    processador3.processar(pedido3)

    print("\n" + "="*50)
    print("=== DEMONSTRANDO FLEXIBILIDADE ===")
    
    # Podemos criar combinações personalizadas facilmente
    processador_personalizado = ProcessadorDePedidos(
        metodo_pagamento=PagamentoPix(),
        notificadores=[NotificadorSMS()]  # Apenas SMS, sem email
    )
    
    pedido_personalizado = pedido1.copy()
    pedido_personalizado['id'] = 999
    processador_personalizado.processar(pedido_personalizado)