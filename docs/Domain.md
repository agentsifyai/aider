# Domain

This file contains Domain Definitions.

## Defect

We consider a defect to be a compound of:
 - Name of damage done on an object
 - Location of a damaged object or the damage itself

These 2 let us indentify a unique defect. 

Let's take a look at the example:
```json
{
    "damage": "Broken lantern and milky lantern glass",
    "location": "Ceiling of the regional court in room no. 12 in Zamość city"
}
```
> Keep in mind that in further development global location (address, such as Zamość city here) would be inferred using related contract.

## Potential Defect

This is an extension of [Defect](#defect).

Potential defect extends a defect with fields containing data about its inference from the source documents.

Additional fields:
 - Likeliness describing how much a damage is likely to be a true defect (true positive)
 - Evidence: { quote, page } where quote is the concrete text in the report and page is a number of a page in the report document (if applicable)

## Detailed Potential Defect

This is an extension of [Potential Defect](#potential-defect)

Detailed potential defect extends a potential defect with fields about detailed defect description and other data about the defect.

Additional fields:
 - Verbose Description - verbose data about the defect if it can be inferred from the report