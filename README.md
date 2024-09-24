<h1 align="center"><i>VendePass</i></h1>

<p align="center"> Uma interface de socket para venda de passagens aéreas.</p>

## Introdução
Desde o primeiro voo de Santos Dumont, a aviação evoluiu rapidamente, passando de uma curiosidade tecnológica a um dos principais meios de transporte no mundo. Inicialmente restrito a elites e serviços militares, o transporte aéreo começou a se popularizar após a Segunda Guerra Mundial, com a expansão de rotas comerciais. A democratização do acesso ao transporte aéreo tem-se acelerado nas últimas décadas, impulsionada pelo surgimento de companhias aéreas de baixo custo que revolucionaram o setor ao oferecer tarifas mais acessíveis e ampliar a conectividade global. Nesse contexto, a tecnologia de venda de passagens aéreas desempenha um papel central, permitindo que sistemas de reserva e processamento de bilhetes acompanhem a evolução e a complexidade desse setor.

Pensando nisso, foi proposto aos alunos do curso de Engenharia de Computação da Universidade Estadual de Feira de Santana(UEFS) o desenvolvimento de um sistema de comunicação usando a interface de socket nativa do TCP/IP para venda de passagens aéreas em um modelo cliente-servidor. Este relatório visa descrever objetivamente o desenvolvimento de tal solução em que o cliente, através da internet, pode comprar passagens para um destino escolhendo os trechos e assentos disponíveis. Além disso, o servidor armazena o grafo das rotas e voos provendo serviços de listagem das rotas, compra de trechos e reserva de assento(s) aos usuários. Ao final do desenvolvimento, a aplicação foi virtualizada por meio de contêineres Docker.

## Fundamentação teórica
<details>
<summary> <b>Interface de Programação de Aplicação (API)</b> </summary>
Interface de Programação de Aplicação ou <i>Application Programming Interface</i> (API) é mecanismo que permite a comunicação entre dois componentes de <i>software</i> ou aplicações através de um conjunto de definições e protocolos. APIs conectam soluções e serviços, sem a necessidade de saber como esses elementos foram implementados, o que simplifica o design e favorece a colaboração entre soluções e serviços. 

Por exemplo, a aplicação para a previsão do tempo em um telefone requer dados meteorológicos que exigiriam um sistema robusto no celular para o acesso às previsões. Entretanto, com o uso de uma API, a aplicação no dispositivo pode acessar e se comunicar com o sistema de software do instituto meteorológico na nuvem solicitando informações para o usuário sem implementar toda a complexidade do sistema no telefone, por exemplo. (O que é uma API? – Guia de APIs para iniciantes – AWS, [s.d.])

</details>

<details>
<summary> <b>Sockets</b> </summary>
Soquetes são canais de comunicação que permitem a processos não relacionados a troca de dados localmente e através de redes. Um único soquete é um ponto final de um canal de comunicação de duas vias (“Soquetes”, [s.d.]).

Um soquete de rede (ou socket) é uma interface de programação que permite a comunicação entre processos, seja no mesmo dispositivo ou em dispositivos diferentes. Essa comunicação ocorre por meio da rede, utilizando uma combinação de endereços Protocolo Internet (IP) e números de porta. Um único soquete é um ponto final de um canal de comunicação de duas vias, e sua função principal é facilitar a troca de dados entre dois pontos (“Soquetes”, [s.d.]).

Para configurar um soquete, é necessário definir dois componentes principais: o domínio de comunicação (nome ou espaço de endereço) e o protocolo de transporte. Esses dois elementos determinam como os dados serão transmitidos pela rede (STEVENS et al, 2003).

Domínios básicos:
- INTERNET (AF_INET) - os endereços consistem do endereço de rede da máquina e da identificação do nº da porta, o que permite a comunicação entre processos de sistemas diferentes. O soquete pode usar endereços IPv4, permitindo a comunicação via endereços IP de 32 bits, ou IPv6 (AF_INET6), com suporte a endereços de 128 bits, projetados para resolver o problema da exaustão de endereços IPv4. 
- Unix (AF_UNIX) - os processos se comunicam referenciando um pathname,
dentro do espaço de nomes do sistema de arquivos

Já os protocolos de transporte, segundo Tanenbaum (2011), determinam como os dados são transferidos entre os dispositivos. Os mais comuns são:

- Protocolo de Controle de Transmissão ou <i>Transmission Control Protocol</i> (TCP): Um protocolo orientado à conexão que garante a entrega confiável dos pacotes. O TCP estabelece uma conexão antes de começar a transmissão de dados, verificando erros e retransmitindo pacotes perdidos, o que o torna adequado para aplicações que precisam de confiabilidade, como a transferência de arquivos ou navegação na web.

- Protocolo de Dtagrama do Usuário ou <i>User Datagram Protocol</i> (UDP): Um protocolo não orientado à conexão, que envia pacotes sem a necessidade de estabelecer uma conexão prévia. Embora seja mais rápido que o TCP, não garante a entrega dos pacotes, o que o torna ideal para aplicações que priorizam a velocidade e a eficiência sobre a confiabilidade, como transmissões de vídeo ou jogos online.

- Protocolo Raw: Permite o acesso direto aos pacotes IP, sem passar pelos protocolos de transporte TCP ou UDP. É utilizado em aplicações de baixo nível, como testes de rede e ferramentas de diagnóstico.

</details>

<details>
<summary> <b>Plataforma Docker</b> </summary>
O Docker é uma plataforma de software open source que permite a criação, o teste e a implantação de aplicações rapidamente. Esta solução cria pacotes de software em unidades padronizadas e independentes chamadas de contêineres que têm tudo o que o software precisa para ser executado, inclusive bibliotecas, ferramentas de sistema e  código sem demandar que todos estes recursos sejam instalados na máquina física. Ao usar o Docker, é possível implantar, padronizar as operações e escalar rapidamente aplicações em qualquer ambiente com facilidade e melhor  utilização de recursos.(“AWS Docker - Amazon Web Services”, [s.d.]).

</details>

## Metodologia
### Arquitetura da Solução
### Paradigma de Comunicação
### Protocolo de Comunicação
### Formatação e tratamento de Dados
### Tratamento de Conexões Simultâneas
### Tratamento de Concorrência
## Resultados
## Conclusão
## Referências

AWS Docker - Amazon Web Services. Disponível em: <https://aws.amazon.com/pt/docker/>.

Soquetes. Disponível em: <https://www.ibm.com/docs/pt-br/aix/7.3?topic=concepts-sockets>.

Stevens, W. R., Fenner, B., & Rudoff, A. M. (2003). Unix network programming. Volume 1: The sockets networking API. Pearson Education.

Tanenbaum, A. S., & Wetherall, D. J. (2011). Redes de computadores. 5ª ed. Rio de Janeiro: Pearson.

‌
