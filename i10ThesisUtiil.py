import sublime, sublime_plugin
import re


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
		textQuoted = textClipboard.replace("“", "``") \
						.replace("”", "''") \
						.replace("’", "'") \
						.replace("%", "\\%") \
						.replace("<", "\\textless") \
						.replace(">", "\\textgreater") \
						.replace("–", "--") \
						.replace("—", "---") \

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
		