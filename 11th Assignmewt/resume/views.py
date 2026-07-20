from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from services.resume_service import ResumeService
from services.pdf_service import PDFService
from services.word_service import WordService


@login_required
def download_pdf(request, employee_id):
    data = ResumeService.get_employee_resume(employee_id)
    buf = PDFService.render_pdf(data)
    resp = HttpResponse(buf, content_type='application/pdf')
    resp['Content-Disposition'] = f'attachment; filename="{data.get("name","resume")}.pdf"'
    return resp


@login_required
def download_docx(request, employee_id):
    data = ResumeService.get_employee_resume(employee_id)
    buf = WordService.render_docx(data)
    resp = HttpResponse(buf.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    resp['Content-Disposition'] = f'attachment; filename="{data.get("name","resume")}.docx"'
    return resp
