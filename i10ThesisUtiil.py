import sublime, sublime_plugin
import re

# paste margin note at the beginning of the paragraph
class AddMarginNoteFromClipboardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# get the beginning of the paragraph
		cursorPoint = self.view.sel()[0].begin()
		paragraphBegin = self.view.find_by_class(cursorPoint, False, sublime.CLASS_EMPTY_LINE)

		# create margin note text
		textClipboard = sublime.get_clipboard()
		marginNote = "\n\\mnote{%s}%%" % ThesisUtil.pagesToTex(textClipboard)

		# insert text
		self.view.insert(edit, paragraphBegin, marginNote)


# create a figure placeholder with the current label at the end of the current paragraph
class AddFigureFromLabelCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# get the figure label
		cursorPoint = self.view.sel()[0].begin()
		labelRegion = self.view.expand_by_class(cursorPoint, sublime.CLASS_WORD_START | sublime.CLASS_WORD_END)
		labelText = self.view.substr(labelRegion)

		# crate a command for figure insertion
		figureCommand = "%%\n\
\myFigureN[%s]{placeholder}%%\n\
{longcaption}%%\n\
{shortcaption}" % labelText

		# find the end of the paragraph
		insertPoint = self.view.find_by_class(cursorPoint, True, sublime.CLASS_EMPTY_LINE)

		# insert the figure command
		self.view.insert(edit, insertPoint, figureCommand)

		# got to the figure caption
		captionRegion = self.view.find("longcaption", insertPoint, sublime.LITERAL)
		self.view.sel().clear()
		self.view.sel().add(captionRegion)



# create index term from the selected text at the beginning of the current paragraph
class IndexFromSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# get selected term
		termRegion = self.view.sel()[0]
		termText = self.view.substr(termRegion)

		# wrap term
		termTextWrapped = "\n\index{%s}%%" % termText

		# find the beginning of the paragraph
		paragraphRegion = self.view.find_by_class(termRegion.begin(), False, sublime.CLASS_EMPTY_LINE)
		posInsert = paragraphRegion

		# insert the index
		self.view.insert(edit, posInsert, termTextWrapped)

		# move the cursor to the index
		cursorPos = posInsert + len(termTextWrapped) - 2
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(cursorPos))
		

# paste and reformat text from Apple Pages 5
class PasteFromPagesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		textClipboard = sublime.get_clipboard()

		# replace common characters
		textQuoted = ThesisUtil.pagesToTex(textClipboard)

		# split line at the end of the sentence
		splitLines = [chunk.strip() for chunk in textQuoted.split(". ")]
		textSplitted = ". \n".join(splitLines)

		# add citation
		textCited = textSplitted.replace("{", "\\fullcite{")

		# figure labeling
		textFigured = textCited.replace("Fig #", "Fig.\\ \\myImgRef{fig_}")

		# insert the text
		finalText = textFigured
		self.view.insert(edit, self.view.sel()[0].begin(), finalText)

class ThesisUtil:
	@staticmethod
	def pagesToTex(pagesText):
		retVal = pagesText.replace("“", "``") \
							.replace("”", "''") \
							.replace("’", "'") \
							.replace("%", "\\%") \
							.replace("<", "\\textless") \
							.replace(">", "\\textgreater") \
							.replace("–", "--") \
							.replace("—", "---") \

		return retVal