from django import template

register = template.Library()

class PermCheckNode(template.Node):
    def __init__(self,deployment,capability,nodelist_true,nodelist_false):
        self.capability = capability
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.deployment = template.Variable(deployment)
        
    def render(self,context):
        d = self.deployment.resolve(context)
        u = context['request'].user
        checks = dict(view=d.can_view,
                      push=d.can_push,
                      edit=d.can_edit)
        if checks[self.capability](u):
            return self.nodelist_true.render(context)
        else:
            if self.nodelist_false is not None:
                return self.nodelist_false.render(context)
            else:
                return ""


@register.tag('if_can_view')
def can_view(parser,token):
    deployment = token.split_contents()[1:][0]
    nodelist_true = parser.parse(('else','end_can_view'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('end_can_view',))
        parser.delete_first_token()
    else:
        nodelist_false = None
    return PermCheckNode(deployment,"view",nodelist_true,nodelist_false)

@register.tag('if_can_push')
def can_push(parser,token):
    deployment = token.split_contents()[1:][0]
    nodelist_true = parser.parse(('else','end_can_push'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('end_can_push',))
        parser.delete_first_token()
    else:
        nodelist_false = None
    return PermCheckNode(deployment,"push",nodelist_true,nodelist_false)

@register.tag('if_can_edit')
def can_edit(parser,token):
    deployment = token.split_contents()[1:][0]
    nodelist_true = parser.parse(('else','end_can_edit'))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse(('end_can_edit',))
        parser.delete_first_token()
    else:
        nodelist_false = None
    return PermCheckNode(deployment,"edit",nodelist_true,nodelist_false)
