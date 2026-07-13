import React, { useState } from "react";
import { 
  ModelType, 
  ModelPredictionInput, 
  FeatureEngineeringConfig,
  EvaluationMetrics
} from "../types/ml";
import { 
  DataPreprocessor, 
  DecisionTreeClassifier, 
  RandomForestClassifier, 
  NaiveBayesClassifier 
} from "../utils/mlEngine";
import { 
  UserCheck, 
  HelpCircle, 
  AlertCircle, 
  ChevronRight, 
  BadgeHelp,
  Gauge,
  Sparkles,
  TrendingUp,
  Percent
} from "lucide-react";

interface PredictionPlaygroundProps {
  trainedContainer: {
    type: ModelType;
    model: DecisionTreeClassifier | RandomForestClassifier | NaiveBayesClassifier;
    preprocessor: DataPreprocessor;
    metrics: EvaluationMetrics;
    config: FeatureEngineeringConfig;
  } | null;
}

export default function PredictionPlayground({ trainedContainer }: PredictionPlaygroundProps) {
  // Input Form State
  const [inputs, setInputs] = useState<ModelPredictionInput>({
    Gender: "Female",
    Age: 29,
    City: "New York",
    "Membership Type": "Gold",
    "Total Spend": 1120.2,
    "Items Purchased": 14,
    "Average Rating": 4.6,
    "Discount Applied": true,
    "Days Since Last Purchase": 25
  });

  const [prediction, setPrediction] = useState<string | null>(null);
  const [probabilities, setProbabilities] = useState<Record<string, number> | null>(null);

  const handlePredict = () => {
    if (!trainedContainer) return;

    const { model, preprocessor } = trainedContainer;

    // Preprocess prediction input using the trained parameters
    const featureVector = preprocessor.transformPredictionInput(inputs);

    // Predict
    const predClass = model.predict([featureVector])[0];
    setPrediction(predClass);

    // Predict probabilities (if Random Forest or Naive Bayes)
    if (trainedContainer.type === "random_forest") {
      const probs = (model as RandomForestClassifier).predictProbs(featureVector);
      setProbabilities(probs);
    } else if (trainedContainer.type === "naive_bayes") {
      const probs = (model as NaiveBayesClassifier).predictProbs(featureVector);
      setProbabilities(probs);
    } else {
      // Decision tree output as 100% confidence for simplicity or 0% for others
      setProbabilities({
        Satisfied: predClass === "Satisfied" ? 1.0 : 0.0,
        Neutral: predClass === "Neutral" ? 1.0 : 0.0,
        Unsatisfied: predClass === "Unsatisfied" ? 1.0 : 0.0
      });
    }
  };

  const setRandomFromDataset = () => {
    // Generate some interesting pre-populated profiles
    const profiles = [
      {
        Gender: "Male",
        Age: 45,
        City: "Chicago",
        "Membership Type": "Bronze",
        "Total Spend": 210.5,
        "Items Purchased": 4,
        "Average Rating": 2.8,
        "Discount Applied": false,
        "Days Since Last Purchase": 45
      },
      {
        Gender: "Female",
        Age: 31,
        City: "San Francisco",
        "Membership Type": "Gold",
        "Total Spend": 1540.8,
        "Items Purchased": 22,
        "Average Rating": 4.9,
        "Discount Applied": true,
        "Days Since Last Purchase": 8
      },
      {
        Gender: "Male",
        Age: 35,
        City: "Los Angeles",
        "Membership Type": "Silver",
        "Total Spend": 780.2,
        "Items Purchased": 11,
        "Average Rating": 4.1,
        "Discount Applied": false,
        "Days Since Last Purchase": 16
      }
    ];

    const idx = Math.floor(Math.random() * profiles.length);
    setInputs(profiles[idx]);
    setPrediction(null);
    setProbabilities(null);
  };

  const handleFieldChange = (key: keyof ModelPredictionInput, val: any) => {
    setInputs({
      ...inputs,
      [key]: val
    });
    // Clear old prediction when inputs change
    setPrediction(null);
    setProbabilities(null);
  };

  return (
    <div id="prediction-playground" className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-100 pb-5 mb-6">
        <div>
          <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
            <UserCheck className="w-5 h-5 text-indigo-600" />
            Prediction Playground
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            Test custom client inputs and see live model inferences and confidence outputs.
          </p>
        </div>
        {trainedContainer && (
          <button
            onClick={setRandomFromDataset}
            className="px-3.5 py-1.5 bg-indigo-50 text-indigo-600 hover:bg-indigo-100 rounded-lg text-xs font-semibold transition-colors self-start"
          >
            🎲 Load Pre-set Profile
          </button>
        )}
      </div>

      {!trainedContainer ? (
        <div className="bg-amber-50 rounded-2xl p-6 border border-amber-200 flex items-start gap-3.5 text-amber-900 text-sm">
          <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
          <div>
            <span className="font-bold block">Model Not Trained Yet!</span>
            <span className="text-xs text-amber-800 leading-normal block mt-1">
              Custom prediction chalane se pehle, upar **"Model Training & Validation"** tab me jaakar model train karein. Training pipeline complete hote hi playground automatic activate ho jayega.
            </span>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column: Interactive Form */}
          <div className="lg:col-span-7 space-y-4">
            <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-2">Input Customer Parameters</h3>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm text-gray-700">
              {/* Gender */}
              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">Gender</label>
                <select
                  value={inputs.Gender}
                  onChange={(e) => handleFieldChange("Gender", e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
                >
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                </select>
              </div>

              {/* Age */}
              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">Age (years)</label>
                <input
                  type="number"
                  min="15"
                  max="90"
                  value={inputs.Age}
                  onChange={(e) => handleFieldChange("Age", parseInt(e.target.value, 10) || 0)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
              </div>

              {/* City */}
              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">City</label>
                <select
                  value={inputs.City}
                  onChange={(e) => handleFieldChange("City", e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
                >
                  <option value="New York">New York</option>
                  <option value="Los Angeles">Los Angeles</option>
                  <option value="Chicago">Chicago</option>
                  <option value="San Francisco">San Francisco</option>
                  <option value="Miami">Miami</option>
                  <option value="Houston">Houston</option>
                </select>
              </div>

              {/* Membership Type */}
              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">Membership Type</label>
                <select
                  value={inputs["Membership Type"]}
                  onChange={(e) => handleFieldChange("Membership Type", e.target.value)}
                  className="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
                >
                  <option value="Gold">Gold</option>
                  <option value="Silver">Silver</option>
                  <option value="Bronze">Bronze</option>
                </select>
              </div>

              {/* Total Spend */}
              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">Total Spend ($)</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={inputs["Total Spend"]}
                  onChange={(e) => handleFieldChange("Total Spend", parseFloat(e.target.value) || 0)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
              </div>

              {/* Items Purchased */}
              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">Items Purchased</label>
                <input
                  type="number"
                  min="0"
                  value={inputs["Items Purchased"]}
                  onChange={(e) => handleFieldChange("Items Purchased", parseInt(e.target.value, 10) || 0)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
              </div>

              {/* Average Rating */}
              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">Average Rating (1.0 to 5.0)</label>
                <input
                  type="number"
                  step="0.1"
                  min="1.0"
                  max="5.0"
                  value={inputs["Average Rating"]}
                  onChange={(e) => handleFieldChange("Average Rating", parseFloat(e.target.value) || 0)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
              </div>

              {/* Days Since Last Purchase */}
              <div className="space-y-1">
                <label className="text-xs font-semibold text-gray-700">Days Since Last Purchase</label>
                <input
                  type="number"
                  min="0"
                  value={inputs["Days Since Last Purchase"]}
                  onChange={(e) => handleFieldChange("Days Since Last Purchase", parseInt(e.target.value, 10) || 0)}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
              </div>
            </div>

            {/* Discount Applied Switch */}
            <div className="flex items-center gap-3 p-3 bg-slate-50 border border-slate-100 rounded-xl">
              <input
                id="discount-play"
                type="checkbox"
                checked={inputs["Discount Applied"]}
                onChange={(e) => handleFieldChange("Discount Applied", e.target.checked)}
                className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
              />
              <label htmlFor="discount-play" className="text-xs font-bold text-slate-700 cursor-pointer">
                Discount Applied on last order
              </label>
            </div>

            <button
              onClick={handlePredict}
              className="w-full py-3 bg-indigo-600 text-white hover:bg-indigo-700 rounded-xl font-bold text-sm shadow-sm flex items-center justify-center gap-2 transition-colors mt-6"
            >
              <Gauge className="w-4 h-4" /> Predict Customer Satisfaction
            </button>
          </div>

          {/* Right Column: Prediction Results & Confidence */}
          <div className="lg:col-span-5 bg-slate-50 rounded-2xl p-6 border border-slate-100 flex flex-col justify-between">
            {prediction ? (
              <div className="space-y-6 animate-fade-in">
                {/* Score badge */}
                <div className="text-center">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Predicted Satisfaction</span>
                  <div className="mt-3 inline-block">
                    <span className={`px-5 py-2.5 rounded-2xl text-base font-extrabold shadow-sm ${
                      prediction === "Satisfied" ? "bg-emerald-500 text-white" :
                      prediction === "Neutral" ? "bg-amber-500 text-white" :
                      "bg-red-500 text-white"
                    }`}>
                      {prediction}
                    </span>
                  </div>
                </div>

                {/* Probability meters */}
                {probabilities && (
                  <div className="space-y-3.5 bg-white p-4 rounded-xl border border-slate-200">
                    <span className="text-xs font-bold text-slate-700 flex items-center gap-1">
                      <Percent className="w-3.5 h-3.5 text-indigo-500" /> Class Probabilities
                    </span>

                    <div className="space-y-2.5 text-xs text-slate-600 font-mono">
                      {/* Satisfied meter */}
                      <div className="space-y-1">
                        <div className="flex justify-between font-sans">
                          <span className="font-semibold text-gray-800">Satisfied:</span>
                          <span className="font-bold">{(probabilities.Satisfied * 100).toFixed(0)}%</span>
                        </div>
                        <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-emerald-500 transition-all duration-500" 
                            style={{ width: `${probabilities.Satisfied * 100}%` }}
                          />
                        </div>
                      </div>

                      {/* Neutral meter */}
                      <div className="space-y-1">
                        <div className="flex justify-between font-sans">
                          <span className="font-semibold text-gray-800">Neutral:</span>
                          <span className="font-bold">{(probabilities.Neutral * 100).toFixed(0)}%</span>
                        </div>
                        <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-amber-500 transition-all duration-500" 
                            style={{ width: `${probabilities.Neutral * 100}%` }}
                          />
                        </div>
                      </div>

                      {/* Unsatisfied meter */}
                      <div className="space-y-1">
                        <div className="flex justify-between font-sans">
                          <span className="font-semibold text-gray-800">Unsatisfied:</span>
                          <span className="font-bold">{(probabilities.Unsatisfied * 100).toFixed(0)}%</span>
                        </div>
                        <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                          <div 
                            className="h-full bg-red-500 transition-all duration-500" 
                            style={{ width: `${probabilities.Unsatisfied * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Model reasoning context */}
                <div className="bg-white p-4 rounded-xl border border-slate-200 text-xs text-slate-600 leading-normal">
                  <span className="font-bold text-slate-800 block mb-1">🔍 Prediction Logic Breakdown:</span>
                  {prediction === "Satisfied" && (
                    <p>
                      Customer high spend (<strong className="text-emerald-600">${inputs["Total Spend"]}</strong>) with rating <strong className="text-emerald-600">{inputs["Average Rating"]}★</strong> provides strong positive weight. Gold/Silver membership increases premium affinity scores.
                    </p>
                  )}
                  {prediction === "Neutral" && (
                    <p>
                      The combination of moderate spend (<strong className="text-amber-600">${inputs["Total Spend"]}</strong>) and silver/bronze membership displays average engagement. Recency of <strong className="text-amber-600">{inputs["Days Since Last Purchase"]} days</strong> holds standard retention patterns.
                    </p>
                  )}
                  {prediction === "Unsatisfied" && (
                    <p>
                      Low spend (<strong className="text-red-600">${inputs["Total Spend"]}</strong>) paired with Bronze membership and rating <strong className="text-red-600">{inputs["Average Rating"]}★</strong> strongly flags dissatisfaction. Long purchase delay of <strong className="text-red-600">{inputs["Days Since Last Purchase"]} days</strong> confirms churn alert.
                    </p>
                  )}
                </div>
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-center p-8 text-gray-400">
                <Sparkles className="w-8 h-8 text-indigo-400 animate-pulse mb-3" />
                <span className="text-xs font-bold text-slate-700">Awaiting Form Submission</span>
                <span className="text-[11px] text-slate-400 leading-normal block mt-1 px-3">
                  Adjust custom values on the left form and click **Predict Satisfaction** to run full real-time model inferences.
                </span>
              </div>
            )}

            {/* Config metadata footer */}
            <div className="border-t border-slate-200/60 pt-4 mt-6 flex justify-between items-center text-[10px] text-slate-400">
              <span>Active Model: <strong className="text-slate-600">{trainedContainer.type.toUpperCase()}</strong></span>
              <span>Dimensions: <strong className="text-slate-600">{trainedContainer.metrics.cvScore?.folds.length || 5}-Fold CV</strong></span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
