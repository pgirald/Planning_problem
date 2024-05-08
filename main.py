from Job import Job
from Job_CSP import solveAll

jobs: list[Job] = [
    Job(name="Job1", income=155, start=0, end=2),
    Job(name="Job2", income=142, start=1, end=2),
    Job(name="Job3", income=82, start=2, end=3),
    Job(name="Job4", income=113, start=4, end=5),
    Job(name="Job5", income=62, start=3, end=4),
    Job(name="Job6", income=44, start=5, end=5.5),
    Job(name="Job7", income=142, start=6, end=8),
    Job(name="Job8", income=58, start=6, end=7),
    Job(name="Job9", income=188, start=7, end=8),
    Job(name="Job10", income=54, start=8, end=9),
    Job(name="Job11", income=174, start=10, end=12),
    Job(name="Job12", income=75, start=11, end=12),
    Job(name="Job13", income=42, start=12, end=14),
    Job(name="Job14", income=192, start=13, end=14),
    Job(name="Job15", income=96, start=14, end=15),
]

solution = solveAll(jobs)
jobs: list[Job] = solution["jobs"]
print("\nSolution:\n")
for job in jobs:
    print(job)
