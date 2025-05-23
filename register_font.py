from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Register custom font
pdfmetrics.registerFont(TTFont('CustomFont', '/path/to/your/font.ttf'))

# Use the custom font in your PDF
c = canvas.Canvas("example.pdf")
c.setFont('CustomFont', 12)
c.drawString(100, 750, "Hello, custom font!")
c.save()
