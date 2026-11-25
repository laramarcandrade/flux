# flux

1. O PROBLEMA
--------------------------------------------------------------------------------
Na organização de eventos, controlar as vendas de mesas e ingressos por anotações soltas, 
mensagens ou planilhas separadas costuma gerar falhas. Quando vendedores ou equipes 
diferentes vendem ao mesmo tempo, é comum vender a mesma mesa duas vezes, perder o controle 
de pagamentos pendentes e cancelamentos, e enfrentar filas na portaria por causa de códigos 
repetidos ou listas de acesso que não batem.

O Flux propõe um registro único de vendas. Cada venda guarda o comprador, os titulares dos 
ingressos e a empresa vendedora. O programa bloqueia a venda duplicada de uma mesa, gera um 
código individual para cada ingresso e controla pagamento, cancelamento e reembolso. Na 
portaria, valida o código de cada ingresso e libera a entrada uma única vez.

Nesta versão, o programa funciona no terminal, em um único computador por vez, sem acesso 
simultâneo em rede.


2. ARQUIVOS DO PROJETO
--------------------------------------------------------------------------------
ingressos.py         Regras do sistema: vender, pagar, cancelar, reembolsar,
                     validar entrada, salvar e carregar.

main.py              Menu no terminal que usa as funções de ingressos.py.

testes.py            Casos de teste; gera o arquivo registro_testes.txt.

registro_testes.txt  Registro dos testes: caso, entrada, resultado esperado,
                     resultado obtido e conclusão.

README.txt           Este arquivo.


3. REQUISITOS
--------------------------------------------------------------------------------
- Python 3 (desenvolvido com Python 3.14).
- Não há dependências externas: só módulos da biblioteca padrão (json). Por isso
                                não há requirements.txt.


4. COMO EXECUTAR
--------------------------------------------------------------------------------
Abra um terminal na pasta do projeto:

O programa principal está localizado em: 
    python main.py
E os testes estão localizados em: 
    python testes.py

A última linha dos testes mostra o total de casos e de falhas. 
O arquivo registro_testes.txt é recriado a cada execução. Os testes também criam três
arquivos de apoio (vendas_teste.json, vendas_vazio_teste.json e
corrompido_teste.json), que podem ser apagados depois.


5. COMO USAR O PROGRAMA
--------------------------------------------------------------------------------
5.1. Informe o nome do evento e o modo:
   - MESA: cada pedido é uma mesa com 4 ingressos.
   - INGRESSO: cada pedido tem a quantidade de ingressos informada.

5.2. As vendas de cada evento ficam num arquivo JSON com o nome do evento e do modo
   (por exemplo, Festa_Teste_MESA.json). Para continuar um evento, digite o mesmo
   nome e o mesmo modo.

5.3. Menu:
   1 - Comprar mesa / ingressos
   2 - Confirmar pagamento
   3 - Cancelar
   4 - Registrar reembolso
   5 - Portaria (validar entrada pelo código do ingresso)
   6 - Listar vendas
   0 - Sair


6. EXEMPLO DE EXECUÇÃO (MODO MESA)
--------------------------------------------------------------------------------
6.1. Compre a mesa 5, com comprador, empresa e os nomes dos 4 titulares (Enter usa o
     nome do comprador);
6.2. Confirme o pagamento da mesa 5;
6.3. Tente comprar a mesa 5 de novo: o programa responde "Mesa já vendida.";
6.4. Na portaria, ao digitar M5-01, aparecerá: "Entrada liberada: [Nome do titular], mas, 
     ao digitar M5-01 outra vez, aparecerá "Ingresso já utilizado.";
6.5. Ao tentar cancelar a mesa 5: o programa irá recusar, porque um ingresso já foi usado;
6.6. Compre e pague a mesa 6, cancele-a e registre o reembolso. Na portaria, M6-01
   responde "Ingresso cancelado.".


7. REGRAS PRINCIPAIS
--------------------------------------------------------------------------------
- Uma mesa (ou pedido) só pode ter uma venda ativa por vez; depois de cancelada,
  volta a ficar disponível.
- Cada ingresso tem código próprio (por exemplo, M5-01) e status próprio:
  nao_utilizado, utilizado ou cancelado. A entrada é liberada individualmente.
- Pagamento: pendente, pago, reembolso_pendente, reembolsado ou cancelado.
- Não é possível cancelar um pedido que já tenha ingresso utilizado.
- Cancelar um pedido pago deixa o reembolso como pendente; cancelar um pedido não
  pago apenas o cancela.
- O comprador é quem fica responsável pelo pedido; o nome em que o pagamento foi
  feito não é registrado.


8. DADOS E LIMITAÇÕES
--------------------------------------------------------------------------------
- Todos os dados são simulados; não há dados pessoais reais.
- O ingresso é gerado como texto na tela; não há envio real por WhatsApp ou
  e-mail, nem integração com pagamento.
- Cada evento tem um único arquivo, usado por uma pessoa por vez. Duas equipes só
  compartilham o registro se usarem o mesmo computador e o mesmo arquivo, uma de
  cada vez; não há acesso simultâneo nem rede.
- Nomes de evento com os caracteres / \ : * ? " < > | não funcionam, pois o nome
  é usado no nome do arquivo.
- Trabalhos futuros: prazo de cancelamento por data e hora, histórico de
  alterações, troca de nome de titular e relatório de reembolsos pendentes.


9. DECLARAÇÃO DE USO DE FERRAMENTAS DE IA
--------------------------------------------------------------------------------
Este projeto foi desenvolvido com apoio do assistente Claude (Anthropic). O
problema, as regras de negócio (comprador separado do pagamento, liberação
individual na portaria, regras de cancelamento e reembolso, modos MESA e INGRESSO)
e as decisões de projeto foram definidos por mim. O Claude foi usado para 
sugerir a organização das funções e dos testes e revisar trechos de código. 
O código foi executado e verificado por mim com os casos de testes.py, cujos resultados 
estão em registro_testes.txt, e eu me responsabilizo por compreender todo o conteúdo entregue.
