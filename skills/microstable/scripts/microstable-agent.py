#!/usr/bin/env python3
"""
Microstable agent CLI for OpenClaw skill runtime.

Simulation mode:
- Imports local `microstable.py` and `open_agent_economy.py`
- Persists local state under `.state/microstable-agent-state.json`

Solana mode:
- Read-only RPC probes for devnet (state command)
- Write commands are scaffolded for future on-chain integration
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple
from urllib import request


class AgentCLIError(Exception):
    pass


def _canonical_agent_type(raw: str) -> str:
    lut = {
        "optimizer": "Optimizer",
        "monitor": "Monitor",
        "auditor": "Auditor",
        "liquidator": "Liquidator",
    }
    key = str(raw).strip().lower()
    if key not in lut:
        raise AgentCLIError(f"invalid agent type: {raw}")
    return lut[key]


def _workspace_root() -> Path:
    # .../misskim-skills/skills/microstable/scripts -> workspace root
    return Path(__file__).resolve().parents[4]


def _resolve_microstable_root(cli_value: str | None) -> Path:
    if cli_value:
        return Path(cli_value).expanduser().resolve()
    env_value = os.getenv("MICROSTABLE_ROOT")
    if env_value:
        return Path(env_value).expanduser().resolve()
    return (_workspace_root() / "microstable").resolve()


def _skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _state_path() -> Path:
    return _skill_root() / ".state" / "microstable-agent-state.json"


def _default_state() -> Dict[str, Any]:
    return {
        "protocol": {
            "weights": [0.4, 0.3, 0.2, 0.1],
            "mint_fee": 0.002,
            "cr": 1.28,
            "cr_target": 1.2,
            "supply": 1_000_000.0,
            "reserve_value": 1_280_000.0,
            "current_loss": None,
            "last_epoch": 0,
            "last_update_ms": int(time.time() * 1000),
        },
        "agents": {},
        "tournaments": {},
        "anomaly_reports": [],
        "resolved_alerts": [],
        "heartbeats": {},
    }


def load_state() -> Dict[str, Any]:
    path = _state_path()
    if not path.exists():
        return _default_state()
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("state json root must be an object")
        base = _default_state()
        base.update(data)
        return base
    except Exception as e:
        raise AgentCLIError(f"failed to load state: {e}") from e


def save_state(state: Dict[str, Any]) -> None:
    path = _state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    state["protocol"]["last_update_ms"] = int(time.time() * 1000)
    with path.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)


def _import_sim_modules(microstable_root: Path):
    root_str = str(microstable_root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    try:
        import microstable as ms  # type: ignore
        import open_agent_economy as oae  # type: ignore
    except Exception as e:
        raise AgentCLIError(
            f"simulation imports failed. expected microstable repo at: {microstable_root}. error: {e}"
        ) from e
    return ms, oae


def _protocol_state_from_store(ms: Any, store: Dict[str, Any]):
    ps = ms.ProtocolState()
    proto = store.get("protocol", {})
    for key in [
        "weights",
        "mint_fee",
        "cr",
        "cr_target",
        "supply",
        "reserve_value",
    ]:
        if key in proto:
            setattr(ps, key, proto[key])
    return ps


def _rpc_call(url: str, method: str, params: List[Any] | None = None) -> Any:
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or [],
    }).encode("utf-8")
    req = request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    with request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if "error" in data:
        raise AgentCLIError(f"rpc error: {data['error']}")
    return data.get("result")


def _build_runtime_from_state(oae: Any, state: Dict[str, Any]) -> Tuple[Any, Any, Any]:
    registry = oae.AgentRegistry()
    for agent_id, row in state.get("agents", {}).items():
        registry.records[agent_id] = oae.AgentRecord(
            agent_id=agent_id,
            agent_type=row["agent_type"],
            stake=float(row.get("stake", 0.0)),
            reputation=int(row.get("reputation", 0)),
            registered_at=int(row.get("registered_at", 0)),
            last_active=int(row.get("last_active", 0)),
            total_rewards=float(row.get("total_rewards", 0.0)),
            total_slashed=float(row.get("total_slashed", 0.0)),
            proposals_submitted=int(row.get("proposals_submitted", 0)),
            proposals_accepted=int(row.get("proposals_accepted", 0)),
            status=row.get("status", "Active"),
        )

    reputation = oae.ReputationEngine()
    for agent_id, row in state.get("agents", {}).items():
        reputation.scores[agent_id] = int(row.get("reputation", 0))

    staking = oae.StakingEconomics(registry)
    for agent_id, row in state.get("agents", {}).items():
        staking.balances[agent_id] = float(row.get("balance", row.get("stake", 0.0)))

    return registry, reputation, staking


def _sync_runtime_to_state(state: Dict[str, Any], registry: Any, reputation: Any, staking: Any) -> None:
    agents = state.setdefault("agents", {})
    for agent_id, rec in registry.records.items():
        prev = agents.get(agent_id, {})
        prev_total_rewards = float(prev.get("total_rewards", 0.0))
        new_total_rewards = float(rec.total_rewards)
        delta_rewards = max(0.0, new_total_rewards - prev_total_rewards)

        agents[agent_id] = {
            "agent_type": rec.agent_type,
            "stake": float(rec.stake),
            "balance": float(staking.balances.get(agent_id, rec.stake)),
            "status": rec.status,
            "reputation": int(reputation.get(agent_id)),
            "registered_at": int(rec.registered_at),
            "last_active": int(rec.last_active),
            "total_rewards": new_total_rewards,
            "total_slashed": float(rec.total_slashed),
            "proposals_submitted": int(rec.proposals_submitted),
            "proposals_accepted": int(rec.proposals_accepted),
            "claimable_rewards": float(prev.get("claimable_rewards", 0.0)) + delta_rewards,
            "claimed_rewards": float(prev.get("claimed_rewards", 0.0)),
        }


def cmd_state(args: argparse.Namespace) -> Dict[str, Any]:
    state = load_state()

    if args.mode == "solana":
        health = _rpc_call(args.rpc_url, "getHealth")
        slot = _rpc_call(args.rpc_url, "getSlot")
        version = _rpc_call(args.rpc_url, "getVersion")
        return {
            "mode": "solana",
            "rpc_url": args.rpc_url,
            "cluster": "devnet",
            "health": health,
            "slot": slot,
            "version": version,
            "note": "write operations (register/propose/report) are scaffolded for future on-chain ACP adapters.",
        }

    ms, oae = _import_sim_modules(_resolve_microstable_root(args.microstable_root))
    _ = oae  # explicit import usage for simulation-mode contract

    protocol = _protocol_state_from_store(ms, state)
    epoch = int(args.epoch if args.epoch is not None else state["protocol"].get("last_epoch", 0))

    env = ms.MarketEnv(scenario=args.scenario, seed=args.seed, deterministic=True)
    market = env.step(epoch)

    nav = protocol.effective_collateral_value(market.prices)
    peg = 1.0 + protocol.peg_sensitivity(market.prices) * (nav - 1.0) + 0.0010 * (market.oracle_q - 1.0)
    peg = min(1.10, max(0.90, peg))

    wd = ms.Watchdog().detect(market)
    cb = {
        "cb1": bool(wd.get("cb1", False)),
        "cb2": bool(wd.get("cb2", False)),
        "cb3": bool(wd.get("cb3", False)),
        "cb4": False,
    }

    return {
        "mode": "simulation",
        "epoch": epoch,
        "scenario": args.scenario,
        "protocol_state": {
            "peg": peg,
            "collateral_ratio": float(protocol.cr),
            "target_collateral_ratio": float(protocol.cr_target),
            "weights": list(protocol.weights),
            "mint_fee": float(protocol.mint_fee),
            "supply": float(protocol.supply),
            "reserve_value": float(protocol.reserve_value),
        },
        "market": {
            "prices": market.prices,
            "oracle_q": market.oracle_q,
            "stale_seconds": market.stale_seconds,
            "divergence": market.divergence,
        },
        "circuit_breakers": cb,
        "agents": {
            "registered": len(state.get("agents", {})),
            "active": len([a for a in state.get("agents", {}).values() if a.get("status") == "Active"]),
            "types": list(oae.AGENT_TYPES),
        },
    }


def cmd_register(args: argparse.Namespace) -> Dict[str, Any]:
    if args.mode == "solana":
        return {
            "mode": "solana",
            "status": "not_implemented",
            "rpc_url": args.rpc_url,
            "hint": "on-chain registration adapter will use AgentRegistry PDA in future version.",
        }

    _, oae = _import_sim_modules(_resolve_microstable_root(args.microstable_root))
    state = load_state()

    agent_type = _canonical_agent_type(args.agent_type)
    stake = float(args.stake)
    agent_id = args.agent_id

    if stake <= 0:
        raise AgentCLIError("stake must be > 0")

    min_stake = float(oae.MIN_STAKE_DEFAULT[agent_type])
    if stake < min_stake:
        raise AgentCLIError(f"stake too low for {agent_type}. required >= {min_stake}")

    existing = state["agents"].get(agent_id)
    if existing and existing.get("status") != "Deregistered":
        raise AgentCLIError(f"agent already exists and is active/cooldown/slashed: {agent_id}")

    epoch = int(args.epoch if args.epoch is not None else state["protocol"].get("last_epoch", 0))

    state["agents"][agent_id] = {
        "agent_type": agent_type,
        "stake": stake,
        "balance": stake,
        "status": "Active",
        "reputation": 0,
        "registered_at": epoch,
        "last_active": epoch,
        "total_rewards": 0.0,
        "total_slashed": 0.0,
        "proposals_submitted": 0,
        "proposals_accepted": 0,
        "claimable_rewards": 0.0,
        "claimed_rewards": 0.0,
    }
    state["heartbeats"][agent_id] = epoch
    state["protocol"]["last_epoch"] = max(int(state["protocol"].get("last_epoch", 0)), epoch)
    save_state(state)

    return {
        "mode": "simulation",
        "status": "registered",
        "agent_id": agent_id,
        "agent_type": agent_type,
        "stake": stake,
        "required_min_stake": min_stake,
        "epoch": epoch,
    }


def cmd_propose(args: argparse.Namespace) -> Dict[str, Any]:
    if args.mode == "solana":
        return {
            "mode": "solana",
            "status": "not_implemented",
            "rpc_url": args.rpc_url,
            "hint": "proposal commit/reveal on devnet will be added in a future release.",
        }

    ms, oae = _import_sim_modules(_resolve_microstable_root(args.microstable_root))
    state = load_state()
    agent = state["agents"].get(args.agent_id)

    if not agent:
        raise AgentCLIError(f"agent not found: {args.agent_id}")
    if agent.get("status") != "Active":
        raise AgentCLIError(f"agent is not active: {args.agent_id}")
    if agent.get("agent_type") != "Optimizer":
        raise AgentCLIError("only Optimizer agents can submit tournament proposals")

    raw = json.loads(args.weights_json)
    mint_fee = float(args.mint_fee)
    expected_return = None
    risk = None

    if isinstance(raw, list):
        weights = [float(x) for x in raw]
    elif isinstance(raw, dict):
        if "weights" not in raw:
            raise AgentCLIError("weights-json object must include 'weights'")
        weights = [float(x) for x in raw["weights"]]
        if "mint_fee" in raw:
            mint_fee = float(raw["mint_fee"])
        if "expected_return" in raw:
            expected_return = float(raw["expected_return"])
        if "risk" in raw:
            risk = float(raw["risk"])
    else:
        raise AgentCLIError("weights-json must be a JSON array or object")

    if len(weights) != 4:
        raise AgentCLIError("weights must have exactly 4 elements")
    if any((not math.isfinite(w)) or w < 0.0 for w in weights):
        raise AgentCLIError("weights must be finite and >= 0")
    if abs(sum(weights) - 1.0) > 1e-6:
        raise AgentCLIError("sum(weights) must equal 1.0")

    if mint_fee < 0.0 or mint_fee > 0.02:
        raise AgentCLIError("mint_fee out of allowed range [0, 0.02]")

    epoch = int(args.epoch)
    protocol = _protocol_state_from_store(ms, state)
    protocol.weights = list(weights)
    protocol.mint_fee = mint_fee

    env = ms.MarketEnv(scenario=args.scenario, seed=args.seed, deterministic=True)
    market = env.step(epoch)
    loss_engine = ms.LossEngine()
    loss, _ = loss_engine.compute(protocol, market.prices, market.oracle_q)
    loss_estimate = float(loss.data)

    if expected_return is None:
        expected_return = max(0.0, 0.03 - loss_estimate)
    if risk is None:
        risk = sum((w - 0.25) ** 2 for w in weights) + 0.01

    proposal = oae.Proposal(
        agent_id=args.agent_id,
        epoch=epoch,
        weights=list(weights),
        mint_fee=mint_fee,
        loss_estimate=loss_estimate,
        expected_return=expected_return,
        risk=risk,
    )

    secret = args.secret or f"secret-{args.agent_id}"
    commit_hash = proposal.commit_hash(secret)

    tkey = str(epoch)
    tentry = state["tournaments"].setdefault(tkey, {"proposals": [], "evaluated": False, "winner": None})
    tentry["proposals"].append(
        {
            "agent_id": proposal.agent_id,
            "epoch": proposal.epoch,
            "weights": proposal.weights,
            "mint_fee": proposal.mint_fee,
            "loss_estimate": proposal.loss_estimate,
            "expected_return": proposal.expected_return,
            "risk": proposal.risk,
            "metadata": {"commit_hash": commit_hash, "revealed": True},
        }
    )

    state["protocol"]["last_epoch"] = max(int(state["protocol"].get("last_epoch", 0)), epoch)
    save_state(state)

    return {
        "mode": "simulation",
        "status": "proposal_submitted",
        "agent_id": args.agent_id,
        "epoch": epoch,
        "commit_hash": commit_hash,
        "reveal": {
            "weights": weights,
            "mint_fee": mint_fee,
            "loss_estimate": loss_estimate,
            "expected_return": expected_return,
            "risk": risk,
        },
        "tournament_proposal_count": len(tentry["proposals"]),
    }


def cmd_report(args: argparse.Namespace) -> Dict[str, Any]:
    if args.mode == "solana":
        return {
            "mode": "solana",
            "status": "not_implemented",
            "rpc_url": args.rpc_url,
            "hint": "on-chain anomaly reporting adapter will be added in future version.",
        }

    ms, oae = _import_sim_modules(_resolve_microstable_root(args.microstable_root))
    _ = ms
    state = load_state()

    agent = state["agents"].get(args.agent_id)
    if not agent:
        raise AgentCLIError(f"agent not found: {args.agent_id}")
    if agent.get("status") != "Active":
        raise AgentCLIError(f"agent is not active: {args.agent_id}")

    evidence = json.loads(args.evidence_json)
    if not isinstance(evidence, dict):
        raise AgentCLIError("evidence-json must decode to an object")

    epoch = int(args.epoch if args.epoch is not None else state["protocol"].get("last_epoch", 0))
    evidence.setdefault("timestamp", epoch)
    evidence.setdefault("snapshot", {"protocol": state.get("protocol", {})})
    evidence.setdefault("oracle", {"source": "simulation"})

    report_row = {
        "agent_id": args.agent_id,
        "alert_type": args.anomaly_type,
        "epoch": epoch,
        "evidence": evidence,
        "method": args.method,
    }
    state.setdefault("anomaly_reports", []).append(report_row)

    active_monitors = [
        aid
        for aid, row in state.get("agents", {}).items()
        if row.get("agent_type") == "Monitor" and row.get("status") == "Active"
    ]
    unique_voters = {
        r["agent_id"]
        for r in state.get("anomaly_reports", [])
        if int(r.get("epoch", -1)) == epoch and r.get("alert_type") == args.anomaly_type
    }

    n = len(active_monitors)
    threshold = min(3, math.ceil(n / 2)) if n > 0 else 0
    consensus = n > 0 and len(unique_voters) >= threshold

    resolved_key = f"{epoch}:{args.anomaly_type}"
    already_resolved = resolved_key in set(state.get("resolved_alerts", []))
    resolved_now = False

    if consensus and args.resolve and not already_resolved:
        registry, reputation, staking = _build_runtime_from_state(oae, state)
        watchdog = oae.FederatedWatchdog(registry, staking, reputation)

        for row in state.get("anomaly_reports", []):
            if int(row.get("epoch", -1)) != epoch or row.get("alert_type") != args.anomaly_type:
                continue
            watchdog.report(
                agent_id=row["agent_id"],
                alert_type=row["alert_type"],
                evidence=row["evidence"],
                epoch=epoch,
                method=row.get("method", "default"),
            )

        watchdog.resolve(args.anomaly_type, epoch, is_true=args.is_true)
        _sync_runtime_to_state(state, registry, reputation, staking)
        state.setdefault("resolved_alerts", []).append(resolved_key)
        resolved_now = True

    state["protocol"]["last_epoch"] = max(int(state["protocol"].get("last_epoch", 0)), epoch)
    save_state(state)

    return {
        "mode": "simulation",
        "status": "reported",
        "agent_id": args.agent_id,
        "alert_type": args.anomaly_type,
        "epoch": epoch,
        "consensus": {
            "active_monitors": n,
            "required_votes": threshold,
            "votes": len(unique_voters),
            "reached": consensus,
        },
        "resolution": {
            "requested": bool(args.resolve),
            "is_true": bool(args.is_true),
            "already_resolved": already_resolved,
            "resolved_now": resolved_now,
        },
    }


def cmd_tournament(args: argparse.Namespace) -> Dict[str, Any]:
    if args.mode == "solana":
        return {
            "mode": "solana",
            "status": "not_implemented",
            "rpc_url": args.rpc_url,
            "hint": "on-chain tournament result query is planned for future release.",
        }

    ms, oae = _import_sim_modules(_resolve_microstable_root(args.microstable_root))
    _ = ms
    state = load_state()

    tkey = str(args.epoch)
    tentry = state.get("tournaments", {}).get(tkey)
    if not tentry:
        raise AgentCLIError(f"no tournament found for epoch={args.epoch}")

    if tentry.get("evaluated") and not args.force:
        return {
            "mode": "simulation",
            "epoch": args.epoch,
            "status": "already_evaluated",
            "winner": tentry.get("winner"),
            "ranking": tentry.get("ranking", []),
            "hint": "use --force to re-evaluate",
        }

    proposals_raw = tentry.get("proposals", [])
    if not proposals_raw:
        raise AgentCLIError("tournament has no proposals")

    registry, reputation, staking = _build_runtime_from_state(oae, state)
    tournament = oae.OptimizationTournament(registry, reputation, staking)
    tournament.start_epoch(int(args.epoch))
    tournament.current_params = {
        "weights": list(state["protocol"].get("weights", [0.4, 0.3, 0.2, 0.1])),
        "mint_fee": float(state["protocol"].get("mint_fee", 0.002)),
    }
    tournament.current_loss = state["protocol"].get("current_loss")

    proposals: List[Any] = []
    for row in proposals_raw:
        prop = oae.Proposal(
            agent_id=row["agent_id"],
            epoch=int(row["epoch"]),
            weights=[float(x) for x in row["weights"]],
            mint_fee=float(row["mint_fee"]),
            loss_estimate=float(row["loss_estimate"]),
            expected_return=float(row["expected_return"]),
            risk=float(row["risk"]),
            metadata=dict(row.get("metadata", {})),
        )
        if tournament.submit_direct(prop):
            proposals.append(prop)

    if not proposals:
        raise AgentCLIError("no valid active proposals available for evaluation")

    winner = tournament.evaluate(float(args.epoch_fees))
    ranking = sorted(
        [
            {
                "agent_id": p.agent_id,
                "score": float(tournament._score(p)),
                "loss_estimate": float(p.loss_estimate),
                "expected_return": float(p.expected_return),
                "risk": float(p.risk),
            }
            for p in proposals
        ],
        key=lambda x: x["score"],
        reverse=True,
    )

    _sync_runtime_to_state(state, registry, reputation, staking)

    if winner is not None:
        state["protocol"]["weights"] = list(winner.weights)
        state["protocol"]["mint_fee"] = float(winner.mint_fee)
        state["protocol"]["current_loss"] = float(winner.loss_estimate)

    tentry["evaluated"] = True
    tentry["winner"] = (
        {
            "agent_id": winner.agent_id,
            "weights": list(winner.weights),
            "mint_fee": float(winner.mint_fee),
            "loss_estimate": float(winner.loss_estimate),
        }
        if winner is not None
        else None
    )
    tentry["ranking"] = ranking
    state["tournaments"][tkey] = tentry
    save_state(state)

    return {
        "mode": "simulation",
        "epoch": args.epoch,
        "status": "evaluated",
        "winner": tentry["winner"],
        "ranking": ranking,
        "epoch_fees": float(args.epoch_fees),
    }


def cmd_rewards(args: argparse.Namespace) -> Dict[str, Any]:
    state = load_state()
    agent = state.get("agents", {}).get(args.agent_id)
    if not agent:
        raise AgentCLIError(f"agent not found: {args.agent_id}")

    claimable = float(agent.get("claimable_rewards", 0.0))
    claimed = 0.0
    if args.claim:
        claimed = claimable
        agent["claimable_rewards"] = 0.0
        agent["claimed_rewards"] = float(agent.get("claimed_rewards", 0.0)) + claimed
        state["agents"][args.agent_id] = agent
        save_state(state)

    return {
        "agent_id": args.agent_id,
        "mode": args.mode,
        "status": "ok",
        "wallet": {
            "balance": float(agent.get("balance", 0.0)),
            "stake": float(agent.get("stake", 0.0)),
            "total_rewards": float(agent.get("total_rewards", 0.0)),
            "total_slashed": float(agent.get("total_slashed", 0.0)),
            "claimable_rewards": float(agent.get("claimable_rewards", 0.0)),
            "claimed_rewards": float(agent.get("claimed_rewards", 0.0)),
        },
        "claim": {
            "requested": bool(args.claim),
            "claimed_amount": claimed,
        },
    }


def cmd_heartbeat(args: argparse.Namespace) -> Dict[str, Any]:
    if args.mode == "solana":
        return {
            "mode": "solana",
            "status": "not_implemented",
            "rpc_url": args.rpc_url,
            "hint": "heartbeat transaction adapter is planned for future on-chain release.",
        }

    _, oae = _import_sim_modules(_resolve_microstable_root(args.microstable_root))
    state = load_state()

    if args.agent_id not in state.get("agents", {}):
        raise AgentCLIError(f"agent not found: {args.agent_id}")

    epoch = int(args.epoch if args.epoch is not None else state["protocol"].get("last_epoch", 0))
    registry, reputation, staking = _build_runtime_from_state(oae, state)

    ok = registry.heartbeat(args.agent_id, epoch)
    if not ok:
        raise AgentCLIError("heartbeat failed")

    _sync_runtime_to_state(state, registry, reputation, staking)
    state["heartbeats"][args.agent_id] = epoch
    state["protocol"]["last_epoch"] = max(int(state["protocol"].get("last_epoch", 0)), epoch)
    save_state(state)

    return {
        "mode": "simulation",
        "status": "alive",
        "agent_id": args.agent_id,
        "epoch": epoch,
        "last_active": state["agents"][args.agent_id]["last_active"],
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Microstable protocol agent CLI")
    p.add_argument("--mode", choices=["simulation", "solana"], default="simulation", help="execution mode")
    p.add_argument("--microstable-root", default=None, help="path to microstable repository")
    p.add_argument("--rpc-url", default="https://api.devnet.solana.com", help="Solana RPC endpoint")
    p.add_argument("--agent-id", default=os.getenv("MICROSTABLE_AGENT_ID", "local-agent"), help="active agent id")
    p.add_argument("--scenario", default="normal", help="market scenario for simulation")
    p.add_argument("--seed", type=int, default=0, help="deterministic seed for simulation")

    sp = p.add_subparsers(dest="command", required=True)

    s_state = sp.add_parser("state", help="query protocol state")
    s_state.add_argument("--epoch", type=int, default=None, help="epoch/tick hint for market snapshot")
    s_state.set_defaults(func=cmd_state)

    s_register = sp.add_parser("register", help="register protocol agent")
    s_register.add_argument("agent_type", help="Optimizer|Monitor|Auditor|Liquidator")
    s_register.add_argument("stake", type=float, help="stake amount")
    s_register.add_argument("--epoch", type=int, default=None, help="registration epoch")
    s_register.set_defaults(func=cmd_register)

    s_propose = sp.add_parser("propose", help="submit optimization proposal")
    s_propose.add_argument("epoch", type=int, help="tournament epoch")
    s_propose.add_argument("weights_json", help="JSON array or object with weights/mint_fee")
    s_propose.add_argument("--mint-fee", type=float, default=0.002, help="mint fee when weights_json is a bare array")
    s_propose.add_argument("--secret", default=None, help="commit secret for hash generation")
    s_propose.set_defaults(func=cmd_propose)

    s_report = sp.add_parser("report", help="report protocol anomaly")
    s_report.add_argument("anomaly_type", help="PEG_DEVIATION|CR_VIOLATION|ORACLE_STALE|ANOMALY")
    s_report.add_argument("evidence_json", help="JSON object with evidence payload")
    s_report.add_argument("--epoch", type=int, default=None, help="report epoch")
    s_report.add_argument("--method", default="default", help="detection method label")
    s_report.add_argument("--resolve", action="store_true", help="attempt immediate watchdog resolution")
    s_report.add_argument("--is-true", action="store_true", help="mark anomaly as true positive on resolve")
    s_report.set_defaults(func=cmd_report)

    s_tournament = sp.add_parser("tournament", help="query/evaluate tournament result")
    s_tournament.add_argument("epoch", type=int, help="target epoch")
    s_tournament.add_argument("--epoch-fees", type=float, default=100.0, help="fee pool for reward distribution")
    s_tournament.add_argument("--force", action="store_true", help="force re-evaluation")
    s_tournament.set_defaults(func=cmd_tournament)

    s_rewards = sp.add_parser("rewards", help="query or claim rewards")
    s_rewards.add_argument("agent_id", help="target agent id")
    s_rewards.add_argument("--claim", action="store_true", help="claim all claimable rewards")
    s_rewards.set_defaults(func=cmd_rewards)

    s_heartbeat = sp.add_parser("heartbeat", help="liveness heartbeat")
    s_heartbeat.add_argument("--epoch", type=int, default=None, help="heartbeat epoch")
    s_heartbeat.set_defaults(func=cmd_heartbeat)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.func(args)
        print(json.dumps(result, indent=2, sort_keys=True))
    except AgentCLIError as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2, sort_keys=True), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
