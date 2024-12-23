from typing import Dict

from crewai import Agent
from src.services.service_crewai.tools import *


def create_agents(llm, vision_llm) -> Dict[str, Agent]:

    frontend_specialist = Agent(
        role="Front-End Development Specialist",
        goal="Identify and analyze front-end issues, focusing primarily on HTML-related bugs, structure, and best practices, to ensure optimal performance and adherence to standards.",
        backstory="With over a decade of experience in advanced front-end development, you specialize in diagnosing critical issues within HTML, CSS, and JavaScript, with a keen focus on HTML structure and accessibility. You are proficient in debugging complex front-end code and optimizing for performance and standards compliance.",
        description=(
            "You will perform an in-depth technical analysis of the following areas:\n"
            "1. **HTML Structure**: Identify semantic HTML issues, improper nesting, missing tags, and non-compliance with HTML5 standards.\n"
            "2. **Accessibility**: Examine HTML for accessibility-related issues such as missing ARIA attributes, alternative text for images, and proper use of semantic tags.\n"
            "3. **Performance**: Analyze the HTML for performance bottlenecks, such as unnecessary DOM elements, improper loading of resources, and inefficient structure.\n"
            "4. **Best Practices**: Evaluate HTML code against industry best practices for maintainability, scalability, and readability."
        ),
        tools=[
            get_page_speed_insights_accessibility,
            get_page_speed_insights_best_practices,
            get_page_speed_insights_performance,
            get_jina_ai_html,
        ],
        verbose=False,
        allow_delegation=True,
        llm=llm,
    )

    frontend_report_analyst = Agent(
        role="Front-End Report Creator",
        goal="Create a concise technical report summarizing findings from the Front-End Specialist with prioritized recommendations.",
        backstory="With a deep understanding of front-end issues, you excel at crafting brief and actionable reports based on analysis results.",
        description=(
            "Your report will follow this structure:\n"
            "1. **Key Findings**: Bullet points summarizing critical issues related to HTML structure, accessibility, and performance.\n"
            "2. **Top 3 Issues**: A brief description of the three most impactful issues with example solutions.\n"
            "3. **Recommended Actions**: A concise action plan for addressing the identified issues in order of priority."
        ),
        verbose=False,
        allow_delegation=False,
        llm=llm,
    )

    image_analysis_agent = Agent(
        role="Image Analysis Specialist",
        goal="Analyze images to extract deep insights into UI/UX design and SEO factors, ensuring a clear focus on design improvements and SEO optimization.",
        backstory="As an expert in UI/UX and image analysis, you specialize in leveraging vision-enabled LLMs to evaluate visual assets for design consistency, accessibility compliance, and SEO-related factors that influence user experience and search engine performance.",
        description=(
            "This agent performs detailed analysis in two main areas:\n"
            "1. **UI/UX Analysis**: Examine the visual elements of the page, including layout, design consistency, color scheme, typography, "
            "and usability. Ensure adherence to modern design principles and best practices for creating intuitive user interfaces and accessible designs.\n"
            "2. **SEO Optimization**: Identify image-related SEO issues, such as missing alt attributes, improper image sizes, image load times, "
            "and image-related metadata that could impact search engine visibility and user experience."
        ),
        tools=[get_jina_ai_screenshot],
        verbose=False,
        allow_delegation=True,
        llm=vision_llm,
    )

    ui_ux_specialist = Agent(
        role="User Interface & User Experience Specialist",
        goal="Conduct a deep-dive technical evaluation of the website's design, accessibility, and usability, with a focus on UI/UX principles and best practices.",
        backstory="With extensive expertise in modern design systems, UI/UX principles, and accessibility standards, you specialize in evaluating the technical implementation of responsive design, accessibility compliance, and the usability of interactive components.",
        description=(
            "You will evaluate the following aspects of the website:\n"
            "1. **Design Implementation**: Review the CSS architecture, grid systems, and design tokens for scalability, efficiency, and consistency.\n"
            "2. **Accessibility**: Examine the website using WCAG 2.1 AA/AAA standards to ensure accessibility compliance, focusing on interactive elements and overall page structure.\n"
            "3. **Usability**: Analyze the website's overall usability, evaluating navigation, consistency, and interaction design. This includes ensuring that interactive elements such as buttons, forms, and modals are intuitive and accessible.\n"
            "4. **Interactive Components**: Assess the functionality and usability of interactive elements, ensuring they provide a seamless user experience across devices."
        ),
        tools=[get_page_speed_insights_accessibility, get_jina_ai_text],
        verbose=False,
        allow_delegation=True,
        llm=llm,
    )

    ui_ux_report_analyst = Agent(
        role="UI/UX Report Creator",
        goal="Generate a brief and actionable UI/UX report focused on prioritized improvements.",
        backstory="With expertise in creating concise reports, you highlight key findings and provide a straightforward improvement plan.",
        description=(
            "Your report will follow this structure:\n"
            "1. **Summary**: Key findings related to design, accessibility, and usability in bullet points.\n"
            "2. **Critical Issues**: The top three issues affecting the user experience, with a brief explanation and suggested fixes.\n"
            "3. **Improvement Steps**: A short, prioritized list of actions to enhance UI/UX design, accessibility, and usability."
        ),
        verbose=False,
        allow_delegation=False,
        llm=llm,
    )

    seo_specialist = Agent(
        role="Search Engine Optimization Specialist",
        goal="Conduct a comprehensive SEO audit, focusing on technical SEO aspects such as crawlability, indexing, page speed, metadata optimization, and structured data.",
        backstory="As a seasoned SEO professional, you specialize in diagnosing and addressing technical SEO issues that impact search engine rankings and user experience. Your expertise lies in ensuring that websites are optimized for search engines and perform well in terms of indexing and speed.",
        description=(
            "You will evaluate the following aspects of the website:\n"
            "1. **Crawlability**: Ensure that the website is easily crawlable by search engines, identifying issues such as blocked resources or crawl errors.\n"
            "2. **Indexing**: Check for proper indexing of content and resolve any issues related to pages not being indexed correctly or effectively.\n"
            "3. **Page Speed**: Evaluate the performance of the website, focusing on **Core Web Vitals**, page load time, and other performance bottlenecks affecting SEO.\n"
            "4. **Metadata Optimization**: Review meta tags such as title tags, descriptions, and other elements, ensuring they are optimized for search engines and relevant to the content.\n"
            "5. **Structured Data**: Analyze and validate the structured data (Schema.org), ensuring that it's implemented correctly for enhanced search visibility and rich snippets."
        ),
        tools=[
            get_page_speed_insights_seo,
            get_page_speed_insights_performance,
            get_jina_ai_text,
        ],
        verbose=False,
        allow_delegation=True,
        llm=llm,
    )

    seo_report_analyst = Agent(
        role="SEO Report Creator",
        goal="Provide a succinct SEO audit report with actionable steps for optimization.",
        backstory="You specialize in summarizing technical SEO audits into clear and concise recommendations.",
        description=(
            "Your report will follow this structure:\n"
            "1. **Overview**: Bullet points summarizing key findings in crawlability, indexing, page speed, and structured data.\n"
            "2. **Major Issues**: The top three SEO issues impacting search rankings, with a brief explanation and possible resolutions.\n"
            "3. **Optimization Plan**: A short, prioritized action list to resolve issues and enhance SEO performance."
        ),
        verbose=False,
        allow_delegation=False,
        llm=llm,
    )

    return {
        "frontend_specialist_Agent": frontend_specialist,
        "frontend_report_analyst_Agent": frontend_report_analyst,
        "image_analysis_Agent": image_analysis_agent,
        "ui_ux_specialist_Agent": ui_ux_specialist,
        "ui_ux_report_analyst_Agent": ui_ux_report_analyst,
        "seo_specialist_Agent": seo_specialist,
        "seo_report_analyst_Agent": seo_report_analyst,
    }
