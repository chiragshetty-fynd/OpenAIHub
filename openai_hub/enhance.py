import os
import time
from openai import OpenAI


class Enhancer:
    def __init__(self):
        org_id = os.environ["OPENAI_ORG_ID"]
        api_key = os.environ["OPENAI_API_KEY"]
        asst_id = os.environ["OPENAI_ASST_ID"]

        self.client = OpenAI(organization=org_id, api_key=api_key)
        self.assistant = self._get_assistant(asst_id)
        self.thread = self._start_new_chat()

    def _get_assistant(self, asst_id):
        assistant = self.client.beta.assistants.retrieve(asst_id)
        return assistant

    def _start_new_chat(self):
        empty_thread = self.client.beta.threads.create()
        return empty_thread

    def _get_messages_in_chat(self):
        messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
        return messages

    # Description: "Run the thread with the assistant"
    def _run_chat(self):
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
        )
        while run.status != "completed":
            time.sleep(1)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id, run_id=run.id
            )
            print(f"{run.status=}")
        return run

    def _get_last_message(self):
        self._run_chat()
        history = self._get_messages_in_chat()
        messages = history.data
        for i in messages:
            if i.role.upper() != "USER":
                return i.content[0].text.value

    def enhance(self, prompt):
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=prompt,
        )
        enhanced_prompt = self._get_last_message()
        return enhanced_prompt
