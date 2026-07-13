import React, { useState, useRef, useEffect } from "react";
import { ModelType, FeatureEngineeringConfig, EvaluationMetrics } from "../types/ml";
import { 
  Bot, 
  Send, 
  Sparkles, 
  Bookmark, 
  RefreshCcw, 
  ArrowRight,
  BrainCircuit,
  MessageSquare,
  BadgeAlert
} from "lucide-react";

interface AiAssistantProps {
  currentModelType: ModelType | null;
  feConfig: FeatureEngineeringConfig;
  trainedMetrics: EvaluationMetrics | null;
}

interface Message {
  sender: "user" | "bot";
  text: string;
}

export default function AiAssistant({ currentModelType, feConfig, trainedMetrics }: AiAssistantProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      sender: "bot",
      text: "Hello! Main aapka AI Data Science Companion hoon. Mujhe is dataset, feature engineering, machine learning classifiers, ya cross-validation ke baare me kuch bhi puchiye!"
    }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const chatEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages list updates
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (textToSend: string) => {
    if (!textToSend.trim()) return;

    const newMessages = [...messages, { sender: "user", text: textToSend } as Message];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);
    setApiError(null);

    // Build context to inform Gemini about current UI configurations
    const context = {
      modelType: currentModelType || "Not trained yet",
      featureEngineering: {
        imputeMethod: feConfig.imputeMethod,
        scaleNumerical: feConfig.scaleNumerical,
        derivedFeatures: {
          spendPerItem: feConfig.enableDerivedSpendPerItem,
          purchaseFrequency: feConfig.enableDerivedPurchaseFrequency,
          discountSpend: feConfig.enableDerivedDiscountSpend
        }
      },
      metrics: trainedMetrics ? {
        trainingAccuracy: trainedMetrics.accuracy,
        cvScoreMean: trainedMetrics.cvScore?.mean,
        cvScoreStd: trainedMetrics.cvScore?.std,
        topFeatures: trainedMetrics.featureImportance?.slice(0, 3).map(f => f.feature)
      } : "Not trained yet"
    };

    try {
      const response = await fetch("/api/gemini/explain", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: textToSend, context })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to contact Gemini endpoint.");
      }

      const data = await response.json();
      setMessages([...newMessages, { sender: "bot", text: data.text }]);
    } catch (err: any) {
      console.error(err);
      setApiError(err.message || "Something went wrong.");
      setMessages([...newMessages, { sender: "bot", text: "Maaf kijiye, lagta hai API key ya connection me koi issue hai. Settings > Secrets panel check karein." }]);
    } finally {
      setIsLoading(false);
    }
  };

  const suggestions = [
    "K-Fold Cross-Validation kya hai aur kyu zaroori hai?",
    "Hamare feature engineering choices (scaling) se model accuracy pe kya farq padta hai?",
    "Bronze members ki satisfaction badhane ke liye data-driven recommendation do.",
    "Decision Tree vs Random Forest me kya diff hai aur accuracy me kaunsa behtar hai?"
  ];

  return (
    <div id="ai-assistant" className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-col h-[520px]">
      {/* Header */}
      <div className="flex items-center gap-2 border-b border-gray-100 pb-5 mb-4 flex-shrink-0">
        <div className="bg-indigo-50 p-2 rounded-xl text-indigo-600">
          <BrainCircuit className="w-5 h-5 animate-pulse" />
        </div>
        <div>
          <h2 className="text-base font-bold text-gray-900 flex items-center gap-1.5">
            AI Data Scientist Companion
            <span className="text-[10px] bg-indigo-50 text-indigo-700 font-bold px-2 py-0.5 rounded-full border border-indigo-200">
              Gemini Power
            </span>
          </h2>
          <p className="text-xs text-gray-500 mt-0.5">
            Ask questions in Urdu, Hindi, or English about your model results and parameters.
          </p>
        </div>
      </div>

      {/* Messages Window */}
      <div className="flex-1 overflow-y-auto space-y-3.5 pr-2 mb-4 scrollbar-thin">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex gap-2.5 max-w-[85%] ${
              msg.sender === "user" ? "ml-auto flex-row-reverse" : "mr-auto"
            }`}
          >
            {/* Avatar */}
            <div className={`w-7 h-7 rounded-lg flex items-center justify-center text-xs flex-shrink-0 ${
              msg.sender === "user" ? "bg-indigo-100 text-indigo-700" : "bg-slate-900 text-indigo-400"
            }`}>
              {msg.sender === "user" ? "U" : <Bot className="w-4 h-4" />}
            </div>

            {/* Bubble */}
            <div className={`rounded-2xl p-3.5 text-xs leading-relaxed border ${
              msg.sender === "user"
                ? "bg-indigo-600 text-white border-indigo-600 rounded-tr-none"
                : "bg-slate-50 text-slate-800 border-slate-100 rounded-tl-none whitespace-pre-line"
            }`}>
              {msg.text}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex gap-2.5 max-w-[85%] mr-auto items-center">
            <div className="w-7 h-7 rounded-lg bg-slate-900 text-indigo-400 flex items-center justify-center text-xs flex-shrink-0">
              <Bot className="w-4 h-4" />
            </div>
            <div className="bg-slate-50 border border-slate-100 rounded-2xl p-3.5 text-xs rounded-tl-none text-slate-400 flex items-center gap-1">
              <span>Companion is typing</span>
              <span className="inline-flex gap-0.5 ml-1">
                <span className="w-1 h-1 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                <span className="w-1 h-1 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                <span className="w-1 h-1 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
              </span>
            </div>
          </div>
        )}

        {apiError && (
          <div className="p-3 bg-red-50 border border-red-100 text-[11px] text-red-700 rounded-xl flex items-start gap-2">
            <BadgeAlert className="w-4 h-4 mt-0.5 flex-shrink-0" />
            <div>
              <span className="font-bold block">Gemini Error:</span>
              <span className="block">{apiError}</span>
            </div>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Suggested chips if chat is fresh */}
      {messages.length === 1 && (
        <div className="mb-4 flex-shrink-0">
          <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider block mb-2">Suggested Topics</span>
          <div className="flex flex-wrap gap-1.5">
            {suggestions.map((s, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(s)}
                className="text-left text-[11px] px-3 py-1.5 bg-gray-50 border border-gray-100 hover:bg-indigo-50/50 hover:border-indigo-100 hover:text-indigo-950 text-slate-700 rounded-lg transition-all truncate max-w-full"
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Form Input */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSend(input);
        }}
        className="flex gap-2 border-t border-gray-100 pt-3 flex-shrink-0"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about hyperparameters, Gini impurity, etc..."
          disabled={isLoading}
          className="flex-1 px-3.5 py-2.5 border border-gray-200 rounded-xl text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl flex items-center justify-center transition-colors disabled:opacity-50"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
