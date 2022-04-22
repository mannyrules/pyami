import unittest
from pathlib import Path

import lxml
import lxml.etree
import lxml.html

# local
from py4ami.ami_pdf import SVG_NS, SVGX_NS, STYLE, AmiPage, X, Y, FILL, STROKE, FONT_FAMILY, FONT_SIZE, HtmlUtil

# class PDFTest:

FINAL_DRAFT_DIR = "/Users/pm286/projects/readable_climate_reports/ipcc/dup/finalDraft/svg"  # PMR only
RESOURCES = Path(Path(__file__).parent, "resources")  # only works for PMR
CLIMATE = Path(RESOURCES, "climate")
PAGE_9 = Path(CLIMATE, "fulltext-page.9.svg")
PAGE_6 = Path(CLIMATE, "fulltext-page.6.svg")
HTML_TEMP_DIR = Path(Path(__file__).parent.parent, "temp", "html")
FULL_TEMP_DIR = Path(Path(__file__).parent.parent, "temp", "full")


def test_pdfbox_output_exists():
    assert str(CLIMATE) == "/Users/pm286/workspace/pyami/test/resources/climate", f"resources {CLIMATE}"
    assert CLIMATE.exists(), f"{CLIMATE} should exist"


def test_findall_svg():
    assert PAGE_9.exists(), f"{PAGE_9} should exist"
    page9_elem = lxml.etree.parse(str(PAGE_9))
    texts = page9_elem.findall(f"//{{{SVG_NS}}}text")
    assert len(texts) == 108


def test_get_text_attribs():
    ami_page = AmiPage.create_page_from_SVG(PAGE_9)
    text0 = ami_page.get_svg_text(0)
    assert text0.svg_text_elem.tag == f"{{{SVG_NS}}}text"
    assert text0.svg_text_elem.attrib.get(Y) == '44.76'
    assert text0.svg_text_elem.attrib.get(
        X) == '72.0,79.201,84.721,90.241,96.961,104.162,111.363,117.482,124.798,127.288,258.242,263.762,268.802,276.601,284.401,288.841,292.202,297.241,299.761,303.001,308.041,311.402,313.921,319.441,324.481,327.241,330.001,334.441,339.481,347.28,351.601,356.641,361.081,364.442,368.28,370.77,448.08,451.439,456.96,463.563,470.167,472.687,480.006,486.61,491.651,494.171,503.533,510.718,513.238,516.594,519.951,523.307'
    assert text0.svg_text_elem.attrib.get(
        f"{{{SVGX_NS}}}width") == '0.72,0.56,0.56,0.67,0.72,0.72,0.61,0.72,0.25,0.55,0.56,0.5,0.78,0.78,0.44,0.33,0.5,0.25,0.33,0.5,0.33,0.25,0.56,0.5,0.28,0.28,0.44,0.5,0.78,0.44,0.5,0.44,0.33,0.39,0.25,0.55,0.33,0.56,0.67,0.67,0.25,0.72,0.67,0.5,0.25,0.94,0.72,0.25,0.33,0.33,0.33,0.25'
    assert text0.svg_text_elem.get(
        STYLE) == 'fill:rgb(0,0,0);font-family:TimesNewRomanPSMT;font-size:9.96px;stroke:none;'
    text_content = text0.get_text_content()
    assert text_content == "APPROVED Summary for Policymakers IPCC AR6 WG III "
    assert len(text_content) == 50  # some spaces have been elided??


def test_get_text_attrib_vals():
    ami_page = AmiPage.create_page_from_SVG(PAGE_9)
    ami_text0 = ami_page.get_svg_text(0)
    x_coords = ami_text0.get_x_coords()
    assert x_coords == [
        72.0, 79.201, 84.721, 90.241,
        96.961, 104.162, 111.363, 117.482, 124.798, 127.288, 258.242, 263.762, 268.802,
        276.601, 284.401, 288.841, 292.202, 297.241, 299.761,
        303.001, 308.041, 311.402, 313.921, 319.441, 324.481, 327.241, 330.001,
        334.441, 339.481, 347.28, 351.601, 356.641, 361.081, 364.442,
        368.28, 370.77, 448.08, 451.439, 456.96, 463.563, 470.167,
        472.687, 480.006, 486.61, 491.651, 494.171, 503.533, 510.718, 513.238, 516.594, 519.951, 523.307]
    assert len(x_coords) == 52

    widths = ami_text0.get_widths()
    assert widths == [
        0.72, 0.56, 0.56, 0.67, 0.72, 0.72, 0.61,
        0.72, 0.25, 0.55, 0.56, 0.5, 0.78, 0.78, 0.44, 0.33, 0.5, 0.25, 0.33, 0.5, 0.33,
        0.25, 0.56, 0.5, 0.28, 0.28, 0.44, 0.5, 0.78, 0.44, 0.5, 0.44, 0.33,
        0.39, 0.25, 0.55, 0.33, 0.56, 0.67, 0.67, 0.25, 0.72, 0.67, 0.5, 0.25, 0.94, 0.72, 0.25, 0.33, 0.33,
        0.33, 0.25
    ]
    assert len(widths) == 52

    style_dict = ami_text0.extract_style_dict_from_svg()
    # assert style_dict == {'fill': 'rgb(0,0,0)',\n 'font-family': 'TimesNewRomanPSMT',\n 'font-size': '9.96px',\n 'stroke': 'none'}
    assert style_dict[FILL] == 'rgb(0,0,0)'
    assert style_dict[FONT_FAMILY] == 'TimesNewRomanPSMT'
    assert style_dict[FONT_SIZE] == '9.96px'
    assert style_dict[STROKE] == 'none'
    assert ami_text0.get_font_size() == 9.96


def test_create_text_lines_page6():
    page = AmiPage.create_page_from_SVG(PAGE_6)
    page.create_and_process_text_spans()


def test_create_html():
    """
    Test 10 pages
    """
    pretty_print = True
    use_lines = True
    for page_index in range(1,9):
        page_path = Path(CLIMATE, f"fulltext-page.{page_index}.svg")
        html_path = Path(HTML_TEMP_DIR, f"page.{page_index}.html")
        if not HTML_TEMP_DIR.exists():
            HTML_TEMP_DIR.mkdir()
        ami_page = AmiPage.create_page_from_SVG(page_path)
        ami_page.write_html(html_path, pretty_print, use_lines)

def test_create_chapters():
    pretty_print = True
    use_lines = True
    make_full_draft_html(pretty_print, use_lines)
    for page_index in range(1, 500):
        html_path = Path(FULL_TEMP_DIR, f"page.{page_index}.html")
        with open(html_path, "r") as h:
            xml = h.read()
        root = lxml.etree.fromstring(xml)
        spans = root.findall("./body/p/span")
        span0 = HtmlUtil.get_text_content(spans[0])
        print(f" {page_index}: {span0}")



# /Users/pm286/projects/readable_climate_reports/ipcc/dup/finalDraft/svg
@unittest.skip("Not yet ready; depends on line analysis")
def test_find_breaks_in_many_pages():
    """test hundreds if pages"""
    numpages = 20  # increase later
    for page_index in range(numpages):
        page_path = Path(FINAL_DRAFT_DIR,
                         f"fulltext-page.{page_index}.svg")
        page = AmiPage.create_page_from_SVG(page_path)
        page.create_and_process_text_spans()

# ==============================

def make_full_draft_html(pretty_print, use_lines):
    if not Path(FINAL_DRAFT_DIR, f"fulltext-page.2912.svg").exists():
        for page_index in range(1, 2912):
            page_path = Path(FINAL_DRAFT_DIR, f"fulltext-page.{page_index}.svg")
            html_path = Path(FULL_TEMP_DIR, f"page.{page_index}.html")
            if not FULL_TEMP_DIR.exists():
                FULL_TEMP_DIR.mkdir()
            ami_page = AmiPage.create_page_from_SVG(page_path)
            ami_page.write_html(html_path, pretty_print, use_lines)
