import customtkinter as ctk
import random
import time
from threading import Thread
from datetime import datetime
import re


class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot App")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.chat_window = ctk.CTkScrollableFrame(root, width=600, height=400)
        self.chat_window.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        self.input_field = ctk.CTkEntry(root, width=570, placeholder_text="Enter a message......")
        self.input_field.grid(column=0, row=1, padx=10, pady=10)
        self.input_field.bind("<Return>", self.send_message)

        self.send_button = self.create_circular_send_button("➣", (60, 60))
        self.send_button.grid(column=1, row=1, padx=10, pady=10)

        self.user_name = "User"  # Default user name
        self.bot_name = "Bot"  # Default bot name
        self.typing_label = None  # To keep track of the typing label for updating

    def create_circular_send_button(self, symbol, size):
        send_button = ctk.CTkButton(
            self.root,
            text=symbol,
            width=10,
            height=10,
            text_color="white",
            font=("Arial", 24, "bold"),
            corner_radius=10 // 2,
            command=self.send_message
        )
        return send_button

    def send_message(self, event=None):
        user_input = self.input_field.get()
        if user_input:
            self.display_message(user_input, is_user=True)
            self.input_field.delete(0, ctk.END)
            Thread(target=self.get_response, args=(user_input,)).start()

    def get_response(self, user_input):
        time.sleep(1)  # Simulate a delay in response

        # Mapping the user input to a response function
        response_func = self.get_response_function(user_input)

        # Call the response function and get the bot's reply
        reply = response_func(user_input)

        # Display the typing effect and then the bot's response
        self.display_typing_effect()
        time.sleep(2)  # Simulate typing delay before the response
        self.update_typing_with_response(reply)

    def get_response_function(self, user_input):
        response_map = {
            "hello": self.greet,
            "yo": self.greet,
            "hi": self.greet,
            "bye": self.farewell,
            "how are you": self.how_are_you,
            "time": self.tell_time,
            "joke": self.tell_joke,
            "sad": self.express_emotion,
            "feel": self.express_emotion,
            "thank": self.express_gratitude,
            "thanks": self.express_gratitude,
            "thank you": self.express_gratitude,
            "recommend": self.recommend,
            "president": self.general_knowledge,
            "capital": self.general_knowledge,
            "who are you": self.introduce,
            "help": self.show_help,
            "play a game": self.start_guess_game,
            "guess a number": self.guess_the_number
        }

        # Iterate over possible variations of each command
        for key, func in response_map.items():
            if re.search(r'\b' + re.escape(key) + r'\b', user_input.lower()):
                return func

        return self.unknown

    def greet(self, user_input):
        return random.choice([
            f"Hello {self.user_name}! How can I assist you today?",
            f"Hi {self.user_name}! How can I help?",
            f"Hey {self.user_name}! What can I do for you?",
            f"Yo {self.user_name}! What's up? How can I help?"
        ])

    def farewell(self, user_input):
        return random.choice([
            f"Goodbye {self.user_name}! Have a fantastic day!",
            f"See you later {self.user_name}! Take care!",
            f"Bye {self.user_name}! Hope to chat again soon!"
        ])

    def how_are_you(self, user_input):
        return random.choice([
            f"I'm just a bunch of code, but I'm doing great {self.user_name}! How about you?",
            f"I'm always good, thanks for asking {self.user_name}! How are you?",
            f"I'm alive and kicking... in code! How about you {self.user_name}?"
        ])

    def tell_time(self, user_input):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"The current time is: {current_time}"

    def tell_joke(self, user_input):
        return random.choice([
            "Why don't skeletons fight each other? They don't have the guts.",
            "Why did the computer go to the doctor? It had a virus!",
            "Why don't programmers like nature? It has too many bugs.",
            "Why did the math book look sad? Because it had too many problems.",
            "Why do cows wear bells? Because their horns don’t work.",
            "Why can't your nose be 12 inches long? Because then it would be a foot!",
            "What did the ocean say to the beach? Nothing, it just waved.",
            "I told my computer I needed a break, and now it won’t stop sending me Kit-Kats!",
            "Why do chicken coops only have two doors? Because if they had four, they’d be chicken sedans.",
            "How do you organize a space party? You planet!"
        ])

    def start_guess_game(self, user_input):
        self.secret_number = random.randint(1, 100)  # Random number between 1 and 100
        self.guesses_left = 10  # Number of guesses the user has
        return "I'm thinking of a number between 1 and 100. You have 10 guesses. Try to guess it!"

    def guess_the_number(self, user_input):
        try:
            guess = int(user_input)  # Try to convert user input to an integer
        except ValueError:
            return "Please enter a valid number."

        if self.guesses_left > 0:
            if guess < self.secret_number:
                self.guesses_left -= 1
                return f"Too low! You have {self.guesses_left} guesses left."
            elif guess > self.secret_number:
                self.guesses_left -= 1
                return f"Too high! You have {self.guesses_left} guesses left."
            else:
                return f"Congratulations! You guessed the number {self.secret_number} correctly! 🎉"
        else:
            return f"Sorry, you've run out of guesses. The number was {self.secret_number}. Better luck next time!"

    def express_emotion(self, user_input):
        user_input = user_input.lower()

        if "sad" in user_input or "down" in user_input or "unhappy" in user_input:
            return random.choice([
                "I'm sorry you're feeling down. How can I make it better?",
                "It's okay to feel sad sometimes. I'm here to chat if you need me.",
                "I understand you're feeling low. Want to talk about what's bothering you?",
                "I'm really sorry you're feeling this way. You don't have to go through it alone.",
                "Sometimes life can be tough, but you're not alone. Let me know if you want to talk."
            ])

        elif "angry" in user_input or "mad" in user_input or "frustrated" in user_input:
            return random.choice([
                "I'm sorry you're feeling frustrated. Would you like to talk about what made you angry?",
                "It's okay to feel angry. Sometimes it helps to express what's on your mind.",
                "I get that you're upset. Would you like to share what's going on?",
                "Anger can be tough to deal with. I'm here to listen if you want to talk it out."
            ])

        elif "happy" in user_input or "excited" in user_input or "joyful" in user_input:
            return random.choice([
                "I'm so glad you're feeling happy! What's bringing you joy today?",
                "That's awesome! I'm glad you're feeling excited. What's going on?",
                "It's great to hear you're feeling happy! What’s making you smile?",
                "I'm so happy for you! Keep that positive energy flowing!"
            ])

        elif "anxious" in user_input or "nervous" in user_input or "stressed" in user_input:
            return random.choice([
                "I'm sorry you're feeling anxious. It's okay to take a moment for yourself.",
                "Feeling nervous can be really hard. I'm here to listen if you need to talk.",
                "I know you're stressed right now, but you're doing your best. Would you like to talk it through?",
                "It's normal to feel nervous sometimes. Take a deep breath, and I'm here if you want to chat."
            ])

        elif "lonely" in user_input or "isolated" in user_input or "alone" in user_input:
            return random.choice([
                "I'm sorry you're feeling lonely. I'm here with you. Want to talk?",
                "It sounds like you're feeling isolated. I’m here for you, let’s chat!",
                "I know loneliness can feel overwhelming, but you're not alone. How can I support you?",
                "I can tell you're feeling alone right now. You can talk to me whenever you need."
            ])

        elif "grateful" in user_input or "thankful" in user_input or "blessed" in user_input:
            return random.choice([
                "It's wonderful you're feeling grateful. What's something you're thankful for today?",
                "Gratitude can really brighten your day! What are you feeling thankful for?",
                "It’s beautiful to be grateful. What’s one thing that’s making you feel blessed right now?",
                "I'm glad you're feeling thankful. What’s been going well for you?"
            ])

        elif "scared" in user_input or "fear" in user_input or "terrified" in user_input:
            return random.choice([
                "I'm sorry you're feeling scared. It's okay to feel this way, and I'm here for you.",
                "Fear can be overwhelming, but you don't have to face it alone. Want to talk?",
                "It’s normal to feel scared sometimes. Let’s talk about what’s making you feel this way.",
                "I understand you're feeling terrified. Take your time, and I’m here to help if you need."
            ])

        else:
            return random.choice([
                "I'm here for you. Want to talk about what's on your mind?",
                "I'm sorry you're feeling this way. How can I support you?",
                "Whatever you're going through, you're not alone. Let me know how I can help.",
                "I’m here to listen. What’s on your mind?"
            ])

    def express_gratitude(self, user_input):
        return random.choice([
            "You're welcome! I'm always here to help.",
            "No problem! Let me know if you need anything else.",
            "Anytime! I'm happy to assist."
        ])

    def recommend(self, user_input):
        return random.choice([
            "If you're looking for a book recommendation, I suggest '1984' by George Orwell.",
            "How about trying some fun activities like learning a new hobby or watching a movie?",
            "I recommend exploring a new genre of music or trying a new recipe!"
        ])

    def general_knowledge(self, user_input):
        if "president" in user_input:
            if "usa" in user_input:
                return "The current president of the USA is Joe Biden."
            elif "france" in user_input:
                return "The president of France is Emmanuel Macron."
            elif "uk" in user_input or "united kingdom" in user_input:
                return "The prime minister of the UK is Rishi Sunak."
            elif "germany" in user_input:
                return "The president of Germany is Frank-Walter Steinmeier."
            elif "china" in user_input:
                return "The president of China is Xi Jinping."
            elif "russia" in user_input:
                return "The president of Russia is Vladimir Putin."
            elif "brazil" in user_input:
                return "The president of Brazil is Luiz Inácio Lula da Silva."
            elif "india" in user_input:
                return "The president of India is Droupadi Murmu."
            elif "mexico" in user_input:
                return "The president of Mexico is Andrés Manuel López Obrador."
            elif "south africa" in user_input:
                return "The president of South Africa is Cyril Ramaphosa."
            elif "australia" in user_input:
                return "The prime minister of Australia is Anthony Albanese."
            elif "canada" in user_input:
                return "The prime minister of Canada is Justin Trudeau."
            elif "argentina" in user_input:
                return "The president of Argentina is Javier Milei."
            elif "japan" in user_input:
                return "The prime minister of Japan is Fumio Kishida."
            elif "south korea" in user_input:
                return "The president of South Korea is Yoon Suk-yeol."
            elif "nigeria" in user_input:
                return "The president of Nigeria is Bola Ahmed Tinubu."
            elif "italy" in user_input:
                return "The president of Italy is Sergio Mattarella."
            elif "egypt" in user_input:
                return "The president of Egypt is Abdel Fattah el-Sisi."
            elif "turkey" in user_input:
                return "The president of Turkey is Recep Tayyip Erdoğan."


        elif "capital" in user_input:
            if "france" in user_input:
                return "The capital of France is Paris."
            elif "italy" in user_input:
                return "The capital of Italy is Rome."
            elif "spain" in user_input:
                return "The capital of Spain is Madrid."
            elif "germany" in user_input:
                return "The capital of Germany is Berlin."
            elif "canada" in user_input:
                return "The capital of Canada is Ottawa."
            elif "usa" in user_input:
                return "The capital of the USA is Washington, D.C."
            elif "uk" in user_input or "united kingdom" in user_input:
                return "The capital of the UK is London."
            elif "brazil" in user_input:
                return "The capital of Brazil is Brasília."
            elif "argentina" in user_input:
                return "The capital of Argentina is Buenos Aires."
            elif "mexico" in user_input:
                return "The capital of Mexico is Mexico City."
            elif "india" in user_input:
                return "The capital of India is New Delhi."
            elif "china" in user_input:
                return "The capital of China is Beijing."
            elif "russia" in user_input:
                return "The capital of Russia is Moscow."
            elif "australia" in user_input:
                return "The capital of Australia is Canberra."
            elif "japan" in user_input:
                return "The capital of Japan is Tokyo."
            elif "south korea" in user_input:
                return "The capital of South Korea is Seoul."
            elif "south africa" in user_input:
                return "The capital of South Africa is Pretoria."
            elif "nigeria" in user_input:
                return "The capital of Nigeria is Abuja."
            elif "egypt" in user_input:
                return "The capital of Egypt is Cairo."
            elif "turkey" in user_input:
                return "The capital of Turkey is Ankara."

        elif "largest country" in user_input:
            return "The largest country by land area is Russia."
        elif "smallest country" in user_input:
            return "The smallest country by land area is Vatican City."
        elif "longest river" in user_input:
            return "The longest river is the Nile."
        elif "highest mountain" in user_input:
            return "The highest mountain is Mount Everest."
        elif "largest ocean" in user_input:
            return "The largest ocean is the Pacific Ocean."
        elif "world population" in user_input:
            return "The world population is over 8 billion."
        elif "oldest civilization" in user_input:
            return "The oldest known civilization is the Sumerians in Mesopotamia."

        return "I can provide info about presidents, capitals, and world facts. Ask away!"

    def introduce(self, user_input):
        return "I'm an AI chatbot, here to assist you with anything you need!"

    def unknown(self, user_input):
        return random.choice([
            f"That's interesting {self.user_name}! Tell me more.",
            f"Hmm, I didn't quite get that {self.user_name}. Can you clarify?",
            f"I'm not sure how to respond to that {self.user_name}. Could you rephrase?",
            f"Sorry I don't get it."
        ])

    def show_help(self, user_input):
        return (
            "Here are the available commands:\n"
            " - hello / hi / bye\n"
            " - how are you\n"
            " - time\n"
            " - joke\n"
            " - sad / feel\n"
            " - thank / thanks / thank you\n"
            " - recommend\n"
            " - president / capital\n"
            " - who are you\n"
            " - guess a number\n"
            " - play a game\n"
            " - help"
        )

    def display_message(self, message, is_user):
        frame = ctk.CTkFrame(self.chat_window, fg_color="transparent", width=450, height=100)
        frame.pack(pady=3, anchor='e' if is_user else 'w')  # 'e' for user (right side), 'w' for bot (left side)

        avatar_text = self.user_name if is_user else self.bot_name  # Ensure correct name is displayed
        avatar_label = ctk.CTkLabel(
            frame,
            text=avatar_text,
            width=30,
            height=30,
            fg_color="transparent" if is_user else "transparent",
            text_color="white",
            corner_radius=100,
            font=("Arial", 16, "bold")
        )
        avatar_label.pack(side='right' if is_user else 'left', padx=10, pady=5)  # 'right' for user, 'left' for bot

        message_label = ctk.CTkLabel(frame, text=message, anchor='e' if is_user else 'w', text_color="white")
        message_label.pack(padx=11, pady=5)

    def display_typing_effect(self):
        frame = ctk.CTkFrame(self.chat_window, fg_color="transparent", width=450, height=100)
        frame.pack(pady=3, anchor='w')

        avatar_text = self.bot_name
        avatar_label = ctk.CTkLabel(
            frame,
            text=avatar_text,
            width=30,
            height=30,
            fg_color="transparent",
            text_color="white",
            corner_radius=100,
            font=("Arial", 16, "bold")
        )
        avatar_label.pack(side='left', padx=10, pady=5)

        typing_frame = ctk.CTkFrame(frame, fg_color="transparent", corner_radius=50)
        typing_frame.pack(side='left', fill='both', expand=True, padx=(11, 0))

        typing_label = ctk.CTkLabel(typing_frame, text="Bot is typing...", anchor='w', text_color="white")
        typing_label.pack(padx=11, pady=5)

        # Store reference to the typing label to update it later
        self.typing_label = typing_label
        self.typing_label.update_idletasks()

    def update_typing_with_response(self, response):
        if self.typing_label is not None:
            self.typing_label.configure(text=response)  # Use configure instead of config
            self.typing_label.update_idletasks()
            self.typing_label = None  # Reset the typing label reference


if __name__ == "__main__":
    root = ctk.CTk()
    ChatbotApp(root)
    root.mainloop()
