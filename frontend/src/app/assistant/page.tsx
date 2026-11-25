"use client";
import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Bot, User, Send, AlertTriangle, Sparkles } from "lucide-react";
import apiClient from "@/lib/api-client";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  citations?: Array<{
    scheme_name: string;
    source_text: string;
    source_page?: number;
  }>;
  timestamp: Date;
}

const SUGGESTIONS = [
  "What scholarships are available for SC students in Andhra Pradesh?",
  "What income limit applies for AP fee reimbursement?",
  "Has the deadline for TS ePass changed recently?",
  "What documents do I need for NSP post-matric scholarship?",
];

export default function AssistantPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setSessionId(crypto.randomUUID());
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendMessage(text?: string) {
    const q = (text ?? input).trim();
    if (!q) return;
    setInput("");

    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: q,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await apiClient.post<{
        answer: string;
        citations?: Message["citations"];
      }>("/assistant/chat", {
        session_id: sessionId,
        message: q,
      });

      const assistantMsg: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: res.data.answer,
        citations: res.data.citations,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      const errorMsg: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content:
          err?.response?.status === 503
            ? "AI service is not configured. Please add an OpenAI or Anthropic API key."
            : "Sorry, I could not process your request. Please try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] max-w-3xl mx-auto p-4">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
          <Bot className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-white">Policy Assistant</h1>
          <p className="text-sm text-slate-500">
            Evidence-linked answers from official scheme documents
          </p>
        </div>
      </div>

      <div className="rounded-xl bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 p-3 flex gap-2 text-xs text-amber-700 dark:text-amber-300 mb-4">
        <AlertTriangle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
        <p>
          Answers are based on uploaded official documents. Always verify with the
          original notification. This is not legal or financial advice.
        </p>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 pb-4">
        {messages.length === 0 && (
          <div className="text-center pt-8 space-y-6">
            <div className="w-16 h-16 rounded-2xl gradient-primary flex items-center justify-center mx-auto">
              <Sparkles className="w-8 h-8 text-white" />
            </div>
            <div>
              <p className="font-semibold text-slate-700 dark:text-slate-300">
                Ask anything about government schemes
              </p>
              <p className="text-sm text-slate-500 mt-1">
                Get answers with citations from official documents
              </p>
            </div>
            <div className="grid gap-2 max-w-md mx-auto">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => sendMessage(s)}
                  className="text-left text-sm p-3 rounded-xl border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-400 transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            {msg.role === "assistant" && (
              <div className="w-7 h-7 rounded-lg gradient-primary flex items-center justify-center shrink-0 mt-1">
                <Bot className="w-4 h-4 text-white" />
              </div>
            )}
            <div
              className={`max-w-[80%] space-y-2 flex flex-col ${
                msg.role === "user" ? "items-end" : "items-start"
              }`}
            >
              <div
                className={`rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                  msg.role === "user"
                    ? "gradient-primary text-white"
                    : "bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200"
                }`}
              >
                {msg.content}
              </div>
              {msg.citations && msg.citations.length > 0 && (
                <div className="space-y-1">
                  {msg.citations.map((c, i) => (
                    <div
                      key={i}
                      className="rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 px-3 py-2 text-xs text-blue-700 dark:text-blue-300"
                    >
                      <span className="font-medium">{c.scheme_name}</span>
                      {c.source_page && (
                        <span className="text-blue-500"> (p.{c.source_page})</span>
                      )}
                      {c.source_text && (
                        <p className="text-blue-600 dark:text-blue-400 mt-0.5 italic">
                          &ldquo;{c.source_text}&rdquo;
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
            {msg.role === "user" && (
              <div className="w-7 h-7 rounded-lg bg-slate-200 dark:bg-slate-700 flex items-center justify-center shrink-0 mt-1">
                <User className="w-4 h-4 text-slate-600 dark:text-slate-400" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex gap-3">
            <div className="w-7 h-7 rounded-lg gradient-primary flex items-center justify-center shrink-0">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div className="rounded-2xl px-4 py-3 bg-slate-100 dark:bg-slate-800">
              <div className="flex gap-1 items-center h-5">
                {[0, 1, 2].map((i) => (
                  <span
                    key={i}
                    className="w-1.5 h-1.5 rounded-full bg-slate-400 animate-bounce"
                    style={{ animationDelay: `${i * 0.15}s` }}
                  />
                ))}
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <div className="flex gap-2 pt-2 border-t border-slate-200 dark:border-slate-800">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
          placeholder="Ask about eligibility, deadlines, documents…"
          disabled={loading}
          className="flex-1 h-10 px-4 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 disabled:opacity-50"
        />
        <Button
          onClick={() => sendMessage()}
          disabled={!input.trim() || loading}
          loading={loading}
          className="shrink-0"
        >
          <Send className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
}
