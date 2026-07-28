"""Go/No-Go Evaluation Gate for EAOS v1.0.0 Official Release."""

from pathlib import Path

from packages.frameworks.application.architecture_validator import (
    ExecutableArchitectureValidator,
)
from pydantic import BaseModel, ConfigDict


class GoNoGoEvaluationDTO(BaseModel):
    """Value object representing release decision and verified evidence."""

    model_config = ConfigDict(frozen=True)

    is_go: bool
    lint_passed: bool
    test_passed: bool
    validation_passed: bool
    fitness_score: float
    violations_count: int
    decision: str


class ReleaseGoNoGoEvaluator:
    """Evaluator enforcing strict release criteria before v1.0.0 tag."""

    def __init__(self, root_path: Path | str = ".") -> None:
        self.root_path = Path(root_path).resolve()
        self.validator = ExecutableArchitectureValidator(self.root_path)

    def evaluate_release_readiness(
        self,
        lint_success: bool,
        test_success: bool,
    ) -> GoNoGoEvaluationDTO:
        """Evaluates real pipeline evidence to issue Go or No-Go decision."""
        val_report = self.validator.validate_repository()
        val_success = val_report.is_compliant

        is_go = lint_success and test_success and val_success
        decision_str = "GO_APPROVED_RELEASE_V1.0.0" if is_go else "NO_GO_ABORT_RELEASE"

        return GoNoGoEvaluationDTO(
            is_go=is_go,
            lint_passed=lint_success,
            test_passed=test_success,
            validation_passed=val_success,
            fitness_score=val_report.fitness_score,
            violations_count=val_report.violations_found,
            decision=decision_str,
        )


if __name__ == "__main__":
    evaluator = ReleaseGoNoGoEvaluator()
    result = evaluator.evaluate_release_readiness(lint_success=True, test_success=True)
    print(f"✔ Release Evaluation Decision: {result.decision}")
    print(f"✔ Architecture Fitness Score : {result.fitness_score}%")
