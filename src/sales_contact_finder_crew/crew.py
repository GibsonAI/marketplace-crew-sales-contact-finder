from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

from sales_contact_finder_crew.tools.contact_storage_tool import ContactStorageTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class SalesContactFinderCrew:
    """SalesContactFinder crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def company_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["company_researcher"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def org_structure_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["org_structure_analyst"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def contact_finder(self) -> Agent:
        return Agent(
            config=self.agents_config["contact_finder"],
            tools=[
                SerperDevTool(),
                ScrapeWebsiteTool(),
                ContactStorageTool(),
            ],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def sales_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_strategist"],
            tools=[],
            allow_delegation=False,
            verbose=True,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_company_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_company_task"],
        )

    @task
    def analyze_org_structure_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_org_structure_task"],
        )

    @task
    def find_key_contacts_task(self) -> Task:
        return Task(
            config=self.tasks_config["find_key_contacts_task"],
        )

    @task
    def develop_approach_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config["develop_approach_strategy_task"],
            output_file="output/buyer_contact.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SalesContactFinder crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
