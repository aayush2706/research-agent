from agents import build_serach_agent, build_reader_agent, writer_chain, critic_prompt
from rich import print

def run_reseach_pipeline(topic : str) -> dict:

    state = {}

    #search agent
    print("[bold green]Running Search Agent...[/bold green]")
    print("\n"+"="* 50)
    print("step 1 - Searching the web for relevant information...")
    print("\n"+"="* 50)

    search_agent = build_serach_agent()
    search_results = search_agent.invoke({
        "messages": [(
            "user",f"find recent , reliable and detailed information about: {topic}"
            )]
        })

    state['search_results'] = search_results['messages'][-1].content
    
    print("\n Search Results: \n",state['search_results'])

    #STEP 2 reader agent
    
    print("[bold green]Running Reader Agent...[/bold green]")
    print("\n"+"="* 50)
    print("step 2 - Reading and analyzing the retrieved information...")
    print("\n"+"="* 50)

    reader_agent = build_reader_agent()
    read_results = reader_agent.invoke({
        "messages": [
            ("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })

    state['read_results'] = read_results['messages'][-1].content

    print("\n Scraped Content: \n",state['read_results'])


    #STEP 3 writer agent

    print("\n"+"="* 50)
    print("step 3 - Writing the final report...")
    print("\n"+"="* 50)

    research_combined = (  
                        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                        f"DETAILED SCRAPED CONTENT:\n{state['read_results']}")
    state['report'] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n Final Report: \n",state['report'])

    #STEP 4 critic agent

    print("\n"+"="* 50)
    print("step 4 - Critiquing the report...")
    print("\n"+"="* 50)

    state['critique'] = critic_prompt.invoke({
        "report": state['report']
    })

    print("\n Critique: \n",state['critique'])

    return state


if __name__ == "__main__":
    topic = input("Enter the research topic: ")
    run_reseach_pipeline(topic)