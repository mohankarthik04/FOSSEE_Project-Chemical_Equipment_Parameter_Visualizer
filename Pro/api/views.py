from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import EquipmentData
from .serializers import EquipmentDataSerializer

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from io import BytesIO


class UploadCSV(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES['file']
        data = EquipmentData(file=file)
        data.save()
        serializer = EquipmentDataSerializer(data)
        return Response(serializer.data)


class Summary(APIView):
    def get(self, request):
        last = EquipmentData.objects.last()
        if last and last.summary:
            return Response(last.summary)
        return Response({"message": "No CSV uploaded yet"})


def history_view(request):
    records = EquipmentData.objects.all().order_by('-uploaded_at')[:5]
    data = []
    for r in records:
        data.append({
            "id": r.id,
            "time": r.uploaded_at.strftime("%d-%m-%Y %H:%M"),
            "summary": r.summary
        })

    return JsonResponse(data, safe=False)


def generate_pdf(request):
    latest = EquipmentData.objects.order_by('-uploaded_at').first()

    if not latest or not latest.summary:
        return HttpResponse("No data available", status=400)

    s = latest.summary

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Chemical Equipment Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        f"Total: {s.get('total_count')} | "
        f"Avg. Flow: {float(s.get('avg_flowrate', 0)):.3f} m³/s | "
        f"Avg. Pressure: {float(s.get('avg_pressure', 0)):.3f} Pa | "
        f"Avg. Temp: {float(s.get('avg_temperature', 0)):.3f} °C",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 12))

    table_data = [["Equipment Type", "Count"]]
    for k, v in s.get("type_distribution", {}).items():
        table_data.append([k, v])

    table = Table(table_data)
    table.setStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ])

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


def summary_dashboard(request):
    latest = EquipmentData.objects.order_by('-uploaded_at').first()

    if not latest or not latest.summary:
        return render(request, 'no_data.html')

    summary = latest.summary
    type_distribution = summary.get("type_distribution", {})

    context = {
        "total_count": summary.get("total_count"),
        "avg_flowrate": summary.get("avg_flowrate"),
        "avg_pressure": summary.get("avg_pressure"),
        "avg_temperature": summary.get("avg_temperature"),
        "type_distribution": type_distribution,
        "types_json": json.dumps(list(type_distribution.keys())),
        "counts_json": json.dumps(list(type_distribution.values())),
    }

    return render(request, "summary.html", context)
