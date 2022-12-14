from application.dto.reporting_read_dto import ReportingReadDto
from domain.repositories.reporting_repository import ReportingRepository
from injector import inject


class ReportingController:
    @inject
    def __init__(self, reporting_repository: ReportingRepository):
        self.reporting_repository = reporting_repository

    def get_reports(self) -> list[ReportingReadDto]:
        reports = self.reporting_repository.get_all()
        result = []

        for report in reports:
            result.append(ReportingReadDto(
                user_id=report.user_id,
                username=report.username,
                timestamp=report.timestamp,
                event_type=report.event_type.value,
                old_role=report.old_role,
                new_role=report.new_role
            ))

        return result
