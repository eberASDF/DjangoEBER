import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / 'web'
OUT.mkdir(exist_ok=True)

STYLE = '''<style>
body{font-family:Arial,sans-serif;background:#fff;color:#111;margin:26px;max-width:980px}
h1{font-size:23px;margin:0 0 6px}p{margin:0 0 18px;font-size:15px}
pre{font-family:Consolas,monospace;font-size:15px;line-height:1.45;
background:#f6f6f6;border:1px solid #bbb;padding:18px;white-space:pre-wrap;margin:9px 0 20px}
.row{margin-bottom:18px}.url{font-family:Consolas,monospace;font-size:14px}
.status{font-weight:bold}
</style>'''

def page(filename, title, note, content):
    (OUT / filename).write_text(
        '<!doctype html><html lang="es"><meta charset="utf-8">' + STYLE +
        '<body><h1>' + html.escape(title) + '</h1><p>' + html.escape(note) +
        '</p>' + content + '</body></html>', encoding='utf-8'
    )

def lines(path, start, end):
    source = (ROOT / path).read_text(encoding='utf-8').splitlines()
    return '\n'.join(f'{n:>3}  {source[n-1]}' for n in range(start, min(end, len(source))+1))

def code_page(filename, title, note, path, start, end):
    content = '<div class="url">' + html.escape(path) + '</div><pre>' + html.escape(lines(path, start, end)) + '</pre>'
    page(filename, title, note, content)

code_page('services.html', 'Evidencia: estrategia de descuento',
          'Fragmento del archivo real del proyecto.', 'products/services.py', 1, 44)
model_lines = (ROOT / 'products/models.py').read_text(encoding='utf-8').splitlines()
factory_start = next(i for i, line in enumerate(model_lines, 1) if 'def crear_con_categoria_default' in line) - 1
code_page('models.html', 'Evidencia: creación con categoría predeterminada',
          'Fragmento del archivo real del proyecto.', 'products/models.py', factory_start, factory_start + 10)
test_lines = (ROOT / 'products/tests.py').read_text(encoding='utf-8').splitlines()
test_start = next(i for i, line in enumerate(test_lines, 1) if 'def test_precio_final_con_token' in line)
code_page('tests.html', 'Evidencia: dos pruebas del endpoint',
          'Fragmento del archivo real del proyecto.', 'products/tests.py', test_start, len(test_lines))
code_page('views.html', 'Evidencia: endpoint protegido con JWT',
          'La vista llama a la capa de servicios.', 'products/views.py', 1, 35)

results = json.loads((OUT.parent / 'respuestas_api.json').read_text(encoding='utf-8'))
blocks = []
for item in results:
    blocks.append('<div class="row"><div class="url">GET ' + html.escape(item['url']) +
                  '</div><div class="status">HTTP ' + str(item['status']) + '</div><pre>' +
                  html.escape(json.dumps(item['response'], ensure_ascii=False, indent=2)) +
                  '</pre></div>')
page('api.html', 'Evidencia: /precio-final/ con JWT',
     'Respuestas reales obtenidas con un token temporal de acceso.', ''.join(blocks))

log = (OUT.parent / 'test_output.txt').read_text(encoding='utf-8')
page('terminal.html', 'Salida de python manage.py test',
     'Registro real de la ejecución de pruebas del proyecto.',
     '<pre>PS C:\\Users\\eberh\\django-project&gt; python manage.py test\n' + html.escape(log) + '</pre>')

print(OUT)
