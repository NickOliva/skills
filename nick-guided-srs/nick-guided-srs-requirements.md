---
skill_name: nick-guided-srs
installation_scope: repo
installation_target: .agents/skills/nick-guided-srs
installation_method: symlink
---

# Guided SRS Learning Requirements

## Terminology and Flow

The `items` for learning generated in this process are categorized or otherwise attributed as follows. This list follows progression, but presentation is inverse.

1. parsed and ingested - one or more `item` artifacts generated
2. retained - promotion based on determination that there is at least a minimum value, but the current value has not been measured. In the current implementation this happens in place, so there is no immediate risk of loss of context. 
2. 
2. 

## Capability to parse Great Courses into Atomic Bits

This skill will distill a source into a collection of facts and quotes that seem both atomic and significant. These will be put into a list of checklist items by chapter. If there is a logical subgrouping within a chapter, that may be used, too.

The data will be put into a file in `~/Vaults/Knowledge/Learning/Active SRS Sources`.

One source type is a Great Courses course guide which will take a simplified name for the folder and data file. For example, `~/Vaults/Knowledge/Learning/Active SRS Sources/Eastern Intellectual Tradition/Eastern Intellectual Tradition.md`

Nick will request parsing and generation of data, and the agent will segment the guide information into atomid, well-formatted quotes, each preceded by a checkbox, grouped by lecture, and any other reasonably simple logical further grouping. These will be put into the bottom of the md file under heading `# Source Data`.

The generation of source data is known as `1. Auto Ingest Source`. The individual items are just called `items`.

## Capability to curate the ingested items

The source will be updated in place by nick directly or with agent assistance and interaction to:

- determine what to promote or ignore by checking the boxes 
- make edits, splits, and combinations



- for each keeper decide the desired level of knowledge and important using high-volume interface
- ingest into learning material for achieving the targets
- lectures, chapters, articles, and other groupings will be used to chunk the learning; preserve these in the data as they apply for particular source content types.

## 
