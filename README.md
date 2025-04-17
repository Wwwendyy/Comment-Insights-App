# 🧠 Comment Insights App

This project is a simple web application that allows users to upload an Excel or CSV file of unstructured consumer comments and automatically classifies each comment using a powerful Large Language Model (LLM) API. The processed output includes:

- **Sentiment**: Positive, Neutral, or Negative  
- **Category**: Broad topic such as Delivery, Product Quality, Customer Service, etc.  
- **Key Themes**: Highlighted key phrases from the comment  

## 🌐 Live Access

**Login Credentials**:  
- **Username**: `admin`  
- **Password**: `password123`  

---

## 🗂 Sample Input

Upload an Excel or CSV file with the following structure:

```csv
Comment
"The delivery was fast, but the packaging was damaged."
"I love the design, but the material feels cheap."
...
```

---

## 📤 Output

After processing, the app will display a table and also allow you to download a structured file (CSV) with these columns:

| Comment                                           | Sentiment | Category         | Key Themes                     |
|---------------------------------------------------|-----------|------------------|--------------------------------|
| "The delivery was fast, but the packaging..."     | Mixed     | Delivery         | fast delivery, damaged package |
| "I love the design, but the material feels cheap" | Mixed     | Product Quality  | design, cheap material         |

---

## 🧰 Tech Stack

- **Frontend**: React.js (or Next.js)  
- **Backend**: Python (Flask / FastAPI)  
- **Authentication**: Simple username/password login  
- **File Upload**: Excel (.xlsx) and CSV supported  
- **LLM API**: OpenAI GPT-4 / DeepSeek / Other configurable APIs  
- **Data Processing**: Pandas  
- **Hosting**: Localhost / Server IP / Public URL  

---

## ⚙️ How It Works

1. **Login**: Users log into the app.
2. **Upload File**: Upload an Excel or CSV file of comments.
3. **Process**: Click "Process" to send each comment to the LLM.
4. **Results**: View structured data in a table, and optionally download results.
5. **Logs**: Any failed API calls or parsing errors will be logged with timestamps.

---

## 🧪 Testing & Example Data

Test the app with the following example comments:

- "The product quality exceeded my expectations."
- "The website is user-friendly and easy to navigate."
- "The product stopped working after a week."

Or upload your own comments in English or Chinese.

---

## 🔐 Security Notes

- The LLM API key is **not hardcoded**. Use `.env` file to securely store credentials.
- User authentication ensures that only authorized users can access the app.

---

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/comment-insights-app.git
cd comment-insights-app
```

### 2. Set up Environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Add API Keys

Create a `.env` file:

```env
LLM_API_KEY=your_openai_or_deepseek_key
```

### 4. Run the App

```bash
python app.py
# Or with FastAPI: uvicorn app:app --reload
```

Then open your browser at: `http://localhost:8000` (or server IP).

---

## 📦 Output File

The structured result can be downloaded as `categorized_comments.csv`.

---

## 👩‍💻 Contributors

- Wenjun Dong  

---
