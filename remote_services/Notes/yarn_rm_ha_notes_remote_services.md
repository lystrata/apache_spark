# YARN ResourceManager — HA vs Single Node
_2026-04-10_

---

## Background

The YARN ResourceManager (RM) is the cluster coordinator responsible for job submission and container allocation. It must have network visibility to all NodeManagers. It does not need to be co-located with them — the "has to see the NodeManagers" requirement is a network connectivity requirement, not a co-location requirement.

YARN NodeManagers run inside each YARN executor VM on every node. They are not a service VM decision — they are baked into the executor VM footprint and non-negotiable.

---

## Scenario A — YARN RM HA (service VM on multiple nodes)

- Active RM on one node, standby on a second node
- ZooKeeper handles leader election (3 instances required for quorum — one per node)
- If the active RM's node goes down, ZooKeeper promotes the standby automatically within seconds
- Higher complexity, higher resource cost

**ZooKeeper requirement:**
- 1 vCPU / 2 GB RAM per node × 3 nodes
- Only required for Scenario A — serves no purpose in Scenario B

---

## Scenario B — Single YARN RM (service VM on one node)

- One RM on one node
- No ZooKeeper needed — there is nothing to elect between
- If that node goes down, job submission stops until the node recovers
- Simpler, lower overhead
- Correct choice for single-user, single daily pipeline at current scale

---

## State Persistence and Task Recovery

### How RM state is preserved during failover (Scenario A)

The RM continuously checkpoints its state to ZooKeeper as it works — application state, queue state, container assignments. The standby RM reads from the ZooKeeper state store on promotion, not from the failed RM's RAM. RAM state loss does not mean application state loss.

```
Active RM  ──writes──→  ZooKeeper state store
Standby RM ──reads──→  ZooKeeper state store (on promotion)
```

### What survives RM failover

| | Survives? |
|---|---|
| Application definitions, queue state | Yes — from ZooKeeper store |
| NodeManager registrations | Yes — NMs re-register with new RM automatically |
| Running executors on surviving nodes | Yes — NMs keep running containers during RM gap |
| Spark ApplicationMaster (driver) | Yes — if work-preserving-recovery is enabled |
| In-flight task assignments not yet checkpointed | No — those tasks retry |

### Work-preserving RM recovery

YARN has a `yarn.resourcemanager.work-preserving-recovery.enabled` setting. With this on:
- Running ApplicationMasters survive RM restart
- NodeManagers re-register their running containers with the new RM
- Jobs continue without user intervention
- Only mid-assignment tasks that weren't checkpointed need retry

### Who handles task retry — ZooKeeper or Spark?

**ZooKeeper does not replay tasks.** It operates at application/queue level, not task level.

Task retry is entirely the **Spark ApplicationMaster's** responsibility:

1. Node fails → RM fails over via ZooKeeper (seconds)
2. New RM comes up, NodeManagers re-register
3. ApplicationMaster re-registers with new RM
4. AM detects executors on failed node have gone silent (missed heartbeats)
5. AM marks their in-flight tasks as failed
6. AM requests replacement containers from the new RM
7. AM reschedules tasks on surviving executors
8. Job continues

### Is the user notified of retried tasks?

No proactive notification. The retry is transparent by design.

| Where it's visible | What you see |
|---|---|
| Spark UI / History Server | Task attempt count > 0 (attempt 0 failed, attempt 1 succeeded) |
| Spark driver logs | Task retry events logged |
| Airflow | Job still shows as running — not failed |
| User | Nothing, unless explicit alerting is wired up |

The user only receives notification if the task failure count exceeds `spark.task.maxFailures` (default: 4), at which point Spark aborts the job and Airflow handles the failure per the DAG's retry/alert configuration.

---

## Recommendation for Current Scale

**Scenario B is the correct choice** for a single-user, daily ETL pipeline on a tight 3-node cluster.

- A node failure loses the job's executors regardless of RM placement — the job fails either way
- Airflow (on the remote service host) detects the failure and alerts
- Once the node recovers, the pipeline retries
- YARN RM HA adds ZooKeeper complexity and resource overhead for a failure mode that results in the same outcome at current scale

Scenario A becomes worth the cost when multiple concurrent pipelines or multiple users make RM downtime have broader consequences.
