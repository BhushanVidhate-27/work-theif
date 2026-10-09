from agents.worker import do_work
from agents.manager import review_and_decide
from alerts.telegram import send_alert, wait_for_new_task

def run(initial_task: str):
    current_task = initial_task
    history = []  # shared memory

    print(f"\n🚀 Starting: {current_task}\n")
    send_alert(f"🚀 Starting task:\n{current_task}")

    max_steps = 6  # safety limit to prevent infinite loops
    step = 0

    while step < max_steps:
        step += 1
        print(f"\n----- Step {step} -----")
        print("🛠️  Worker is working...")

        # Give Worker the full history so it remembers previous work
        full_context = f"Original Task: {initial_task}\n\n"
        if history:
            full_context += "Previous work:\n" + "\n\n".join(history) + "\n\n"
        full_context += f"Current instruction: {current_task}"

        result = do_work(full_context)
        history.append(f"Worker output:\n{result}")
        print("Worker finished.\n")

        print("🧠 Manager is reviewing...")
        decision = review_and_decide(initial_task, result, history)
        print("-" * 50)

        raw = decision["raw"].lower()

        # Strong stop conditions
        if any(x in raw for x in ["next_task: done", "next_task: none", "status: done", "finished", "completed"]):
            print("\n✅ Work finished. Agents going to sleep.")
            send_alert("✅ Task completed successfully!\nAgents are now sleeping.")
            return

        if decision["approved"]:
            if "NEXT_TASK:" in decision["raw"]:
                next_task = decision["raw"].split("NEXT_TASK:")[1].split("REASON:")[0].strip()
                if next_task.lower() in ["none", "done", "", "n/a"]:
                    print("\n✅ Work finished.")
                    send_alert("✅ Task completed!\nAgents sleeping.")
                    return
                current_task = next_task
            else:
                current_task = "Improve or finalize the previous result"
        else:
            current_task = f"Fix the issues mentioned by the Manager:\n{decision['raw']}"

    print("\n⚠️ Reached maximum steps. Stopping to prevent infinite loop.")
    send_alert("⚠️ Stopped after maximum steps to prevent infinite loop.")


if __name__ == "__main__":
    task = input("Enter the high-level task (or press Enter to wait for Telegram): ").strip()

    while True:
        if not task:
            task = wait_for_new_task()

        run(task)
        task = None   # go back to sleep