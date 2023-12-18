import streamlit as st
import openai
import random

openai.api_key = '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'


def main():
    
    st.markdown(
        """
        <style>
            body {
                background-color: #e0b482;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    
    logo = st.image("PwC_logo_PricewaterhouseCoopers.png", use_column_width=False, width=150)
    
    
    st.title("qAIz")

    # Input options
    topic = st.text_input("Enter the topic for the quiz:")
    num_questions = st.number_input("Number of questions:", min_value=1, step=1, value=5)

    
    questions, options, answers = generate_questions(topic, num_questions)

    # Display questions and options
    st.header("Quiz Questions:")
    for i, (question, option) in enumerate(zip(questions, options), start=1):
        st.write(f"{i}. {question}")
        user_answer = st.radio("Select the correct option:", option, key=f"question_{i}")
        st.write(f"Your Answer: {user_answer}")
        st.write(f"Correct Answer: {answers[i-1]}")
        st.write("----")

    

    # Submir button
    if st.button("Submit"):
        st.experimental_rerun()


def generate_questions(topic, num_questions):
    questions = []
    options = []
    answers = []

    for _ in range(num_questions):
        prompt = f"Generate one multiple choice question on the topic of {topic}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
        )
        ansresponse = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Which option letter is the answer. State just the option and nothing else",
            max_tokens=150,
            n=1,
        )

        question = response['choices'][0]['text'].strip()
        answer = ansresponse['choices'][0]['text'].strip()

        # Generating options for the correct answer
        options_set = set([answer])
        while len(options_set) < 4:
            options_set.add(generate_random_option())

        # options
        options_list = list(options_set)
        random.shuffle(options_list)

        questions.append(question)
        options.append(options_list)
        answers.append(answer)

    return questions, options, answers

# Generate a random option letter (A, B, C, or D)
def generate_random_option():
    return random.choice(['A', 'B', 'C', 'D'])

if __name__ == "__main__":
    main()
