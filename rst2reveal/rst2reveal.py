import os.path as osp

from docutils import nodes
from docutils.parsers import rst
from docutils.writers import html4css1
from docutils.parsers.rst import directives

class CodeDirective(rst.Directive):
    required_arguments = 0 # no required argument
    optional_arguments = 1 # language
    final_argument_whitespace = True
    option_spec = {'font-size': directives.length_or_percentage_or_unitless,
                   }
    has_content = True # content block

    def run(self):
        if self.arguments: # a specific language was specified
            text = u'<pre><code class="%s" style="font-size: %s;">\n%s\n</code></pre>' % (
                self.arguments[0],
                self.options.get('font-size', '80%'),
                u'\n'.join(self.content))
        else:
            text = u'<pre><code style="font-size: %s;">\n%s\n</code></pre>' % (
                self.options.get('font-size', '80%'),
                u'\n'.join(self.content))
        # return [nodes.literal_block(text, text)]
        return [nodes.raw('', text, format='html')]


class RevealJSWriter(html4css1.Writer):

    default_template_path = osp.join(osp.dirname(osp.abspath(__file__)), 'boilerplate.html')
    default_stylesheet_path = osp.join(osp.dirname(osp.abspath(__file__)), 'css')
    default_javascript_path = osp.join(osp.dirname(osp.abspath(__file__)), 'js')

    settings_spec = html4css1.Writer.settings_spec + (
        'reveal.js specific options',
        None,
        (
            # XXX find a clean to override stylesheet_path
            ('base path for reveal.js stylesheets. '
             'Default: "%s"' % default_stylesheet_path,
             ['--reveal-stylesheet-path'],
             {'metavar': '<file>', 'overrides': 'reveal_stylesheet_path',
              'default': default_stylesheet_path}),
            ('base path for reveal.js javascript files. '
             'Default: "%s"' % default_javascript_path,
             ['--javascript-path'],
             {'metavar': '<file>', 'overrides': 'javascript',
              'default': default_javascript_path}),
            ('logo path if any. Default: no logo',
             ['--logo-path'],
             {'metavar': '<file>', 'overrides': 'logo_path',
              'default': None}),
            )
        )

    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = RevealHTMLTranslator

    def interpolation_dict(self):
        subs = html4css1.Writer.interpolation_dict(self)
        subs['javascript-path'] = self.document.settings.javascript_path
        subs['stylesheet-path'] = self.document.settings.reveal_stylesheet_path
        if self.document.settings.logo_path:
            logo = u'<img src="%s" />' % self.document.settings.logo_path
        else:
            logo = u''
        subs['logo'] = logo
        return subs

class RevealHTMLTranslator(html4css1.HTMLTranslator):
    """rst -> reveal.js html translator"""

    def __init__(self, *args, **kwargs):
        html4css1.HTMLTranslator.__init__(self, *args, **kwargs)
        self.fragment_li = False

    def visit_section(self, node):
        self.section_level += 2 # hack to get <h2> in sections
        self.body.append(self.starttag(node, 'section'))

    def depart_section(self, node):
        self.section_level -= 2
        self.body.append(u'</section>')

    def visit_definition(self, node):
        self.fragment_li = True
        self.body.append('</dt>\n')
        self.body.append(self.starttag(node, 'dd', '', CLASS='fragment'))
        self.set_first_last(node)

    def depart_definition(self, node):
        self.fragment_li = False
        self.body.append('</dd>\n')

    def visit_enumerated_list(self, node):
        self.fragment_li = True
        html4css1.HTMLTranslator.visit_enumerated_list(self, node)

    def depart_enumerated_list(self, node):
        self.fragment_li = False
        html4css1.HTMLTranslator.depart_enumerated_list(self, node)

    def visit_list_item(self, node):
        if self.fragment_li:
            kwargs = {'CLASS': 'fragment'}
        else:
            kwargs = {}
        self.body.append(self.starttag(node, 'li', '', **kwargs))
        if len(node):
            node[0]['classes'].append('first')

    def visit_foobar(self, node):
        asdasdassd


def run():
    from docutils.core import publish_cmdline
    from docutils.parsers.rst import directives
    directives.register_directive('code', CodeDirective)
    writer = RevealJSWriter()
    publish_cmdline(writer_name='revealjs', writer=writer,
                    settings_overrides={'template': writer.default_template_path,
                                        })

if __name__ == '__main__':
    run()
