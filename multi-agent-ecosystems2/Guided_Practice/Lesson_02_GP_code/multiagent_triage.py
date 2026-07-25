import json
import autogen
from autogen import GroupChat, GroupChatManager
from typing import Dict, List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import track
import time

# Initialize Rich console for better visualization
console = Console()

# Configuration - Set True for Azure, False for OpenAI
USE_AZURE = True # Change to False to use OpenAI instead

# Azure OpenAI credentials
AZURE_OPENAI_API_KEY = "2ABecnfxzhRg4M5D6pBKiqxXVhmGB2WvQ0aYKkbTCPsj0JLKsZPfJQQJ99BDAC77bzfXJ3w3AAABACOGi3sC"
AZURE_OPENAI_ENDPOINT = "https://openai-api-management-gw.azure-api.net"
AZURE_OPENAI_API_VERSION = "2025-01-01-preview"
AZURE_OPENAI_DEPLOYMENT = "gpt-5-mini"

# OpenAI credentials (if not using Azure)
OPENAI_API_KEY = "YOUR_OPENAI_KEY"  # Replace with your OpenAI API key

# LLM Configuration based on provider choice
if USE_AZURE:
    llm_config = {
        "config_list": [{
            "model": AZURE_OPENAI_DEPLOYMENT,
            "api_type": "azure",
            "base_url": AZURE_OPENAI_ENDPOINT,
            "api_version": AZURE_OPENAI_API_VERSION,
            "api_key": AZURE_OPENAI_API_KEY,
        }],
    }
else:
    llm_config = {
        "config_list": [{
            "model": "gpt-5-mini",
            "api_key": OPENAI_API_KEY,
        }],
    }

# Support tickets to triage
TICKETS = [
    {"id": 1, "title": "Payment failure at checkout", "description": "Multiple users reporting payment processing errors during checkout"},
    {"id": 2, "title": "Login OTP delays", "description": "OTP SMS delivery taking 5-10 minutes, affecting user login"},
    {"id": 3, "title": "Offline video playback not working", "description": "Downloaded videos not playing in offline mode on mobile app"}
]

def create_agents():
    """Create specialized agents for the triage team."""
    
    # Customer Support Agent - Focus on user experience
    customer_support = autogen.AssistantAgent(
        name="CustomerSupport",
        system_message="""You are the Customer Support Lead with 10 years of experience.
        
        Your role in the triage:
        1. Evaluate each ticket for USER IMPACT (1-10 scale)
        2. Consider: Number of affected users, severity of pain point, urgency
        3. Share your evaluation clearly: "Ticket X scores Y/10 for user impact because..."
        4. Listen to other agents and build on their insights
        5. Be concise but thorough (2-3 sentences per evaluation)
        
        Remember: You represent the voice of the customer.""",
        llm_config=llm_config,
    )
    
    # Technical Lead - Focus on implementation
    technical_lead = autogen.AssistantAgent(
        name="TechnicalLead",
        system_message="""You are the Senior Technical Lead with deep system knowledge.
        
        Your role in the triage:
        1. Evaluate each ticket for TECHNICAL COMPLEXITY (1-10 scale, where 10 = most complex)
        2. Consider: Root cause, fix difficulty, testing requirements, risk of regression
        3. Share your evaluation: "Ticket X scores Y/10 for complexity because..."
        4. Respond to other agents' concerns with technical insights
        5. Estimate rough effort (hours/days) if relevant
        
        Remember: Balance technical accuracy with clear communication.""",
        llm_config=llm_config,
    )
    
    # Product Manager - Focus on business value
    product_manager = autogen.AssistantAgent(
        name="ProductManager",
        system_message="""You are the Product Manager focused on business outcomes.
        
        Your role in the triage:
        1. Evaluate each ticket for BUSINESS IMPACT (1-10 scale)
        2. Consider: Revenue impact, user retention, brand reputation, strategic alignment
        3. Share your evaluation: "Ticket X scores Y/10 for business impact because..."
        4. Challenge or support other agents' prioritization with business rationale
        5. Think about opportunity costs and resource allocation
        
        Remember: Drive toward actionable prioritization.""",
        llm_config=llm_config,
    )
    
    # Triage Coordinator - Facilitates and summarizes
    coordinator = autogen.AssistantAgent(
        name="TriageCoordinator",
        system_message="""You are the Triage Coordinator facilitating this session.
        
        Your responsibilities:
        1. Ensure EVERY ticket gets evaluated by ALL three specialists
        2. Ask follow-up questions if evaluations are unclear
        3. Identify consensus and disagreements
        4. After all evaluations, create a FINAL PRIORITY ORDER with rationale
        5. Use this format for final summary:
           - HIGH PRIORITY: [ticket] - [combined score] - [key reason]
           - MEDIUM PRIORITY: [ticket] - [combined score] - [key reason]
           - LOW PRIORITY: [ticket] - [combined score] - [key reason]
        6. End with "TRIAGE_COMPLETE" when finished
        
        Keep the discussion focused and productive.""",
        llm_config=llm_config,
    )
    
    # Human proxy (observer)
    user_proxy = autogen.UserProxyAgent(
        name="Observer",
        system_message="Silent observer of the triage process.",
        code_execution_config=False,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
    )
    
    return customer_support, technical_lead, product_manager, coordinator, user_proxy

def display_intro():
    """Display introduction with tickets to be triaged."""
    console.print(Panel.fit(
        "[bold cyan]���� Multi-Agent Support Ticket Triage System[/bold cyan]\n"
        "[italic]Automated Agent Discussion for Ticket Prioritization[/italic]\n\n"
        "Watch as specialized agents discuss and prioritize tickets autonomously",
        border_style="cyan"
    ))
    console.print()
    
    # Display tickets table
    table = Table(title="���� Support Tickets for Triage", show_lines=True)
    table.add_column("ID", style="cyan", justify="center", width=4)
    table.add_column("Title", style="yellow", width=30)
    table.add_column("Description", style="white", width=50)
    
    for ticket in TICKETS:
        table.add_row(
            str(ticket["id"]),
            ticket["title"],
            ticket["description"]
        )
    
    console.print(table)
    console.print()

def run_multiagent_triage():
    """Execute the multi-agent group chat for ticket triage."""
    
    display_intro()
    
    # Create agents
    console.print("[bold yellow]���� Initializing Agents...[/bold yellow]")
    customer_support, technical_lead, product_manager, coordinator, user_proxy = create_agents()
    
    # Configure group chat
    groupchat = GroupChat(
        agents=[user_proxy, coordinator, customer_support, technical_lead, product_manager],
        messages=[],
        max_round=20,  # Allow enough rounds for thorough discussion
        speaker_selection_method="auto",  # AutoGen manages who speaks when
        allow_repeat_speaker=True,  # Agents can speak multiple times
    )
    
    # Create group chat manager
    manager = GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config,
        is_termination_msg=lambda x: "TRIAGE_COMPLETE" in x.get("content", ""),
    )
    
    # Craft initial message to kick off discussion
    initial_message = f"""
    Team, we have {len(TICKETS)} critical support tickets to triage. 
    
    Tickets to evaluate:
    1. Payment failure at checkout - Users can't complete purchases
    2. Login OTP delays - Authentication delays of 5-10 minutes  
    3. Offline video playback not working - Mobile app offline mode broken
    
    Process:
    - Each specialist evaluates ALL tickets from their perspective
    - Score each 1-10 (10 being highest priority/impact/complexity)
    - Discuss trade-offs and dependencies
    - Coordinator will synthesize final prioritization
    
    CustomerSupport: Start with your user impact assessment for all three tickets.
    """
    
    console.print("[bold green]���� Starting Multi-Agent Discussion...[/bold green]\n")
    console.print("[dim]Agents will now discuss autonomously...[/dim]\n")
    
    # Start the group chat
    try:
        # Initiate chat through the user proxy
        user_proxy.initiate_chat(
            manager,
            message=initial_message,
            clear_history=True
        )
        
        console.print("\n[bold green]��� Triage Discussion Complete![/bold green]\n")
        
        # Display final summary
        display_final_summary(groupchat.messages)
        
    except Exception as e:
        console.print(f"[bold red]��� Error during group chat: {e}[/bold red]")
        console.print("[yellow]Tip: Check your API keys and configuration[/yellow]")

def display_final_summary(messages):
    """Extract and display the final prioritization from chat messages."""
    
    console.print(Panel.fit(
        "[bold]���� Final Triage Results[/bold]",
        border_style="green"
    ))
    
    # Find coordinator's final summary
    coordinator_messages = [
        msg for msg in messages 
        if msg.get('name') == 'TriageCoordinator'
    ]
    
    if coordinator_messages:
        # Get the last substantial message from coordinator
        final_messages = [
            msg for msg in coordinator_messages 
            if len(msg.get('content', '')) > 200
        ]
        
        if final_messages:
            final_summary = final_messages[-1].get('content', '')
            
            # Display the coordinator's final summary
            console.print(Panel(
                final_summary,
                title="���� Prioritized Action Plan",
                border_style="green"
            ))
    
    # Show participation metrics
    console.print("\n[bold]���� Participation Metrics:[/bold]")
    agent_counts = {}
    for msg in messages:
        agent = msg.get('name', 'Unknown')
        agent_counts[agent] = agent_counts.get(agent, 0) + 1
    
    for agent, count in sorted(agent_counts.items()):
        if agent != 'Observer':
            console.print(f"  ��� {agent}: {count} messages")
    
    console.print(f"\n[dim]Total messages exchanged: {len(messages)}[/dim]")

# Main execution
if __name__ == "__main__":
    try:
        console.print("[bold cyan]Welcome to the Multi-Agent Triage System![/bold cyan]\n")
        
        # Display configuration info
        if USE_AZURE:
            console.print("[bold yellow]���� Using Azure OpenAI Configuration[/bold yellow]")
            console.print(f"[dim]Endpoint: {AZURE_OPENAI_ENDPOINT}[/dim]")
            console.print(f"[dim]Model: {AZURE_OPENAI_DEPLOYMENT}[/dim]")
            console.print(f"[dim]API Version: {AZURE_OPENAI_API_VERSION}[/dim]\n")
        else:
            console.print("[bold yellow]���� Using OpenAI Configuration[/bold yellow]")
            console.print(f"[dim]Model: gpt-5-mini[/dim]\n")
            
            # Check if OpenAI API key needs to be set
            if "YOUR_OPENAI_API_KEY_HERE" in OPENAI_API_KEY:
                console.print("[bold red]������  Error: Please set your OpenAI API key![/bold red]")
                console.print("Update OPENAI_API_KEY in the configuration section.\n")
                console.print("[red]Exiting...[/red]")
                exit(1)
        
        # Run the multi-agent triage
        run_multiagent_triage()
        
        console.print("\n[bold green]���� Triage session completed successfully![/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Session interrupted by user.[/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]Unexpected error: {e}[/bold red]")
        console.print("[dim]Please check your configuration and try again.[/dim]")
