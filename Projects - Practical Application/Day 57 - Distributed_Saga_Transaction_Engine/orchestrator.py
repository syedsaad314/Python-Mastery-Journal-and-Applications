# Lead Engineer: Syed Saad Bin Irfan
"""
Portfolio Layer: Centralized Core Asynchronous Saga Orchestrator Engine
"""
import sys
from typing import List
from models import SagaContext, SagaStatus, SagaStepDefinition

class DistributedSagaOrchestrator:
    def __init__(self, step_pipeline: List[SagaStepDefinition]) -> None:
        self.step_pipeline = step_pipeline

    async def launch_orchestration_flow(self, transaction_payload: dict) -> SagaContext:
        ctx = SagaContext(payload=transaction_payload, status=SagaStatus.RUNNING)
        executed_milestones: List[SagaStepDefinition] = []
        
        print(f"\n[ORCHESTRATOR START] Deploying Transaction Scope ID: {ctx.saga_id}")
        
        try:
            for step in self.step_pipeline:
                print(f" -> [FORWARD STEP] Initiating: {step.name}")
                await step.action_coro(ctx)
                executed_milestones.append(step)
                
            ctx.status = SagaStatus.SUCCESSFUL
            print(f"[ORCHESTRATOR END] Workflow completed successfully. Status code: {ctx.status.value}")
            return ctx

        except Exception as fault:
            print(f"\n[ORCHESTRATOR FAULT DETECTED] Interruption at level: '{step.name}' -> {fault}")
            ctx.status = SagaStatus.COMPENSATING
            ctx.errors["failed_component"] = step.name
            ctx.errors["root_cause_message"] = str(fault)
            
            await self._run_compensations(ctx, executed_milestones)
            ctx.status = SagaStatus.FAILED
            print(f"[ORCHESTRATOR END] Workflow terminated cleanly. Status code: {ctx.status.value}")
            return ctx

    async def _run_compensations(self, ctx: SagaContext, executed_milestones: List[SagaStepDefinition]) -> None:
        print("\n[COMPENSATE RUN] Stepping through compensation pipeline in reverse order...")
        for step in reversed(executed_milestones):
            print(f" <- [COMPENSATING STEP] Reverting: {step.name}")
            try:
                await step.compensate_coro(ctx)
            except Exception as nested_error:
                print(f"!! [SYSTEM EMERGENCY] Fault during compensation run for '{step.name}': {nested_error}", file=sys.stderr)