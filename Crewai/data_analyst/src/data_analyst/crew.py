from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai_tools import FileReadTool
from .tools.csv_info_tool import CSVInfoTool

analysis_guidelines = TextFileKnowledgeSource(
    file_paths=["analysis_guidelines.txt"]
)

# Attached to report_writer agent
report_style_guide = TextFileKnowledgeSource(
    file_paths=["report_style_guide.txt"]
)

# Shared across the whole crew
business_context = TextFileKnowledgeSource(
    file_paths=["business_context.txt"]
)


@CrewBase
class DataAnalyst():
    """DataAnalyst crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def data_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['data_analyst'], # type: ignore[index]
            tools=[FileReadTool(), CSVInfoTool()],
            knowledge_sources=[analysis_guidelines],
            verbose=True
        )

    @agent
    def report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['report_writer'], # type: ignore[index]
            knowledge_sources=[report_style_guide],
            verbose=True
        )

    @task
    def data_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_analysis_task'], # type: ignore[index]
        )

    @task
    def report_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_writing_task'], # type: ignore[index]
            output_file='report2.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DataAnalyst crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            knowledge_sources=[business_context],
            verbose=True,
        )
