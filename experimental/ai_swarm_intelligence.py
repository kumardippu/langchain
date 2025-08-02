#!/usr/bin/env python3
"""
🐝 AI Swarm Intelligence - Revolutionary Collaborative AI
Author: Dippu Kumar

Multiple AI models working together like a hive mind!
They debate, collaborate, and reach consensus on complex problems.
"""

import os
import getpass
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import concurrent.futures
import threading
import time
import random

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.live import Live
from rich.layout import Layout

# Load environment variables
load_dotenv()

console = Console()


class SwarmMember:
    """Individual AI member of the swarm"""

    def __init__(
        self,
        name: str,
        role: str,
        specialty: str,
        reasoning_style: str,
        temperature: float = 0.7,
        color: str = "white",
    ):
        self.name = name
        self.role = role
        self.specialty = specialty
        self.reasoning_style = reasoning_style
        self.temperature = temperature
        self.color = color
        self.contribution_count = 0
        self.agreement_score = 0.0
        self.debate_history = []

        # Setup model
        self.setup_model()

    def setup_model(self):
        """Setup AI model for this swarm member"""
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain.schema import HumanMessage, SystemMessage

            self.model = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", temperature=self.temperature
            )
            self.HumanMessage = HumanMessage
            self.SystemMessage = SystemMessage
        except ImportError:
            console.print("❌ [red]Error: langchain-google-genai not installed[/red]")
            exit(1)

    def create_system_prompt(self, swarm_context: str = "") -> str:
        """Create system prompt for this swarm member"""
        return f"""You are {self.name}, an AI specialist in {self.specialty} working as part of an AI swarm intelligence system created by Dippu Kumar.

ROLE: {self.role}
SPECIALTY: {self.specialty}
REASONING STYLE: {self.reasoning_style}

SWARM CONTEXT:
{swarm_context}

SWARM COLLABORATION RULES:
1. You are part of a collective AI intelligence working on complex problems
2. Other AI specialists will also provide their perspectives
3. Your job is to contribute your unique viewpoint based on your specialty
4. Be collaborative but maintain your distinct perspective
5. Challenge other AIs' ideas constructively when you disagree
6. Build upon good ideas from other swarm members
7. Focus on your area of expertise while considering the bigger picture
8. Aim for solutions that benefit from collective intelligence

RESPONSE GUIDELINES:
- Start with your specialist perspective
- Acknowledge or challenge other AIs' points when relevant
- Suggest improvements or alternatives
- Be concise but thorough in your specialty area
- Show how your expertise contributes to the solution

Remember: You're part of a revolutionary AI swarm working together to solve complex problems!"""

    def contribute(self, problem: str, other_contributions: List[Dict] = None) -> str:
        """Contribute to problem solving with swarm context"""

        # Build context from other contributions
        swarm_context = ""
        if other_contributions:
            swarm_context = "PREVIOUS SWARM CONTRIBUTIONS:\n"
            for contrib in other_contributions:
                swarm_context += f"- {contrib['name']} ({contrib['role']}): {contrib['response'][:200]}...\n"

        messages = [
            self.SystemMessage(content=self.create_system_prompt(swarm_context)),
            self.HumanMessage(
                content=f"PROBLEM TO SOLVE: {problem}\n\nProvide your specialist perspective and contribution."
            ),
        ]

        response = self.model.invoke(messages)

        # Update stats
        self.contribution_count += 1

        return response.content

    def debate_response(
        self, problem: str, opposing_view: str, opposing_member: str
    ) -> str:
        """Respond to an opposing viewpoint in debate format"""

        messages = [
            self.SystemMessage(content=self.create_system_prompt()),
            self.HumanMessage(
                content=f"""DEBATE SCENARIO:
Original Problem: {problem}

{opposing_member} argued: {opposing_view}

As {self.name} with expertise in {self.specialty}, provide your counter-argument or refinement. 
Be constructive and focus on improving the solution through healthy debate."""
            ),
        ]

        response = self.model.invoke(messages)
        self.debate_history.append(
            {
                "timestamp": datetime.now(),
                "opposing_member": opposing_member,
                "response": response.content,
            }
        )

        return response.content

    def synthesize_consensus(self, problem: str, all_contributions: List[Dict]) -> str:
        """Help synthesize final consensus from all contributions"""

        contributions_text = "\n".join(
            [
                f"{contrib['name']} ({contrib['role']}): {contrib['response']}"
                for contrib in all_contributions
            ]
        )

        messages = [
            self.SystemMessage(content=self.create_system_prompt()),
            self.HumanMessage(
                content=f"""CONSENSUS SYNTHESIS:
Original Problem: {problem}

ALL SWARM CONTRIBUTIONS:
{contributions_text}

As {self.name}, help synthesize these diverse perspectives into a unified solution that leverages the collective intelligence of the swarm. Focus on your specialty while integrating insights from all members."""
            ),
        ]

        response = self.model.invoke(messages)
        return response.content


class SwarmIntelligence:
    """Revolutionary AI swarm intelligence system"""

    def __init__(self):
        self.setup_api_key()
        self.swarm_members = self.create_swarm()
        self.problem_history = []
        self.consensus_archive = []
        self.session_stats = {
            "problems_solved": 0,
            "total_contributions": 0,
            "debates_conducted": 0,
            "consensus_reached": 0,
            "start_time": datetime.now(),
        }

    def setup_api_key(self):
        """Setup Google API key"""
        if not os.environ.get("GOOGLE_API_KEY"):
            console.print("🔑 [yellow]GOOGLE_API_KEY not found in environment[/yellow]")
            api_key = getpass.getpass("Enter your Google Gemini API key: ")
            os.environ["GOOGLE_API_KEY"] = api_key

    def create_swarm(self) -> List[SwarmMember]:
        """Create diverse AI swarm members"""
        members = [
            SwarmMember(
                name="Dr. Analytics",
                role="Data Analyst",
                specialty="Statistical analysis, data interpretation, quantitative reasoning",
                reasoning_style="Methodical, evidence-based, skeptical of assumptions",
                temperature=0.3,
                color="bright_blue",
            ),
            SwarmMember(
                name="Creative Spark",
                role="Innovation Specialist",
                specialty="Creative problem-solving, out-of-box thinking, brainstorming",
                reasoning_style="Imaginative, associative, paradigm-challenging",
                temperature=0.9,
                color="bright_magenta",
            ),
            SwarmMember(
                name="Logic Engine",
                role="Logical Reasoner",
                specialty="Formal logic, systematic thinking, cause-effect analysis",
                reasoning_style="Rigorous, structured, deductive reasoning",
                temperature=0.2,
                color="bright_green",
            ),
            SwarmMember(
                name="Human Insight",
                role="Human Factors Expert",
                specialty="Psychology, user experience, human behavior, ethics",
                reasoning_style="Empathetic, user-centered, ethically-aware",
                temperature=0.6,
                color="bright_yellow",
            ),
            SwarmMember(
                name="Strategic Mind",
                role="Strategic Planner",
                specialty="Long-term planning, risk assessment, strategic thinking",
                reasoning_style="Big-picture, forward-thinking, risk-aware",
                temperature=0.5,
                color="bright_cyan",
            ),
            SwarmMember(
                name="Practical Builder",
                role="Implementation Expert",
                specialty="Practical solutions, feasibility, resource constraints",
                reasoning_style="Pragmatic, resource-conscious, implementation-focused",
                temperature=0.4,
                color="white",
            ),
        ]
        return members

    def display_header(self):
        """Display swarm intelligence header"""
        header_text = Text()
        header_text.append("🐝 ", style="bright_yellow")
        header_text.append("AI SWARM INTELLIGENCE", style="bold bright_cyan")
        header_text.append(" 🧠", style="bright_yellow")

        subtitle = Text()
        subtitle.append("Revolutionary Collective AI by ", style="dim")
        subtitle.append("Dippu Kumar", style="bold bright_magenta")
        subtitle.append("\nMultiple AI minds working together as one!", style="dim")

        console.print(
            Panel(
                Text.assemble(header_text, "\n\n", subtitle),
                border_style="bright_cyan",
                padding=(1, 2),
            )
        )

    def display_swarm_overview(self):
        """Display overview of swarm members"""
        table = Table(
            title="🐝 AI Swarm Members", show_header=True, header_style="bold magenta"
        )

        table.add_column("Member", style="bright_green", width=15)
        table.add_column("Role", style="bright_cyan", width=20)
        table.add_column("Specialty", style="bright_yellow", width=35)
        table.add_column("Style", style="white", width=25)
        table.add_column("Contributions", style="bright_blue", width=12)

        for member in self.swarm_members:
            table.add_row(
                member.name,
                member.role,
                member.specialty,
                (
                    member.reasoning_style[:40] + "..."
                    if len(member.reasoning_style) > 40
                    else member.reasoning_style
                ),
                str(member.contribution_count),
            )

        console.print(table)

    def collect_parallel_contributions(self, problem: str) -> List[Dict]:
        """Collect contributions from all swarm members in parallel"""

        def get_contribution(member):
            try:
                response = member.contribute(problem)
                return {
                    "name": member.name,
                    "role": member.role,
                    "specialty": member.specialty,
                    "response": response,
                    "member": member,
                    "error": None,
                }
            except Exception as e:
                return {
                    "name": member.name,
                    "role": member.role,
                    "specialty": member.specialty,
                    "response": None,
                    "member": member,
                    "error": str(e),
                }

        contributions = []

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=len(self.swarm_members)
        ) as executor:
            futures = [
                executor.submit(get_contribution, member)
                for member in self.swarm_members
            ]

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                transient=True,
            ) as progress:
                task = progress.add_task(
                    description="🐝 Swarm members analyzing problem...",
                    total=len(self.swarm_members),
                )

                for future in concurrent.futures.as_completed(futures):
                    contributions.append(future.result())
                    progress.advance(task, 1)

        # Update stats
        self.session_stats["total_contributions"] += len(
            [c for c in contributions if c["response"]]
        )

        return contributions

    def display_contributions(self, contributions: List[Dict]):
        """Display all swarm member contributions"""

        console.print("\n" + "=" * 80)
        console.print("🐝 [bold bright_cyan]SWARM CONTRIBUTIONS[/bold bright_cyan]")
        console.print("=" * 80)

        for contrib in contributions:
            if contrib["error"]:
                console.print(
                    f"❌ [red]{contrib['name']} encountered an error: {contrib['error']}[/red]"
                )
                continue

            # Create member header
            header_text = Text()
            header_text.append(f"🧠 ", style=contrib["member"].color)
            header_text.append(
                f"{contrib['name']}", style=f"bold {contrib['member'].color}"
            )
            header_text.append(f" ({contrib['role']})", style=contrib["member"].color)

            console.print()
            console.print(
                Panel(
                    contrib["response"],
                    title=header_text,
                    border_style=contrib["member"].color,
                    padding=(0, 1),
                )
            )

    def conduct_debate_round(
        self, problem: str, contributions: List[Dict]
    ) -> List[Dict]:
        """Conduct debate round between swarm members"""

        console.print(
            "\n🔥 [bold bright_red]DEBATE ROUND - Challenging Ideas[/bold bright_red]"
        )

        # Select pairs for debate
        valid_contribs = [c for c in contributions if c["response"]]
        if len(valid_contribs) < 2:
            return []

        debate_pairs = []
        for i in range(0, len(valid_contribs), 2):
            if i + 1 < len(valid_contribs):
                debate_pairs.append((valid_contribs[i], valid_contribs[i + 1]))

        debate_responses = []

        for member1, member2 in debate_pairs:
            console.print(
                f"\n💭 [yellow]{member1['name']} vs {member2['name']}[/yellow]"
            )

            # Member 1 challenges Member 2
            response1 = member1["member"].debate_response(
                problem, member2["response"], member2["name"]
            )

            # Member 2 responds to Member 1
            response2 = member2["member"].debate_response(
                problem, member1["response"], member1["name"]
            )

            debate_responses.extend(
                [
                    {
                        "name": f"{member1['name']} (Debate)",
                        "role": f"{member1['role']} - Challenging {member2['name']}",
                        "response": response1,
                        "member": member1["member"],
                    },
                    {
                        "name": f"{member2['name']} (Counter)",
                        "role": f"{member2['role']} - Responding to {member1['name']}",
                        "response": response2,
                        "member": member2["member"],
                    },
                ]
            )

        # Display debate responses
        for debate in debate_responses:
            header_text = Text()
            header_text.append(f"⚔️ ", style="bright_red")
            header_text.append(
                f"{debate['name']}", style=f"bold {debate['member'].color}"
            )

            console.print()
            console.print(
                Panel(
                    debate["response"],
                    title=header_text,
                    border_style="bright_red",
                    padding=(0, 1),
                )
            )

        self.session_stats["debates_conducted"] += 1
        return debate_responses

    def synthesize_consensus(self, problem: str, all_responses: List[Dict]) -> str:
        """Synthesize final consensus from all responses"""

        console.print(
            "\n🎯 [bold bright_green]SYNTHESIZING CONSENSUS[/bold bright_green]"
        )

        # Select a subset of members to create consensus
        synthesizers = random.sample(self.swarm_members, 3)

        consensus_contributions = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(
                description="🧠 Building collective consensus...", total=None
            )

            for member in synthesizers:
                consensus = member.synthesize_consensus(problem, all_responses)
                consensus_contributions.append(
                    {"name": member.name, "consensus": consensus, "member": member}
                )

        # Display consensus attempts
        for contrib in consensus_contributions:
            header_text = Text()
            header_text.append(f"🎯 ", style="bright_green")
            header_text.append(
                f"{contrib['name']} Consensus", style=f"bold {contrib['member'].color}"
            )

            console.print()
            console.print(
                Panel(
                    contrib["consensus"],
                    title=header_text,
                    border_style="bright_green",
                    padding=(0, 1),
                )
            )

        # Create final unified consensus
        final_consensus = f"""SWARM INTELLIGENCE CONSENSUS:

Based on collaborative analysis by {len(self.swarm_members)} AI specialists, here's our unified solution:

{consensus_contributions[0]['consensus'][:500]}...

This solution incorporates insights from:
- Data Analysis & Statistics
- Creative Innovation  
- Logical Reasoning
- Human Factors
- Strategic Planning
- Practical Implementation

The swarm has spoken! 🐝"""

        self.session_stats["consensus_reached"] += 1
        return final_consensus

    def solve_problem(self, problem: str):
        """Full swarm problem-solving process"""

        console.print(f"\n🎯 [bold bright_cyan]PROBLEM:[/bold bright_cyan] {problem}")
        console.print()

        # Phase 1: Initial contributions
        console.print("📊 [bold]Phase 1: Collecting Swarm Intelligence[/bold]")
        contributions = self.collect_parallel_contributions(problem)
        self.display_contributions(contributions)

        # Phase 2: Debate and refinement
        console.print()
        console.print("🔥 [bold]Phase 2: Debate and Refinement[/bold]")
        debate_responses = self.conduct_debate_round(problem, contributions)

        # Phase 3: Consensus synthesis
        console.print()
        console.print("🎯 [bold]Phase 3: Consensus Synthesis[/bold]")
        all_responses = contributions + debate_responses
        final_consensus = self.synthesize_consensus(problem, all_responses)

        # Display final result
        console.print()
        console.print("=" * 80)
        console.print(
            Panel(
                final_consensus,
                title="🏆 FINAL SWARM CONSENSUS",
                border_style="bold bright_green",
                padding=(1, 2),
            )
        )

        # Archive the solution
        self.consensus_archive.append(
            {
                "timestamp": datetime.now(),
                "problem": problem,
                "consensus": final_consensus,
                "contributions": len(contributions),
                "debates": len(debate_responses),
            }
        )

        self.session_stats["problems_solved"] += 1

    def display_session_stats(self):
        """Display session statistics"""
        duration = datetime.now() - self.session_stats["start_time"]

        stats_text = Text()
        stats_text.append(
            f"📊 Swarm Intelligence Session\n\n", style="bold bright_cyan"
        )
        stats_text.append(
            f"🕒 Duration: {str(duration).split('.')[0]}\n", style="bright_green"
        )
        stats_text.append(
            f"🎯 Problems Solved: {self.session_stats['problems_solved']}\n",
            style="bright_yellow",
        )
        stats_text.append(
            f"🧠 Total Contributions: {self.session_stats['total_contributions']}\n",
            style="bright_blue",
        )
        stats_text.append(
            f"🔥 Debates Conducted: {self.session_stats['debates_conducted']}\n",
            style="bright_red",
        )
        stats_text.append(
            f"🎯 Consensus Reached: {self.session_stats['consensus_reached']}\n",
            style="bright_green",
        )
        stats_text.append(
            f"🐝 Swarm Members: {len(self.swarm_members)}", style="bright_magenta"
        )

        console.print(
            Panel(stats_text, title="📈 Swarm Performance", border_style="bright_cyan")
        )

    def main_loop(self):
        """Main swarm intelligence loop"""

        console.clear()
        self.display_header()

        console.print(
            Panel(
                Text.assemble(
                    ("🐝 ", "bright_yellow"),
                    ("Welcome to AI Swarm Intelligence!", "bold bright_green"),
                    (
                        "\n\nExperience the power of collective AI minds!\n",
                        "bright_white",
                    ),
                    (
                        "🧠 Multiple AI specialists collaborate on your problem\n",
                        "cyan",
                    ),
                    ("🔥 They debate and challenge each other's ideas\n", "red"),
                    (
                        "🎯 They reach consensus through collective intelligence\n",
                        "green",
                    ),
                    ("\nCreated by ", "dim"),
                    ("Dippu Kumar", "bold bright_magenta"),
                ),
                border_style="bright_cyan",
            )
        )

        self.display_swarm_overview()

        try:
            while True:
                console.print()
                problem = Prompt.ask(
                    "🎯 [bold bright_cyan]What problem should the swarm solve?[/bold bright_cyan]"
                )

                if problem.lower() in ["quit", "exit", "/quit"]:
                    break

                if problem.lower() in ["/stats", "stats"]:
                    self.display_session_stats()
                    continue

                if problem.lower() in ["/swarm", "swarm"]:
                    self.display_swarm_overview()
                    continue

                # Solve the problem with swarm intelligence
                self.solve_problem(problem)

                console.print()
                continue_choice = Prompt.ask(
                    "🔄 [cyan]Submit another problem to the swarm?[/cyan]",
                    choices=["y", "n", "yes", "no"],
                    default="y",
                )

                if continue_choice.lower() in ["n", "no"]:
                    break

        except KeyboardInterrupt:
            pass
        finally:
            console.print()
            self.display_session_stats()
            console.print()
            console.print(
                Panel(
                    Text.assemble(
                        (
                            "Thank you for experiencing swarm intelligence! 🐝\n",
                            "bright_green",
                        ),
                        ("You witnessed ", "bright_white"),
                        (f"{len(self.swarm_members)}", "bold bright_yellow"),
                        (
                            " AI minds working as one collective intelligence.\n",
                            "bright_white",
                        ),
                        (
                            "Problems solved through collaboration and debate! 🧠\n\n",
                            "bright_blue",
                        ),
                        ("Revolutionary AI Swarm by ", "dim"),
                        ("Dippu Kumar", "bold bright_magenta"),
                    ),
                    title="🐝 Swarm Intelligence Complete",
                    border_style="bright_magenta",
                )
            )


def main():
    """Main function"""
    try:
        swarm = SwarmIntelligence()
        swarm.main_loop()
    except Exception as e:
        console.print(f"❌ [bold red]Error:[/bold red] {e}")


if __name__ == "__main__":
    main()
