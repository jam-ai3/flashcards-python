import weasyprint

html = "<h1>Hello from EC2</h1><p>This is a test.</p>"
pdf = weasyprint.HTML(string=html).write_pdf()
with open("output.pdf", "wb") as f:
    f.write(pdf)

print("PDF generated as output.pdf")
