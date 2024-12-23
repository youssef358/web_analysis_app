from typing import List

from crewai import Task
from src.services.service_crewai.agents import *


def create_tasks(agents: Dict[str, Agent], url: str) -> List[Task]:

    frontend_analysis_task = Task(
        description=(
            f"Perform an in-depth technical analysis of the HTML, CSS, and JavaScript code of the {url} webpage. "
            "Focus on identifying bugs, invalid HTML, missing semantic elements, outdated implementations, and performance bottlenecks. "
            "Tools: PageSpeed Insights (Accessibility, Best Practices, Performance), Jina AI HTML Analysis."
        ),
        expected_output=(
            "A brief technical summary of critical front-end issues: 1) Structural HTML errors, 2) CSS/JavaScript inefficiencies, "
            "3) Non-compliance with modern standards. Include key recommendations for improvement."
        ),
        tools=[
            get_page_speed_insights_accessibility,
            get_page_speed_insights_best_practices,
            get_page_speed_insights_performance,
            get_jina_ai_html,
        ],
        agent=agents["frontend_specialist_Agent"],
        async_execution=True,
    )

    frontend_report_task = Task(
        description=(
            f"Summarize the front-end analysis findings for {url}. Provide key issues, technical explanations, and a brief action plan. "
            "Tools: Analysis context from Frontend Specialist Agent."
        ),
        expected_output=(
            "Structured report: 1) Executive Summary, 2) Key Technical Issues, 3) Prioritized Action Plan. Keep details concise."
        ),
        agent=agents["frontend_report_analyst_Agent"],
        context=[frontend_analysis_task],
        output_file="frontend_report.md",
    )

    image_analysis_task = Task(
        description=(
            f"Analyze the visual design of the image assets on the {url} webpage. "
            "Identify design inconsistencies and accessibility issues. "
            "Tools: Jina AI Screenshot Analysis."
        ),
        expected_output=(
            "Brief report on: 1) Design flaws, 2) Accessibility issues, 3) Key improvement suggestions."
        ),
        tools=[get_jina_ai_screenshot],
        agent=agents["image_analysis_Agent"],
        async_execution=True,
    )

    ui_ux_analysis_task = Task(
        description=(
            f"Evaluate the design, usability, accessibility, and responsiveness of the {url} webpage. "
            "Focus on WCAG standards, media queries, and interactive components. "
            "Tools: PageSpeed Insights (Accessibility, Performance), Jina AI Text Analysis."
        ),
        expected_output=(
            "Brief technical summary: 1) Accessibility gaps, 2) Usability issues, 3) Non-responsive elements. Provide key recommendations."
        ),
        tools=[
            get_page_speed_insights_accessibility,
            get_page_speed_insights_performance,
            get_jina_ai_text,
        ],
        agent=agents["ui_ux_specialist_Agent"],
        async_execution=True,
    )

    ui_ux_report_task = Task(
        description=(
            f"Summarize the UI/UX analysis for {url}. Provide key findings and prioritized recommendations. "
            "Tools: Analysis context from UI/UX Specialist Agent and Image Analysis Agent."
        ),
        expected_output=(
            "Structured report: 1) Summary of issues, 2) Key Technical Explanations, 3) Prioritized Action Plan."
        ),
        context=[ui_ux_analysis_task, image_analysis_task],
        agent=agents["ui_ux_report_analyst_Agent"],
        output_file="ui_ux_report.md",
    )

    seo_analysis_task = Task(
        description=(
            f"Perform a technical SEO audit of the {url} webpage. "
            "Focus on Core Web Vitals, structured data, indexing, and metadata optimization. "
            "Tools: PageSpeed Insights (SEO, Performance), Jina AI Text Analysis."
        ),
        expected_output=(
            "Brief SEO summary: 1) Crawlability issues, 2) Metadata inefficiencies, 3) Structured data errors. Provide key recommendations."
        ),
        tools=[
            get_page_speed_insights_seo,
            get_page_speed_insights_performance,
            get_jina_ai_text,
        ],
        agent=agents["seo_specialist_Agent"],
        async_execution=True,
    )

    seo_report_task = Task(
        description=(
            f"Compile a concise SEO report summarizing findings for {url}. Include key recommendations for improvements. "
            "Tools: Analysis context from SEO Specialist Agent and Image Analysis Agent."
        ),
        expected_output=(
            "Structured report: 1) Summary of issues, 2) Key Technical Explanations, 3) Prioritized Action Plan."
        ),
        context=[seo_analysis_task, image_analysis_task],
        agent=agents["seo_report_analyst_Agent"],
        output_file="seo_report.md",
    )

    return [
        frontend_analysis_task,
        frontend_report_task,
        image_analysis_task,
        ui_ux_analysis_task,
        ui_ux_report_task,
        seo_analysis_task,
        seo_report_task,
    ]
