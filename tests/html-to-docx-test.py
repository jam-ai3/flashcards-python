



from utils.docx.html2docx import html_to_docx


html = "<h1 style=\"text-align: center\">LinkedIn Video 1</h1><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><p><strong><em><s><u>Let me know if you want a fully copy-pasteable script, or if you want to handle other tags as well!</u></s></em></strong></p><h5><a target=\"_blank\" rel=\"noopener noreferrer nofollow\" href=\"http://localhost:3001/document/8ded61e2-2094-493a-ba40-c9c700be3a28\">The link section</a></h5><pre><code>Code Section</code></pre><p><s>This is the strike text</s></p><p><u>This is the underline</u></p><p><strong>This is Bold</strong></p><p><mark data-color=\"var(--tt-highlight-yellow)\" style=\"background-color: var(--tt-highlight-yellow); color: inherit\">This is highlighted yellow</mark></p><p><mark data-color=\"var(--tt-highlight-green)\" style=\"background-color: var(--tt-highlight-green); color: inherit\">Green</mark></p><p><mark data-color=\"var(--tt-highlight-blue)\" style=\"background-color: var(--tt-highlight-blue); color: inherit\">Blue</mark></p><p><mark data-color=\"var(--tt-highlight-red)\" style=\"background-color: var(--tt-highlight-red); color: inherit\">Pink</mark></p><p><mark data-color=\"var(--tt-highlight-purple)\" style=\"background-color: var(--tt-highlight-purple); color: inherit\">Purple</mark></p><blockquote><p>Blockquote</p></blockquote><ul><li><p>Bullet List 1</p></li><li><p>Bullet List 2</p></li></ul><ol><li><p>OrderedList 1</p></li><li><p>OrderedList 2</p></li></ol><ul data-type=\"taskList\"><li data-checked=\"true\" data-type=\"taskItem\"><label><input type=\"checkbox\" checked=\"checked\"><span></span></label><div><p>Checkbox 1</p></div></li><li data-checked=\"false\" data-type=\"taskItem\"><label><input type=\"checkbox\"><span></span></label><div><p>Checkbox 2</p></div></li></ul><p><sup>SuperScript</sup></p><p><sub>SubScript</sub></p><p></p><p style=\"text-align: justify\">AlignJustify</p><p style=\"text-align: left\">AlignLeft</p><p style=\"text-align: center\">AlignCenter</p><p style=\"text-align: right\">AlignRight</p>",
# Convert HTML to a BytesIO object containing the .docx data
buffer = html_to_docx(html)

# Write the BytesIO content to a .docx file
with open("output.docx", "wb") as f:
    f.write(buffer.getvalue())
