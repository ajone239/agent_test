# Agentic AI test

This so far is my look into agentic AI.
The work in this repo largely stems from [this tutorial](https://www.tensorops.ai/post/building-ai-and-llm-agents-from-the-ground-up-a-step-by-step-guide) by [Tensorops](https://www.tensorops.ai).


# Jul 6, 2025

The current agent is very simple.
It only has tools, memory, and LLM access.
This means it can only plan one to.

At the time of writing the agent can evaluate math, tell the time, and respond with an LLM.
Below is a rather painful exchange where I try to get the agent to add the hour to the minute.
As you can see, it can get the time, parse the info needed, and sum the numbers.
However, it is doing so with the "agency" of someone with very little agency.

```
❯ poetry run python src/main.py
LLM Agent: Hello! How can I assist you today?

You: Add the hour to the minute for the current time.

LLM Agent: The current time is 2025-07-06 21:23:11 .

You: Now that you have the time stamp, what is the number for the hour and number for the minute.

LLM Agent: The current time is 2025-07-06 21:23:39 .

You: reformat the time to hh:mm

LLM Agent: The current time is 2025-07-06 21:24:09 .

You: do that without tools

LLM Agent: 15:04

You: add those numbers

LLM Agent: The result of '15+4' is 19.
```

The plan is to add some working memory and some idea of planning so that
