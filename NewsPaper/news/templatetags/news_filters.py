from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    censored_words = ['хуй', 'пизда']
    for word in censored_words:
        value = value.replace(word, '*' * len(word))
    return value


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
