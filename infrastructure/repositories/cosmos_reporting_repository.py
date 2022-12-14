import uuid
from uuid import uuid4

from injector import inject

from domain.enums.event_types import EventTypes
from domain.repositories.reporting_repository import ReportingRepository
from domain.models.reporting import ReportingModel

from ..db.database_provider import DatabaseProvider


class CosmosReportingRepository(ReportingRepository):
    @inject
    def __init__(self, db_provider: DatabaseProvider):
        self.db_provider = db_provider

    def get_all(self) -> list[ReportingModel]:
        db = self.db_provider.get_database()
        container = db.get_container_client('ReportingDb')

        items = container.query_items(
            query="SELECT * FROM ReportingDb",
            enable_cross_partition_query=True
        )

        valid_events = set(item.value for item in EventTypes)

        reports = [
            ReportingModel(
                user_id=item.get("user_id"),
                username=item.get("username"),
                timestamp=item.get("timestamp"),
                event_type=EventTypes(item.get("event_type")),
                old_role=item.get("old_role"),
                new_role=item.get("new_role")
            )
            for item in items
            if item.get("event_type") in valid_events
        ]

        return reports

