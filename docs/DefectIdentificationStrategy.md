# Defect Identification strategy

Defect Identification strategy is meant to interpret a report accounting for the corresponding [**report type**](Architecture.md#report-analysis-strategy-selection) to identify all the [potential defects](Domain.md#potential-defect) in the report.

## Contract

### Input:

 - Contents of the report provided as string in markdown format

### Output

 - List of Potential Defects


## Goal

Goal of the strategy is to correctly understand given report type and based on that understanding provide a list of potential defects.

Key point here is that all the defects present in input content must be identified. Therefore we may specify many strategies for various report types which differ in terms of how defect information is conveyed in the report. 

## Strategy selection

Strategies may be selected using a [selection engine](DefectIdSelectionEngine.md)

Ideally some defect identification will occur regardless of the chosen strategy, however the correct strategy matching should improve **accuracy** regarding both defect presence and factual damage identification.

The strategy should expose a *prompt fragment* for the selection engine about the criteria that should be met to select this strategy.

## Further flow - details identification

Further flows involves additional details identification, thus strategy must expose an interface to get corresponding [defect detailing strategy](DefectDetailingStrategy.md)
