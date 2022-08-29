from docutils.parsers.rst import Directive
from docutils import nodes
from sphinx.application import Sphinx
from docutils.parsers.rst.states import Body

def decode_die_string(die: str) -> tuple[int,int]:
    try:
        n_str, d_str= die.split("d",1)
        return int(n_str), int(d_str)
    except ValueError:
        raise ValueError("Invalid die encoding. Should be like 20d100")
    pass

def split_list(l: list, seperator: str):
    """With help from https://stackoverflow.com/a/15358005"""
    group= []
    for e in l:
        if e == seperator:
            yield group
            group= []
            pass
        else:
            group.append(e)
            pass
        pass

    yield group
    pass

def decode_content(content: list[str]) -> list[tuple[int,int,str]]:
    segment_gen= split_list(content,".. rtable_entry::")
    next(segment_gen) # Drop first entry since it is not relevant

    result= []
    for segment in segment_gen:
        segment: list[str]
        min_val= max_value= ...
        other= ""
        for line in segment:
            line= line.strip()
            if line.startswith(":min: "): min_val= int(line[6:])
            elif line.startswith(":max: "): max_val= int(line[6:])
            else: other= other+"\n"+line
            pass

        if Ellipsis in (min_val, max_val):
            raise ValueError("Missing definition for min or max in rolltable entry")
            pass

        result.append((min_val,max_val,other.strip()))
        pass

    return result
    pass

def make_row(texts: list[str]) -> nodes.row:
    row= nodes.row()
    for t in texts:
        entry= nodes.entry()
        entry += nodes.paragraph(text=t)
        row+= entry
        pass

    return row
    pass

def generate_column_lengths(data: list[list[str]]) -> list[int]:
    """This could be done in a cleverer way, but I don't care anymore"""
    lengths= [0]*max([len(row) for row in data])
    
    for row in data:
        for i, _ in enumerate(row):
            lengths[i]+= 1
            pass
        pass

    return lengths
    pass

def make_table(titles: list[str], data: list[list[str]], classes:list[str]=...) -> nodes.table:
    if classes is ...: classes= []
    table= nodes.table(classes=classes)
    
    column_lengths= generate_column_lengths(data)
    tgroup= nodes.tgroup(cols=len(column_lengths))
    for width in column_lengths:
        tgroup+= nodes.colspec(colwidth=width)
    table+=tgroup

    thead= nodes.thead()
    thead+= make_row(titles)
    tgroup+= thead

    tbody= nodes.tbody()
    for row in data:
        tbody+= make_row(row)
        pass
    tgroup+= tbody

    return table
    pass

class RollingTable(Directive):
    has_content= True
    option_spec= {
        "die": str,
        "result_titles": str,
    }

    def run(self):
        if "die" not in self.options.keys():
            self.error("rollingtable requires :die: option")
        if "result_titles" not in self.options.keys():
            self.error("rollingtable requires :result_titles: option")

        
        table= nodes.table(classes=["rollingtable"])
        tgroup= nodes.tgroup(cols=2)
        
        thead= nodes.thead()
        thead+= make_row((self.options["die"],self.options.get("result_titles","result")))
        tgroup+= thead
        
        tbody= nodes.tbody()
        self.state.nested_parse(self.content,self.content_offset,tbody)
        tgroup+= tbody


        rows_count= len(tbody)+1 # Count thead as well
        for i in range(2):
            tgroup.insert(0,nodes.colspec(colwidth=rows_count))
            pass

        table+= tgroup
        return [table]
        pass
    pass

class RollingTableEntry(Directive):
    has_content= True
    option_spec= {
        "min": int,
        "max": int
    }

    def run(self):
        if not {"min","max"}.issubset(set(self.options.keys())):
            self.error("options :min: and :max: are required for rtable_entry")
              
        
        row= nodes.row()
        
        d_entry= nodes.entry()
        d_entry+= nodes.paragraph(text=f"{self.options['min']}-{self.options['max']}")
        row+= d_entry

        res_entry= nodes.entry()
        self.state.nested_parse(self.content,self.content_offset,res_entry)
        row+= res_entry

        return [row]
        pass
    pass


def dice_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    return [
        nodes.inline(classes=["roll"],text=text)
    ], []
    pass

def setup(app: Sphinx):
    app.add_directive("rollingtable",RollingTable)
    app.add_directive("rtable_entry",RollingTableEntry)
    app.add_role("roll",dice_role)

    return {
        "version": "0.1",
        "parallel_read_safe": False,
        "parallel_write_safe": False
    }