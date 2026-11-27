import re
from pathlib import Path

import pytest
from django.contrib.staticfiles import finders

FONTES = [
    "core/fonts/plus-jakarta-sans-latin-wght-normal.woff2",
    "core/fonts/instrument-serif-latin-400-normal.woff2",
]
LICENCAS = [
    "core/fonts/OFL-plus-jakarta-sans.txt",
    "core/fonts/OFL-instrument-serif.txt",
]


def ler_css():
    caminho = finders.find("core/css/fonts.css")
    assert caminho, "não encontrei core/css/fonts.css"
    return Path(caminho).read_text(encoding="utf-8")


@pytest.mark.parametrize("ficheiro", FONTES)
def test_as_fontes_existem_e_sao_woff2_validos(ficheiro):
    caminho = finders.find(ficheiro)

    assert caminho, f"não encontrei {ficheiro}"
    assert Path(caminho).read_bytes()[:4] == b"wOF2"


@pytest.mark.parametrize("ficheiro", LICENCAS)
def test_cada_fonte_leva_a_sua_licenca(ficheiro):
    caminho = finders.find(ficheiro)

    assert caminho, f"não encontrei {ficheiro}"
    assert "SIL Open Font License" in Path(caminho).read_text(encoding="utf-8")


def test_o_css_so_aponta_para_ficheiros_que_existem():
    referencias = re.findall(r'url\("\.\./([^"]+)"\)', ler_css())

    assert len(referencias) == 2
    for referencia in referencias:
        assert finders.find(f"core/{referencia}"), f"em falta: {referencia}"


def test_o_css_declara_as_duas_familias_do_sistema_de_design():
    css = ler_css()

    assert 'font-family: "Plus Jakarta Sans"' in css
    assert 'font-family: "Instrument Serif"' in css
    assert css.count("font-display: swap") == 2
