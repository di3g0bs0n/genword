
# <a id='s1' />Index

* [Index](#s1)
* [Genword](#s2)
* [How to install?](#s4)
* [How to use Genword?](#s4)
	* [Create an empty document](s4-1)


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
from genword.word import Word

w = Word()
w.create('/tmp/example.docx')
w.dump()
w.zip()
```