# Debug Session: project-slides-missing

Status: OPEN

## Symptom
项目卡片 `ai-rd-system` 显示 0 pages，用户认为项目数据丢失。

## Hypotheses
1. 最近的反向提交删除了该项目受版本控制的 SVG 幻灯片。
2. 本地生成的项目输出目录曾被清理，数据未被 Git 跟踪。
3. `/api/scan-projects` 的扫描条件与项目目录结构不一致。
4. 浏览器展示了接口返回的空 slides 数据，而非前端渲染故障。

## Evidence
待收集。
