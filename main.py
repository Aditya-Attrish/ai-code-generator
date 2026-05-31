from system_prompt import SYSTEM_PROMPT
from config import client
from tools import execute_tool
import json

def main():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
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
            print(f"🤖: {reply_json['goal']}")
            for action in reply_json["actions"]:
                print(f"  - {action['tool']}: {action['action']}")
                try:
                    execute_tool(action['tool'], action['action'])
                except Exception as e:
                    print(f"Error executing action: {e}")
        except json.JSONDecodeError:
            print(f"🤖 Error: {assistant_reply}")

if __name__ == "__main__":
    main()