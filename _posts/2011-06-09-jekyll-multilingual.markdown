---
layout: post
title: Multilingual Site using Jekyl &amp; Liquid
categories: [en, blog]
tags: [blog, jekyll, liquid]
uuid: 85bb17e6-4e53-4a39-9dc0-f9f1a7dc1e01
---

Here is a tip to make a multilingual site using
[Liquid](http://www.liquidmarkup.org/) templates and
[Jekyll](http://jekyllrb.com/) relatively easily and with few duplications.

I will be giving examples from my own experience for
[{{site.url}}/]({{site.url}}/)

Start by specifying the language in
[YAML Front Matter](http://github.com/mojombo/jekyll/wiki/YAML-Front-Matter)
using a custom tag like `lang`:

{% highlight yaml %}
    ---
    layout: default
    title: Projelerim
    lang: tr
    ---
{% endhighlight %}

Here `lang` is just a custom tag which we can make use via `page.lang` variable
from within our pages.

Next, change your \_layouts/ and \_includes/ to be multilingual using simple
`case` statements:

{% highlight html %}
    <h3>{{ "{% case page.lang" }} %}{{ "{% when 'tr'" }} %}Etiket Bulutu{{ "{% else" }} %}Tag Cloud{{ "{% endcase" }} %}</h3>
{% endhighlight %}

Make note of the `else` statements which we use to specify a default
language. So pages without the `lang` tag will be in English.

That's all!

For more information, feel free to play with the source code of my blog:
[http://github.com/alip/alip.github.com](http://github.com/alip/alip.github.com)

Now I'll be writing a Turkish translation of this post and see if it works :)

Note to self: writing literal Liquid inside Liquid requires some weird syntax mentioned
[here](http://tesoriere.com/2010/08/25/liquid-code-in-a-liquid-template-with-jekyll/).

<!-- vim: set tw=0 nowrap ft=markdown spell spelllang=en sw=4 sts=4 et : -->
