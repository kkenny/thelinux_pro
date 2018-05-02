---
layout: post
title: Jekyll ve Liquid ile Çok dilli Siteler
categories: [tr, blog]
tags: [blog, jekyll, liquid]
lang: tr
uuid: 740a8575-be83-42fd-bd9b-f8271069f7c9
---

Burada [Liquid](http://www.liquidmarkup.org/) şablonları ve
[Jekyll](http://jekyllrb.com/) ile nasıl basitçe çok dilli bir site
tasarlayabileceğinizden bahsedeceğim.

Örnekleri [{{site.url}}/]({{site.url}}/) sitesini
tasarlarkenki tecrübelerimden vereceğim.

Öncelikle dili özel bir etiket ile - ben bunun için `lang` kelimesini seçtim -
[YAML Front Matter](http://github.com/mojombo/jekyll/wiki/YAML-Front-Matter)'da
belirtiyoruz:

{% highlight yaml %}
    ---
    layout: default
    title: Projelerim
    lang: tr
    ---
{% endhighlight %}

Burda `lang` özel etiketini sayfalarımızdan `page.lang` değişkeni ile
kullanabileceğiz.

Daha sonra, \_layouts ve \_includes dizinlerindeki taslaklarınızı basit
`case` ifadeleriyle çok dilli yapın:

{% highlight html %}
    <h3>{{ "{% case page.lang" }} %}{{ "{% when 'tr'" }} %}Etiket Bulutu{{ "{% else" }} %}Tag Cloud{{ "{% endcase" }} %}</h3>
{% endhighlight %}

Burada dikkat edilmesi gereken `else` ifadesiyle öntanımlı bir dil
belirtmemiz. Yani `lang` etiketi olmayan sayfalar İngilizce olacak.

İşte bu kadar!

Daha fazla bilgi için günlüğümün kaynak kodlarını kurcalayabilirsiniz:
[http://github.com/alip/alip.github.com](http://github.com/alip/alip.github.com)

Kişisel not: Liquid ifadelerini olduğu gibi yazmak
[burada](http://tesoriere.com/2010/08/25/liquid-code-in-a-liquid-template-with-jekyll/)
bahsedildiği üzere garip bir sözdizimi gerektiriyor.

<!-- vim: set tw=80 ft=markdown sw=4 sts=4 et : -->
