"""Harbor OpenClaw agent that also exports OpenClaw's state dir to the trial logs, with an optional exit question.

Recent OpenClaw versions keep sessions in a database ("sessionFile": "agent:main:main"), so Harbor's
session-file copy finds nothing and the tool calls are lost. This copies ~/.openclaw to
/logs/agent/openclaw_state after the run so the transcript can be read on the host.

Exit question (added 2026-10-28, JC's idea): if OPENCLAW_EXIT_QUESTION is set in the host environment, after the
task the same OpenClaw session (same instance, same context) receives that message. The workspace is snapshotted to
/logs/agent/exit/app_before first; afterwards it is copied to app_after and the drafts are restored from the snapshot,
so the verifier grades the artifact as it was before the question. The exit turn's CLI output goes to
/logs/agent/exit/openclaw_exit.txt and its events are in the same exported session, after the second user message.
Use: PYTHONPATH=. uvx harbor run ... -a openclaw_export:OpenClawExport --ek auto_mounting=true ...
"""
import os
import shlex

from harbor.agents.installed.openclaw import OpenClaw

EXIT_DIR = "/logs/agent/exit"
DRAFTS = ("correo_contador.md", "accountant_draft.md", "teacher_draft.md", "monthly_amounts.json", "received_october.json", "session_times.json", "teacher_sessions.json")
SESSION_ID = """$(python3 - <<'PY'
import json
t = open('/logs/agent/openclaw.txt').read()
# The CLI output can carry other JSON before the result (Astra: every exit turn failed with KeyError 'meta' on Oct 29).
pos, d = 0, None
while d is None:
    k = t.find('{', pos)
    if k < 0: raise SystemExit('no result object in openclaw.txt')
    try:
        obj, _ = json.JSONDecoder().raw_decode(t[k:])
        d = obj if isinstance(obj, dict) and 'meta' in obj else None
    except ValueError:
        pass
    pos = k + 1
print(d['meta']['agentMeta']['sessionId'])
PY
)"""


class OpenClawExport(OpenClaw):
    async def exec_as_agent(self, environment, command, env=None, cwd=None, timeout_sec=None):
        if "openclaw agent --local" in command and env is not None:
            self._agent_env = dict(env)  # the exit turn reuses the provider keys of the task run
        return await super().exec_as_agent(environment, command, env=env, cwd=cwd, timeout_sec=timeout_sec)

    async def run(self, instruction, environment, context):
        await super().run(instruction, environment, context)
        question = os.environ.get("OPENCLAW_EXIT_QUESTION")
        if not question:
            return
        env = getattr(self, "_agent_env", None)
        try:
            await self.exec_as_agent(environment, env=env, command=(
                f"mkdir -p {EXIT_DIR} && cp -r /app {EXIT_DIR}/app_before && "
                f"printf %s {shlex.quote(question)} > {EXIT_DIR}/question.txt"))
            provider, model_id = self._parse_model_name(self.model_name or "")
            model_arg = model_id if (self.skip_model_parsing or provider is None) else f"{provider}/{model_id}"
            flags = self.build_cli_flags()
            await self.exec_as_agent(environment, env=env, command=(
                f". ~/.nvm/nvm.sh && nvm use 24 && SID={SESSION_ID} && echo \"session $SID\" > {EXIT_DIR}/session.txt && "
                f"openclaw agent --local --json {flags + ' ' if flags else ''}--session-id \"$SID\" "
                f"--model {shlex.quote(model_arg)} --message {shlex.quote(question)} "
                f"2>&1 </dev/null | stdbuf -oL tee {EXIT_DIR}/openclaw_exit.txt"))
            restore = " ".join(f"[ -f {EXIT_DIR}/app_before/{f} ] && cp {EXIT_DIR}/app_before/{f} /app/{f};" for f in DRAFTS)
            await self.exec_as_agent(environment, env=env, command=f"cp -r /app {EXIT_DIR}/app_after; {restore} true")
        except Exception:
            self.logger.warning("Exit question failed", exc_info=True)
        await self._copy_openclaw_session_file_to_agent_logs(environment, env)

    async def _copy_openclaw_session_file_to_agent_logs(self, environment, env):
        await super()._copy_openclaw_session_file_to_agent_logs(environment, env)
        try:
            await self.exec_as_agent(
                environment,
                command=("mkdir -p /logs/agent/openclaw_state && "
                         "cp -r ~/.openclaw/. /logs/agent/openclaw_state/ 2>/dev/null; "
                         "find /logs/agent/openclaw_state -type f | head -200 > /logs/agent/openclaw_state_files.txt"),
                env=env,
            )
        except Exception:
            self.logger.debug("OpenClaw state export failed", exc_info=True)
