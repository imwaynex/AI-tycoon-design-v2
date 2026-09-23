"""Export the repository token snapshot into CSS. Run from the Site root."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
index=json.loads((root/'tokens/index.json').read_text())
docs={name:json.loads((root/f'tokens/{name}.json').read_text()) for name in index['files']}
def get(path):
    keys=path.split('.'); value=docs[keys.pop(0)]
    for key in keys:value=value[key]
    return get(value[1:-1]) if isinstance(value,str) and value.startswith('{') else value
def rem(value):return f'{value/index["rootPx"]:g}rem'
rules=[]
for n in docs['space']['scale']:rules.append(f'--space-{n}: {rem(get("space.scale."+n))};')
for name,path in {'target-fine':'size.target.fine','target-coarse':'size.target.coarse','target-comfortable':'size.target.comfortable','target-gap':'size.targetGap','focus-width':'size.focus.width','focus-offset':'size.focus.offset','border-width':'size.border.hairline'}.items():rules.append(f'--{name}: {get(path)}px;')
for n in ['body','label','caption','heading']:rules += [f'--type-{n}: {get("type.role."+n+".size")};',f'--leading-{n}: {get("type.role."+n+".lineHeight")};']
for n in ['control','container','dialog','pill']:rules.append(f'--radius-{n}: {rem(get("radius.usage."+n))};')
for n in docs['layer']['z']:rules.append(f'--layer-{n}: {get("layer.z."+n)};')
for n in ['bg.surface','bg.inverse','text.primary','text.inverse','focus.ring','focus.ringInverse','border.strong']:rules.append(f'--color-{n.replace(".","-")}: {get("color.semantic."+n)};')
rules += [f'--dialog-max: {rem(get("layout.dialogMax"))};',f'--motion-fast: {get("motion.durationMs.fast")}ms;']
for n in ['margin','gutter','regionGap']:rules.append(f'--layout-{n}: {rem(get("layout."+n+".base"))};')
css='/* Generated from tokens/index.json '+index['version']+'; do not edit. */\n:root {\n  '+'\n  '.join(rules)+'\n}\n'
# Root-relative sizing; breakpoints use em as required by SPEC §2.
css+=':root { --target-size: var(--target-fine); --control-size: '+str(get('size.control.regular'))+'px; }\n@media (any-pointer: coarse) { :root { --target-size: var(--target-coarse); } }\n'
for band in ['sm','md','lg']:
 css+=f'@media (min-width: {get("layout.breakpoint."+band)/index["rootPx"]:g}em) {{ :root {{ '+ ' '.join(f'--layout-{n}: {rem(get("layout."+n+"."+band))};' for n in ['margin','gutter','regionGap'])+' } }\n'
css+=f'@media (max-height: {get("layout.shortHeight")/index["rootPx"]:g}em) {{ :root {{ --control-size: {get("size.control.compact")}px; --layout-regionGap: var(--space-5); }} }}\n'
(root/'dist/tokens.css').write_text(css)
