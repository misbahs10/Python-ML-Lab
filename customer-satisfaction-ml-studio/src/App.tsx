import React, { useState, useMemo } from "react";
import { rawDatasetCSV } from "./data/rawDataset";
import { parseCSV } from "./utils/mlEngine";
import { 
  DataRow, 
  FeatureEngineeringConfig, 
  ModelType, 
  EvaluationMetrics 
} from "./types/ml";
import DatasetViewer from "./components/DatasetViewer";
import FeatureEngineeringPanel from "./components/FeatureEngineeringPanel";
import ModelTrainer from "./components/ModelTrainer";
import PredictionPlayground from "./components/PredictionPlayground";
import AiAssistant from "./components/AiAssistant";
import { 
  Database, 
  Sparkles, 
  Cpu, 
  UserCheck, 
  BrainCircuit, 
  TrendingUp, 
  Github, 
  Info,
  ChevronRight
} from "lucide-react";

export default function App() {
  // Load and parse initial data
  const initialData = useMemo(() => parseCSV(rawDatasetCSV), []);
  const [data, setData] = useState<DataRow[]>(initialData);

  // Active step / tab in workspace
  const [activeTab, setActiveTab] = useState<"explore" | "engineering" | "train" | "playground">("explore");

  // Feature Engineering configuration
  const [feConfig, setFeConfig] = useState<FeatureEngineeringConfig>({
    imputeMethod: "mode",
    scaleNumerical: "standardize",
    enableDerivedSpendPerItem: true,
    enableDerivedPurchaseFrequency: true,
    enableDerivedDiscountSpend: true
  });

  // Trained model container state
  const [trainedModel, setTrainedModel] = useState<{
    type: ModelType;
    model: any;
    preprocessor: any;
    metrics: EvaluationMetrics;
    config: FeatureEngineeringConfig;
  } | null>(null);

  // Reset dataset to default
  const handleResetData = () => {
    setData(initialData);
    setTrainedModel(null);
  };

  // Sample row for displaying the preprocessor preview
  const previewSample = useMemo(() => {
    return data.find(row => row["Satisfaction Level"] && row["Satisfaction Level"] !== "") || data[0];
  }, [data]);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 flex flex-col font-sans">
      {/* Top Header Banner */}
      <header className="bg-white border-b border-gray-100 shadow-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="bg-indigo-600 text-white rounded-xl p-2.5 shadow-md shadow-indigo-600/10">
              <BrainCircuit className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <h1 className="text-xl font-extrabold text-gray-900 tracking-tight flex items-center gap-2">
                Customer Satisfaction ML Studio
              </h1>
              <p className="text-xs text-gray-500 font-medium">
                In-browser Machine Learning Pipeline • Feature Engineering • K-Fold Cross Validation
              </p>
            </div>
          </div>
          {trainedModel && (
            <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-100 rounded-xl px-4 py-2 text-xs font-semibold text-emerald-800">
              <span className="w-2 h-2 bg-emerald-500 rounded-full animate-ping" />
              Trained: {trainedModel.type.toUpperCase()} (CV: {(trainedModel.metrics.cvScore?.mean! * 100).toFixed(1)}%)
            </div>
          )}
        </div>
      </header>

      {/* Main Body */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* LEFT SECTION: Tabs Workspace (8 cols) */}
          <div className="lg:col-span-8 space-y-6">
            
            {/* Step-by-Step Navigation Bar */}
            <div className="bg-white p-2 rounded-2xl shadow-sm border border-gray-100 flex flex-wrap gap-1">
              {[
                { id: "explore", label: "1. Explore Dataset", icon: Database },
                { id: "engineering", label: "2. Feature Engineering", icon: Sparkles },
                { id: "train", label: "3. Train & Validate", icon: Cpu },
                { id: "playground", label: "4. Prediction Playground", icon: UserCheck }
              ].map(step => {
                const IconComp = step.icon;
                const isActive = activeTab === step.id;
                return (
                  <button
                    key={step.id}
                    onClick={() => setActiveTab(step.id as any)}
                    className={`flex-1 min-w-[150px] py-2.5 px-3 rounded-xl text-xs font-bold flex items-center justify-center gap-2 transition-all ${
                      isActive
                        ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/10"
                        : "text-gray-500 hover:text-gray-800 hover:bg-gray-50"
                    }`}
                  >
                    <IconComp className="w-4 h-4 flex-shrink-0" />
                    {step.label}
                  </button>
                );
              })}
            </div>

            {/* Content Windows per Step */}
            <div className="transition-all duration-300">
              {activeTab === "explore" && (
                <DatasetViewer 
                  data={data} 
                  onUpdateData={setData} 
                  onResetData={handleResetData} 
                />
              )}

              {activeTab === "engineering" && (
                <FeatureEngineeringPanel 
                  config={feConfig} 
                  onChangeConfig={(newCfg) => {
                    setFeConfig(newCfg);
                    setTrainedModel(null); // clear model when preprocessing changes
                  }} 
                  rawSample={previewSample}
                />
              )}

              {activeTab === "train" && (
                <ModelTrainer 
                  data={data} 
                  feConfig={feConfig} 
                  onModelTrained={setTrainedModel} 
                />
              )}

              {activeTab === "playground" && (
                <PredictionPlayground 
                  trainedContainer={trainedModel} 
                />
              )}
            </div>

            {/* Informative notice card */}
            <div className="bg-blue-50 border border-blue-100 rounded-2xl p-4 flex gap-3 text-blue-900 text-xs leading-normal">
              <Info className="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0" />
              <div>
                <span className="font-bold">ML Pipeline Steps:</span> 
                <span className="mt-1 block">
                  Pehle **Explore Dataset** me missing value rows (red) check karein. Phir **Feature Engineering** panel me categories ko one-hot encoded vector me aur numbers ko scale karein. Final model ko **Train & Validate** me train karke **Prediction Playground** me predict karein.
                </span>
              </div>
            </div>

          </div>

          {/* RIGHT SECTION: AI Companion (4 cols) */}
          <div className="lg:col-span-4 lg:sticky lg:top-24 space-y-6">
            <AiAssistant 
              currentModelType={trainedModel ? trainedModel.type : null} 
              feConfig={feConfig} 
              trainedMetrics={trainedModel ? trainedModel.metrics : null} 
            />

            {/* Informational guide */}
            <div className="bg-slate-900 text-slate-100 rounded-2xl p-5 border border-slate-950 shadow-md">
              <span className="text-[10px] font-bold text-indigo-400 uppercase tracking-wider block mb-1">Theoretical Concept</span>
              <span className="text-xs font-bold text-white block mb-2">Cross-Validation Details</span>
              <p className="text-[11px] text-slate-400 leading-relaxed mb-3">
                K-Fold splits the dataset into equal folds. Each fold is tested on a model trained on the remaining folds, providing out-of-sample error estimates before deployment.
              </p>
              <div className="text-[11px] text-slate-400 flex items-center gap-1">
                <span>Read companion guides in sidebar</span>
                <ChevronRight className="w-3.5 h-3.5 text-indigo-400" />
              </div>
            </div>
          </div>

        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-100 py-6 mt-12 text-center text-xs text-gray-500">
        <p>© 2026 Customer Satisfaction Machine Learning Studio. Built with React, Tailwind & Gemini 3.5.</p>
      </footer>
    </div>
  );
}
