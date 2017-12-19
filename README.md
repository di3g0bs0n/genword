
# <a id='s1' />Index

* [Index](#s1)
* [Genword](#s2)
* [How to install?](#s4)
* [How to use Genword?](#s4)
	* [Create an empty document](#s4-1)
	* [Load an existent document](#s4-2)
* [Components](#s5)
	* [Paragraphs](#s5-1)
	* [Breaks](#s5-2)
	* [Images](#s5-3)
	* [Tables](#s5-4)
* [Known issues](#s99)


# <a id='s2' />Genword

*Genword* is a tool in order to generate Word files (.docx) dynamically from Python code. This tool is not based in HTML code which is pasted into a document. This tool build native Word entities and write an document component by component.

# <a id="s3" />How to install?

You can install _genword_ through pip:

```bash
pip install genword
```

If you can't install via pip, you also can install it manually:

```bash
pip install -r requirements.txt
python setup.py install
```

# <a id='s4' />How to use Genword?

Genword can be used to create an empty document or to load an existent document.

## <a id='s4-1' />Create an empty document

```python
from genword import Word

w = Word()
w.create('/tmp/example.docx')

# Do stuff...

w.dump()
w.zip()
```

## <a id='s4-2' />Load an existent document

If you want load an existent document, you can do it:

```python
from genword import Word

w = Word()
w.load('/tmp/example.docx')

# Do stuff...

w.dump()
w.zip()
```

# <a id='s5' />Components

You can create word components. Some components can be added into other components.

## <a id='s5-1' />Paragraphs

A paragraph item is used to store text or other component. A text item always must be inside paragraph item.

```python
from genword import Word, wParagraph

w = Word()
w.create('/tmp/example.docx')

p = wParagraph("Hello World!")
w.add(p)

p2 = wParagraph()
w.add(p2)

w.dump()
w.zip()

```

The text can be formatted with the *option* argument. The formats supported are listed below:

* align (Values allowed: _left_, _right_, _center_, _justify_)
* bold (No values required)
* smallCaps (No values required)
* color (Hex code)
* size (Point size)
* lang (ISO Code language)
* font (Font name. Example: Verdana)

```python
from genword import Word, wParagraph

w = Word()
w.create('/tmp/example.docx')

p = wParagraph("Hello World!", options={
		"font": "Verdana",
		"bold": True,
		"smallCaps": True,
		"align": "center",
		"size": 48
	})
w.add(p)

p2 = wParagraph()
w.add(p2)

w.dump()
w.zip()

```


## <a id='s5-2' />Breaks

If you can insert a breakpage, you must use the _wBreak_ element.
```python
from genword import Word, wParagraph, wBreak

w = Word()
w.create('/tmp/example.docx')

p = wParagraph("Hello World!", options={
		"font": "Verdana",
		"bold": True,
		"smallCaps": True,
		"align": "center",
		"size": 48
	})
w.add(p)

b = wBreak()
w.add(b)

p2 = wParagraph("Next page!")
w.add(p2)

w.dump()
w.zip()
```


## <a id='s5-3' />Images

```python
from genword import Word, wImage, wBreak

w = Word()
w.create('/tmp/example.docx')

#IMPORTANT! You must add the content-type
w.addContentType(ext="png", ctype="image/png")
w.addContentType(ext="jpg", ctype="image/jpeg")	

# Use this option
i = wImage("/tmp/logo.png")
w.add(i)

w.add(wBreak())

# Or this option
w.addImage("/tmp/logo.png")

w.dump()
w.zip()
```

## <a id='s5-4' />Tables

```python
from genword import Word, wTable, wParagraph, wTableRow, wTableCell

w = Word()
w.create('/tmp/example.docx')

# Create the table
t = wTable()
t.setBorders()

# Create row (headers)
r = wTableRow(columns=3)
r.setAlign("center")

hoptions = {
	"size":"28", 
	"color": "00C6DA", 
	"align":"center", 
	"smallCaps": True, 
	"bold": True
}

t1 = wParagraph("Header 1", hoptions)
t2 = wParagraph("Header 2", hoptions)
t3 = wParagraph("Header 3", hoptions)

# Create the Cells
c1 = wTableCell({"bgcolor":"2C6584"})
c2 = wTableCell({"bgcolor":"2C6584"})
c3 = wTableCell({"bgcolor":"2C6584"})

c1.setText(t1)
c2.setText(t2)
c3.setText(t3)

# Add cells to row
r.addCells([c1, c2, c3])

# Add row to table
t.addRow(r)

# You can repeat this process to add more rows...

w.add(t)

w.dump()
w.zip()
```













# <a id='s99' />Known issues

* When you load a document, some elements can be splited in several components. For example, a textline can be stored in two or more wParagraph elements. This is a problem when you trying read or iterate the wParagraphs elements.