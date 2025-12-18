from app.chat.tracing.langfuse import langfuse
from langfuse.model import CreateTrace
import logging


class TraceableChain:
    def __call__(self, *args, **kwargs):
        logger = logging.getLogger(__name__)

        # Берём существующие callbacks или создаём список
        callbacks = list(kwargs.get("callbacks", []))

        trace = None

        try:
            metadata = self.metadata

            # metadata ДОЛЖНА быть dict
            if not isinstance(metadata, dict):
                metadata = metadata.dict()

            conversation_id = metadata.get("conversation_id")

            trace = langfuse.trace(
                CreateTrace(
                    id=str(conversation_id),
                    metadata=metadata,
                )
            )

            callbacks.append(trace.getNewHandler())

        except Exception as e:
            logger.warning("Langfuse disabled for this request", exc_info=e)

        # Обновляем callbacks в kwargs
        kwargs["callbacks"] = callbacks

        return super().__call__(*args, **kwargs)
