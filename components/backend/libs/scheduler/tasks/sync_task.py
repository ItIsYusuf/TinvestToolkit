from datetime import datetime, timezone

from .base_task import BaseTask
from ..interfaces import ISyncTask


class SyncTask(BaseTask, ISyncTask):

    def _run(self) -> None:
        self._logger.info(f'Task - [{self._name}]. UUID - [{self._instance_key}]. CRON -> [{self._cron}]')

        self._last_started_at = datetime.now(timezone.utc)
        try:
            self._job(*self._job_args, **self._job_kwargs)
        except Exception as e:
            self._logger.error(f'Task completed with error. UUID - [{self._instance_key}]. \n{e}')
        else:
            self._logger.info(f'The task completed. UUID - [{self._instance_key}]')

        self._on_finish()