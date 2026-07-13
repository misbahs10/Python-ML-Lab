import React, { useState, useMemo } from "react";
import { 
  ModelType, 
  ModelHyperparameters, 
  DataRow, 
  FeatureEngineeringConfig,
  EvaluationMetrics
} from "../types/ml";
import { 
  DataPreprocessor, 
  DecisionTreeClassifier, 
  RandomForestClassifier, 
  NaiveBayesClassifier, 
  evaluateModel, 
  crossValidate 
} from "../utils/mlEngine";
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer 
} from "recharts";
import { 
  Play, 
  Cpu, 
  Layers, 
  Sliders, 
  Grid, 
  GitBranch, 
  CheckCircle2, 
  Activity, 
  HelpCircle,
  Clock,
  Sparkles
} from "lucide-react";

interface ModelTrainerProps {
  data: DataRow[];
  feConfig: FeatureEngineeringConfig;
  onModelTrained: (trainedContainer: {
    type: ModelType;
    model: DecisionTreeClassifier | RandomForestClassifier | NaiveBayesClassifier;
    preprocessor: DataPreprocessor;
    metrics: EvaluationMetrics;
    config: FeatureEngineeringConfig;
  }) => void;
}

export default function ModelTrainer({ data, feConfig, onModelTrained }: ModelTrainerProps) {
  const [modelType, setModelType] = useState<ModelType>("random_forest");
  const [cvFolds, setCvFolds] = useState<number>(5);
  
  // Model hyperparameters
  const [hyperparams, setHyperparams] = useState<ModelHyperparameters>({
    maxDepth: 5,
    minSamplesSplit: 2,
    numTrees: 10
  });

  const [isTraining, setIsTraining] = useState(false);
  const [trainingLog, setTrainingLog] = useState<string[]>([]);
  const [results, setResults] = useState<EvaluationMetrics | null>(null);

  const handleTrain = async () => {
    setIsTraining(true);
    setTrainingLog([]);
    setResults(null);

    const logs: string[] = [];
    const addLog = (msg: string) => {
      logs.push(msg);
      setTrainingLog([...logs]);
    };

    // Simulate standard training logs for real-time engagement feel
    addLog("🚀 Machine learning pipeline initialized...");
    await new Promise(r => setTimeout(r, 200));

    // 1. Data preprocessing
    addLog(`⚙️ Feature Engineering applied (Scaling: ${feConfig.scaleNumerical}, Imputation: ${feConfig.imputeMethod})...`);
    const preprocessor = new DataPreprocessor(feConfig);
    const { X, y } = preprocessor.fitAndTransform(data);
    addLog(`📦 Cleaned dataset shapes: Features X = [${X.length} x ${X[0].length}], Targets y = [${y.length}]`);
    await new Promise(r => setTimeout(r, 200));

    // 2. K-Fold Cross Validation
    addLog(`🔄 Running ${cvFolds}-fold Cross-Validation using ${modelType.toUpperCase()}...`);
    const cvResult = crossValidate(X, y, modelType, hyperparams, preprocessor.featureNames, cvFolds);
    addLog(`📊 Fold accuracies: [${cvResult.folds.join(", ")}]`);
    addLog(`📈 Validation Accuracy (Mean): ${(cvResult.mean * 100).toFixed(2)}% (StdDev: ${(cvResult.std * 100).toFixed(2)}%)`);
    await new Promise(r => setTimeout(r, 250));

    // 3. Train final model on entire clean dataset
    addLog(`🧠 Training final model on 100% of dataset records...`);
    let finalModel: DecisionTreeClassifier | RandomForestClassifier | NaiveBayesClassifier;

    if (modelType === "decision_tree") {
      finalModel = new DecisionTreeClassifier(hyperparams.maxDepth, hyperparams.minSamplesSplit);
    } else if (modelType === "random_forest") {
      finalModel = new RandomForestClassifier(hyperparams.numTrees, hyperparams.maxDepth, hyperparams.minSamplesSplit);
    } else {
      finalModel = new NaiveBayesClassifier();
    }

    finalModel.fit(X, y, preprocessor.featureNames);
    const preds = finalModel.predict(X);
    addLog(`🎉 Model fit complete. Generating performance statistics...`);
    await new Promise(r => setTimeout(r, 200));

    // Calculate accuracy and classification matrix
    const evalMetrics = evaluateModel(y, preds);
    evalMetrics.cvScore = cvResult;

    // Feature Importances
    if (modelType === "decision_tree" || modelType === "random_forest") {
      const importances = (finalModel as DecisionTreeClassifier | RandomForestClassifier).getFeatureImportance();
      const mappedImp = preprocessor.featureNames.map((name, idx) => ({
        feature: name,
        importance: Math.round(importances[idx] * 1000) / 1000
      })).sort((a, b) => b.importance - a.importance);
      
      evalMetrics.featureImportance = mappedImp;
      addLog(`✨ Top predictor feature identified: ${mappedImp[0]?.feature || "None"} (${(mappedImp[0]?.importance * 100 || 0).toFixed(1)}%)`);
    }

    setResults(evalMetrics);
    setIsTraining(false);

    // Pass trained parameters up
    onModelTrained({
      type: modelType,
      model: finalModel,
      preprocessor,
      metrics: evalMetrics,
      config: feConfig
    });
  };

  // Convert feature importance array to clean sorted format for chart
  const featureImportanceChartData = useMemo(() => {
    if (!results?.featureImportance) return [];
    // Show top 8 features for readability
    return results.featureImportance.slice(0, 8);
  }, [results]);

  const updateHyperparam = (key: keyof ModelHyperparameters, val: number) => {
    setHyperparams({
      ...hyperparams,
      [key]: val
    });
  };

  return (
    <div id="model-trainer" className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-100 pb-5 mb-6">
        <div className="flex items-center gap-2">
          <Cpu className="w-5 h-5 text-indigo-600" />
          <div>
            <h2 className="text-xl font-bold text-gray-900">Model Training & Validation</h2>
            <p className="text-sm text-gray-500 mt-1">
              Configure hyperparameters, perform cross-validation, and evaluate accuracy.
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Configuration & Triggers */}
        <div className="lg:col-span-5 space-y-6 border-r border-gray-50 pr-0 lg:pr-8">
          <h3 className="text-sm font-bold text-gray-800 flex items-center gap-1.5 uppercase tracking-wide">
            <Sliders className="w-4 h-4 text-indigo-500" /> Hyperparameter Tuning
          </h3>

          {/* Model selection */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-gray-700">Select Classifier Algorithm</label>
            <div className="space-y-2">
              {[
                { id: "random_forest", name: "Random Forest Classifier", desc: "Bootstrap ensemble of decision trees. Highly accurate." },
                { id: "decision_tree", name: "Decision Tree Classifier", desc: "Single decision flow with nodes split on Gini impurity. Interpretable." },
                { id: "naive_bayes", name: "Gaussian Naive Bayes", desc: "Probabilistic classifier assuming independent feature distributions." }
              ].map(opt => (
                <button
                  key={opt.id}
                  onClick={() => setModelType(opt.id as ModelType)}
                  className={`w-full p-3 rounded-xl border text-left flex items-start gap-3 transition-all ${
                    modelType === opt.id
                      ? "border-indigo-600 bg-indigo-50/50 text-indigo-900"
                      : "border-gray-100 hover:border-gray-200 text-gray-600"
                  }`}
                >
                  <input
                    type="radio"
                    checked={modelType === opt.id}
                    onChange={() => {}} // Handled by button click
                    className="mt-1 h-3.5 w-3.5 text-indigo-600 focus:ring-indigo-500 border-gray-300"
                  />
                  <div>
                    <span className="text-xs font-bold block">{opt.name}</span>
                    <span className="text-[11px] text-gray-400 mt-0.5 block leading-normal">{opt.desc}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Hyperparameters based on Model Type */}
          {modelType !== "naive_bayes" && (
            <div className="bg-slate-50 p-4 rounded-xl border border-slate-100 space-y-4">
              <span className="text-xs font-bold text-slate-700 block mb-2">Algorithm Hyperparameters</span>
              
              {modelType === "random_forest" && (
                <div className="space-y-1.5">
                  <div className="flex justify-between text-xs text-slate-600">
                    <span className="font-bold">Number of Trees (Ensemble Size)</span>
                    <span className="font-mono bg-indigo-50 text-indigo-700 px-1.5 rounded">{hyperparams.numTrees} trees</span>
                  </div>
                  <input
                    type="range"
                    min="2"
                    max="30"
                    value={hyperparams.numTrees}
                    onChange={(e) => updateHyperparam("numTrees", parseInt(e.target.value, 10))}
                    className="w-full accent-indigo-600"
                  />
                  <span className="text-[10px] text-slate-400 block">Higher trees reduce overfitting but increase training latency.</span>
                </div>
              )}

              <div className="space-y-1.5">
                <div className="flex justify-between text-xs text-slate-600">
                  <span className="font-bold">Max Tree Depth</span>
                  <span className="font-mono bg-indigo-50 text-indigo-700 px-1.5 rounded">{hyperparams.maxDepth} levels</span>
                </div>
                <input
                  type="range"
                  min="2"
                  max="12"
                  value={hyperparams.maxDepth}
                  onChange={(e) => updateHyperparam("maxDepth", parseInt(e.target.value, 10))}
                  className="w-full accent-indigo-600"
                />
                <span className="text-[10px] text-slate-400 block">Restricts maximum split levels. Lower depth avoids overfitting.</span>
              </div>

              <div className="space-y-1.5">
                <div className="flex justify-between text-xs text-slate-600">
                  <span className="font-bold">Min Samples Split</span>
                  <span className="font-mono bg-indigo-50 text-indigo-700 px-1.5 rounded">{hyperparams.minSamplesSplit} records</span>
                </div>
                <input
                  type="range"
                  min="2"
                  max="15"
                  value={hyperparams.minSamplesSplit}
                  onChange={(e) => updateHyperparam("minSamplesSplit", parseInt(e.target.value, 10))}
                  className="w-full accent-indigo-600"
                />
                <span className="text-[10px] text-slate-400 block">Minimum dataset samples required to split an internal tree node.</span>
              </div>
            </div>
          )}

          {/* Cross Validation Folds */}
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs text-slate-600">
              <span className="font-bold">Cross-Validation folds (K-Fold)</span>
              <span className="font-mono bg-indigo-50 text-indigo-700 px-1.5 rounded">{cvFolds}-Folds</span>
            </div>
            <div className="grid grid-cols-3 gap-2">
              {[3, 5, 10].map(k => (
                <button
                  key={k}
                  onClick={() => setCvFolds(k)}
                  className={`py-1.5 text-xs font-bold rounded-lg border transition-all ${
                    cvFolds === k
                      ? "border-indigo-600 bg-indigo-50 text-indigo-700"
                      : "border-gray-200 hover:border-gray-300 text-gray-500"
                  }`}
                >
                  {k}-Fold
                </button>
              ))}
            </div>
          </div>

          {/* Trigger button */}
          <button
            onClick={handleTrain}
            disabled={isTraining}
            className="w-full py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 font-bold text-sm flex items-center justify-center gap-2 shadow-sm shadow-indigo-600/10 disabled:opacity-50 transition-all active:scale-[0.98]"
          >
            <Play className={`w-4 h-4 ${isTraining ? "animate-spin" : ""}`} />
            {isTraining ? "Training Model..." : "Train & Cross-Validate Model"}
          </button>

          {/* Training Logs Stream */}
          {trainingLog.length > 0 && (
            <div className="bg-slate-900 rounded-xl p-4 border border-slate-950 font-mono text-[10px] text-indigo-300 space-y-1 max-h-48 overflow-y-auto">
              <div className="text-slate-400 border-b border-slate-800 pb-1 mb-2 flex items-center gap-1">
                <Clock className="w-3.5 h-3.5" /> Pipeline Console
              </div>
              {trainingLog.map((log, idx) => (
                <div key={idx} className="leading-relaxed whitespace-pre-wrap">
                  {log}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Right Column: Performance Results */}
        <div className="lg:col-span-7 space-y-6">
          <h3 className="text-sm font-bold text-gray-800 flex items-center gap-1.5 uppercase tracking-wide">
            <Activity className="w-4 h-4 text-indigo-500" /> Training Results
          </h3>

          {results ? (
            <div className="space-y-6 animate-fade-in">
              {/* Metrics cards */}
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-emerald-50 rounded-xl p-4 border border-emerald-100 text-center">
                  <span className="text-[10px] font-bold text-emerald-700 uppercase tracking-wider block">Training Accuracy</span>
                  <p className="text-2xl font-extrabold text-emerald-900 mt-1">{(results.accuracy * 100).toFixed(1)}%</p>
                </div>
                <div className="bg-indigo-50 rounded-xl p-4 border border-indigo-100 text-center col-span-2">
                  <span className="text-[10px] font-bold text-indigo-700 uppercase tracking-wider block">
                    {cvFolds}-Fold Cross-Validation Accuracy
                  </span>
                  <p className="text-2xl font-extrabold text-indigo-900 mt-1">
                    {(results.cvScore?.mean! * 100).toFixed(1)}%
                    <span className="text-xs font-normal text-indigo-500 ml-1">
                      (&plusmn;{(results.cvScore?.std! * 100).toFixed(1)}%)
                    </span>
                  </p>
                </div>
              </div>

              {/* Class report table */}
              <div className="bg-gray-50 rounded-xl p-4 border border-gray-100">
                <span className="text-xs font-bold text-gray-700 block mb-3">Classification Report (Class-wise precision/recall)</span>
                
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs font-mono">
                    <thead className="bg-white/80 text-gray-500 border-b border-gray-100">
                      <tr>
                        <th className="py-2 px-3 text-left">Class Name</th>
                        <th className="py-2 px-3 text-right">Precision</th>
                        <th className="py-2 px-3 text-right">Recall</th>
                        <th className="py-2 px-3 text-right">F1-Score</th>
                        <th className="py-2 px-3 text-right">Support</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {Object.entries(results.classMetrics).map(([c, m]) => {
                        const metrics = m as any;
                        return (
                          <tr key={c} className="hover:bg-white/50">
                            <td className="py-2 px-3 text-left font-sans font-bold text-gray-800">{c}</td>
                            <td className="py-2 px-3 text-right text-indigo-600 font-bold">{metrics.precision.toFixed(2)}</td>
                            <td className="py-2 px-3 text-right text-indigo-600 font-bold">{metrics.recall.toFixed(2)}</td>
                            <td className="py-2 px-3 text-right text-indigo-600 font-bold">{metrics.f1.toFixed(2)}</td>
                            <td className="py-2 px-3 text-right text-gray-400">{metrics.support}</td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Grid: Confusion Matrix & Feature Importance */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Confusion Matrix Heatmap */}
                <div className="bg-white rounded-xl p-4 border border-gray-100 flex flex-col justify-between">
                  <div>
                    <span className="text-xs font-bold text-gray-700 block mb-3">Confusion Matrix Heatmap</span>
                    <div className="grid grid-cols-4 gap-1.5 max-w-xs mx-auto text-center text-xs font-mono">
                      {/* Empty top corner */}
                      <div></div>
                      {results.confusionMatrix.classes.map(c => (
                        <div key={c} className="text-[10px] text-gray-400 truncate" title={`Predicted ${c}`}>
                          Pred {c.substring(0, 3)}
                        </div>
                      ))}

                      {results.confusionMatrix.classes.map((actClass, actIdx) => (
                        <React.Fragment key={actClass}>
                          {/* Row Header */}
                          <div className="text-[10px] text-gray-400 text-left flex items-center pr-1 font-bold">
                            Act {actClass.substring(0, 3)}
                          </div>
                          
                          {/* Matrix values */}
                          {results.confusionMatrix.classes.map((predClass, predIdx) => {
                            const val = results.confusionMatrix.matrix[actIdx][predIdx];
                            const isDiagonal = actIdx === predIdx;
                            const bgOpacity = val === 0 ? "bg-gray-50 text-gray-300" : 
                              isDiagonal ? "bg-indigo-600 text-white font-extrabold" : "bg-red-100 text-red-700";

                            return (
                              <div 
                                key={predClass} 
                                className={`h-11 flex items-center justify-center rounded-lg text-xs transition-all ${bgOpacity}`}
                                title={`Actual: ${actClass}, Predicted: ${predClass}`}
                              >
                                {val}
                              </div>
                            );
                          })}
                        </React.Fragment>
                      ))}
                    </div>
                  </div>
                  <span className="text-[10px] text-gray-400 mt-4 leading-normal block">
                    Diagonal matches indicate correct predictions. Red non-diagonals represent model errors.
                  </span>
                </div>

                {/* Feature Importance Recharts (Only if available) */}
                {results.featureImportance && results.featureImportance.length > 0 ? (
                  <div className="bg-white rounded-xl p-4 border border-gray-100">
                    <span className="text-xs font-bold text-gray-700 block mb-3">Relative Feature Importances (Top predictors)</span>
                    <div className="h-44">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={featureImportanceChartData} layout="vertical">
                          <XAxis type="number" stroke="#9ca3af" style={{ fontSize: "9px" }} hide />
                          <YAxis 
                            type="category" 
                            dataKey="feature" 
                            stroke="#6b7280" 
                            style={{ fontSize: "9px" }} 
                            width={110} 
                            tickLine={false}
                          />
                          <Tooltip />
                          <Bar dataKey="importance" fill="#4f46e5" radius={[0, 4, 4, 0]} />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                ) : (
                  <div className="bg-gray-50 rounded-xl p-4 border border-gray-100 flex items-center justify-center text-center">
                    <p className="text-xs text-gray-400 leading-normal">
                      Naive Bayes classifier uses direct conditional distributions so relative split-impurity is not calculable.
                    </p>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="border border-dashed border-gray-200 rounded-2xl p-12 text-center text-gray-400">
              <Layers className="w-10 h-10 mx-auto text-gray-300 mb-3" />
              <p className="text-sm font-medium">Model parameters tuned. Ready to begin training.</p>
              <p className="text-xs text-gray-400 mt-1">Select your classifier, tweak hyperparameters and click Train.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
