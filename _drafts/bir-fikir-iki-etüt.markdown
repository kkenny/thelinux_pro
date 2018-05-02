---
layout: post
title: Bir Fikir, İki Etüt
categories: [tr, blog]
tags: [satranç, etüt, oyunsonu]
lang: tr
uuid: d4bb8b7d-0ef8-4f44-93a9-7e0e731af536
chess: true
---

Etüt, satranç oyununun sanatsal yönünü yücelten bir sahnedir. Sanatçı, satranç
taşlarını fırça gibi kullanarak oyunun kuralları çerçevesinde bir eser yaratır ve
eserin güzelliğinin alımlanması için etütün çözülmesi gerekir. Etütlerin bu saklı
güzelliği, özgünlük, çeldiricilik ve şaşırtıcılık gibi niteliklerle ilintilidir. Bu
niteliklerin her biri, etütün çözümünü zorlaştırmakla birlikte oyuncunun çözümden
alacağı keyfi de arttırır.

Etüt çözmek, turnuva satrancıyla karşılaştırıldığında alışılageldik satranç
oyunundan kopuk, verimsiz bir uğraş gibi görünebilir. Bu nedenden ötürü çoğu satranç
oyuncusu, etüt çözmenin keyifli bir uğraş olduğunu kabul etmekle birlikte bu uğraşın
satranççının tekniğine yapabileceği olası katkıları yadsır. Bu yazımda etütlerin
satranççının oyunsonu tekniğine yapabileceği katkıları seçtiğim iki örnek üzerinden
betimlemeye çalışacağım. Aşağıdaki satranç tahtalarında bu iki etüt verilmiştir.
Yazımı okumaya devam etmeden etütleri çözmenizi öneririm. Taşları oynatarak
bulduğunuz çözümü doğrulayabilirsiniz.

{% assign board_counter = 0 %}
{% assign board_title = 'Neumann, M 1926 (Shakhmatny Listok#149)' %}
{% assign board_fen = '8/7K/7P/1P6/2n4k/4n3/1P6/8 w - - 0 1' %}
{% assign board_mov = 'h7g6 c4e5 g6f6 e5g4 f6e6 g4h6 b5b6 h6f7 e6f7 e3c4 b6b7 c4d6 f7e7 d6b7 b2b4' %}
{% assign board_res = '1-0' %}
{% include tahta.liquid %}

{% assign board_counter = 1 %}
{% assign board_title = 'Fritz, J 1950 (Svobodne Slovo)' %}
{% assign board_fen = '2b5/2n2K1k/8/8/8/8/RP6/8 w - - 0 1' %}
{% assign board_mov = 'a2a1 c8b7 a1a7 c7b5 a7b7 b5d6 f7e7 d6b7 b2b4' %}
{% assign board_res = '1-0' %}
{% include tahta.liquid %}
