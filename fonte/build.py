#!/usr/bin/env python3
"""Gera o app independente (um único HTML) a partir do artboard Main.dc.html."""
import re, sys, pathlib

src, react, out = map(pathlib.Path, sys.argv[1:4])
s = src.read_text()
helm = s[s.index('<helmet>') + 8:s.index('</helmet>')]
body = s[s.index('</helmet>') + 9:s.index('</x-dc>')]
m = re.search(r'data-dc-script[^>]*>(.*?)</script>', s, re.S)
js = m.group(1)
title = re.search(r'<title>(.*?)</title>', s).group(1)
ver = re.search(r'(\d+\.\d+) beta', title).group(1)

RUNTIME = r"""
(function () {
  var h = React.createElement;
  var WHOLE = /^\{\{\s*([^}]+?)\s*\}\}$/, HOLE = /\{\{\s*([^}]+?)\s*\}\}/g;
  var EV = { onclick: 'onClick', onchange: 'onChange', oninput: 'onInput', onsubmit: 'onSubmit', onkeydown: 'onKeyDown', onfocus: 'onFocus', onblur: 'onBlur' };
  var REN = { 'class': 'className', 'for': 'htmlFor', inputmode: 'inputMode', autocomplete: 'autoComplete', tabindex: 'tabIndex', readonly: 'readOnly', maxlength: 'maxLength' };
  function look(sc, p) {
    if (p === 'true') return true; if (p === 'false') return false; if (p === 'null') return null;
    if (/^-?\d+(\.\d+)?$/.test(p)) return +p;
    return p.split('.').reduce(function (o, k) { return o == null ? undefined : o[k]; }, sc);
  }
  function val(str, sc) {
    var m = str.match(WHOLE); if (m) return look(sc, m[1]);
    if (str.indexOf('{{') < 0) return str;
    return str.replace(HOLE, function (_, p) { var v = look(sc, p); return v == null ? '' : String(v); });
  }
  function css(str) {
    var o = {};
    str.split(';').forEach(function (d) {
      var i = d.indexOf(':'); if (i < 0) return;
      var k = d.slice(0, i).trim(), v = d.slice(i + 1).trim(); if (!k) return;
      if (k.indexOf('--') !== 0) k = k.replace(/-([a-z])/g, function (_, c) { return c.toUpperCase(); });
      o[k] = v;
    });
    return o;
  }
  function kids(node, sc) {
    var out = [];
    node.childNodes.forEach(function (c) { var r = conv(c, sc); if (Array.isArray(r)) out.push.apply(out, r); else if (r != null) out.push(r); });
    return out;
  }
  function conv(n, sc) {
    if (n.nodeType === 3) { var v = val(n.nodeValue, sc); return v == null || v === false || v === true ? null : String(v); }
    if (n.nodeType !== 1) return null;
    var tag = n.localName;
    if (tag === 'sc-if') return val(n.getAttribute('value'), sc) ? kids(n, sc) : null;
    if (tag === 'sc-for') {
      var list = val(n.getAttribute('list'), sc) || [], as = n.getAttribute('as') || 'item', out = [];
      list.forEach(function (it, i) { var s2 = Object.create(sc); s2[as] = it; s2.$index = i; out.push.apply(out, kids(n, s2)); });
      return out;
    }
    var props = {};
    for (var i = 0; i < n.attributes.length; i++) {
      var a = n.attributes[i], name = a.name;
      if (name.indexOf('hint-') === 0) continue;
      var v = val(a.value, sc);
      if (name.indexOf('on') === 0) { if (typeof v !== 'function') continue; name = EV[name] || name; }
      else if (name === 'style') v = css(String(v));
      else name = REN[name] || name;
      props[name] = v;
    }
    var ch = kids(n, sc);
    return h.apply(null, [tag, props].concat(ch));
  }
  window.DCLogic = function DCLogic(props) { this.props = props || {}; this.state = {}; };
  var queued = false, inst, root, tpl;
  function draw() {
    var v = inst.renderVals();
    root.render(h.apply(null, [React.Fragment, null].concat(kids(tpl, v))));
  }
  function schedule() {
    if (queued) return; queued = true;
    Promise.resolve().then(function () { queued = false; draw(); setTimeout(function () { inst.componentDidUpdate && inst.componentDidUpdate(); }, 0); });
  }
  DCLogic.prototype.setState = function (o) { this.state = Object.assign({}, this.state, typeof o === 'function' ? o(this.state, this.props) : o); schedule(); };
  DCLogic.prototype.forceUpdate = schedule;
  window.__mountDC = function (C) {
    var q = new URLSearchParams(location.search);
    tpl = document.getElementById('tpl').content;
    inst = new C({ tema: q.get('tema') || 'sistema', destaque: q.get('destaque') || 'lima' });
    var el = document.getElementById('root'); root = createRoot(el);
    var nj = document.getElementById('nojs'); if (nj) nj.remove();
    draw();
    inst.componentDidMount && inst.componentDidMount();
  };
})();
"""

STANDALONE_CSS = """
html,body{height:100%;margin:0;background:#F2F3EE}
@media (prefers-color-scheme:dark){html,body{background:#0B0D10}}
#root{height:100%}
.app{width:100% !important;max-width:600px;height:100% !important;margin:0 auto}
@supports (height:100dvh){.app{height:100dvh !important}}
.scr{top:env(safe-area-inset-top);bottom:env(safe-area-inset-bottom)}
.sheet{padding-bottom:env(safe-area-inset-bottom)}
#nojs{font-family:system-ui,sans-serif;max-width:420px;margin:15vh auto;padding:24px;text-align:center;color:#555}
"""

html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0B0D10">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Vai Pra Cima">
<meta name="description" content="Vai Pra Cima: a ponte entre você e o seu futuro. Encontre peneiras de futebol e futsal em São Paulo.">
<title>{title}</title>
{helm.strip()}
<style>{STANDALONE_CSS}</style>
</head>
<body>
<div id="nojs"><h1 style="font-size:22px">Vai Pra Cima</h1><p>Este app precisa de JavaScript. Abra o link HTTPS no Safari ou no Chrome (o visualizador do WhatsApp ou do e-mail não roda o app).</p></div>
<noscript><style>#nojs{{display:block}}</style></noscript>
<div id="root"></div>
<template id="tpl">{body}</template>
<script>/* React 19 (MIT) */
{react.read_text()}</script>
<script>{RUNTIME}</script>
<script>
{js}
window.__mountDC(Component);
</script>
</body>
</html>
"""
out.write_text(html)
print(out, len(html), 'bytes, versão', ver)
