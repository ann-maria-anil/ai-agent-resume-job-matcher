import asyncio
from browser_use import Agent
from urllib.parse import quote


def build_linkedin_url(role_query, experience_level, industry):
    search_string = f"{role_query} {industry}".strip()
    encoded_keywords = quote(search_string)

    exp_map = {
        "Entry": "1",
        "Intern": "1",
        "Junior": "2",
        "Mid": "3",
        "Senior": "4",
        "Lead": "5"
    }

    exp_code = ""

    for key in exp_map:
        if key.lower() in experience_level.lower():
            exp_code = exp_map[key]
            break

    url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_keywords}"

    if exp_code:
        url += f"&f_E={exp_code}"

    return url


async def open_linkedin_jobs(role_query, experience_level, industry):

    jobs_url = build_linkedin_url(role_query, experience_level, industry)

    task = f"""
    1. Navigate to https://www.linkedin.com

    2. If the login page appears,
       WAIT until the user logs in manually.
       Continue only when the URL contains 'feed' or shows the LinkedIn home page.
       Do NOT end the task.

    3. Once logged in, navigate directly to:
       {jobs_url}

    4. Wait until job listings are visible.

    5. Once job listings are visible,
   do nothing further.
   Do not mark the task as complete.
   Remain idle on the page.
    Do NOT close the browser.
    """

    agent = Agent(
        task=task,
        headless=False,
        keep_alive=True
    )

    await agent.run()