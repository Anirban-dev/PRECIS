import sys
import logging
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from orchestration.workflow_engine import WorkflowEngine
from orchestration.pipeline_scheduler import PipelineScheduler
from orchestration.state_sync_engine import StateSyncEngine
from orchestration.distributed_lock_manager import DistributedLockManager
from orchestration.recovery_manager import RecoveryManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self):
        logger.info("Initializing Orchestrator...")
        self.workflow = WorkflowEngine()
        self.scheduler = PipelineScheduler()
        self.sync = StateSyncEngine()
        self.lock = DistributedLockManager()
        self.recovery = RecoveryManager()
        logger.info("All orchestration services initialized.")

    def run(self):
        lock_acquired = False
        try:
            logger.info("Acquiring distributed lock...")
            self.lock.acquire()
            lock_acquired = True

            logger.info("Executing predictive pipeline...")
            result = self.workflow.execute()

            logger.info("Synchronizing state...")
            self.sync.sync(result)

            logger.info("Pipeline execution completed.")

            print("\n===== PRECIS EXECUTION RESULT =====")
            print(result)
            print("===================================\n")
            return result

        except Exception as e:
            logger.exception("Pipeline execution failed.")
            try:
                recovery_result = self.recovery.recover(e)
                print("\n===== RECOVERY RESULT =====")
                print(recovery_result)
                print("===========================\n")
                return recovery_result
            except Exception as recovery_error:
                logger.exception("Recovery mechanism failed.")
                print(f"Recovery failed: {recovery_error}")
        finally:
            if lock_acquired:
                try:
                    if hasattr(self.lock, "release"):
                        self.lock.release()
                        logger.info("Distributed lock released.")
                except Exception as lock_error:
                    logger.warning(f"Failed to release lock: {lock_error}")


if __name__ == "__main__":
    logger.info("Starting PRECIS Orchestrator...")
    orchestrator = Orchestrator()
    orchestrator.run()
