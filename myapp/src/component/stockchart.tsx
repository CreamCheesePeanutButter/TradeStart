import { useEffect, useState } from "react";
import { LineChart } from "@mui/x-charts/LineChart";
import { colors } from "@mui/material";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:5000";

interface HistoryPoint {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
}

interface Props {
  ticker: string;
}

export default function StockChart({ ticker }: Props) {
  const [dates, setDates] = useState<string[]>([]);
  const [openPrices, setOpenPrices] = useState<number[]>([]);
  const [closePrices, setClosePrices] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!ticker) return;

    const fetchHistory = async () => {
      setLoading(true);

      try {
        const res = await fetch(`${API_URL}/stocks/${ticker}/history`);
        if (!res.ok) throw new Error("history fetch failed");

        const data = await res.json();

        const history: HistoryPoint[] = (data.history ?? []).filter(
          (h) => h?.date && h.open != null && h.close != null,
        );

        setDates(history.map((h) => h.date));
        setOpenPrices(history.map((h) => Number(h.open)));
        setClosePrices(history.map((h) => Number(h.close)));
      } catch {
        setDates([]);
        setOpenPrices([]);
        setClosePrices([]);
      }

      setLoading(false);
    };

    fetchHistory();
  }, [ticker]);

  if (loading) return <p>Loading chart...</p>;

  if (dates.length === 0) return <p>No history data</p>;

  return (
    <div>
      <h1>Stock value in 1 month</h1>
      <LineChart
        height={250}
        // The 'title' prop works, but we must style the SVG text element
        title="Stock value in 1 month"
        series={[
          { label: "Open", data: openPrices },
          { label: "Close", data: closePrices },
        ]}
        xAxis={[{ scaleType: "point", data: dates }]}
        margin={{ top: 50, bottom: 50, left: 60, right: 30 }} // Adds space for labels
        sx={{
          // 1. Force ALL text in the chart to be white (Titles, Legend, Axes)
          "& text": {
            fill: "white !important",
          },
          // 2. Make the Legend labels ("Open" & "Close") white
          "& .MuiChartsLegend-label": {
            fill: "white !important",
          },
          // 3. Make all Axis lines and small tick marks white
          "& .MuiChartsAxis-line, & .MuiChartsAxis-tick": {
            stroke: "white !important",
          },
          // 4. Make the Axis numbers/dates white
          "& .MuiChartsAxis-tickLabel": {
            fill: "white !important",
          },
          // 5. Optional: Make the grid lines a subtle white (if you use them)
          "& .MuiChartsGrid-line": {
            stroke: "rgba(255, 255, 255, 0.1) !important",
          },
        }}
      />
    </div>
  );
}
