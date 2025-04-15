# Report analysis strategy selection engine

This component is meant to select appropriate report analysis strategy based on the markdown content of the report.

## Contract

### Input

 - Contents of the report provided as string in markdown format

### Output

 - Report Analysis Strategy

## Goal

Selection engine selects the appropriate [defect identification strategy](DefectIdentificationStrategy.md) based on the contents of the report.

The idea is to provide LLM the content of the report together with the criteria for each strategy and let the LLM match the content with the criteria.

Each strategy provides a prompt fragment to be used by the engine describing its selection criteria.
