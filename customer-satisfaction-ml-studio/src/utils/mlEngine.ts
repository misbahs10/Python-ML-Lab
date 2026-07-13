import {
  DataRow,
  SummaryStats,
  FeatureEngineeringConfig,
  ModelHyperparameters,
  EvaluationMetrics,
  ModelPredictionInput,
  ClassMetrics
} from "../types/ml";

// Seeded pseudo-random number generator for reproducible results
export class SeededRandom {
  private seed: number;
  constructor(seed = 42) {
    this.seed = seed;
  }
  // Returns number in [0, 1)
  next(): number {
    const x = Math.sin(this.seed++) * 10000;
    return x - Math.floor(x);
  }

  // Shuffle array in-place
  shuffle<T>(array: T[]): T[] {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(this.next() * (i + 1));
      const temp = arr[i];
      arr[i] = arr[j];
      arr[j] = temp;
    }
    return arr;
  }
}

// 1. CSV Parser
export function parseCSV(csvString: string): DataRow[] {
  const lines = csvString.trim().split("\n");
  if (lines.length <= 1) return [];

  const headers = lines[0].split(",").map(h => h.trim());
  const rows: DataRow[] = [];

  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;

    // Use a robust split that handles potential commas inside quotes, although our dataset is simple
    const values = line.split(",").map(v => v.trim());
    if (values.length < headers.length - 1) continue; // Allow missing satisfaction level at the end

    const row: any = {};
    headers.forEach((header, index) => {
      const value = values[index];
      if (header === "Customer ID") {
        row[header] = parseInt(value, 10);
      } else if (header === "Age") {
        row[header] = parseInt(value, 10);
      } else if (header === "Total Spend") {
        row[header] = parseFloat(value);
      } else if (header === "Items Purchased") {
        row[header] = parseInt(value, 10);
      } else if (header === "Average Rating") {
        row[header] = parseFloat(value);
      } else if (header === "Discount Applied") {
        row[header] = value.toUpperCase() === "TRUE";
      } else if (header === "Days Since Last Purchase") {
        row[header] = parseInt(value, 10);
      } else if (header === "Satisfaction Level") {
        row[header] = value || ""; // Handle empty target
      } else {
        row[header] = value;
      }
    });

    // Handle case where trailing comma leaves Satisfaction Level empty
    if (row["Satisfaction Level"] === undefined) {
      row["Satisfaction Level"] = "";
    }

    rows.push(row as DataRow);
  }

  return rows;
}

// 2. Summary Statistics Calculator
export function calculateSummaryStats(data: DataRow[]): SummaryStats[] {
  if (data.length === 0) return [];

  const columns: { name: string; type: "numerical" | "categorical" | "boolean" | "id" }[] = [
    { name: "Customer ID", type: "id" },
    { name: "Gender", type: "categorical" },
    { name: "Age", type: "numerical" },
    { name: "City", type: "categorical" },
    { name: "Membership Type", type: "categorical" },
    { name: "Total Spend", type: "numerical" },
    { name: "Items Purchased", type: "numerical" },
    { name: "Average Rating", type: "numerical" },
    { name: "Discount Applied", type: "boolean" },
    { name: "Days Since Last Purchase", type: "numerical" },
    { name: "Satisfaction Level", type: "categorical" }
  ];

  return columns.map(col => {
    const values = data.map(row => (row as any)[col.name]);
    const missingCount = values.filter(v => v === undefined || v === null || v === "").length;

    const stats: SummaryStats = {
      columnName: col.name,
      type: col.type,
      missingCount
    };

    if (col.type === "numerical") {
      const numValues = values.filter(v => typeof v === "number" && !isNaN(v)) as number[];
      if (numValues.length > 0) {
        numValues.sort((a, b) => a - b);
        const sum = numValues.reduce((a, b) => a + b, 0);
        const mean = sum / numValues.length;
        const median = numValues[Math.floor(numValues.length / 2)];
        const min = numValues[0];
        const max = numValues[numValues.length - 1];

        // Standard deviation
        const variance = numValues.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / numValues.length;
        const std = Math.sqrt(variance);

        stats.mean = Math.round(mean * 100) / 100;
        stats.median = Math.round(median * 100) / 100;
        stats.min = Math.round(min * 100) / 100;
        stats.max = Math.round(max * 100) / 100;
        stats.std = Math.round(std * 100) / 100;
      }
    } else if (col.type === "categorical" || col.type === "boolean") {
      const nonMissing = values.filter(v => v !== undefined && v !== null && v !== "") as string[];
      const unique = Array.from(new Set(nonMissing)).map(v => String(v));
      stats.uniqueValues = unique;
    }

    return stats;
  });
}

// Preprocessor class that holds Scaling parameters and Categorical lists
export class DataPreprocessor {
  private config: FeatureEngineeringConfig;
  private targetImputeValue: string = "Neutral";
  private numericStats: Record<string, { mean: number; std: number; min: number; max: number }> = {};

  // For encoding categorical variables consistently
  private categoricalValues: Record<string, string[]> = {
    Gender: ["Male", "Female"],
    City: ["New York", "Los Angeles", "Chicago", "San Francisco", "Miami", "Houston"],
    "Membership Type": ["Gold", "Silver", "Bronze"]
  };

  // List of generated feature names in order
  public featureNames: string[] = [];

  constructor(config: FeatureEngineeringConfig) {
    this.config = config;
  }

  // 1. Fit & Preprocess the Training Set
  fitAndTransform(data: DataRow[]): { X: number[][]; y: string[] } {
    // Determine the imputation value for Satisfaction Level
    if (this.config.imputeMethod === "mode") {
      const counts: Record<string, number> = {};
      data.forEach(row => {
        if (row["Satisfaction Level"]) {
          counts[row["Satisfaction Level"]] = (counts[row["Satisfaction Level"]] || 0) + 1;
        }
      });
      let mode = "Satisfied";
      let maxCount = 0;
      Object.entries(counts).forEach(([val, count]) => {
        if (count > maxCount) {
          maxCount = count;
          mode = val;
        }
      });
      this.targetImputeValue = mode;
    } else if (this.config.imputeMethod === "neutral") {
      this.targetImputeValue = "Neutral";
    }

    // Clean data according to missing target configs
    let cleanedData = [...data];
    if (this.config.imputeMethod === "drop") {
      cleanedData = cleanedData.filter(row => row["Satisfaction Level"] && row["Satisfaction Level"].trim() !== "");
    } else {
      cleanedData = cleanedData.map(row => {
        if (!row["Satisfaction Level"] || row["Satisfaction Level"].trim() === "") {
          return { ...row, "Satisfaction Level": this.targetImputeValue };
        }
        return row;
      });
    }

    // Compute stats for scaling based on cleaned data
    const numericCols = ["Age", "Total Spend", "Items Purchased", "Average Rating", "Days Since Last Purchase"];
    numericCols.forEach(col => {
      const vals = cleanedData.map(row => (row as any)[col] as number);
      const sum = vals.reduce((a, b) => a + b, 0);
      const mean = sum / vals.length;
      const variance = vals.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / vals.length;
      const std = Math.sqrt(variance) || 1; // avoid division by zero
      const min = Math.min(...vals);
      const max = Math.max(...vals);

      this.numericStats[col] = { mean, std, min, max };
    });

    // Extract dynamic unique categories if we want to be absolutely sure we capture everything
    Object.keys(this.categoricalValues).forEach(col => {
      const vals = cleanedData.map(row => String((row as any)[col]));
      const unique = Array.from(new Set(vals)).filter(v => v && v !== "undefined");
      if (unique.length > 0) {
        this.categoricalValues[col] = unique;
      }
    });

    // Build the list of engineered feature names
    this.buildFeatureNames();

    // Map rows to numeric arrays
    const X = cleanedData.map(row => this.transformRowToFeatures(row));
    const y = cleanedData.map(row => row["Satisfaction Level"]);

    return { X, y };
  }

  // 2. Transform a custom input row (for prediction)
  transformPredictionInput(input: ModelPredictionInput): number[] {
    return this.transformRowToFeatures(input);
  }

  private buildFeatureNames() {
    const names: string[] = [];

    // Numerical columns
    names.push("Age", "Total Spend", "Items Purchased", "Average Rating", "Days Since Last Purchase");

    // Categorical (One-Hot Encoded)
    Object.entries(this.categoricalValues).forEach(([col, uniqueVals]) => {
      uniqueVals.forEach(val => {
        names.push(`${col}_${val}`);
      });
    });

    // Boolean features
    names.push("Discount Applied");

    // Derived features
    if (this.config.enableDerivedSpendPerItem) {
      names.push("Derived_SpendPerItem");
    }
    if (this.config.enableDerivedPurchaseFrequency) {
      names.push("Derived_PurchaseFrequency");
    }
    if (this.config.enableDerivedDiscountSpend) {
      names.push("Derived_DiscountSpend");
    }

    this.featureNames = names;
  }

  private transformRowToFeatures(row: any): number[] {
    const features: number[] = [];

    // Scale or pass numerical columns
    const numCols = ["Age", "Total Spend", "Items Purchased", "Average Rating", "Days Since Last Purchase"];
    numCols.forEach(col => {
      let val = row[col] !== undefined ? row[col] : 0;
      const stats = this.numericStats[col];

      if (stats) {
        if (this.config.scaleNumerical === "standardize") {
          val = (val - stats.mean) / stats.std;
        } else if (this.config.scaleNumerical === "minmax") {
          val = (val - stats.min) / ((stats.max - stats.min) || 1);
        }
      }
      features.push(val);
    });

    // One-Hot Encode Categorical columns
    Object.entries(this.categoricalValues).forEach(([col, uniqueVals]) => {
      const rowVal = String(row[col] || "");
      uniqueVals.forEach(val => {
        features.push(rowVal.toLowerCase() === val.toLowerCase() ? 1 : 0);
      });
    });

    // Boolean
    const discount = row["Discount Applied"] === true || String(row["Discount Applied"]).toUpperCase() === "TRUE";
    features.push(discount ? 1 : 0);

    // Derived Features
    const totalSpend = row["Total Spend"] !== undefined ? row["Total Spend"] : 0;
    const itemsPurchased = row["Items Purchased"] !== undefined ? row["Items Purchased"] : 0;
    const daysSince = row["Days Since Last Purchase"] !== undefined ? row["Days Since Last Purchase"] : 0;

    if (this.config.enableDerivedSpendPerItem) {
      const spendPerItem = totalSpend / (itemsPurchased || 1);
      // We should scale this too, but a simple ratio helps models like Decision Trees tremendously
      features.push(spendPerItem);
    }
    if (this.config.enableDerivedPurchaseFrequency) {
      const freq = itemsPurchased / (daysSince + 1);
      features.push(freq);
    }
    if (this.config.enableDerivedDiscountSpend) {
      const discSpend = totalSpend * (discount ? 1 : 0);
      features.push(discSpend);
    }

    return features;
  }
}

// 3. Hand-written Machine Learning Algorithms

// Interface for TreeNode
export interface TreeNode {
  featureIndex?: number;
  threshold?: number;
  left?: TreeNode;
  right?: TreeNode;
  prediction?: string;
  gini?: number;
  samplesCount: number;
}

// Decision Tree Classifier from scratch using Gini impurity
export class DecisionTreeClassifier {
  private maxDepth: number;
  private minSamplesSplit: number;
  public root: TreeNode | null = null;
  public featureNames: string[] = [];

  constructor(maxDepth = 5, minSamplesSplit = 2) {
    this.maxDepth = maxDepth;
    this.minSamplesSplit = minSamplesSplit;
  }

  // Calculate Gini Impurity of a subset of labels
  private calculateGini(labels: string[]): number {
    if (labels.length === 0) return 0;
    const counts: Record<string, number> = {};
    labels.forEach(l => {
      counts[l] = (counts[l] || 0) + 1;
    });

    let sumSquares = 0;
    const total = labels.length;
    Object.values(counts).forEach(c => {
      sumSquares += Math.pow(c / total, 2);
    });

    return 1 - sumSquares;
  }

  // Find the best split for a node
  private findBestSplit(X: number[][], y: string[]): {
    bestFeature: number;
    bestThreshold: number;
    bestGiniGain: number;
    leftX: number[][];
    leftY: string[];
    rightX: number[][];
    rightY: string[];
  } | null {
    const numFeatures = X[0].length;
    const currentGini = this.calculateGini(y);
    let bestGiniGain = -1;
    let bestFeature = -1;
    let bestThreshold = -1;
    let bestSplitLeftX: number[][] = [];
    let bestSplitLeftY: string[] = [];
    let bestSplitRightX: number[][] = [];
    let bestSplitRightY: string[] = [];

    for (let f = 0; f < numFeatures; f++) {
      // Get all values of feature f
      const values = X.map(row => row[f]);
      // Sort and get unique thresholds
      const uniqueVals = Array.from(new Set(values)).sort((a, b) => a - b);
      if (uniqueVals.length <= 1) continue;

      // Try thresholds in-between values
      for (let t = 0; t < uniqueVals.length - 1; t++) {
        const threshold = (uniqueVals[t] + uniqueVals[t + 1]) / 2;

        const leftIndices: number[] = [];
        const rightIndices: number[] = [];

        for (let i = 0; i < X.length; i++) {
          if (X[i][f] < threshold) {
            leftIndices.push(i);
          } else {
            rightIndices.push(i);
          }
        }

        if (leftIndices.length === 0 || rightIndices.length === 0) continue;

        const leftY = leftIndices.map(idx => y[idx]);
        const rightY = rightIndices.map(idx => y[idx]);

        const leftGini = this.calculateGini(leftY);
        const rightGini = this.calculateGini(rightY);

        const weightedGini = (leftY.length / y.length) * leftGini + (rightY.length / y.length) * rightGini;
        const giniGain = currentGini - weightedGini;

        if (giniGain > bestGiniGain) {
          bestGiniGain = giniGain;
          bestFeature = f;
          bestThreshold = threshold;
          bestSplitLeftX = leftIndices.map(idx => X[idx]);
          bestSplitLeftY = leftY;
          bestSplitRightX = rightIndices.map(idx => X[idx]);
          bestSplitRightY = rightY;
        }
      }
    }

    if (bestFeature === -1 || bestGiniGain <= 0) return null;

    return {
      bestFeature,
      bestThreshold,
      bestGiniGain,
      leftX: bestSplitLeftX,
      leftY: bestSplitLeftY,
      rightX: bestSplitRightX,
      rightY: bestSplitRightY
    };
  }

  // Get majority class in list of labels
  private getMajorityClass(labels: string[]): string {
    const counts: Record<string, number> = {};
    labels.forEach(l => {
      counts[l] = (counts[l] || 0) + 1;
    });

    let majority = "";
    let maxCount = -1;
    Object.entries(counts).forEach(([val, count]) => {
      if (count > maxCount) {
        maxCount = count;
        majority = val;
      }
    });

    return majority;
  }

  // Recursive tree building
  private buildTree(X: number[][], y: string[], depth: number): TreeNode {
    const samplesCount = X.length;
    const currentGini = this.calculateGini(y);

    // Stop conditions
    if (
      depth >= this.maxDepth ||
      samplesCount < this.minSamplesSplit ||
      currentGini === 0
    ) {
      return {
        prediction: this.getMajorityClass(y),
        gini: currentGini,
        samplesCount
      };
    }

    const split = this.findBestSplit(X, y);
    if (!split) {
      return {
        prediction: this.getMajorityClass(y),
        gini: currentGini,
        samplesCount
      };
    }

    const node: TreeNode = {
      featureIndex: split.bestFeature,
      threshold: split.bestThreshold,
      gini: currentGini,
      samplesCount
    };

    node.left = this.buildTree(split.leftX, split.leftY, depth + 1);
    node.right = this.buildTree(split.rightX, split.rightY, depth + 1);

    return node;
  }

  fit(X: number[][], y: string[], featureNames: string[] = []): void {
    this.featureNames = featureNames;
    if (X.length === 0 || y.length === 0) return;
    this.root = this.buildTree(X, y, 0);
  }

  private predictRow(node: TreeNode, row: number[]): string {
    if (node.prediction !== undefined) {
      return node.prediction;
    }

    if (node.featureIndex !== undefined && node.threshold !== undefined && node.left && node.right) {
      if (row[node.featureIndex] < node.threshold) {
        return this.predictRow(node.left, row);
      } else {
        return this.predictRow(node.right, row);
      }
    }

    return "";
  }

  predict(X: number[][]): string[] {
    if (!this.root) return X.map(() => "Neutral");
    return X.map(row => this.predictRow(this.root!, row));
  }

  // Calculate Gini impurity reduction per feature (Feature Importance)
  getFeatureImportance(): number[] {
    const importance = new Array(this.featureNames.length).fill(0);
    if (!this.root) return importance;

    const traverse = (node: TreeNode) => {
      if (node.featureIndex !== undefined && node.threshold !== undefined && node.left && node.right && node.gini !== undefined) {
        const leftGini = node.left.gini || 0;
        const rightGini = node.right.gini || 0;
        const gain = node.samplesCount * node.gini - (node.left.samplesCount * leftGini + node.right.samplesCount * rightGini);
        importance[node.featureIndex] += gain;

        traverse(node.left);
        traverse(node.right);
      }
    };

    traverse(this.root);

    // Normalize importance to sum up to 1
    const sum = importance.reduce((a, b) => a + b, 0);
    if (sum > 0) {
      return importance.map(v => v / sum);
    }
    return importance;
  }
}

// Random Forest Classifier
export class RandomForestClassifier {
  private numTrees: number;
  private maxDepth: number;
  private minSamplesSplit: number;
  private trees: DecisionTreeClassifier[] = [];
  public featureNames: string[] = [];

  constructor(numTrees = 5, maxDepth = 5, minSamplesSplit = 2) {
    this.numTrees = numTrees;
    this.maxDepth = maxDepth;
    this.minSamplesSplit = minSamplesSplit;
  }

  fit(X: number[][], y: string[], featureNames: string[] = []): void {
    this.featureNames = featureNames;
    this.trees = [];

    if (X.length === 0 || y.length === 0) return;

    const rand = new SeededRandom(1337); // stable training seed

    for (let t = 0; t < this.numTrees; t++) {
      // 1. Bootstrapping (sample with replacement of size N)
      const bootstrapX: number[][] = [];
      const bootstrapY: string[] = [];

      for (let i = 0; i < X.length; i++) {
        const randIdx = Math.floor(rand.next() * X.length);
        bootstrapX.push(X[randIdx]);
        bootstrapY.push(y[randIdx]);
      }

      // 2. Train a single decision tree on bootstrapped samples
      const tree = new DecisionTreeClassifier(this.maxDepth, this.minSamplesSplit);
      tree.fit(bootstrapX, bootstrapY, this.featureNames);
      this.trees.push(tree);
    }
  }

  predict(X: number[][]): string[] {
    if (this.trees.length === 0) return X.map(() => "Neutral");

    // Let each tree make a prediction
    const treePredictions = this.trees.map(tree => tree.predict(X));

    // Majority vote
    return X.map((_, sampleIdx) => {
      const votes: Record<string, number> = {};
      this.trees.forEach((_, treeIdx) => {
        const pred = treePredictions[treeIdx][sampleIdx];
        votes[pred] = (votes[pred] || 0) + 1;
      });

      let winner = "";
      let maxVotes = -1;
      Object.entries(votes).forEach(([pred, voteCount]) => {
        if (voteCount > maxVotes) {
          maxVotes = voteCount;
          winner = pred;
        }
      });

      return winner;
    });
  }

  // Predict class probabilities
  predictProbs(row: number[]): Record<string, number> {
    const counts: Record<string, number> = { Satisfied: 0, Neutral: 0, Unsatisfied: 0 };
    if (this.trees.length === 0) return { Satisfied: 0.33, Neutral: 0.33, Unsatisfied: 0.33 };

    this.trees.forEach(tree => {
      const pred = tree.predict([row])[0];
      if (counts[pred] !== undefined) {
        counts[pred]++;
      } else {
        counts[pred] = 1;
      }
    });

    const total = this.trees.length;
    return {
      Satisfied: (counts["Satisfied"] || 0) / total,
      Neutral: (counts["Neutral"] || 0) / total,
      Unsatisfied: (counts["Unsatisfied"] || 0) / total
    };
  }

  getFeatureImportance(): number[] {
    const importances = new Array(this.featureNames.length).fill(0);
    if (this.trees.length === 0) return importances;

    this.trees.forEach(tree => {
      const treeImp = tree.getFeatureImportance();
      for (let i = 0; i < importances.length; i++) {
        importances[i] += treeImp[i];
      }
    });

    // Average and normalize
    const sum = importances.reduce((a, b) => a + b, 0);
    if (sum > 0) {
      return importances.map(v => v / sum);
    }
    return importances;
  }
}

// Naive Bayes Classifier
export class NaiveBayesClassifier {
  private classPriors: Record<string, number> = {};
  private numericParams: Record<string, Array<{ mean: number; variance: number }>> = {}; // class -> [featureIndex -> params]
  private classes: string[] = ["Satisfied", "Neutral", "Unsatisfied"];
  public featureNames: string[] = [];

  fit(X: number[][], y: string[], featureNames: string[] = []): void {
    this.featureNames = featureNames;
    const numSamples = X.length;
    if (numSamples === 0) return;

    // 1. Class priors
    const classCounts: Record<string, number> = { Satisfied: 0, Neutral: 0, Unsatisfied: 0 };
    y.forEach(label => {
      if (classCounts[label] !== undefined) classCounts[label]++;
    });

    this.classes.forEach(c => {
      this.classPriors[c] = (classCounts[c] + 1) / (numSamples + this.classes.length); // Laplace smoothing
    });

    // 2. Continuous Gaussian parameter computation for each feature by class
    const numFeatures = X[0].length;
    this.classes.forEach(c => {
      const classIndices = y.map((label, idx) => label === c ? idx : -1).filter(idx => idx !== -1);
      const classRows = classIndices.map(idx => X[idx]);

      this.numericParams[c] = [];

      for (let f = 0; f < numFeatures; f++) {
        const featureVals = classRows.map(row => row[f]);
        if (featureVals.length === 0) {
          this.numericParams[c].push({ mean: 0, variance: 1e-4 });
          continue;
        }

        const sum = featureVals.reduce((a, b) => a + b, 0);
        const mean = sum / featureVals.length;
        const squaredDiffSum = featureVals.reduce((a, b) => a + Math.pow(b - mean, 2), 0);
        const variance = (squaredDiffSum / featureVals.length) + 1e-4; // small epsilon to prevent variance of 0

        this.numericParams[c].push({ mean, variance });
      }
    });
  }

  // Probability density function of Gaussian distribution
  private calculateGaussianPDF(x: number, mean: number, variance: number): number {
    const exponent = Math.exp(-Math.pow(x - mean, 2) / (2 * variance));
    return (1 / Math.sqrt(2 * Math.PI * variance)) * exponent;
  }

  predictProbs(row: number[]): Record<string, number> {
    const scoreLogProbs: Record<string, number> = {};

    this.classes.forEach(c => {
      let logProb = Math.log(this.classPriors[c] || 0.33);

      const params = this.numericParams[c];
      if (params) {
        row.forEach((val, fIdx) => {
          const fParam = params[fIdx];
          if (fParam) {
            const pdf = this.calculateGaussianPDF(val, fParam.mean, fParam.variance);
            logProb += Math.log(pdf || 1e-10); // avoid log(0)
          }
        });
      }

      scoreLogProbs[c] = logProb;
    });

    // Convert log probs to actual probabilities (softmax-like stabilization)
    const maxLog = Math.max(...Object.values(scoreLogProbs));
    const exps: Record<string, number> = {};
    let sumExps = 0;

    this.classes.forEach(c => {
      exps[c] = Math.exp(scoreLogProbs[c] - maxLog);
      sumExps += exps[c];
    });

    const probs: Record<string, number> = {};
    this.classes.forEach(c => {
      probs[c] = exps[c] / (sumExps || 1);
    });

    return probs;
  }

  predict(X: number[][]): string[] {
    return X.map(row => {
      const probs = this.predictProbs(row);
      let bestClass = "Neutral";
      let highestProb = -1;

      Object.entries(probs).forEach(([c, p]) => {
        if (p > highestProb) {
          highestProb = p;
          bestClass = c;
        }
      });

      return bestClass;
    });
  }
}

// Helper to calculate classification metrics
export function evaluateModel(
  actual: string[],
  predicted: string[],
  classes: string[] = ["Satisfied", "Neutral", "Unsatisfied"]
): EvaluationMetrics {
  const numSamples = actual.length;

  // 1. Overall Accuracy
  let correct = 0;
  actual.forEach((act, idx) => {
    if (act === predicted[idx]) correct++;
  });
  const accuracy = numSamples > 0 ? correct / numSamples : 0;

  // 2. Confusion Matrix
  // Matrix indices match classes array
  const size = classes.length;
  const matrix: number[][] = Array.from({ length: size }, () => Array(size).fill(0));

  actual.forEach((act, idx) => {
    const pred = predicted[idx];
    const actIdx = classes.indexOf(act);
    const predIdx = classes.indexOf(pred);

    if (actIdx !== -1 && predIdx !== -1) {
      matrix[actIdx][predIdx]++;
    }
  });

  // 3. Class-specific metrics
  const classMetrics: Record<string, ClassMetrics> = {};

  classes.forEach((c, cIdx) => {
    // True Positives, False Positives, False Negatives
    let tp = 0;
    let fp = 0;
    let fn = 0;
    let support = 0;

    actual.forEach((act, idx) => {
      const pred = predicted[idx];

      if (act === c) {
        support++;
        if (pred === c) {
          tp++;
        } else {
          fn++;
        }
      } else {
        if (pred === c) {
          fp++;
        }
      }
    });

    const precision = tp + fp > 0 ? tp / (tp + fp) : 0;
    const recall = tp + fn > 0 ? tp / (tp + fn) : 0;
    const f1 = precision + recall > 0 ? (2 * precision * recall) / (precision + recall) : 0;

    classMetrics[c] = {
      precision: Math.round(precision * 100) / 100,
      recall: Math.round(recall * 100) / 100,
      f1: Math.round(f1 * 100) / 100,
      support
    };
  });

  return {
    accuracy: Math.round(accuracy * 1000) / 1000,
    classMetrics,
    confusionMatrix: {
      classes,
      matrix
    }
  };
}

// 4. K-Fold Cross Validation Function
export function crossValidate(
  X: number[][],
  y: string[],
  modelType: "decision_tree" | "random_forest" | "naive_bayes",
  hyperparameters: ModelHyperparameters,
  featureNames: string[],
  foldsCount = 5
): { folds: number[]; mean: number; std: number } {
  if (X.length < foldsCount) {
    return { folds: [], mean: 0, std: 0 };
  }

  const rand = new SeededRandom(42); // Stable cross-validation seed
  const indices = Array.from({ length: X.length }, (_, i) => i);
  const shuffledIndices = rand.shuffle(indices);

  const foldSize = Math.floor(X.length / foldsCount);
  const foldScores: number[] = [];

  for (let f = 0; f < foldsCount; f++) {
    const valStart = f * foldSize;
    // For the last fold, capture any remainder samples
    const valEnd = f === foldsCount - 1 ? X.length : (f + 1) * foldSize;

    const valIndices = shuffledIndices.slice(valStart, valEnd);
    const trainIndices = shuffledIndices.filter(idx => !valIndices.includes(idx));

    const trainX = trainIndices.map(idx => X[idx]);
    const trainY = trainIndices.map(idx => y[idx]);
    const valX = valIndices.map(idx => X[idx]);
    const valY = valIndices.map(idx => y[idx]);

    // Instantiate model
    let model: any;
    if (modelType === "decision_tree") {
      model = new DecisionTreeClassifier(hyperparameters.maxDepth, hyperparameters.minSamplesSplit);
    } else if (modelType === "random_forest") {
      model = new RandomForestClassifier(hyperparameters.numTrees, hyperparameters.maxDepth, hyperparameters.minSamplesSplit);
    } else {
      model = new NaiveBayesClassifier();
    }

    model.fit(trainX, trainY, featureNames);
    const preds = model.predict(valX);

    // Calculate validation accuracy
    let correct = 0;
    preds.forEach((pred: string, idx: number) => {
      if (pred === valY[idx]) correct++;
    });

    const foldAcc = correct / valX.length;
    foldScores.push(foldAcc);
  }

  const sum = foldScores.reduce((a, b) => a + b, 0);
  const mean = sum / foldsCount;
  const variance = foldScores.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / foldsCount;
  const std = Math.sqrt(variance);

  return {
    folds: foldScores.map(v => Math.round(v * 1000) / 1000),
    mean: Math.round(mean * 1000) / 1000,
    std: Math.round(std * 1000) / 1000
  };
}
