from system_prompt import SYSTEM_PROMPT
from config import client
from tools import execute_tool
from colorama import Fore, Style, init
import json

init(autoreset=True)

ALLOWED_TOOLS = {"python", "terminal", "write_file"}


def ask_yes_no(prompt: str, default: bool = False) -> bool:
    default_answer = "y" if default else "n"
    while True:
        choice = input(f"{prompt} (y/n) [{default_answer}]: ").strip().lower()
        if choice == "":
            return default
        if choice in {"y", "yes"}:
            return True
        if choice in {"n", "no"}:
            return False
        print("Please answer 'y' or 'n'.")


def request_tool_permission(tool: str, action: str) -> bool:
    if tool not in ALLOWED_TOOLS:
        print(f"⚠️ Permission denied: tool '{tool}' is not allowed.")
        return False
    return ask_yes_no(f"Allow execution of tool '{tool}' with action '{action}'?")


def review_actions(action_history: list[dict]) -> bool:
    print("\n🔎 Review executed actions and outputs:")
    if not action_history:
        print("No executed actions to review.")
        return ask_yes_no("Do you still want to mark the task as completed?", default=False)

    for entry in action_history:
        tool = entry.get("tool")
        action = entry.get("action")
        output = entry.get("output logs")
        print(f"- {tool}: {action}")
        if output is not None:
            print(f"  output: {output}")
    return ask_yes_no("Do you confirm these actions completed successfully?", default=True)


def main():
    while True:
        user_input = input(f"{Fore.GREEN}You{Style.RESET_ALL}> ").strip()
        if user_input.lower() in ['exit', 'quit']:
            print(f"{Fore.RED}Goodbye!{Style.RESET_ALL}")
            break
        
        response = client.chat.completions.create(
            model="gemini-3-flash-preview",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        
        assistant_reply = response.choices[0].message.content
        try:
            reply_json = json.loads(assistant_reply)
        except json.JSONDecodeError:
            print(f"🤖 Error: Unable to parse assistant response as JSON:\n{assistant_reply}")
            continue

        memory_agent_verify = [{"goal": reply_json.get("goal")}]
        action_history: list[dict] = []

        while True:
            print(f"\n🤖 Assistant status: {reply_json.get('status')}")
            print(f"🤖 Goal: {reply_json.get('goal')}")

            if reply_json.get("status") == "completed":
                if review_actions(action_history):
                    print(f"✅ {reply_json['goal']} completed successfully!")
                    break
                print("Continuing to verify completion with the assistant...")

            if not reply_json.get("actions"):
                print("No actions provided by the assistant.")
                break

            print("⏳ Actions suggested by the assistant:")
            for action in reply_json["actions"]:
                print(f"  - {action['tool']}: {action['action']}")

            permitted_actions = []
            for action in reply_json["actions"]:
                tool = action.get("tool")
                act = action.get("action")
                if not request_tool_permission(tool, str(act)):
                    print(f"Skipping action for tool '{tool}'.")
                    continue
                permitted_actions.append(action)

            for action in permitted_actions:
                tool = action["tool"]
                act = action["action"]
                try:
                    output = execute_tool(tool, act)
                    entry = {"tool": tool, "action": act, "output logs": output}
                    action_history.append(entry)
                    memory_agent_verify.append(entry)
                except Exception as e:
                    error_msg = f"Error executing action: {e}"
                    print(error_msg)
                    entry = {"tool": tool, "action": act, "output logs": error_msg}
                    action_history.append(entry)
                    memory_agent_verify.append(entry)

            if not permitted_actions:
                print("No permitted actions were executed. Ending current task loop.")
                break

            response = client.chat.completions.create(
                model="gemini-3-flash-preview",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": json.dumps(memory_agent_verify)}
                ]
            )
            assistant_reply = response.choices[0].message.content
            try:
                reply_json = json.loads(assistant_reply)
            except json.JSONDecodeError:
                print(f"🤖 Error decoding assistant reply: {assistant_reply}")
                break

if __name__ == "__main__":
    main()