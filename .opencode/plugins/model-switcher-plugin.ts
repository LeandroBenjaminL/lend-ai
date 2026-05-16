import type { Plugin, PluginInput } from "@opencode-ai/plugin"
import { tool } from "@opencode-ai/plugin"
import { readFile, writeFile, unlink } from "fs/promises"
import { join } from "path"
import { tmpdir } from "os"

const BASE_DIR = join(__dirname, "..", "..")
const ROUTER_SCRIPT = join(BASE_DIR, "mcp-servers", "model-router.py")
const CONFIG_FILE = join(BASE_DIR, "model-routing.config.json")
const AGENT_ROUTER_SCRIPT = join(BASE_DIR, "mcp-servers", "agent-router.py")

const DEPTH_TIER_MAP: Record<number, string> = {
  1: "T4-reasoning",
  2: "T3-balanced",
  3: "T2-fast",
  4: "T1-ultra-fast",
  5: "T1-ultra-fast",
}

const DEPTH_LABEL_MAP: Record<number, string> = {
  1: "orchestrator",
  2: "domain supervisor",
  3: "specialist",
  4: "deep specialist",
  5: "deep specialist",
}

async function runRouter(args: string[]): Promise<unknown> {
  const { spawn } = await import("child_process")
  return new Promise((resolve) => {
    const proc = spawn("python3", [ROUTER_SCRIPT, ...args], {
      cwd: BASE_DIR,
      shell: true,
    })
    let stdout = ""
    let stderr = ""
    proc.stdout.on("data", (d) => (stdout += d.toString()))
    proc.stderr.on("data", (d) => (stderr += d.toString()))
    proc.on("close", (code) => {
      if (code === 0 && stdout) {
        try {
          resolve(JSON.parse(stdout))
        } catch {
          resolve({ error: "Invalid JSON output", raw: stdout })
        }
      } else {
        resolve({ error: stderr || `Exit code ${code}` })
      }
    })
  })
}

async function runPythonScript(scriptContent: string): Promise<unknown> {
  const tmpFile = join(tmpdir(), `lend-ai-py-${Date.now()}-${Math.random().toString(36).slice(2, 8)}.py`)
  await writeFile(tmpFile, scriptContent, "utf-8")
  const { spawn } = await import("child_process")
  return new Promise((resolve) => {
    const proc = spawn("python3", [tmpFile], { cwd: BASE_DIR, shell: true })
    let stdout = ""
    let stderr = ""
    proc.stdout.on("data", (d) => (stdout += d.toString()))
    proc.stderr.on("data", (d) => (stderr += d.toString()))
    proc.on("close", async (code) => {
      await unlink(tmpFile).catch(() => {})
      if (code === 0 && stdout) {
        try {
          resolve(JSON.parse(stdout))
        } catch {
          resolve({ error: "Invalid JSON output", raw: stdout })
        }
      } else {
        resolve({ error: stderr || `Exit code ${code}` })
      }
    })
  })
}

function formatTreeAscii(data: { task: string; depth: number; tree?: Record<string, unknown>; error?: string }): string {
  if (data.error) {
    return JSON.stringify(data, null, 2)
  }
  if (!data.tree) {
    return JSON.stringify(data, null, 2)
  }

  const lines: string[] = []
  lines.push(`Task: ${data.task}`)
  lines.push(`Max Depth: ${data.depth}`)
  lines.push("")

  function renderNode(node: Record<string, unknown>, prefix: string, isLast: boolean): void {
    const connector = isLast ? "└── " : "├── "
    const childPrefix = isLast ? "    " : "│   "
    const subs = (node.sub_agents || []) as Record<string, unknown>[]
    const name = node.name as string
    const layer = node.layer as string
    const tier = node.tier as string
    const desc = node.description as string
    const label = desc ? `  (${desc})` : ""
    lines.push(`${prefix}${connector}${name}  [layer ${layer}, ${tier}]${label}`)
    for (let i = 0; i < subs.length; i++) {
      renderNode(subs[i], prefix + childPrefix, i === subs.length - 1)
    }
  }

  renderNode(data.tree as Record<string, unknown>, "", true)

  const count = lines.length - 3
  lines.push("")
  lines.push(`Total agents in tree: ${count}`)
  return lines.join("\n")
}

const modelSwitcherPlugin: Plugin = async (input: PluginInput) => {
  const { directory } = input

  return {
    tools: {
      set_agent_model: tool({
        description: "Cambiar el modelo LLM de un agente específico",
        args: {
          agent: tool.schema.string("Nombre del agente (ej: data-analyst, data-explorer)"),
          tier: tool.schema.string("Tier del modelo (T1-ultra-fast, T2-fast, T3-balanced, T4-reasoning, T5-deep)")
        },
        execute: async ({ agent, tier }) => {
          const result = await runRouter(["set-agent-tier", agent, tier])
          return JSON.stringify(result, null, 2)
        }
      }),

      set_skill_model: tool({
        description: "Cambiar el modelo LLM de una skill específica",
        args: {
          skill: tool.schema.string("Nombre de la skill (ej: data-analysis, ml-modeling)"),
          tier: tool.schema.string("Tier del modelo (T1-ultra-fast, T2-fast, T3-balanced, T4-reasoning, T5-deep)")
        },
        execute: async ({ skill, tier }) => {
          const result = await runRouter(["set-skill-tier", skill, tier])
          return JSON.stringify(result, null, 2)
        }
      }),

      get_agent_model: tool({
        description: "Ver qué modelo está asignado a un agente",
        args: {
          agent: tool.schema.string("Nombre del agente")
        },
        execute: async ({ agent }) => {
          const result = await runRouter(["resolve", "--agent", agent])
          return typeof result === "string" ? result : JSON.stringify(result, null, 2)
        }
      }),

      get_skill_model: tool({
        description: "Ver qué modelo está asignado a una skill",
        args: {
          skill: tool.schema.string("Nombre de la skill")
        },
        execute: async ({ skill }) => {
          const result = await runRouter(["resolve", "--skill", skill])
          return typeof result === "string" ? result : JSON.stringify(result, null, 2)
        }
      }),

      list_all_models: tool({
        description: "Listar todos los agentes, skills y sus modelos asignados"
      },
      async () => {
        const result = await runRouter(["list"])
        return typeof result === "string" ? result : JSON.stringify(result, null, 2)
      }),

      list_overrides: tool({
        description: "Ver los overrides de modelo activos (cambios respecto al default)"
      },
      async () => {
        const result = await runRouter(["list-overrides"])
        return typeof result === "string" ? result : JSON.stringify(result, null, 2)
      }),

      reset_agent_model: tool({
        description: "Resetear el modelo de un agente al default",
        args: {
          agent: tool.schema.string("Nombre del agente")
        },
        execute: async ({ agent }) => {
          const result = await runRouter(["reset-agent-tier", agent])
          return JSON.stringify(result, null, 2)
        }
      }),

      reset_skill_model: tool({
        description: "Resetear el modelo de una skill al default",
        args: {
          skill: tool.schema.string("Nombre de la skill")
        },
        execute: async ({ skill }) => {
          const result = await runRouter(["reset-skill-tier", skill])
          return JSON.stringify(result, null, 2)
        }
      }),

      show_available_tiers: tool({
        description: "Mostrar los tiers disponibles y sus modelos"
      },
      async () => {
        try {
          const config = JSON.parse(await readFile(CONFIG_FILE, "utf-8"))
          const tiers = config.tiers || {}
          let output = "═══ TIERS DISPONIBLES ═══\n\n"
          for (const [name, data] of Object.entries(tiers)) {
            const d = data as { model?: string; description?: string }
            output += `\u2022 ${name}\n`
            output += `  Modelo: ${d.model || "?"}\n`
            output += `  ${d.description || ""}\n\n`
          }
          return output
        } catch (e) {
          return `Error: ${e}`
        }
      }),

      auto_assign_tier_by_depth: tool({
        description: "Auto-asignar tier a un agente según profundidad en el árbol de delegación. depth=1 (orquestador) → T4-reasoning, depth=2 (supervisor) → T3-balanced, depth=3 (especialista) → T2-fast, depth=4+ (deep specialist) → T1-ultra-fast",
        args: {
          agent_name: tool.schema.string("Nombre del agente a asignar"),
          depth: tool.schema.number("Profundidad (1-5): 1=orquestador, 2=supervisor, 3=especialista, 4+=deep specialist")
        },
        execute: async ({ agent_name, depth }) => {
          const d = Math.max(1, Math.min(5, Math.round(depth)))
          const tier = DEPTH_TIER_MAP[d]
          const label = DEPTH_LABEL_MAP[d]

          const result = await runRouter(["set-agent-tier", agent_name, tier])
          return JSON.stringify({
            agent: agent_name,
            depth: d,
            role: label,
            assigned_tier: tier,
            result
          }, null, 2)
        }
      }),

      get_delegation_tree: tool({
        description: "Obtener el árbol completo de delegación para una tarea, con profundidades y tiers asignados. Renderizado como ASCII tree.",
        args: {
          agent_name: tool.schema.string("Nombre del agente raíz del árbol (ej: data-analyst)")
        },
        execute: async ({ agent_name }) => {
          const script = `
import sys, json
sys.path.insert(0, ${JSON.stringify(join(BASE_DIR, "mcp-servers"))})
import importlib.util as _u
_spec = _u.spec_from_file_location("agent_router", ${JSON.stringify(AGENT_ROUTER_SCRIPT)})
_mod = _u.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

def _resolve_recursive(agent_name, depth, max_depth, visited):
    if agent_name in visited:
        return None
    visited.add(agent_name)

    data = _mod.ALL_AGENTS.get(agent_name)
    if data is None:
        return None

    agent_info = data.get("agent", {})
    routing = _mod._resolve_model_router(agent_name)

    node = {
        "name": agent_name,
        "layer": str(agent_info.get("layer", "?")),
        "tier": routing["tier"],
        "model": routing["model"],
        "description": agent_info.get("description", ""),
        "trigger": agent_info.get("trigger", ""),
        "mcp_bindings": data.get("mcp_bindings", []),
        "sub_agents": []
    }

    if depth < max_depth:
        subs = data.get("sub_agents", [])
        if isinstance(subs, list):
            for sub_name in subs:
                sub_node = _resolve_recursive(sub_name, depth + 1, max_depth, visited)
                if sub_node:
                    node["sub_agents"].append(sub_node)
    return node

tree = _resolve_recursive(${JSON.stringify(agent_name)}, 1, 5, set())
if tree is None:
    print(json.dumps({"error": "Agente '" + ${JSON.stringify(agent_name)} + "' no encontrado."}))
else:
    # Count total nodes
    def count_nodes(n):
        c = 1
        for s in n.get("sub_agents", []):
            c += count_nodes(s)
        return c
    total = count_nodes(tree)
    print(json.dumps({
        "task": "Delegation tree for: " + ${JSON.stringify(agent_name)},
        "depth": 5,
        "total_agents": total,
        "tree": tree
    }, ensure_ascii=False, indent=2))
`

          const raw = await runPythonScript(script)
          const data = raw as Record<string, unknown>
          return formatTreeAscii(data as { task: string; depth: number; tree?: Record<string, unknown>; error?: string })
        }
      }),

      suggest_depth: tool({
        description: "Sugerir profundidad óptima de delegación y tiers según complejidad de la tarea. Útil para planificar la arquitectura de agentes antes de ejecutar.",
        args: {
          task_description: tool.schema.string("Descripción de la tarea a analizar"),
          complexity: tool.schema.string("Nivel de complejidad: simple, medium, complex, critical")
        },
        execute: async ({ task_description, complexity }) => {
          const suggestions: Record<string, { max_depth: number; tiers: string[]; levels: { depth: number; role: string; tier: string }[]; reason: string }> = {
            simple: {
              max_depth: 1,
              tiers: ["T1-ultra-fast"],
              levels: [{ depth: 1, role: "orchestrator", tier: "T1-ultra-fast" }],
              reason: "Tareas simples requieren un único agente directo T1-ultra-fast. Sin delegación."
            },
            medium: {
              max_depth: 2,
              tiers: ["T4-reasoning", "T2-fast"],
              levels: [
                { depth: 1, role: "orchestrator", tier: "T4-reasoning" },
                { depth: 2, role: "specialist", tier: "T2-fast" }
              ],
              reason: "Tareas medianas: un orquestador T4 planifica y un especialista T2 ejecuta."
            },
            complex: {
              max_depth: 3,
              tiers: ["T4-reasoning", "T3-balanced", "T2-fast"],
              levels: [
                { depth: 1, role: "orchestrator", tier: "T4-reasoning" },
                { depth: 2, role: "domain supervisor", tier: "T3-balanced" },
                { depth: 3, role: "specialist", tier: "T2-fast" }
              ],
              reason: "Tareas complejas: orquestador T4 → supervisor T3 → especialista T2."
            },
            critical: {
              max_depth: 4,
              tiers: ["T4-reasoning", "T3-balanced", "T2-fast", "T1-ultra-fast"],
              levels: [
                { depth: 1, role: "orchestrator", tier: "T4-reasoning" },
                { depth: 2, role: "domain supervisor", tier: "T3-balanced" },
                { depth: 3, role: "specialist", tier: "T2-fast" },
                { depth: 4, role: "deep specialist", tier: "T1-ultra-fast" }
              ],
              reason: "Tareas críticas: cadena completa de 4 niveles. Máxima profundidad de delegación."
            }
          }

          const c = complexity?.toLowerCase() || "medium"
          const suggestion = suggestions[c] || suggestions.medium

          return JSON.stringify({
            task: task_description,
            complexity: c,
            suggested_max_depth: suggestion.max_depth,
            levels: suggestion.levels,
            tier_assignment: suggestion.tiers,
            reason: suggestion.reason,
            note: c === "critical"
              ? "Usar T5-deep para el nivel orquestador si se requiere razonamiento extremo."
              : undefined
          }, null, 2)
        }
      })
    }
  }
}

export default modelSwitcherPlugin
