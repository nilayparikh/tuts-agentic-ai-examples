# Code Map

This is the shortest map from course lesson to code surface.

| Lesson | Primary code path                                                                                                                                                              |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 01     | [status_snapshot.py#L16](../../status_snapshot.py#L16), [util.py#L357](../../util.py#L357), [verify.py#L168](../../verify.py#L168)                                             |
| 02     | [clean_data_runtime.py#L28](../../clean_data_runtime.py#L28), [mutation_playbook.py#L106](../../mutation_playbook.py#L106), [export_writer.py#L12](../../export_writer.py#L12) |
| 03     | [loop.py#L617](../../loop.py#L617), [loop.py#L260](../../loop.py#L260)                                                                                                         |
| 04     | [dashboard.py#L58](../../dashboard.py#L58), [history_store.py#L10](../../history_store.py#L10), [tracing.py#L19](../../tracing.py#L19)                                         |
| 05     | [prepare.py#L324](../../prepare.py#L324), [challenger.py#L106](../../challenger.py#L106)                                                                                       |
| 06     | [reranker.py#L67](../../reranker.py#L67), [reranker.py#L118](../../reranker.py#L118)                                                                                           |
| 07     | [sandbox.py#L56](../../sandbox.py#L56), [autonomy.py#L148](../../autonomy.py#L148), [reset_workflow.py#L9](../../reset_workflow.py#L9)                                         |

## Inline Coding Example

The lesson-02 runtime stays readable because the helpers use flat job-based names.

```python
from cleanloop.input_loader import read_finance_records
from cleanloop.mutation_playbook import normalize_numeric_amount
```
