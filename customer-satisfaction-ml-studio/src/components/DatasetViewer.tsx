import React, { useState, useMemo } from "react";
import { DataRow, SummaryStats } from "../types/ml";
import { calculateSummaryStats } from "../utils/mlEngine";
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  Legend, 
  ScatterChart, 
  Scatter,
  Cell
} from "recharts";
import { 
  Database, 
  Table, 
  BarChart3, 
  AlertTriangle, 
  Plus, 
  RotateCcw, 
  Check, 
  HelpCircle,
  TrendingUp,
  Award,
  Users
} from "lucide-react";

interface DatasetViewerProps {
  data: DataRow[];
  onUpdateData: (newData: DataRow[]) => void;
  onResetData: () => void;
}

export default function DatasetViewer({ data, onUpdateData, onResetData }: DatasetViewerProps) {
  const [activeTab, setActiveTab] = useState<"table" | "stats" | "charts">("table");
  const [searchTerm, setSearchTerm] = useState("");
  const [page, setPage] = useState(1);
  const itemsPerPage = 8;

  const [csvInput, setCsvInput] = useState("");
  const [showCsvImporter, setShowCsvImporter] = useState(false);

  // Compute summary stats dynamically
  const stats = useMemo(() => calculateSummaryStats(data), [data]);

  // Compute label distribution for chart
  const labelDistribution = useMemo(() => {
    const counts: Record<string, number> = { Satisfied: 0, Neutral: 0, Unsatisfied: 0, "Missing": 0 };
    data.forEach(row => {
      const label = row["Satisfaction Level"] || "Missing";
      counts[label] = (counts[label] || 0) + 1;
    });
    return Object.entries(counts).map(([name, value]) => ({ name, value }));
  }, [data]);

  // Grouped data for Membership Type vs Satisfaction
  const membershipDistribution = useMemo(() => {
    const counts: Record<string, Record<string, number>> = {
      Gold: { Satisfied: 0, Neutral: 0, Unsatisfied: 0 },
      Silver: { Satisfied: 0, Neutral: 0, Unsatisfied: 0 },
      Bronze: { Satisfied: 0, Neutral: 0, Unsatisfied: 0 }
    };

    data.forEach(row => {
      const mem = row["Membership Type"] as "Gold" | "Silver" | "Bronze";
      const sat = row["Satisfaction Level"] || "Unsatisfied"; // default to unsatisfied if missing for visual
      if (counts[mem] && counts[mem][sat] !== undefined) {
        counts[mem][sat]++;
      }
    });

    return Object.entries(counts).map(([membership, satCounts]) => ({
      membership,
      ...satCounts
    }));
  }, [data]);

  // Scatter data: Spend vs Rating colored by satisfaction
  const scatterData = useMemo(() => {
    const colors: Record<string, string> = {
      Satisfied: "#10b981", // green-500
      Neutral: "#f59e0b",   // amber-500
      Unsatisfied: "#ef4444", // red-500
      "": "#6b7280"          // gray-500 for missing
    };

    return data.map(row => ({
      name: `ID ${row["Customer ID"]}`,
      spend: row["Total Spend"],
      rating: row["Average Rating"],
      satisfaction: row["Satisfaction Level"] || "Missing",
      color: colors[row["Satisfaction Level"]] || "#6b7280"
    }));
  }, [data]);

  // Filtered rows for the table
  const filteredData = useMemo(() => {
    return data.filter(row => {
      const matchSearch = 
        row.City.toLowerCase().includes(searchTerm.toLowerCase()) ||
        row["Membership Type"].toLowerCase().includes(searchTerm.toLowerCase()) ||
        (row["Satisfaction Level"] || "Missing").toLowerCase().includes(searchTerm.toLowerCase()) ||
        String(row["Customer ID"]).includes(searchTerm);
      return matchSearch;
    });
  }, [data, searchTerm]);

  // Paginated data
  const paginatedData = useMemo(() => {
    const startIndex = (page - 1) * itemsPerPage;
    return filteredData.slice(startIndex, startIndex + itemsPerPage);
  }, [filteredData, page]);

  const totalPages = Math.ceil(filteredData.length / itemsPerPage);

  // Missing values details
  const missingRowsCount = useMemo(() => {
    return data.filter(row => !row["Satisfaction Level"] || row["Satisfaction Level"].trim() === "").length;
  }, [data]);

  const handleCsvImport = () => {
    try {
      const lines = csvInput.trim().split("\n");
      if (lines.length <= 1) return;
      const parsed: DataRow[] = [];
      const headers = lines[0].split(",").map(h => h.trim());

      for (let i = 1; i < lines.length; i++) {
        const line = lines[i].trim();
        if (!line) continue;
        const values = line.split(",").map(v => v.trim());
        const row: any = {};
        headers.forEach((header, idx) => {
          const val = values[idx];
          if (header === "Customer ID" || header === "Age" || header === "Items Purchased" || header === "Days Since Last Purchase") {
            row[header] = parseInt(val, 10) || 0;
          } else if (header === "Total Spend" || header === "Average Rating") {
            row[header] = parseFloat(val) || 0;
          } else if (header === "Discount Applied") {
            row[header] = val?.toUpperCase() === "TRUE";
          } else {
            row[header] = val || "";
          }
        });
        parsed.push(row as DataRow);
      }
      onUpdateData(parsed);
      setShowCsvImporter(false);
      setCsvInput("");
    } catch (e) {
      alert("CSV parse karne me error hui. Format check karein.");
    }
  };

  return (
    <div id="dataset-viewer" className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-gray-100 pb-5 mb-6">
        <div>
          <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2">
            <Database className="w-5 h-5 text-indigo-600" />
            Dataset Explorer
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            Analyze, clean, and visualize the customer satisfaction dataset ({data.length} records).
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setShowCsvImporter(!showCsvImporter)}
            className="px-3.5 py-1.5 bg-indigo-50 text-indigo-600 hover:bg-indigo-100 rounded-lg text-sm font-medium flex items-center gap-1.5 transition-colors"
          >
            <Plus className="w-4 h-4" /> Import CSV
          </button>
          <button
            onClick={onResetData}
            className="px-3.5 py-1.5 bg-gray-50 text-gray-600 hover:bg-gray-100 rounded-lg text-sm font-medium flex items-center gap-1.5 transition-colors"
            title="Reset Dataset to Default"
          >
            <RotateCcw className="w-4 h-4" /> Reset
          </button>
        </div>
      </div>

      {/* CSV Importer Modal-like expandable */}
      {showCsvImporter && (
        <div className="bg-gray-50 rounded-xl p-4 border border-gray-200 mb-6 animate-fade-in">
          <h3 className="text-sm font-bold text-gray-800 mb-2">Paste Custom CSV Data</h3>
          <p className="text-xs text-gray-500 mb-3">
            Header parameters bilkul default format ke hone chahiye: 
            <code className="bg-white px-1.5 py-0.5 rounded ml-1 text-indigo-600">Customer ID,Gender,Age,City,Membership Type,Total Spend,Items Purchased,Average Rating,Discount Applied,Days Since Last Purchase,Satisfaction Level</code>
          </p>
          <textarea
            value={csvInput}
            onChange={(e) => setCsvInput(e.target.value)}
            placeholder="ID,Gender,Age,City,Membership,Spend,Items,Rating,Discount,Days,Satisfaction..."
            rows={5}
            className="w-full text-xs font-mono p-3 bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500 mb-3"
          />
          <div className="flex gap-2 justify-end">
            <button
              onClick={() => setShowCsvImporter(false)}
              className="px-3 py-1.5 text-xs font-medium text-gray-600 bg-white border border-gray-200 rounded-md hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              onClick={handleCsvImport}
              className="px-3.5 py-1.5 text-xs font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700"
            >
              Apply Dataset
            </button>
          </div>
        </div>
      )}

      {/* Key Metric Highlights */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-indigo-50/50 rounded-xl p-4 border border-indigo-100/50">
          <div className="flex items-center gap-2 text-indigo-700 text-xs font-medium uppercase tracking-wider mb-1">
            <Users className="w-4 h-4" /> Total Customers
          </div>
          <p className="text-2xl font-extrabold text-indigo-900">{data.length}</p>
        </div>
        <div className="bg-emerald-50/50 rounded-xl p-4 border border-emerald-100/50">
          <div className="flex items-center gap-2 text-emerald-700 text-xs font-medium uppercase tracking-wider mb-1">
            <TrendingUp className="w-4 h-4" /> Avg Total Spend
          </div>
          <p className="text-2xl font-extrabold text-emerald-900">
            ${(data.reduce((acc, row) => acc + row["Total Spend"], 0) / data.length || 0).toFixed(2)}
          </p>
        </div>
        <div className="bg-amber-50/50 rounded-xl p-4 border border-amber-100/50">
          <div className="flex items-center gap-2 text-amber-700 text-xs font-medium uppercase tracking-wider mb-1">
            <Award className="w-4 h-4" /> Average Rating
          </div>
          <p className="text-2xl font-extrabold text-amber-900">
            {(data.reduce((acc, row) => acc + row["Average Rating"], 0) / data.length || 0).toFixed(1)} / 5.0
          </p>
        </div>
        <div className={`rounded-xl p-4 border ${missingRowsCount > 0 ? "bg-red-50 border-red-100" : "bg-teal-50 border-teal-100"}`}>
          <div className={`flex items-center gap-2 text-xs font-medium uppercase tracking-wider mb-1 ${missingRowsCount > 0 ? "text-red-700" : "text-teal-700"}`}>
            <AlertTriangle className="w-4 h-4" /> Missing Targets
          </div>
          <p className={`text-2xl font-extrabold ${missingRowsCount > 0 ? "text-red-900" : "text-teal-900"}`}>
            {missingRowsCount} rows
          </p>
        </div>
      </div>

      {/* Tabs Menu */}
      <div className="flex border-b border-gray-100 mb-6">
        <button
          onClick={() => setActiveTab("table")}
          className={`px-4 py-2.5 -mb-px text-sm font-medium flex items-center gap-2 border-b-2 transition-all ${
            activeTab === "table"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-gray-500 hover:text-gray-700"
          }`}
        >
          <Table className="w-4 h-4" /> Data Table ({filteredData.length})
        </button>
        <button
          onClick={() => setActiveTab("stats")}
          className={`px-4 py-2.5 -mb-px text-sm font-medium flex items-center gap-2 border-b-2 transition-all ${
            activeTab === "stats"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-gray-500 hover:text-gray-700"
          }`}
        >
          <Database className="w-4 h-4" /> Feature Statistics
        </button>
        <button
          onClick={() => setActiveTab("charts")}
          className={`px-4 py-2.5 -mb-px text-sm font-medium flex items-center gap-2 border-b-2 transition-all ${
            activeTab === "charts"
              ? "border-indigo-600 text-indigo-600"
              : "border-transparent text-gray-500 hover:text-gray-700"
          }`}
        >
          <BarChart3 className="w-4 h-4" /> Visual Analysis
        </button>
      </div>

      {/* Tab Contents */}
      {activeTab === "table" && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <input
              type="text"
              placeholder="Search by City, Membership, Satisfaction..."
              value={searchTerm}
              onChange={(e) => {
                setSearchTerm(e.target.value);
                setPage(1);
              }}
              className="w-full sm:w-80 px-3.5 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
            {missingRowsCount > 0 && (
              <span className="text-xs bg-amber-50 text-amber-700 px-2.5 py-1 rounded-full border border-amber-200 flex items-center gap-1">
                <AlertTriangle className="w-3.5 h-3.5" /> Note: satisfaction values highlighted in red represent targets to be predicted during training.
              </span>
            )}
          </div>

          <div className="overflow-x-auto border border-gray-100 rounded-xl">
            <table className="w-full text-left text-sm text-gray-600">
              <thead className="bg-gray-50 text-xs font-semibold text-gray-700 uppercase border-b border-gray-100">
                <tr>
                  <th className="py-3 px-4">ID</th>
                  <th className="py-3 px-4">Gender</th>
                  <th className="py-3 px-4">Age</th>
                  <th className="py-3 px-4">City</th>
                  <th className="py-3 px-4">Membership</th>
                  <th className="py-3 px-4">Spend</th>
                  <th className="py-3 px-4">Items</th>
                  <th className="py-3 px-4">Rating</th>
                  <th className="py-3 px-4">Discount</th>
                  <th className="py-3 px-4">Days Since</th>
                  <th className="py-3 px-4">Satisfaction</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {paginatedData.map((row) => (
                  <tr key={row["Customer ID"]} className="hover:bg-gray-50/50 transition-colors">
                    <td className="py-3 px-4 font-mono font-bold text-gray-900 text-xs">#{row["Customer ID"]}</td>
                    <td className="py-3 px-4">{row.Gender}</td>
                    <td className="py-3 px-4">{row.Age}</td>
                    <td className="py-3 px-4">{row.City}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                        row["Membership Type"] === "Gold" ? "bg-yellow-50 text-yellow-700 border border-yellow-200" :
                        row["Membership Type"] === "Silver" ? "bg-slate-50 text-slate-700 border border-slate-200" :
                        "bg-orange-50 text-orange-700 border border-orange-200"
                      }`}>
                        {row["Membership Type"]}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono">${row["Total Spend"]}</td>
                    <td className="py-3 px-4">{row["Items Purchased"]}</td>
                    <td className="py-3 px-4">{row["Average Rating"]} ★</td>
                    <td className="py-3 px-4">
                      <span className={`px-1.5 py-0.5 rounded text-xs font-mono font-bold ${
                        row["Discount Applied"] ? "bg-teal-50 text-teal-700" : "bg-gray-50 text-gray-500"
                      }`}>
                        {row["Discount Applied"] ? "TRUE" : "FALSE"}
                      </span>
                    </td>
                    <td className="py-3 px-4">{row["Days Since Last Purchase"]}</td>
                    <td className="py-3 px-4 font-bold">
                      {row["Satisfaction Level"] ? (
                        <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${
                          row["Satisfaction Level"] === "Satisfied" ? "bg-emerald-50 text-emerald-700 border border-emerald-200" :
                          row["Satisfaction Level"] === "Neutral" ? "bg-amber-50 text-amber-700 border border-amber-200" :
                          "bg-red-50 text-red-700 border border-red-200"
                        }`}>
                          {row["Satisfaction Level"]}
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-red-100 text-red-800 animate-pulse border border-red-300">
                          MISSING (Imputed)
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between border-t border-gray-100 pt-4 text-sm">
              <span className="text-gray-500">
                Showing <strong className="text-gray-900">{(page - 1) * itemsPerPage + 1}</strong> to{" "}
                <strong className="text-gray-900">{Math.min(page * itemsPerPage, filteredData.length)}</strong> of{" "}
                <strong className="text-gray-900">{filteredData.length}</strong> entries
              </span>
              <div className="flex items-center gap-1.5">
                <button
                  onClick={() => setPage(p => Math.max(p - 1, 1))}
                  disabled={page === 1}
                  className="px-3 py-1 bg-white border border-gray-200 text-gray-600 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                <span className="text-gray-700 font-medium">
                  Page {page} of {totalPages}
                </span>
                <button
                  onClick={() => setPage(p => Math.min(p + 1, totalPages))}
                  disabled={page === totalPages}
                  className="px-3 py-1 bg-white border border-gray-200 text-gray-600 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === "stats" && (
        <div className="overflow-x-auto border border-gray-100 rounded-xl">
          <table className="w-full text-left text-sm text-gray-600">
            <thead className="bg-gray-50 text-xs font-semibold text-gray-700 uppercase border-b border-gray-100">
              <tr>
                <th className="py-3 px-4">Feature Name</th>
                <th className="py-3 px-4">DataType</th>
                <th className="py-3 px-4">Missing Value Count</th>
                <th className="py-3 px-4">Mean / Unique values</th>
                <th className="py-3 px-4">Std Dev</th>
                <th className="py-3 px-4">Min</th>
                <th className="py-3 px-4">Median</th>
                <th className="py-3 px-4">Max</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {stats.map((s) => (
                <tr key={s.columnName} className="hover:bg-gray-50/50 transition-colors">
                  <td className="py-3 px-4 font-medium text-gray-900">{s.columnName}</td>
                  <td className="py-3 px-4">
                    <span className="px-1.5 py-0.5 bg-gray-100 text-gray-600 rounded text-xs font-mono font-semibold uppercase">
                      {s.type}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${
                      s.missingCount > 0 ? "bg-red-50 text-red-600 border border-red-100" : "bg-emerald-50 text-emerald-700"
                    }`}>
                      {s.missingCount} missing
                    </span>
                  </td>
                  <td className="py-3 px-4 max-w-xs truncate">
                    {s.type === "numerical" && s.mean !== undefined ? (
                      <span className="font-mono">{s.mean}</span>
                    ) : s.uniqueValues ? (
                      <span className="text-xs text-indigo-600 font-semibold">
                        [{s.uniqueValues.join(", ")}]
                      </span>
                    ) : (
                      "-"
                    )}
                  </td>
                  <td className="py-3 px-4 font-mono">{s.std !== undefined ? s.std : "-"}</td>
                  <td className="py-3 px-4 font-mono">{s.min !== undefined ? s.min : "-"}</td>
                  <td className="py-3 px-4 font-mono">{s.median !== undefined ? s.median : "-"}</td>
                  <td className="py-3 px-4 font-mono">{s.max !== undefined ? s.max : "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === "charts" && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Chart 1: Target distribution */}
          <div className="bg-gray-50 rounded-xl p-5 border border-gray-100">
            <h3 className="text-sm font-bold text-gray-800 mb-4 flex items-center gap-1.5">
              Target Distribution (Satisfaction Level)
            </h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={labelDistribution.filter(d => d.name !== "Missing" || d.value > 0)}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="name" stroke="#6b7280" style={{ fontSize: "12px" }} />
                  <YAxis stroke="#6b7280" style={{ fontSize: "12px" }} />
                  <Tooltip cursor={{ fill: "rgba(0, 0, 0, 0.05)" }} />
                  <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                    {labelDistribution.map((entry, index) => {
                      const colors: Record<string, string> = {
                        Satisfied: "#10b981", // emerald-500
                        Neutral: "#f59e0b",   // amber-500
                        Unsatisfied: "#ef4444", // red-500
                        "Missing": "#9ca3af"   // gray-400
                      };
                      return <Cell key={`cell-${index}`} fill={colors[entry.name] || "#6366f1"} />;
                    })}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <p className="text-xs text-gray-500 text-center mt-3">
              Clearly shows whether classes are balanced or imbalanced (important for accuracy metrics!).
            </p>
          </div>

          {/* Chart 2: Membership vs Satisfaction (Stacked) */}
          <div className="bg-gray-50 rounded-xl p-5 border border-gray-100">
            <h3 className="text-sm font-bold text-gray-800 mb-4 flex items-center gap-1.5">
              Membership Type vs Satisfaction Distribution
            </h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={membershipDistribution}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="membership" stroke="#6b7280" style={{ fontSize: "12px" }} />
                  <YAxis stroke="#6b7280" style={{ fontSize: "12px" }} />
                  <Tooltip />
                  <Legend wrapperStyle={{ fontSize: "12px" }} />
                  <Bar dataKey="Satisfied" fill="#10b981" stackId="a" />
                  <Bar dataKey="Neutral" fill="#f59e0b" stackId="a" />
                  <Bar dataKey="Unsatisfied" fill="#ef4444" stackId="a" />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <p className="text-xs text-gray-500 text-center mt-3">
              Gold members display higher satisfaction, while Bronze are mostly unsatisfied.
            </p>
          </div>

          {/* Chart 3: Scatter plot Spend vs Rating */}
          <div className="bg-gray-50 rounded-xl p-5 border border-gray-100 lg:col-span-2">
            <h3 className="text-sm font-bold text-gray-800 mb-2 flex items-center gap-1.5">
              Spend vs. Rating Interaction Plot
            </h3>
            <p className="text-xs text-gray-500 mb-4">
              Green: Satisfied, Orange: Neutral, Red: Unsatisfied. Hover on items to check.
            </p>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis 
                    type="number" 
                    dataKey="spend" 
                    name="Total Spend" 
                    unit="$" 
                    stroke="#6b7280" 
                    style={{ fontSize: "12px" }}
                  />
                  <YAxis 
                    type="number" 
                    dataKey="rating" 
                    name="Average Rating" 
                    domain={[2.5, 5.0]}
                    stroke="#6b7280" 
                    style={{ fontSize: "12px" }}
                  />
                  <Tooltip cursor={{ strokeDasharray: "3 3" }} />
                  <Scatter name="Customers" data={scatterData}>
                    {scatterData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Scatter>
                </ScatterChart>
              </ResponsiveContainer>
            </div>
            <p className="text-xs text-gray-500 text-center mt-3">
              Shows strong linear/cluster boundaries where High Spend + High Rating almost perfectly matches Satisfied customers.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
