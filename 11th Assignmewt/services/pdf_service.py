from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO


class PDFService:
    @staticmethod
    def render_pdf(resume_data: dict) -> BytesIO:
        buf = BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        width, height = A4
        y = height - 50
        c.setFont('Helvetica-Bold', 18)
        c.drawString(50, y, resume_data.get('name', ''))
        y -= 24
        c.setFont('Helvetica', 12)
        c.drawString(50, y, resume_data.get('designation', ''))
        y -= 30
        c.setFont('Helvetica-Bold', 14)
        c.drawString(50, y, 'Professional Summary')
        y -= 18
        c.setFont('Helvetica', 11)
        for bullet in resume_data.get('professional_summary', []):
            c.drawString(60, y, u'• ' + bullet)
            y -= 14
            if y < 80:
                c.showPage()
                y = height - 50
        y -= 8
        c.setFont('Helvetica-Bold', 14)
        c.drawString(50, y, 'Technical Skills')
        y -= 18
        c.setFont('Helvetica', 11)
        skills = ', '.join(resume_data.get('coding', []) + resume_data.get('tools', []))
        c.drawString(50, y, skills)
        y -= 24
        c.setFont('Helvetica-Bold', 14)
        c.drawString(50, y, 'Projects')
        y -= 18
        c.setFont('Helvetica', 11)
        for p in resume_data.get('projects', []):
            c.setFont('Helvetica-Bold', 12)
            c.drawString(50, y, p.get('name', ''))
            y -= 16
            c.setFont('Helvetica', 11)
            techs = ', '.join(p.get('technologies', []) + p.get('tools', []))
            c.drawString(60, y, techs)
            y -= 14
            for line in (p.get('description') or '').splitlines():
                c.drawString(60, y, line)
                y -= 12
                if y < 80:
                    c.showPage(); y = height - 50
            for r in p.get('role_responsibilities', []):
                c.drawString(64, y, u'• ' + r)
                y -= 12
                if y < 80:
                    c.showPage(); y = height - 50
            y -= 8
        c.save()
        buf.seek(0)
        return buf
