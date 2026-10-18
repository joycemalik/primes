# ----------------------------------------------------------------------------
# Prime research archive :: research/09-prime-matrix/day17-prime-matrix-eigenvalues/chat1_two_llms_discuss_primes.py
# Original location      :: research/09-prime-matrix/day17-prime-matrix-eigenvalues/chat1.py   (last edited 2025-08-20)
# What this script does  :: Two local Ollama models discuss "what is the pattern in primes?".
# ----------------------------------------------------------------------------
import ollama

# --- Configuration ---
# Choose the two models you want to use for the conversation.
MODEL_A = 'gemma3:1b'
MODEL_B = 'gemma3:1b'
# MODEL_B = 'gpt-oss:20b'

# Set the number of back-and-forth turns in the conversation.
CONVERSATION_TURNS = 50

# --- Give each model a unique personality using a system prompt! ---
# This helps prevent the conversation from becoming repetitive.
agent_b_system_message = {
    'role': 'system',
    'content': "Be direct and talk only in logical numbers way",
}

agent_a_system_message = {
    'role': 'system',
    'content': "Be direct and talk only in logical numbers way",
}

# --- Initialize Conversation Histories ---
# Each agent gets its own history to maintain its context and personality.
history_a = [agent_a_system_message]
history_b = [agent_b_system_message]

# --- The Conversation Starter ---
# This is the first message that kicks off the dialogue.
initial_prompt = "whats the pattern in primes?"

print(f"--- Conversation Start ---")
print(f"Topic: {initial_prompt}\n")
print(f"Agents: {MODEL_A} (Skepticus) vs. {MODEL_B} (Arturo)\n")

# Add the initial prompt to Agent A's history so it can respond first.
history_a.append({'role': 'user', 'content': initial_prompt})

# --- The Main Conversation Loop ---
try:
    for i in range(CONVERSATION_TURNS):
        # --- Agent A's Turn ---
        print(f"Skepticus ({MODEL_A}):")
        
        # Get response from Agent A
        response_a_chunk = ""
        stream = ollama.chat(
            model=MODEL_A,
            messages=history_a,
            stream=True,
        )
        for chunk in stream:
            part = chunk['message']['content']
            print(part, end='', flush=True)
            response_a_chunk += part
        print("\n")

        # Create the full response message object for Agent A
        response_a = {'role': 'assistant', 'content': response_a_chunk}
        
        # Update histories
        history_a.append(response_a) # Add A's own response to its history
        history_b.append({'role': 'user', 'content': response_a_chunk}) # Add A's response as a prompt for B

        # --- Agent B's Turn ---
        print(f"Arturo ({MODEL_B}):")
        
        # Get response from Agent B
        response_b_chunk = ""
        stream = ollama.chat(
            model=MODEL_B,
            messages=history_b,
            stream=True,
        )
        for chunk in stream:
            part = chunk['message']['content']
            print(part, end='', flush=True)
            response_b_chunk += part
        print("\n")

        # Create the full response message object for Agent B
        response_b = {'role': 'assistant', 'content': response_b_chunk}

        # Update histories
        history_b.append(response_b) # Add B's own response to its history
        history_a.append({'role': 'user', 'content': response_b_chunk}) # Add B's response as a prompt for A

except Exception as e:
    print(f"\nAn error occurred: {e}")

finally:
    print("--- Conversation End ---")