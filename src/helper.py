import os
import re
from textnode import TextType, TextNode, BlockType
from htmlnode import ParentNode, LeafNode, HTMLNode

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_list = os.listdir(dir_path_content)
    for f in dir_list:
        current_f = os.path.join(dir_path_content, f)
        if os.path.isfile(current_f) and current_f.endswith('.md'):
            fname = f.split('.')[0]+'.html'
            dest_f = os.path.join(dest_dir_path, fname)
            generate_page(current_f, template_path, dest_f, basepath)
        else:
            dest_f = os.path.join(dest_dir_path, f)
            generate_pages_recursive(current_f, template_path, dest_f,basepath)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path,'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    dest_dir = dest_path.split('/')
    if len(dest_dir) > 1:
        path = ""
        for d in dest_dir[:-1]:
            path = os.path.join(path, d)
            if not os.path.exists(path):
                os.mkdir(path)
    with open(dest_path, 'w') as f:
        f.write(template)

def extract_title(markdown:str):
    markdown = markdown.strip()
    if '# ' not in markdown:
        raise ValueError("No h1 header found")
    return markdown.split('# ', 1)[1].split('\n',1)[0]

def markdown_to_html_node(markdown:str)->ParentNode:
    children = []
    blocks = markdown_to_blocks(markdown=markdown)
    for block in blocks:
        block_type = block_to_block_type(block=block)
        children.append(block_to_html_nodes(block=block, block_type=block_type))
    return ParentNode(tag='div',children=children)

def block_to_html_nodes(block:str, block_type:BlockType)->HTMLNode:
    match block_type:
        case BlockType.HEADING:
            return heading_block_to_html(block)
        case BlockType.CODE:
            return code_block_to_html(block)
        case BlockType.QUOTE:
            return quote_block_to_html(block)
        case BlockType.UNORDERED_LIST:
            return ul_to_html(block)
        case BlockType.ORDERED_LIST:
            return ol_to_html(block)
        case BlockType.PARAGRAPH:
            return p_to_html(block)
        case _:
            raise Exception("unrecognised Block type")

def heading_block_to_html(heading:str) -> ParentNode:
    num_hash = heading.count('#')
    tag = f'h{num_hash}'
    heading_text = heading.split('#'*num_hash+' ')[1]
    children = raw_text_to_children(heading_text)
    return ParentNode(tag=tag, children=children)

def code_block_to_html(code_block:str) -> LeafNode:
    code_text = code_block.split('```')[1][1:]
    code_node = text_node_to_html_node(TextNode(text=code_text,
                                               type=TextType.CODE))
    return ParentNode(tag='pre',children=[code_node])

def quote_block_to_html(quote_block:str) -> ParentNode:
    lines = quote_block.split('\n')
    raw_lines = ' '.join([line[2:] for line in lines])
    children = raw_text_to_children(raw_lines)
    return ParentNode(tag='blockquote', children=children)

def ul_to_html(ul_block:str) -> ParentNode:
    tag = 'ul'
    lines = ul_block.split('\n')
    ul_children = []
    for line in lines:
        li_children = raw_text_to_children(line[2:])
        ul_children.append(ParentNode(tag='li', children=li_children))
    return ParentNode(tag=tag, children=ul_children)

def ol_to_html(ol_block:str) -> ParentNode:
    tag = 'ol'
    lines = ol_block.split('\n')
    ol_children = []
    for line in lines:
        li_children = raw_text_to_children(line[3:])
        ol_children.append(ParentNode(tag='li', children=li_children))
    return ParentNode(tag=tag, children=ol_children)

def p_to_html(p_block:str) -> ParentNode:
    tag = 'p'
    
    children = raw_text_to_children(' '.join(p_block.split('\n')))
    return ParentNode(tag=tag, children=children)

def raw_text_to_children(text:str)->list[LeafNode]:
    children_tnodes = text_to_textnodes(text=text)
    return text_nodes_to_children(children_tnodes)

def text_nodes_to_children(text_nodes:list[TextNode]) -> list[LeafNode]:
    html_nodes = []
    for tn in text_nodes:
        html_nodes.append(text_node_to_html_node(tn))
    return html_nodes

def text_node_to_html_node(text_node:TextNode):
    match (text_node.text_type):
        case TextType.PLAIN:
            return LeafNode(tag=None,value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a",value=text_node.text,props={"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={
                "src": text_node.url,
                "alt":text_node.text
            })
        case _:
            raise Exception("Unrecognised type")
        
def block_to_block_type(block:str):
    heading_pattern = re.compile(r'^#{1,6} ')
    if heading_pattern.match(block):
        return BlockType.HEADING
    if block[:3] == '```' and block[-3:] == '```':
        return BlockType.CODE
    lines = block.split('\n')
    isquote = all(t.startswith('>') for t in lines)
    if isquote:
        return BlockType.QUOTE
    isul = all(t.startswith('- ') for t in lines )
    if isul:
        return BlockType.UNORDERED_LIST
    isol = True
    n = 1
    for t in lines:
        if not t.startswith(f'{n}. '):
            isol = False
            break
        n += 1
    if isol:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH



def split_nodes_delimiter(old_nodes:list[TextNode], 
                          delimiter, 
                          text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        split_texts = node.text.split(delimiter)
        if len(split_texts) % 2 == 0:
            raise Exception("No closing delimiter found - invalid markdown syntax")
        for i, st in enumerate(split_texts):
            if i%2 == 0:
                new_nodes.append(TextNode(text=st,
                                          type=TextType.PLAIN))
            else:
                new_nodes.append(TextNode(text=st,
                                          type=text_type))
    return new_nodes                        

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes:list[TextNode]):
    return_nodes = []
    for node in old_nodes:
        image_pairs = extract_markdown_images(node.text)
        if len(image_pairs) == 0:
            return_nodes.append(node)
            continue
        nodes = []
        text = node.text
        for alt, link in image_pairs:
            sections = text.split(f"![{alt}]({link})",1)
            if len(sections[0]) > 0:
                nodes.append(TextNode(sections[0],type=TextType.PLAIN))
            nodes.append(TextNode(text=alt,
                                  type=TextType.IMAGE,
                                  url=link))
            text = sections[1]
        if len(text) > 0:
            nodes.append(TextNode(text,type=TextType.PLAIN))
        return_nodes.extend(nodes)   
    return return_nodes 

def split_nodes_link(old_nodes:list[TextNode]):
    return_nodes = []
    for node in old_nodes:
        link_pairs = extract_markdown_links(node.text)
        if len(link_pairs) == 0:
            return_nodes.append(node)
            continue
        nodes = []
        text = node.text
        for alt, link in link_pairs:
            sections = text.split(f"[{alt}]({link})",1)
            if len(sections[0]) > 0:
                nodes.append(TextNode(sections[0],type=TextType.PLAIN))
            nodes.append(TextNode(text=alt,
                                  type=TextType.LINK,
                                  url=link))
            text = sections[1]
        if len(text) > 0:
            nodes.append(TextNode(text,type=TextType.PLAIN))
        return_nodes.extend(nodes)   
    return return_nodes

def text_to_textnodes(text)->list[TextNode]:
    initial_node = TextNode(text=text,
                            type=TextType.PLAIN)
    nodes= [initial_node]
    nodes = split_nodes_delimiter(nodes, "**", text_type=TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", text_type=TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", text_type=TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    
def markdown_to_blocks(markdown:str) -> list[str]:
    texts = markdown.split('\n\n')
    stripped = [t.strip() for t in texts]
    return list(filter(lambda t: len(t)> 0, stripped))