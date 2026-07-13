export interface DataRow {
  "Customer ID": number;
  Gender: string;
  Age: number;
  City: string;
  "Membership Type": string;
  "Total Spend": number;
  "Items Purchased": number;
  "Average Rating": number;
  "Discount Applied": boolean;
  "Days Since Last Purchase": number;
  "Satisfaction Level": string; // Target class (can be empty string for missing labels)
}

export interface SummaryStats {
  columnName: string;
  type: "numerical" | "categorical" | "boolean" | "id";
  missingCount: number;
  uniqueValues?: string[];
  mean?: number;
  median?: number;
  min?: number;
  max?: number;
  std?: number;
}

export interface FeatureEngineeringConfig {
  imputeMethod: "mode" | "drop" | "neutral";
  scaleNumerical: "none" | "standardize" | "minmax";
  enableDerivedSpendPerItem: boolean;
  enableDerivedPurchaseFrequency: boolean;
  enableDerivedDiscountSpend: boolean;
}

export interface ModelHyperparameters {
  maxDepth: number;         // For Decision Tree & Random Forest
  minSamplesSplit: number;  // For Decision Tree & Random Forest
  numTrees: number;         // For Random Forest
  knnK?: number;            // If we implement KNN
}

export type ModelType = "decision_tree" | "random_forest" | "naive_bayes";

export interface ClassMetrics {
  precision: number;
  recall: number;
  f1: number;
  support: number;
}

export interface EvaluationMetrics {
  accuracy: number;
  classMetrics: Record<string, ClassMetrics>;
  confusionMatrix: {
    classes: string[];
    matrix: number[][]; // actual x predicted
  };
  cvScore?: {
    folds: number[];
    mean: number;
    std: number;
  };
  featureImportance?: Array<{ feature: string; importance: number }>;
}

export interface ModelPredictionInput {
  Gender: string;
  Age: number;
  City: string;
  "Membership Type": string;
  "Total Spend": number;
  "Items Purchased": number;
  "Average Rating": number;
  "Discount Applied": boolean;
  "Days Since Last Purchase": number;
}
