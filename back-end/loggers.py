import datetime
import yaml
from logging import Handler, LogRecord, config, getLogger
from db.database import SessionLocal
from db.models import Log
from datetime import datetime


class DBHandler(Handler):
    def emit(self, record: LogRecord) -> None:
        session = SessionLocal()
        session.add(Log(
            time=datetime.fromtimestamp(record.created),
            msg=record.getMessage(),
            level=record.levelname,
            levelno=record.levelno,
            data={
                "args": record.args,
                "logger_name": record.name,
                "module": record.module,
                "funcName": record.funcName,
                "stackinfo": record.stack_info,
                "lineno": record.lineno
            }))
        session.commit()


with open("logging_conf.yml", "r") as f:
    config.dictConfig(yaml.load(f.read(), yaml.FullLoader))

root_logger = getLogger("root")
access_logger = getLogger('access')
runtime_logger = getLogger('runtime')
loggers = [getLogger(name) for name in ("uvicorn.error", "uvicorn.access", "fastapi")]
for logger in loggers:
    logger.addHandler(DBHandler())
