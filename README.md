# 📚 Sanjay AI
[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sanjayai.streamlit.app/)

An intelligent and user-friendly tool designed to fetch and summarize research papers from **arXiv** based on a given topic. The system provides a **question-answering (QA)** feature that generates answers to user queries by analyzing research papers and synthesizing relevant information. Built using **Streamlit**, **Sentence Transformers**, and **Transformers** models, this tool aims to assist researchers, students, and professionals in efficiently exploring and utilizing scientific literature.

## 🚀 Features

- **Paper Fetching**: Fetch research papers from the **arXiv API** based on the user's topic.
- **Semantic Search**: Perform a semantic search on fetched papers to find the most relevant ones.
- **Question Answering**: Answer complex questions based on the summaries and titles of the fetched papers using **Flan-T5** models.
- **Interactive UI**: An intuitive and user-friendly interface powered by **Streamlit**.
- **References**: Provides references to the most relevant papers for each generated answer.

## 🛠️ Technologies Used

- **Python**
- **Streamlit**
- **Sentence Transformers**
- **Transformers (Flan-T5 model)**
- **NLTK**
- **NumPy**
- **Requests**
- **arXiv API**

## 📄 Project Setup

### 1. Prerequisites

Ensure you have **Python 3.8+** installed on your system. You can check your Python version with:

```bash
python --version
```

### 2. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/your-username/arxiv-explorer-qa.git
cd arxiv-explorer-qa
```

### 3. Install Dependencies

To install the required Python libraries, create a virtual environment (optional but recommended), and install the dependencies using the `requirements.txt` file:

```bash
# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the dependencies
pip install -r requirements.txt
```

### 4. Run the Application

Once the dependencies are installed, you can start the Streamlit app:

```bash
streamlit run app.py
```

This will open the app in your browser at `http://localhost:8501`.

## ⚙️ Usage Instructions

### Step 1: Enter a Topic
- On the home page, input a **research topic** into the text box and click **"🔍 Fetch Papers"** to retrieve relevant papers from arXiv.

### Step 2: View the Papers
- After fetching the papers, you will see a list of the top 5 relevant papers, including their titles, summaries, publication dates, and links to read more.

### Step 3: Ask a Question
- Enter a **question** related to the topic or papers in the question box and click **"🤔 Get Detailed Answer"**. The system will generate an answer by analyzing the content of the fetched papers.

### Step 4: View the Answer
- The detailed answer will be displayed along with **references** to the most relevant papers.

### Example Workflow
1. **Topic**: "Graphene Quantum Dots"
2. **Question**: "Can Graphene Quantum Dots be modified with metal oxides?"
3. **Generated Answer**: A synthesized response based on relevant papers.
4. **References**: A list of the most relevant papers cited in the answer.

## 📦 Project Structure

```bash
.
├── app.py               # Main application file
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation (this file)
```

## 📄 Exporting Requirements

To ensure that anyone cloning your repository can install the correct dependencies, you can export the dependencies by running the following command:

```bash
pip freeze > requirements.txt
```

The `requirements.txt` file will now contain all necessary dependencies, which can be installed by others using:

```bash
pip install -r requirements.txt
```

## 🧑‍💻 Contribution Guidelines

Contributions are welcome! If you'd like to improve this project:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 🙌 Acknowledgments

This project uses the following awesome libraries and resources:

- [Streamlit](https://streamlit.io/)
- [Sentence Transformers](https://www.sbert.net/)
- [Transformers by Hugging Face](https://huggingface.co/transformers/)
- [arXiv API](https://arxiv.org/help/api/)

---

Thank you for checking out the project! Feel free to contribute or suggest improvements.

---

By following these instructions, your project will be up and running quickly!
