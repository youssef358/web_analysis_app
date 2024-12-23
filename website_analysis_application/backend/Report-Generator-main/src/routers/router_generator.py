import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from src.config.settings import get_settings
from src.logger.logger import get_logger
from src.schemas.schema_generator import GenerateReportRequest
from src.services.service_generator import agenerate_report

settings = get_settings()
logger = get_logger(__file__)

router = APIRouter(prefix="/generator")


@router.post(path="/generate-reports")
async def generate_reports(generate_report_request: GenerateReportRequest):
    try:
        url = generate_report_request.url
        report_pdf_file_paths = await agenerate_report(url)

        if not report_pdf_file_paths or len(report_pdf_file_paths) < 3:
            logger.error("Report generation failed, insufficient paths returned.")
            raise HTTPException(status_code=500, detail="Failed to generate reports")

        frontend_report_path = report_pdf_file_paths[0]
        ui_ux_report_path = report_pdf_file_paths[1]
        seo_report_path = report_pdf_file_paths[2]

        if not os.path.exists(frontend_report_path):
            logger.error(f"Frontend Report PDF not found: {frontend_report_path}")
            raise HTTPException(status_code=404, detail="Frontend report not found")

        if not os.path.exists(ui_ux_report_path):
            logger.error(f"UI/UX Report PDF not found: {ui_ux_report_path}")
            raise HTTPException(status_code=404, detail="UI/UX report not found")

        if not os.path.exists(seo_report_path):
            logger.error(f"SEO Report PDF not found: {seo_report_path}")
            raise HTTPException(status_code=404, detail="SEO report not found")

        return {
            "frontend_report_url": f"/generator/download-report?type=frontend",
            "ui_ux_report_url": f"/generator/download-report?type=ui_ux",
            "seo_report_url": f"/generator/download-report?type=seo",
        }
    except Exception as e:
        logger.error(f"Critical Error occurred in generate_reports: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while generating the reports"
        )


@router.get(path="/download-report")
async def download_report(type: str):
    try:
        if type == "frontend":
            report_pdf_file_path = "outputs/frontend_report.pdf"
            filename = "frontend_report.pdf"
        elif type == "ui_ux":
            report_pdf_file_path = "outputs/ui_ux_report.pdf"
            filename = "ui_ux_report.pdf"
        elif type == "seo":
            report_pdf_file_path = "outputs/seo_report.pdf"
            filename = "seo_report.pdf"
        else:
            raise HTTPException(status_code=400, detail="Invalid report type")

        if not os.path.exists(report_pdf_file_path):
            logger.error(f"Report PDF file not found: {report_pdf_file_path}")
            raise HTTPException(
                status_code=404, detail=f"Report not found: {report_pdf_file_path}"
            )

        return FileResponse(
            report_pdf_file_path,
            media_type="application/pdf",
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        logger.error(f"Critical Error occurred in download_report: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while downloading the report"
        )
