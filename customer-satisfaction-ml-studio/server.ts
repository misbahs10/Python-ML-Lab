import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import { GoogleGenAI } from "@google/genai";
import dotenv from "dotenv";

dotenv.config();

const app = express();
const PORT = 3000;

app.use(express.json());

// Lazy-initialized Gemini client to prevent crashes if key is missing on start
let aiClient: GoogleGenAI | null = null;

function getGeminiClient(): GoogleGenAI {
  if (!aiClient) {
    const key = process.env.GEMINI_API_KEY;
    if (!key) {
      throw new Error("GEMINI_API_KEY environment variable is not configured in Secrets.");
    }
    aiClient = new GoogleGenAI({
      apiKey: key,
      httpOptions: {
        headers: {
          "User-Agent": "aistudio-build",
        },
      },
    });
  }
  return aiClient;
}

// API Route: AI explanation & questions about dataset and models
app.post("/api/gemini/explain", async (req, res) => {
  try {
    const { prompt, context } = req.body;
    if (!prompt) {
      return res.status(400).json({ error: "Prompt is required." });
    }

    const ai = getGeminiClient();

    const systemInstruction = `You are an expert AI Data Scientist and Machine Learning assistant.
The user has been analyzing a customer satisfaction and purchase dataset with 350+ entries.
Key dataset attributes: Customer ID, Gender, Age, City, Membership Type, Total Spend, Items Purchased, Average Rating, Discount Applied, Days Since Last Purchase, Satisfaction Level.
The user might ask you to explain:
1. Feature engineering techniques (scaling, one-hot encoding, imputing missing values, creating interaction/ratio features).
2. Machine learning classifiers (Decision Trees split by Gini impurity, Random Forest ensembles with majority voting, Naive Bayes models).
3. Cross-validation (how K-Fold divides data to estimate out-of-sample performance).
4. Accuracy metrics (precision, recall, f1-score, confusion matrix).
5. Recommendations to improve customer satisfaction based on spending/ratings.

Provide clear, helpful, easy-to-understand explanations. Keep answers conversational, objective, and data-science focused. Avoid mentioning internal file structures. Use markdown format.`;

    const fullPrompt = context 
      ? `Context details:\n${JSON.stringify(context, null, 2)}\n\nUser Question: ${prompt}`
      : prompt;

    const response = await ai.models.generateContent({
      model: "gemini-3.5-flash",
      contents: fullPrompt,
      config: {
        systemInstruction,
        temperature: 0.7,
      },
    });

    res.json({ text: response.text });
  } catch (err: any) {
    console.error("Gemini API Error:", err);
    res.status(500).json({ 
      error: err.message || "Internal server error occurred while invoking Gemini." 
    });
  }
});

// Vite Middleware & static assets
async function setupServer() {
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Express server running on http://0.0.0.0:${PORT}`);
  });
}

setupServer();
