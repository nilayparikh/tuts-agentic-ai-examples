# Code Map

This is the shortest map from course lesson to code surface.

| Lesson | Primary code path                                                                                                                                                              |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 01     | [status_snapshot.py#L16](../../status_snapshot.py#L16), [util.py#L357](../../util.py#L357), [verify.py#L168](../../verify.py#L168)                                             |
| 02     | [clean_data_runtime.py#L28](../../clean_data_runtime.py#L28), [mutation_playbook.py#L106](../../mutation_playbook.py#L106), [export_writer.py#L12](../../export_writer.py#L12) |
| 03     | [loop.py#L702](../../loop.py#L702), [loop.py#L277](../../loop.py#L277), [loop.py#L332](../../loop.py#L332)                                                                     |
| 04     | [dashboard.py#L66](../../dashboard.py#L66), [util.py#L458](../../util.py#L458), [tracing.py#L19](../../tracing.py#L19)                                                         |
| 05     | [prepare.py#L327](../../prepare.py#L327), [prepare.py#L239](../../prepare.py#L239), [challenger.py#L106](../../challenger.py#L106)                                             |
| 06     | [reranker.py#L67](../../reranker.py#L67), [prepare.py#L327](../../prepare.py#L327), [loop.py#L702](../../loop.py#L702)                                                         |
| 07     | [sandbox.py#L56](../../sandbox.py#L56), [autonomy.py#L78](../../autonomy.py#L78), [reset_workflow.py#L9](../../reset_workflow.py#L9)                                           |
| 08     | [dashboard.py#L66](../../dashboard.py#L66), [dashboard_artifacts.py#L28](../../dashboard_artifacts.py#L28), [dashboard_metrics.py#L47](../../dashboard_metrics.py#L47)         |
| 09     | [sandbox.py#L56](../../sandbox.py#L56), [autonomy.py#L127](../../autonomy.py#L127), [autonomy.py#L148](../../autonomy.py#L148)                                                 |

## Inline Coding Example

The lesson-02 runtime stays readable because the helpers use flat job-based names.

```python
from cleanloop.input_loader import read_finance_records
from cleanloop.mutation_playbook import normalize_numeric_amount
```
