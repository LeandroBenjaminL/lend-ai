import type { Plugin, PluginInput } from "@opencode-ai/plugin"
import { tool } from "@opencode-ai/plugin"
import { readFile, writeFile } from "fs/promises"
import { join } from "path"

const BASE_DIR = join(__dirname, "..", "..")
const ROUTER_SCRIPT = join(BASE_DIR, "mcp-servers", "model-router.py")
const CONFIG_FILE = join(BASE_DIR, "model-routing.config.json")

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
            output += `• ${name}\n`
            output += `  Modelo: ${d.model || "?"}\n`
            output += `  ${d.description || ""}\n\n`
          }
          return output
        } catch (e) {
          return `Error: ${e}`
        }
      })
    }
  }
}

export default modelSwitcherPlugin