import os

from crewai import LLM, Crew
from langchain_groq import ChatGroq
from src.config.settings import get_settings
from src.logger.logger import get_logger
from src.services.service_crewai.agents import create_agents
from src.services.service_crewai.tasks import create_tasks
from src.services.service_crewai.tools import *

settings = get_settings()
logger = get_logger(__file__)


async def agenerate_report(url: str):

    llm = LLM(
        model="chatgpt-4o-latest",
        temperature=0.7,
        api_key=settings.OPENAI_API_KEY,
    )

    vision_llm = LLM(
        model="chatgpt-4o-latest", temperature=0.7, api_key=settings.OPENAI_API_KEY
    )

    # vision_llm = ChatGroq(
    #     temperature=0,
    #     groq_api_key=settings.GROQ_API_KEY,
    #     model_name=settings.VISION_MODEL,
    # )

    pagespeedinsights_tool = PageSpeedInsightsTool(url)
    jina = JinaAITool(url)

    agents = create_agents(llm, vision_llm)
    tasks = create_tasks(agents, url)

    crew = Crew(
        agents=list(agents.values()), tasks=tasks, verbose=False, async_execution=True
    )

    crew_output = crew.kickoff()
    os.makedirs("outputs", mode=0o777, exist_ok=True)
    path_prefix = r"outputs/"

    frontend_input_path = "frontend_report.md"
    frontend_output_path = path_prefix + frontend_input_path[:-3] + ".pdf"

    ui_ux_input_path = "ui_ux_report.md"
    ui_ux_output_path = path_prefix + ui_ux_input_path[:-3] + ".pdf"

    seo_input_path = "seo_report.md"
    seo_output_path = path_prefix + seo_input_path[:-3] + ".pdf"

    from_md_to_pdf(frontend_input_path, frontend_output_path)
    from_md_to_pdf(ui_ux_input_path, ui_ux_output_path)
    from_md_to_pdf(seo_input_path, seo_output_path)

    return [frontend_output_path, ui_ux_output_path, seo_output_path]
