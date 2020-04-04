class Tag:
    def __init__(self, tag, klass = None, is_single = False, indn = "", **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []
        self.indn = indn
        if klass is not None:
            self.attributes["class"] = " ".join(klass)
        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    #сборщик строк с добавкой тегов и childs
    def AddTag(self): 
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append(' {} = "{}"'.format(attribute, value))
        attrs = "".join(attrs)
        if self.children:
            opening = "{}<{}{}>\n".format(self.indn, self.tag, attrs)
            internal = "{}".format(self.text)
            for child in self.children:
                internal += child.text
            ending = "{}</{}>\n".format(self.indn, self.tag)
            return opening + internal + ending
        else:
            if self.is_single:
                return "{}<{}{}/>\n".format(self.indn, self.tag, attrs)
            else:
                return "{indn}<{tag}{attrs}>{text}</{tag}>\n".format(tag=self.tag, attrs=attrs, text=self.text, indn=self.indn)
    
    def __enter__(self):
        self.indn += "    "
        return self

    def __exit__(self, type, value, traceback):
        self.text = self.AddTag()

    def __add__(self, other):
        other.indn = self.indn + "    "
        self.children.append(other)
        return self
    
    def __iadd__(self, other):
        other.indn = self.indn + "    "
        self.children.append(other)
        return self

#для вывода на экран или в файл
def outputter1(outputtype = None):
    if outputtype:
        def outputter2(string):
            with open (outputtype, "w") as x:
                x.write(string)
                print("file " + outputtype + " is created")
        return outputter2
    else:
        def outputter2(string):
            print(string)
        return outputter2

#нужен по заданию, отличается от Tag отсутствием поддержки не закрывающихся тегов
class TopLevelTag(Tag):
    def AddTag(self): 
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append(' {} = "{}"'.format(attribute, value))
        attrs = "".join(attrs)
        if self.children:
            opening = "{}<{}{}>\n".format(self.indn, self.tag, attrs)
            internal = "{}".format(self.text)
            for child in self.children:
                internal += child.text
            ending = "{}</{}>\n".format(self.indn, self.tag)
            return opening + internal + ending
        else:
            return "{indn}<{tag}{attrs}>\n{text}</{tag}>".format(tag=self.tag, attrs=attrs, text=self.text, indn=self.indn)

#Определяет тип вывода (файл или экран) и добавляет свои скобки
class HTML(Tag):
    def __init__(self, output = None):
        self.indn = ""
        self.text = ""
        self.children = []
        self.output = outputter1(output)
    
    def __enter__(self):
        return self
    
    def AddTag(self):  
        if self.children:
            for child in self.children:
                self.text += child.text
        return ("<html>\n{}</html>").format(self.text)
    
    def __exit__(self, type, value, traceback):
        self.text = self.AddTag()
        self.output(self.text)

if __name__ == "__main__":
    #output = None - вывод на экран. Вместо None можно указать имя файла
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                body += div
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph
                    with Tag("div") as div2:
                        div += div2
                        with Tag("h2") as h2:
                            div2 += h2
                            with Tag("h1") as h3:
                                h2 += h3
                                h3.text = "Заголовок"

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img
            doc += body