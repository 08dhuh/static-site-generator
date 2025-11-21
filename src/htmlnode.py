
def tag_text_wrapper(tag_getter,prop_getter):
    def decorator(func):
        def inner(self, *args,**kwargs):
            tag = tag_getter(self)
            prop = prop_getter(self)
            result = func(self,*args,**kwargs)
            if tag is None: 
                return result
            if prop is None:
                props = ''
            else:
                props = ' '+' '.join([f'{k}="{v}"' for k,v in prop.items()])
            return f'<{tag}{props}>{result}</{tag}>'
        return inner
    return decorator

class HTMLNode:
    def __init__(self, 
                 tag=None, 
                 value=None, 
                 children=None, 
                 props:dict|None=None):
        self._tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    @property
    def tag(self):
        return self._tag
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        html = ""
        if self.props is not None:
            for k, v in self.props.items():
                html += f' {k}="{v}"'
        return html
    
    def __eq__(self, hn):
        return self.tag == hn.tag and self.children == hn.children\
            and self.value == hn.value and self.props == hn.props
    
    def __repr__(self):
        return f"""
    HTMLNode object tag:{self.tag},
    value:{self.value},
    children:{self.children},
    props:{self.props}
    """
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag=tag, value=value, props=props)
    
    @tag_text_wrapper(lambda n: n.tag, lambda n:n.props)
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        return self.value
          
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children:list[HTMLNode], props = None):
        super().__init__(tag=tag, children=children, props=props)      
    
    @tag_text_wrapper(lambda n: n.tag, lambda n:n.props)
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent nodes must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Children is missing from this parent node")
        child_string = ""
        for child in self.children:
            child_string += child.to_html()
        return child_string  
    
    
