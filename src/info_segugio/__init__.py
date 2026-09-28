import json

import chainlit as cl
from openai import OpenAI

from info_segugio.config import Config
from info_segugio.prompts import (
    query_writer_instructions,
    reflection_instructions,
    summarizer_instructions,
)
from tavily import TavilyClient


client = OpenAI(
    api_key=Config.OPENAI_API_KEY
)


def llm(
    developer_prompt,
    user_prompt,
    temperature=0,
    response_format={"type": "json_object"},
):
    request = {
        "model": Config.LLM_MODEL,
        "messages": [
            {
                "role": "developer",
                "content": developer_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        "temperature": temperature,
    }

    if response_format is not None:
        request["response_format"] = response_format

    response = client.chat.completions.create(
        **request
    )

    return response.choices[0].message.content


def optimize_search_query(research_topic):
    formatted_instructions = query_writer_instructions.format(
        research_topic=research_topic
    )

    result = llm(
        formatted_instructions,
        "Genera una query per la ricerca web:",
    )

    optimized_query = json.loads(result)

    print(optimized_query)

    return optimized_query


@cl.on_message
async def main(message: cl.Message):
    user_message = message.content

    # 1. Ottimizza la query iniziale
    optimized_query = optimize_search_query(
        user_message
    )

    query = optimized_query["query"]

    await cl.Message(
        content=(
            "🔎 Query di ricerca ottimizzata:\n\n"
            f"{query}\n\n"
            f"Motivo: {optimized_query['reason']}"
        )
    ).send()

    # Memoria della ricerca
    web_research_results = []
    running_summary = None

    # Per il primo test usiamo 2 cicli.
    # Nella videolezione il docente arriva a max_cycles = 4.
    max_cycles = 4

    for cycle in range(max_cycles):
        # 2. Ricerca web
        research_results = web_research(query)

        web_research_results.append(
            research_results
        )

        sources = research_results["sources"]

        if not sources:
            await cl.Message(
                content="Nessuna fonte trovata."
            ).send()
            break

        formatted_sources = "\n".join(
            f"- {source}"
            for source in sources
        )

        await cl.Message(
            content=(
                f"🌐 Fonti trovate - ciclo {cycle + 1}:\n\n"
                f"{formatted_sources}"
            )
        ).send()

        # 3. Genera o aggiorna il riassunto
        running_summary = summarize_sources(
            web_research_results=web_research_results,
            research_topic=user_message,
            running_summary=running_summary,
        )

        await cl.Message(
            content=(
                "📝 Riassunto attuale:\n\n"
                f"{running_summary}"
            )
        ).send()

        # Se abbiamo terminato i cicli non serve
        # generare un'altra query.
        if cycle == max_cycles - 1:
            break

        # 4. Reflection sul riassunto
        reflection = reflect_on_summary(
            research_topic=user_message,
            running_summary=running_summary,
        )

        query = reflection[
            "domanda_approfondimento"
        ]

        await cl.Message(
            content=(
                "💡 Prossima ricerca:\n\n"
                f"Lacuna individuata: "
                f"{reflection['lacuna_conoscenza']}\n\n"
                f"{query}"
            )
        ).send()
        
    await cl.Message(
    content=(
        "✅ Risposta alla tua domanda:\n\n"
        f"{user_message}\n\n"
        "Risposta finale:\n\n"
        f"{running_summary}"
    )
).send()

def _format_content(result):
    return (
        f"Fonte: {result['title']}\n\n"
        f"URL: {result['url']}\n\n"
        f"Contenuto più rilevante: {result['content']}\n\n"
    )

def web_research(search_query):
    tavily_client = TavilyClient(
        api_key=Config.TAVILY_API_KEY
    )

    response = tavily_client.search(
        query=search_query,
        max_results=5,
        include_raw_content=False,
    )

    results = response.get("results", [])

    titles = [
        result["title"]
        for result in results
    ]

    contents = [
        _format_content(result)
        for result in results
    ]

    return {
        "sources": titles,
        "contents": contents,
    }

def summarize_sources(
    web_research_results,
    research_topic,
    running_summary=None,
):
    current_results = web_research_results[-1]

    if running_summary:
        message = (
            f"Estendi questo riassunto: {running_summary}\n\n"
            f"Con questi nuovi risultati: {current_results}\n\n"
            f"Sul tema: {research_topic}"
        )
    else:
        message = (
            f"Genera un riassunto di questi risultati: "
            f"{current_results}\n\n"
            f"Sul tema: {research_topic}"
        )

    return llm(
        summarizer_instructions,
        message,
        temperature=0.2,
        response_format=None,
    )
def reflect_on_summary(
    research_topic,
    running_summary,
):
    formatted_instructions = reflection_instructions.format(
        research_topic=research_topic
    )

    result = llm(
        formatted_instructions,
        running_summary,
    )

    return json.loads(result)