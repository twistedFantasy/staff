try:
    from codemirror import CodeMirrorTextarea
except ImportError:
    pass


THEME = 'eclipse'
ADDON_JS = [
    'mode/multiplex',
    'edit/matchbrackets',
    'edit/closebrackets',
    'fold/foldgutter',
    'fold/foldcode',
    'fold/brace-fold',
    'fold/xml-fold',
    'fold/comment-fold',
    'selection/selection-pointer',
    'selection/active-line',
]
ADDON_CSS = [
    'fold/foldgutter',
]
CONFIG = {
    'foldGutter': True,
    'gutters': ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
    'selectionPointer': True,
    'lineNumbers': True,
    'foldConfig': {},
    'lineWrapping': True,
}


def json_widget(readonly=False, attrs=None):
    config = CONFIG.copy()
    config.update({
        'readOnly': readonly,
        'styleActiveLine': not readonly,
    })
    return CodeMirrorTextarea(attrs=attrs, mode={'name': 'javascript', 'json': True},
        theme=THEME, addon_js=ADDON_JS, addon_css=ADDON_CSS, config=config)


def python_widget(readonly=False, attrs=None):
    config = CONFIG.copy()
    config.update({
        'readOnly': readonly,
        'styleActiveLine': not readonly,
    })
    return CodeMirrorTextarea(attrs=attrs, mode={'name': 'python', 'singleLineStringErrors': True},
        theme=THEME, addon_js=ADDON_JS, config=config)
