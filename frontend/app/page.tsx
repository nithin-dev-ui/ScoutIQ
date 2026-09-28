"use client";

import { FormEvent, useState } from "react";
import ReactMarkdown from "react-markdown";

type Source = {
  title?: string;
  link?: string;
  source?: string;
  domain?: string;
  source_type?: string;
  quality_score?: number;
  query_type?: string;
  engine?: string;
};

type KeyFinding = {
  finding?: string;
  source?: string;
  domain?: string;
  source_type?: string;
  query_type?: string;
  engine?: string;
  quality_score?: number;
  link?: string;
};

type Comparison = {
  topic_a?: string;
  topic_b?: string;
  a_evidence?: unknown[];
  b_evidence?: unknown[];
  shared_evidence?: unknown[];
  stats?: {
    topic_a_results?: number;
    topic_b_results?: number;
    shared_results?: number;
  };
};

type ResearchTrace = {
  query_type?: string;
  engine?: string;
  evidence_count?: number;
};

type Report = {
  summary?: string;
  key_findings?: KeyFinding[];
  comparison?: Comparison;
  ai_reasoning?: string | null;
  ai_reasoning_status?: string;
  limitations?: string[];
  sources?: Source[];
  research_trace?: ResearchTrace[];
};

type ResearchResult = {
  question: string;
  evidence_count: number;
  research_rounds: number;
  gap_count: number;
  llm_status: string;
  report: Report;
};

const stages = [
  "Planning",
  "Searching",
  "Verifying",
  "Detecting gaps",
  "Reasoning",
  "Generating report",
];

export default function Home() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState<ResearchResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeStage, setActiveStage] = useState(-1);
  const [error, setError] = useState("");

  async function investigate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!question.trim()) {
      setError("Enter a research question first.");
      return;
    }

    setLoading(true);
    setResult(null);
    setError("");
    setActiveStage(0);

    const stageTimer = setInterval(() => {
      setActiveStage((current) => {
        if (current >= stages.length - 1) {
          return current;
        }

        return current + 1;
      });
    }, 1200);

    try {
      const response = await fetch(
        "https://scoutiq-backend-5dc6.onrender.com/research",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data?.detail ||
            "ScoutIQ could not complete the investigation."
        );
      }

      setResult(data);
      setActiveStage(stages.length - 1);
    } catch (err) {
      if (err instanceof Error) {
       if (
  err.message.includes("Rate limit exceeded") ||
  err.message.includes("too_many_requests") ||
  err.message.includes("429") ||
  err.message.includes("service_unavailable") ||
  err.message.includes("503") ||
  err.message.includes("high demand")
) {
          setError(
            "AI reasoning is temporarily unavailable because the Gemini free-tier limit has been reached. ScoutIQ's search and evidence pipeline is still working."
          );
        } else {
          setError(err.message);
        }
      } else {
        setError(
          "Something went wrong while investigating."
        );
      }
    } finally {
      clearInterval(stageTimer);
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="mx-auto max-w-7xl px-6 py-8 lg:px-10">

        {/* Header */}
        <header className="flex flex-col gap-5 border-b border-white/10 pb-8 md:flex-row md:items-center md:justify-between">
          <div>
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-cyan-400 text-xl font-black text-slate-950">
                S
              </div>

              <div>
                <h1 className="text-2xl font-bold tracking-tight">
                  ScoutIQ
                </h1>

                <p className="text-xs uppercase tracking-[0.25em] text-slate-400">
                  Research Intelligence Engine
                </p>
              </div>
            </div>
          </div>

          <div className="flex w-fit items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/5 px-4 py-2 text-sm text-emerald-300">
            <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-400" />
            Intelligence system online
          </div>
        </header>

        {/* Hero */}
        <section className="py-14">
          <div className="max-w-4xl">
            <p className="mb-4 text-sm font-semibold uppercase tracking-[0.25em] text-cyan-400">
              AI-powered evidence discovery
            </p>

            <h2 className="text-4xl font-bold leading-tight tracking-tight md:text-6xl">
              Ask a question.
              <br />
              <span className="text-cyan-400">
                Scout the evidence.
              </span>
            </h2>

            <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-400">
              ScoutIQ investigates complex questions using live
              search, source verification, gap detection,
              iterative research, and grounded AI reasoning.
            </p>

            <div className="mt-7 flex flex-wrap gap-3 text-xs text-slate-500">
              <span className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1.5">
                Live search
              </span>

              <span className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1.5">
                Source verification
              </span>

              <span className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1.5">
                Gap detection
              </span>

              <span className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1.5">
                Grounded AI
              </span>
            </div>
          </div>
        </section>

        {/* Search */}
        <section className="rounded-3xl border border-cyan-400/10 bg-gradient-to-br from-cyan-400/[0.05] via-white/[0.03] to-transparent p-5 shadow-2xl shadow-cyan-950/20 md:p-7">
          <form onSubmit={investigate}>
            <div className="flex items-center justify-between">
              <label
                htmlFor="question"
                className="text-sm font-semibold text-slate-300"
              >
                Research question
              </label>

              <span className="text-[11px] uppercase tracking-wider text-slate-600">
                Evidence-first research
              </span>
            </div>

            <textarea
              id="question"
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              placeholder="Example: Should students learn Python or JavaScript first for AI software careers in 2026?"
              rows={4}
              disabled={loading}
              className="mt-3 w-full resize-none rounded-2xl border border-white/10 bg-slate-900 px-5 py-4 text-base leading-7 text-white outline-none transition placeholder:text-slate-600 focus:border-cyan-400/60 focus:ring-2 focus:ring-cyan-400/10 disabled:opacity-60"
            />

            <div className="mt-5 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
              <p className="max-w-xl text-xs leading-5 text-slate-500">
                ScoutIQ uses live SerpApi evidence and grounded
                Gemini reasoning. The AI reasoning layer is based
                on evidence collected by the research pipeline.
              </p>

              <button
                type="submit"
                disabled={loading}
                className="rounded-xl bg-cyan-400 px-7 py-3.5 font-bold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading
                  ? "Investigating..."
                  : "Start Investigation →"}
              </button>
            </div>
          </form>

          {error && (
            <div className="mt-5 rounded-xl border border-red-400/20 bg-red-400/5 px-4 py-3 text-sm text-red-300">
              {error}
            </div>
          )}
        </section>

        {/* Pipeline */}
        {(loading || result) && (
          <section className="mt-8 rounded-3xl border border-white/10 bg-white/[0.02] p-5 md:p-7">
            <div className="mb-6 flex items-end justify-between">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                  Investigation pipeline
                </p>

                <h3 className="mt-2 text-xl font-semibold text-white">
                  Evidence to intelligence
                </h3>
              </div>

              {loading && (
                <span className="text-xs font-medium text-cyan-400">
                  Processing...
                </span>
              )}
            </div>

            <div className="grid gap-3 md:grid-cols-6">
              {stages.map((stage, index) => {
                const completed = activeStage >= index;
                const current =
                  loading && activeStage === index;

                return (
                  <div
                    key={stage}
                    className={`rounded-xl border p-4 transition ${
                      completed
                        ? "border-cyan-400/30 bg-cyan-400/5"
                        : "border-white/10 bg-slate-900/40"
                    }`}
                  >
                    <div className="mb-3 flex items-center justify-between">
                      <span className="text-xs text-slate-500">
                        0{index + 1}
                      </span>

                      <span
                        className={`h-2.5 w-2.5 rounded-full ${
                          completed
                            ? "bg-cyan-400"
                            : "bg-slate-700"
                        } ${
                          current ? "animate-pulse" : ""
                        }`}
                      />
                    </div>

                    <p
                      className={`text-sm font-semibold ${
                        completed
                          ? "text-cyan-300"
                          : "text-slate-500"
                      }`}
                    >
                      {stage}
                    </p>
                  </div>
                );
              })}
            </div>
          </section>
        )}

        {/* Results */}
        {result && (
          <section className="mt-8 space-y-8">

            {/* Metrics */}
            <div className="grid gap-4 md:grid-cols-4">
              <MetricCard
                label="Evidence items"
                value={result.evidence_count}
                accent="cyan"
              />

              <MetricCard
                label="Research rounds"
                value={result.research_rounds}
                accent="blue"
              />

              <MetricCard
                label="Detected gaps"
                value={result.gap_count}
                accent="amber"
              />

              <MetricCard
                label="LLM status"
                value={
                  result.llm_status === "generated"
                    ? "Generated"
                    : result.llm_status
                }
                accent="green"
              />
            </div>

            {/* Research Trace */}
            {result.report?.research_trace?.length ? (
              <section className="rounded-3xl border border-cyan-400/10 bg-gradient-to-br from-cyan-400/[0.06] via-white/[0.03] to-transparent p-6 md:p-8">
                <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.22em] text-cyan-400">
                      Research trace
                    </p>

                    <h3 className="mt-2 text-2xl font-bold tracking-tight">
                      How ScoutIQ investigated
                    </h3>

                    <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
                      A transparent view of the search engines and
                      research paths that contributed evidence to
                      this investigation.
                    </p>
                  </div>

                  <div className="w-fit rounded-xl border border-white/10 bg-black/20 px-4 py-3">
                    <p className="text-[10px] uppercase tracking-[0.18em] text-slate-500">
                      Research paths
                    </p>

                    <p className="mt-1 text-2xl font-bold text-white">
                      {result.report.research_trace.length}
                    </p>
                  </div>
                </div>

                <div className="relative">
                  <div className="absolute left-[18px] top-6 hidden h-[calc(100%-48px)] w-px bg-gradient-to-b from-cyan-400/40 via-white/10 to-transparent md:block" />

                  <div className="space-y-4">
                    {result.report.research_trace.map(
                      (trace, index) => (
                        <div
                          key={`${trace.query_type}-${trace.engine}-${index}`}
                          className="relative rounded-2xl border border-white/10 bg-slate-950/50 p-5 transition hover:border-cyan-400/20 hover:bg-white/[0.04]"
                        >
                          <div className="flex items-start gap-4">
                            <div className="relative z-10 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-cyan-400/20 bg-slate-950 text-xs font-bold text-cyan-300">
                              {String(index + 1).padStart(2, "0")}
                            </div>

                            <div className="min-w-0 flex-1">
                              <div className="flex flex-wrap items-center gap-2">
                                <span className="rounded-full border border-cyan-400/15 bg-cyan-400/10 px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider text-cyan-300">
                                  Live
                                </span>

                                <span className="rounded-full border border-white/10 bg-white/[0.04] px-2.5 py-1 text-xs capitalize text-slate-300">
                                  {(trace.query_type || "web").replace(
                                    /\_/g,
                                    " "
                                  )}
                                </span>
                              </div>

                              <div className="mt-4 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
                                <div>
                                  <p className="text-sm font-semibold text-white">
                                    Search engine
                                  </p>

                                  <p className="mt-1 text-sm text-slate-400">
                                    {trace.engine || "Unknown"}
                                  </p>
                                </div>

                                <div className="rounded-xl border border-white/10 bg-white/[0.03] px-4 py-3 sm:min-w-[130px] sm:text-right">
                                  <p className="text-2xl font-bold text-cyan-300">
                                    {trace.evidence_count || 0}
                                  </p>

                                  <p className="mt-1 text-[10px] uppercase tracking-wider text-slate-600">
                                    evidence items
                                  </p>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      )
                    )}
                  </div>
                </div>
              </section>
            ) : null}

            {/* AI Reasoning */}
            {result.report?.ai_reasoning && (
              <section className="rounded-3xl border border-cyan-400/20 bg-gradient-to-br from-cyan-400/[0.06] via-white/[0.03] to-transparent p-6 md:p-8">
                <div className="mb-6 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-400">
                      Grounded AI reasoning
                    </p>

                    <h3 className="mt-2 text-2xl font-bold">
                      Gemini Research Assessment
                    </h3>
                  </div>

                  <span className="w-fit rounded-full border border-emerald-400/20 bg-emerald-400/5 px-3 py-1 text-xs font-semibold text-emerald-300">
                    Evidence grounded
                  </span>
                </div>

                <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-5 md:p-7">
                  <ReactMarkdown
                    components={{
                      h1: ({ children }) => (
                        <h4 className="mb-4 text-xl font-bold text-white">
                          {children}
                        </h4>
                      ),

                      h2: ({ children }) => (
                        <h4 className="mb-4 mt-6 text-lg font-bold text-cyan-300">
                          {children}
                        </h4>
                      ),

                      h3: ({ children }) => (
                        <h4 className="mb-3 mt-5 text-base font-bold text-cyan-300">
                          {children}
                        </h4>
                      ),

                      h4: ({ children }) => (
                        <h4 className="mb-3 mt-5 text-base font-bold text-cyan-300">
                          {children}
                        </h4>
                      ),

                      p: ({ children }) => (
                        <p className="mb-4 text-sm leading-7 text-slate-300 last:mb-0">
                          {children}
                        </p>
                      ),

                      ul: ({ children }) => (
                        <ul className="mb-5 ml-5 list-disc space-y-2 text-sm leading-7 text-slate-300">
                          {children}
                        </ul>
                      ),

                      ol: ({ children }) => (
                        <ol className="mb-5 ml-5 list-decimal space-y-2 text-sm leading-7 text-slate-300">
                          {children}
                        </ol>
                      ),

                      li: ({ children }) => (
                        <li className="pl-1">
                          {children}
                        </li>
                      ),

                      strong: ({ children }) => (
                        <strong className="font-semibold text-white">
                          {children}
                        </strong>
                      ),

                      em: ({ children }) => (
                        <em className="text-slate-400">
                          {children}
                        </em>
                      ),
                    }}
                  >
                    {result.report.ai_reasoning}
                  </ReactMarkdown>
                </div>

                <p className="mt-4 text-xs leading-5 text-slate-500">
                  Gemini receives the verified evidence collected
                  by ScoutIQ. The reasoning layer is instructed not
                  to invent facts, sources, statistics, URLs, or
                  quotations.
                </p>
              </section>
            )}

            {/* Intelligence Report */}
            <div className="grid gap-8 lg:grid-cols-[1.5fr_1fr]">

              {/* Main report */}
              <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 md:p-8">
                <div className="mb-7">
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-400">
                    Intelligence report
                  </p>

                  <h3 className="mt-2 text-2xl font-bold">
                    Evidence-backed findings
                  </h3>

                  <p className="mt-2 text-sm text-slate-500">
                    Findings prioritized from the verified evidence
                    collected during the investigation.
                  </p>
                </div>

                {result.report?.summary && (
                  <div className="mb-8 rounded-2xl border border-white/10 bg-slate-900/60 p-5">
                    <div className="flex items-center gap-2">
                      <span className="h-2 w-2 rounded-full bg-cyan-400" />

                      <p className="text-sm font-semibold text-slate-300">
                        Evidence overview
                      </p>
                    </div>

                    <p className="mt-3 leading-7 text-slate-400">
                      {result.report.summary}
                    </p>
                  </div>
                )}

                <div className="space-y-4">
                  {result.report?.key_findings?.length ? (
                    result.report.key_findings.map(
                      (finding, index) => (
                        <div
                          key={`${finding.finding || "finding"}-${index}`}
                          className="rounded-2xl border border-white/10 bg-slate-900/40 p-5 transition hover:border-cyan-400/15"
                        >
                          <div className="flex gap-4">
                            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-cyan-400/10 bg-cyan-400/10 text-sm font-bold text-cyan-300">
                              {index + 1}
                            </div>

                            <div className="min-w-0 flex-1">
                              <p className="leading-7 text-slate-300">
                                {finding.finding ||
                                  "No text summary was available for this evidence item."}
                              </p>

                              <div className="mt-4 flex flex-wrap gap-2">
                                {finding.source_type && (
                                  <span className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1 text-xs text-slate-400">
                                    {finding.source_type}
                                  </span>
                                )}

                                {finding.engine && (
                                  <span className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1 text-xs text-slate-400">
                                    {finding.engine}
                                  </span>
                                )}

                                {finding.quality_score !==
                                  undefined && (
                                  <span className="rounded-full border border-cyan-400/10 bg-cyan-400/5 px-3 py-1 text-xs text-cyan-300">
                                    Quality:{" "}
                                    {finding.quality_score}/8
                                  </span>
                                )}
                              </div>

                              {finding.source && (
                                <p className="mt-4 line-clamp-2 text-xs text-slate-500">
                                  Source: {finding.source}
                                </p>
                              )}

                              {finding.link && (
                                <a
                                  href={finding.link}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="mt-3 inline-block text-xs font-semibold text-cyan-400 hover:text-cyan-300"
                                >
                                  View supporting source →
                                </a>
                              )}
                            </div>
                          </div>
                        </div>
                      )
                    )
                  ) : (
                    <p className="text-slate-500">
                      No key findings were returned.
                    </p>
                  )}
                </div>
              </div>

              {/* Sources */}
              <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 md:p-8">
                <div className="mb-7">
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-400">
                    Evidence
                  </p>

                  <h3 className="mt-2 text-2xl font-bold">
                    Sources
                  </h3>

                  <p className="mt-2 text-sm text-slate-500">
                    Sources prioritized by ScoutIQ's verification
                    heuristics.
                  </p>
                </div>

                <div className="space-y-3">
                  {result.report?.sources?.length ? (
                    result.report.sources.map(
                      (source, index) => (
                        <a
                          key={`${source.link || "source"}-${index}`}
                          href={source.link || "#"}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block rounded-xl border border-white/10 bg-slate-900/50 p-4 transition hover:border-cyan-400/30 hover:bg-cyan-400/[0.03]"
                        >
                          <div className="flex gap-3">
                            <span className="text-xs font-bold text-cyan-400">
                              {String(index + 1).padStart(2, "0")}
                            </span>

                            <div className="min-w-0">
                              <p className="line-clamp-2 text-sm font-semibold leading-5 text-slate-200">
                                {source.title ||
                                  "Untitled source"}
                              </p>

                              <p className="mt-2 truncate text-xs text-slate-500">
                                {source.domain ||
                                  source.link ||
                                  "Source"}
                              </p>

                              <div className="mt-2 flex flex-wrap gap-2">
                                {source.source_type && (
                                  <span className="text-[10px] text-slate-600">
                                    {source.source_type}
                                  </span>
                                )}

                                {source.quality_score !==
                                  undefined && (
                                  <span className="text-[10px] font-medium text-cyan-400">
                                    Quality{" "}
                                    {source.quality_score}/8
                                  </span>
                                )}
                              </div>
                            </div>
                          </div>
                        </a>
                      )
                    )
                  ) : (
                    <p className="text-slate-500">
                      No sources returned.
                    </p>
                  )}
                </div>
              </div>
            </div>

            {/* Comparison */}
            {result.report?.comparison?.stats && (
              <section className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 md:p-8">
                <div className="mb-7">
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-400">
                    Comparative evidence
                  </p>

                  <h3 className="mt-2 text-2xl font-bold">
                    Evidence distribution
                  </h3>

                  <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
                    ScoutIQ separates evidence by topic instead of
                    treating a comparison as a single search result.
                  </p>
                </div>

                <div className="grid gap-4 md:grid-cols-3">
                  <ComparisonCard
                    label={
                      result.report.comparison.topic_a ||
                      "Topic A"
                    }
                    value={
                      result.report.comparison.stats
                        .topic_a_results || 0
                    }
                    description="Topic-specific evidence"
                  />

                  <ComparisonCard
                    label={
                      result.report.comparison.topic_b ||
                      "Topic B"
                    }
                    value={
                      result.report.comparison.stats
                        .topic_b_results || 0
                    }
                    description="Topic-specific evidence"
                  />

                  <ComparisonCard
                    label="Shared evidence"
                    value={
                      result.report.comparison.stats
                        .shared_results || 0
                    }
                    description="Evidence mentioning both"
                  />
                </div>
              </section>
            )}

            {/* Limitations */}
            {result.report?.limitations?.length ? (
              <section className="rounded-2xl border border-amber-400/10 bg-amber-400/[0.03] p-6">
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-amber-300">
                  Research limitations
                </p>

                <ul className="mt-4 space-y-2">
                  {result.report.limitations.map(
                    (limitation, index) => (
                      <li
                        key={`${limitation}-${index}`}
                        className="text-sm leading-6 text-amber-200/70"
                      >
                        • {limitation}
                      </li>
                    )
                  )}
                </ul>
              </section>
            ) : null}

            {/* Methodology */}
            <div className="rounded-2xl border border-white/10 bg-white/[0.02] p-5">
              <p className="text-sm leading-6 text-slate-500">
                <span className="font-semibold text-slate-300">
                  Evidence methodology:
                </span>{" "}
                ScoutIQ combines live search evidence, structural
                source verification, gap detection, iterative
                research, and grounded Gemini reasoning. Source
                quality scores are heuristics for prioritization,
                not proof of factual correctness.
              </p>
            </div>
          </section>
        )}

        {/* Footer */}
        <footer className="mt-16 border-t border-white/10 py-8 text-center text-xs text-slate-600">
          ScoutIQ · AI-powered research intelligence · Built with
          SerpApi + Gemini
        </footer>
      </div>
    </main>
  );
}

function MetricCard({
  label,
  value,
  accent,
}: {
  label: string;
  value: string | number;
  accent: "cyan" | "blue" | "amber" | "green";
}) {
  const accentStyles = {
    cyan: "border-cyan-400/15 bg-cyan-400/[0.04] text-cyan-300",
    blue: "border-blue-400/15 bg-blue-400/[0.04] text-blue-300",
    amber: "border-amber-400/15 bg-amber-400/[0.04] text-amber-300",
    green: "border-emerald-400/15 bg-emerald-400/[0.04] text-emerald-300",
  };

  return (
    <div
      className={`rounded-2xl border p-5 ${accentStyles[accent]}`}
    >
      <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
        {label}
      </p>

      <p className="mt-3 text-3xl font-bold text-white">
        {value}
      </p>
    </div>
  );
}

function ComparisonCard({
  label,
  value,
  description,
}: {
  label: string;
  value: number;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-slate-900/50 p-5 transition hover:border-cyan-400/15">
      <p className="text-sm font-semibold text-slate-300">
        {label}
      </p>

      <p className="mt-3 text-4xl font-bold text-white">
        {value}
      </p>

      <p className="mt-2 text-xs text-slate-600">
        {description}
      </p>
    </div>
  );
}