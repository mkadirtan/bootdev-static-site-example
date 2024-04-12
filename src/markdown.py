import re
from textnode import text_to_textnodes, text_node_to_html_node
from htmlnode import ParentNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks[:] = map(lambda x: x.strip(), blocks)
    blocks[:] = filter(lambda x: x != "", blocks)
    return blocks


def block_to_block_type(block):
    heading_pattern = r"^#{1,6}\s"
    heading_start = re.findall(heading_pattern, block)
    if len(heading_start) != 0 and block.lstrip(heading_start[0]) != "":
        return block_type_heading

    if block.startswith("```") and block.endswith("```"):
        return block_type_code

    lines = block.split("\n")

    is_quoted = True
    is_unordered_list = True
    is_ordered_list = True
    order = 1

    for line in lines:
        if not line.startswith(">"):
            is_quoted = False
        if not (line.startswith("*") or line.startswith("-")):
            is_unordered_list = False
        if not (line.startswith(f"{order}.")):
            is_ordered_list = False
        order += 1

    if is_quoted:
        return block_type_quote
    if is_unordered_list:
        return block_type_ulist
    if is_ordered_list:
        return block_type_olist

    return block_type_paragraph


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    heading_pattern = r"^#{1,6}\s"
    heading_start = re.findall(heading_pattern, block)[0]
    heading_level = heading_start.count("#")
    remainder = block.split(heading_start, maxsplit=1)[1]
    children = text_to_children(remainder)
    return ParentNode(f"h{heading_level}", children)


def quote_to_html_node(block):
    lines = block.split("\n")
    text = " ".join(map(lambda x: x.lstrip(">").strip(), lines))
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def ulist_to_html_node(block):
    lines = block.split("\n")
    ulist = []
    for line in lines:
        children = text_to_children(line[2:])
        ulist.append(ParentNode("li", children))
    return ParentNode("ul", ulist)


def olist_to_html_node(block):
    lines = block.split("\n")
    olist = []
    for line in lines:
        children = text_to_children(line[3:])
        olist.append(ParentNode("li", children))
    return ParentNode("ol", olist)


def code_to_html_node(block):
    text = block.lstrip("```").rstrip("```")
    children = text_to_children(text)
    return ParentNode("pre", [
        ParentNode("code", children)
    ])


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_html_node(block, block_type)
        html_nodes.append(node)
    return ParentNode("div", html_nodes)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def block_to_html_node(block, block_type):
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise Exception("Unknown block type")


def extract_title(markdown):
    lines = markdown.split("\n")
    for i in range(0, len(lines)):
        if lines[i].startswith("# "):
            return lines[i][2:]
