import React from "react";
import { FeatureEngineeringConfig, DataRow } from "../types/ml";
import { DataPreprocessor } from "../utils/mlEngine";
import { 
  Sparkles, 
  Check, 
  Sliders, 
  SlidersHorizontal, 
  HelpCircle, 
  ArrowRight,
  Fingerprint
} from "lucide-react";

interface FeatureEngineeringPanelProps {
  config: FeatureEngineeringConfig;
  onChangeConfig: (newConfig: FeatureEngineeringConfig) => void;
  rawSample: DataRow | undefined;
}

export default function FeatureEngineeringPanel({ config, onChangeConfig, rawSample }: FeatureEngineeringPanelProps) {
  
  // Calculate preprocessed sample in real-time
  const preprocessedSample = React.useMemo(() => {
    if (!rawSample) return null;
    
    // Create preprocessor with current configuration
    const preprocessor = new DataPreprocessor(config);
    // Fit and transform with just a wrapper containing this sample row
    // (In reality we fit on the full dataset, but here we can mock fit with this row or a basic set)
    preprocessor.fitAndTransform([rawSample]);
    const featureVector = preprocessor.transformPredictionInput({
      Gender: rawSample.Gender,
      Age: rawSample.Age,
      City: rawSample.City,
      "Membership Type": rawSample["Membership Type"],
      "Total Spend": rawSample["Total Spend"],
      "Items Purchased": rawSample["Items Purchased"],
      "Average Rating": rawSample["Average Rating"],
      "Discount Applied": rawSample["Discount Applied"],
      "Days Since Last Purchase": rawSample["Days Since Last Purchase"]
    });

    return {
      featureNames: preprocessor.featureNames,
      featureVector
    };
  }, [config, rawSample]);

  const updateField = (field: keyof FeatureEngineeringConfig, value: any) => {
    onChangeConfig({
      ...config,
      [field]: value
    });
  };

  return (
    <div id="feature-engineering" className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
      {/* Header */}
      <div className="flex items-center gap-2 border-b border-gray-100 pb-5 mb-6">
        <Sparkles className="w-5 h-5 text-indigo-600" />
        <div>
          <h2 className="text-xl font-bold text-gray-900">Feature Engineering Pipeline</h2>
          <p className="text-sm text-gray-500 mt-1">
            Transform raw messy features into robust numerical inputs optimized for classification algorithms.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left column: Configuration Sliders */}
        <div className="lg:col-span-5 space-y-6">
          <h3 className="text-sm font-bold text-gray-800 flex items-center gap-1.5 uppercase tracking-wide">
            <SlidersHorizontal className="w-4 h-4 text-indigo-500" /> Pipeline Configuration
          </h3>

          {/* Missing Value Imputation */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-gray-700 flex items-center gap-1">
              Impute Missing Targets
              <span className="text-[10px] text-gray-400 font-normal">(Row 172, 244 have missing Satisfaction levels)</span>
            </label>
            <div className="grid grid-cols-3 gap-2">
              {[
                { id: "mode", label: "Mode (Most Frequent)", desc: "Fills missing values with most frequent class" },
                { id: "neutral", label: "Constant ('Neutral')", desc: "Fills missing values with 'Neutral'" },
                { id: "drop", label: "Drop Rows", desc: "Completely drops records with missing labels" }
              ].map(opt => (
                <button
                  key={opt.id}
                  onClick={() => updateField("imputeMethod", opt.id)}
                  className={`p-2.5 rounded-xl border text-left flex flex-col justify-between transition-all ${
                    config.imputeMethod === opt.id
                      ? "border-indigo-600 bg-indigo-50/50 text-indigo-900"
                      : "border-gray-200 hover:border-gray-300 text-gray-600"
                  }`}
                >
                  <span className="text-xs font-bold block">{opt.label}</span>
                  <span className="text-[10px] text-gray-400 mt-1 block leading-normal">{opt.desc}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Numerical Scaling */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-gray-700 flex items-center gap-1">
              Numerical Feature Scaling
            </label>
            <div className="grid grid-cols-3 gap-2">
              {[
                { id: "none", label: "No Scaling", desc: "Keep raw values as they are" },
                { id: "standardize", label: "Standardize (Z-Score)", desc: "X_scaled = (X - Mean) / StdDev" },
                { id: "minmax", label: "MinMax Normalization", desc: "X_scaled = (X - Min) / (Max - Min)" }
              ].map(opt => (
                <button
                  key={opt.id}
                  onClick={() => updateField("scaleNumerical", opt.id)}
                  className={`p-2.5 rounded-xl border text-left flex flex-col justify-between transition-all ${
                    config.scaleNumerical === opt.id
                      ? "border-indigo-600 bg-indigo-50/50 text-indigo-900"
                      : "border-gray-200 hover:border-gray-300 text-gray-600"
                  }`}
                >
                  <span className="text-xs font-bold block">{opt.label}</span>
                  <span className="text-[10px] text-gray-400 mt-1 block leading-normal">{opt.desc}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Derived Features Toggles */}
          <div className="space-y-3">
            <label className="text-xs font-bold text-gray-700">Derived (Interaction) Features</label>
            
            <div className="space-y-2.5">
              {/* Derived Feature 1: Spend per Item */}
              <label className="flex items-start gap-3 p-3 bg-gray-50 hover:bg-gray-100/70 border border-gray-100 rounded-xl cursor-pointer transition-colors">
                <input
                  type="checkbox"
                  checked={config.enableDerivedSpendPerItem}
                  onChange={(e) => updateField("enableDerivedSpendPerItem", e.target.checked)}
                  className="mt-1 h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                />
                <div>
                  <span className="text-xs font-bold text-gray-800 block">Spend per Item (Ratio)</span>
                  <span className="text-[11px] text-gray-500 block leading-normal mt-0.5">
                    Calculates <code className="bg-white px-1 py-0.2 rounded font-mono text-xs font-bold">Total Spend / Items Purchased</code>. Represents average cost per unit, which highly aligns with quality preferences.
                  </span>
                </div>
              </label>

              {/* Derived Feature 2: Purchase Frequency */}
              <label className="flex items-start gap-3 p-3 bg-gray-50 hover:bg-gray-100/70 border border-gray-100 rounded-xl cursor-pointer transition-colors">
                <input
                  type="checkbox"
                  checked={config.enableDerivedPurchaseFrequency}
                  onChange={(e) => updateField("enableDerivedPurchaseFrequency", e.target.checked)}
                  className="mt-1 h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                />
                <div>
                  <span className="text-xs font-bold text-gray-800 block">Purchase Frequency Index</span>
                  <span className="text-[11px] text-gray-500 block leading-normal mt-0.5">
                    Calculates <code className="bg-white px-1 py-0.2 rounded font-mono text-xs font-bold">Items Purchased / (Days Since Last Purchase + 1)</code>. Helps model loyalty and recency patterns.
                  </span>
                </div>
              </label>

              {/* Derived Feature 3: Discount Spend interaction */}
              <label className="flex items-start gap-3 p-3 bg-gray-50 hover:bg-gray-100/70 border border-gray-100 rounded-xl cursor-pointer transition-colors">
                <input
                  type="checkbox"
                  checked={config.enableDerivedDiscountSpend}
                  onChange={(e) => updateField("enableDerivedDiscountSpend", e.target.checked)}
                  className="mt-1 h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                />
                <div>
                  <span className="text-xs font-bold text-gray-800 block">Discounted Spend Interaction</span>
                  <span className="text-[11px] text-gray-500 block leading-normal mt-0.5">
                    Calculates <code className="bg-white px-1 py-0.2 rounded font-mono text-xs font-bold">Total Spend * DiscountApplied</code>. Captures price-sensitivity dynamics for high-value spenders.
                  </span>
                </div>
              </label>
            </div>
          </div>
        </div>

        {/* Right column: Before vs After sample transformation */}
        <div className="lg:col-span-7 bg-slate-50 rounded-2xl p-6 border border-slate-100 space-y-6">
          <h3 className="text-sm font-bold text-slate-800 flex items-center gap-1.5 uppercase tracking-wide">
            <Fingerprint className="w-4 h-4 text-slate-500" /> Pipeline Transformation Preview
          </h3>

          {rawSample && preprocessedSample ? (
            <div className="space-y-5 text-sm">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Before: Raw Customer Data */}
                <div className="bg-white p-4 rounded-xl border border-slate-200/60">
                  <span className="text-[11px] font-bold text-gray-400 uppercase tracking-wider block mb-2">Raw Features Sample (ID #{rawSample["Customer ID"]})</span>
                  <div className="space-y-1.5 text-xs text-slate-600 font-mono">
                    <div className="flex justify-between border-b border-gray-50 pb-1">
                      <span>Age:</span> <span className="text-gray-900 font-bold">{rawSample.Age}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-50 pb-1">
                      <span>Gender:</span> <span className="text-gray-900 font-bold">{rawSample.Gender}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-50 pb-1">
                      <span>City:</span> <span className="text-gray-900 font-bold">{rawSample.City}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-50 pb-1">
                      <span>Membership:</span> <span className="text-gray-900 font-bold">{rawSample["Membership Type"]}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-50 pb-1">
                      <span>Total Spend:</span> <span className="text-gray-900 font-bold">${rawSample["Total Spend"]}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-50 pb-1">
                      <span>Items Purchased:</span> <span className="text-gray-900 font-bold">{rawSample["Items Purchased"]}</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-50 pb-1">
                      <span>Average Rating:</span> <span className="text-gray-900 font-bold">{rawSample["Average Rating"]} ★</span>
                    </div>
                    <div className="flex justify-between border-b border-gray-50 pb-1">
                      <span>Discount:</span> <span className="text-gray-900 font-bold">{String(rawSample["Discount Applied"]).toUpperCase()}</span>
                    </div>
                    <div className="flex justify-between pb-1">
                      <span>Days Since:</span> <span className="text-gray-900 font-bold">{rawSample["Days Since Last Purchase"]}</span>
                    </div>
                  </div>
                </div>

                {/* Arrow indicator for desktop */}
                <div className="bg-indigo-600/5 hover:bg-indigo-600/10 p-4 rounded-xl border border-indigo-100 flex flex-col justify-center items-center text-center">
                  <div className="bg-indigo-600 text-white rounded-full p-2 mb-2 shadow-sm">
                    <Sparkles className="w-4 h-4 animate-pulse" />
                  </div>
                  <span className="text-xs font-bold text-indigo-950">One-Hot Encoding & Scaling</span>
                  <span className="text-[10px] text-indigo-700 leading-normal px-2 mt-1 block">
                    One-hot converts {`"Membership_Gold"`} into 1/0. Numerical values get standardized to avoid scaling bias.
                  </span>
                </div>
              </div>

              {/* Resulting Transformed Feature Vector */}
              <div className="bg-white p-4 rounded-xl border border-slate-200">
                <span className="text-[11px] font-bold text-indigo-600 uppercase tracking-wider block mb-3">Resulting Numeric Feature Vector (Input to Classifier)</span>
                
                <div className="max-h-56 overflow-y-auto border border-gray-100 rounded-lg text-xs font-mono">
                  <div className="grid grid-cols-12 bg-slate-50 p-2 font-bold text-gray-700 border-b border-gray-100 text-[10px]">
                    <div className="col-span-1 text-center">Index</div>
                    <div className="col-span-7">Transformed Feature Name</div>
                    <div className="col-span-4 text-right">Numeric Value</div>
                  </div>
                  <div className="divide-y divide-gray-50">
                    {preprocessedSample.featureNames.map((name, idx) => (
                      <div key={name} className="grid grid-cols-12 p-2 hover:bg-slate-50 transition-colors">
                        <div className="col-span-1 text-center text-gray-400">{idx}</div>
                        <div className="col-span-7 text-gray-800 font-medium truncate" title={name}>{name}</div>
                        <div className="col-span-4 text-right font-bold text-indigo-600">
                          {preprocessedSample.featureVector[idx] !== undefined 
                            ? Number(preprocessedSample.featureVector[idx]).toFixed(4) 
                            : "0.0000"}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-slate-50 p-3 rounded-lg border border-slate-100 mt-4 text-[11px] text-slate-500 leading-normal flex items-center gap-2">
                  <Check className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                  Successfully created a robust <strong className="text-slate-800">{preprocessedSample.featureVector.length} dimensional feature space</strong> ready for training!
                </div>
              </div>
            </div>
          ) : (
            <p className="text-sm text-slate-400">Loading pipeline transformation sample...</p>
          )}
        </div>
      </div>
    </div>
  );
}
