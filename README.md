
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


# <a id='s2' />Genword

*Genword* is a tool in order to generate Word files (.docx) dynamically from Python code. This tool is not based in HTML code which is pasted into a document. This tool build native Word entities and write an document component by component.

# <a id="s3" />How to install?

You can install _genword_ through pip:

```bash
pip install genword
```

If you can't install via pip, you also can install it manually:

```bash
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
