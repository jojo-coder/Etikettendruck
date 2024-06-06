# etikettendruck.py
#
# Dieses Skript erzeugt 189 Etiketten mit fortlaufendem QR-Code auf Etikettenblättern
# von Avery Zweckform (L4731). Die Etiketten werden verwendet, um Originalschriftstücke
# mit einer fortlaufenden Nummer zu versehen. Diese Nummer (ASN=Archive Serial Number) wird
# zusätzlich zum Scan des Dokuments in paperless_ngx erfasst. Im Idealfall erfolgt diese 
# Erfassung automatisch durch paperless durch das eingebaute OCR.
#
# Es muss im Code ein Startwert (s.u.) vorgegeben werden.
#
# Unter MacOS kann dann das PDF mit Vorschau gedruckt werden. Auf dem Kyocera wird mit 104%
# Vergrößerung aus dem Vielzweckfach ein Blatt gedruckt. Wenn die Variable border auf True 
# steht, wird ein Rand um jedes Etikett gedruckt. Dies ist für die notwendige Kalibrierung
# zwischen Druck und Etikettenpapier hilfreich.
#
# Für das Modul reportlab gibt es eine hervorragende Beschreibung im Netz.
#
# (c)2024 Dr. Joachim Burbach
#----------------------------------------------------------------------------------------
import qrcode
from reportlab.lib.pagesizes import portrait, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch, mm

output_dir = "output/"

def generate_qr_code(text, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_dir + filename)

def generate_labels(start_asn, filename, draw_border=False):
    # Diese Funktion erstellt die PDF-Datei
    #---------------------------------------
    # Vorbereitung der Geometrie:
    c = canvas.Canvas(output_dir+filename, pagesize=portrait(A4))
    label_width = 1*inch  # Breite eines Labels in inch (Avery L4731)
    label_height = 10*mm  # Höhe eines labels in mm (Avery L4731)
    margin_x = 0.379*inch # Abstand vom Papierrand (x)
    margin_y = 0.579*inch # Abstand vom Papierrand (y)
    delta_x = 0.1*inch # horizontaler Abstand zwischen den Klebeetiketten
    delty_y = 0.0*inch # vertikaler Abstand zwischen den Klebeetiketten
    text_xpos = 10*mm # x-Position des Klartextes (ASNnnnnn) auf dem Etikett
    text_ypos = 4*mm # y-Position des Klartextes (ASNnnnnn) auf dem Etikett
    qr_code_xpos = 0*mm # x-Position des QR-Codes auf dem Etikett
    qr_code_ypos = 0*mm # y-Position des QR-Codes auf dem Etikett

    asn = start_asn
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.black)

    # Erstellung der 189 fortlaufenden ASN Nummern
    #---------------------------------------------
    for j in range (27):
        for i in range(7):
            text = f"ASN{asn}"
            qr_code_filename = f"qr_code_{text}.png"
            generate_qr_code(text, qr_code_filename)
            c.drawImage(output_dir+qr_code_filename, 
                        margin_x+qr_code_xpos+i*(label_width+delta_x), 
                        margin_y+qr_code_ypos+j*(label_height+delty_y), 
                        width=10*mm, 
                        height=10*mm)
            c.drawString(margin_x+text_xpos+i*(label_width+delta_x), 
                         margin_y+text_ypos+j*(label_height+delty_y), 
                         text)

            if draw_border: # Bei Bedarf einen Rahmen zeichnen
                c.rect(margin_x+i*(label_width+delta_x), 
                        margin_y+j*(label_height+delty_y), 
                        label_width, 
                        label_height)

            asn += 1

    c.save() # Speichern der PDF-Datei

if __name__ == "__main__":
    start = 10000 # <--- Startnummer der Etiketten
    filename = "qr_codes_labels"

    generate_labels(start, f"{filename}.pdf", draw_border=False)