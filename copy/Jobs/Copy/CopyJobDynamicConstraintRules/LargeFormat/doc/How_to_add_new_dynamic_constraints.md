
# How to add a new constraint

*Its recommended to read this howto in preview mode.*

The following example showcases how to add a new constraint.

## Step 1

We will add the following dynamic constraint:

**When scan job intent colormode is black and white, disable fileformat TIFF.**

### Step 1. Identify if your product has a configuration file .csf onto conf folder

- Make sure *CopyJobDynamicConstraintRulesLargeFormat.csf* does not define the constraint.
- If exist, take care on how you modify the file to not broke the rest of constraints.
- If not exist, create a new one on your family and product folder

#### Step 2. Create your dynamic constraint

#### Example of a constraint definition on  config

``` json
{
    "settingName":"src/scan/invertColors",
    "rules":[
        {
            "ifOperation":"NAND",
            "if":[
                {
                    "settingName":"scanJobIntent_originalMediaType",
                    "withValueIn": [
                        {"unionValue":{"value":"BLUEPRINTS"},"unionValue_type":"OriginalMediaType"},
                        {"unionValue":{"value":"DARK_BLUEPRINTS"},"unionValue_type":"OriginalMediaType"}
                    ]
                }
            ],
            "then":{
                "supportedValues": [
                    {"unionValue":{"value":"false"},"unionValue_type":"BOOL"}
                ],
                "constrainedMessageStringId":"StringIds.cThisOptionUnavailable",
                "disabled":true
            },
            "rulePolicy":"STOP"
        }
    ]
}
```

#### Example of description

A constraint rule that depends from a job ticket value, has the next structure:

On First Level:
- **SettingName:**

  - Here you will indicate the setting that will be affected by a list of constraint rules.
  
- **Rules:**
  - Here you will add a list of rules that must to be applied to setting.


On rule level:  

- **ifOperation:**
  
  - This field will indicate what type of statement operation will be applied when if list will be checked.
  - Exist 4 statements that currently can be applied:

    - *AND (default):* This will apply AND logic to list of ifs, when checking the ticket if there is two "ifs", and two are correctly selected on ticket, then rule check result satisfactory.
    If there is a value from ticket that not are contained on rule, rule is not satisfied and will be ignored.
    - *OR:* Logic operation, when on list of "ifs" if there is one if statement satisfied, then rule applications will be invoked
    - *NAND:* Reverse operation of AND. Then result, only will be invoked in case of any of "ifs" list, is not satisfied.
    - *NOR:* Reverse of operation OR. Then result only will be applied when all list of "ifs" is not satisfied.

To have a graphic description:

**- With one if**

| If    | And result   | Nand result    | OR result | NOR result|
|:---   |   :---:      |   :---:        |  :---:    |    ---:   |
|  1    |     1        |      0         |   1       |       0   |
|  0    |     0        |      1         |   0       |       1   |

**- With Two ifs**

| If1   |   If2 | And result   | Nand result    | OR result | NOR result|
|:---   |:---:  |   :---:      |   :---:        |  :---:    |    ---:   |
|  1    |   1   |     1        |      0         |   1       |       0   |
|  1    |   0   |     0        |      1         |   1       |       0   |
|  0    |   1   |     0        |      1         |   1       |       0   |
|  0    |   0   |     0        |      1         |   0       |       1   |

**- With Three ifs**

| If1   |   If2 |   If3 | And result   | Nand result    | OR result | NOR result|
|:---   |:---:  |:---:  |   :---:      |   :---:        |  :---:    |    ---:   |
|  1    |   1   |   1   |     1        |      0         |   1       |       0   |
|  1    |   1   |   0   |     0        |      1         |   1       |       0   |
|  1    |   0   |   1   |     0        |      1         |   1       |       0   |
|  1    |   0   |   0   |     0        |      1         |   1       |       0   |
|  0    |   1   |   1   |     0        |      1         |   1       |       0   |
|  0    |   1   |   0   |     0        |      1         |   1       |       0   |
|  0    |   0   |   1   |     0        |      1         |   1       |       0   |
|  0    |   0   |   0   |     0        |      1         |   0       |       1   |

By default this field is AND logic operation, and It's not need to be added on csf if you want an AND logic execution.

- ***if***. This section is a list of settings to be checked on job ticket:
  - *SettingName*: this name is on CopyJobDynamicConstraintRulesLargeFormatConfig fbs, is a list of settints that have an equivalence with CopyJobIntent.fbs.
  Structure of the name is based on variable names on fbs, and if the variable is a table with more variables, is named and separated its internal names with "_" as the example: scanJobIntent_originalMediaType

    In this case, the setting is on scan job intent part, and the variable setting name is originalMediaType.
    It's important take care of this setting name.

  - *WithValueIN:* Section that will indicate a list of values to check on ticket. If any of this values is on current ticket will satisfy or not the rule, depends of the ifOperation expected.


    - *Union Value:* This field is an encapsulation to indicate a value, that is on fbs file.
    Call to this as an object to select next possible fields:
      -*Value | min,max,step | minLength,maxLength* : The field added here are relative to the different tables supported, indicated on fbs file. Check all current possibilities.
    - *unionValue_type:* Field used to indicate the table type that is contained on UnionValue object.
    Supported formats must to be on union CopyIntentValues of the fbs.

- *then:* Here there will be encapsulated the actions for settingName indicated.
  - *Supported values:* here will be indicated the supported values that settingName will support it in case of if statement part is satisfied.
  The list internally is the same as WithValueIn, is a list of UnionValues with CopyIntentValues type.

- *constrainedMessageStringId*: Field to indicate a generic string id, for certain constraints. If this field is not indicated, message will be created based on a behavior of Axure All options. Check the axure if you want to know better how is this message format. By default this is empty, and can be not added on csf file

- *disabled*: This field is to indicated that constraint must to have a Lock constraint, this normally means that constraint will be constrained on clients. By default this is false and can be not added on csf file.

- *rule policy*: 

**Important message**

If you want to combine different if operations (certain setting check with AND, others with OR), better think to combine new rules on list
A rule that apply an AND operation, with rulePolicy continue, and then another rule that have other operation.

Rules on this case must to combine, will be explained better on above section Rule policy.

### Force Sets logic

Current component have an internal behavior, that if you add a "settingName" on the list of listOfRulesBasedOnTicketValues.

There will be a method invoked about *checkAndApplyForce*, that will read this list, only the name, and will map several functions from the name to try to auto-adjust current job tickets on the expected correct values.

Component do this based on the idea that we haven't got any setting with a non supported value.
So if thicket have a value not supported, when enter to this method, and check that constraint not supported current value, job ticket value will be changed to the new expected suppported.

Take always this behavior in mind.

### What occurs if there is a setting that I not support here?

There could be the situation where we have a setting or a variable that is not currently supported.

So, what are the main fields that must to be checked?

On CopyJobDynamicConstraintRulesLargeFormatConfig.fbs

- Setting of CopyJobIntent is on TicketSettingEnum?
In case that no, create it here, and then goes to CopyJobDynamicConstraintRulesLargeFormatMapper.h on Map2CheckerTicketMethod namespace.

Here on the unordered map, add a new field as the next example:
```cpp
{
    TicketSettingEnum::scanJobIntent_inputMediaSizeId,                 
    [](CopyIntentValuesUnion value, std::shared_ptr<ICopyJobTicket> ticket) -> bool 
    { 
        Map2CheckerTicketMethod::checkValueType(value, CopyIntentValues::MediaSizeId);         
        return Map2CheckerTicketMethod::getValue<dune::imaging::types::MediaSizeId>(value) == ticket->getIntent()->getInputMediaSizeId(); 
    }
},
```

    - Key tuple is the ticket enum from fbs.
    - Value tuple is a lambda function that will check if value type expected is correctly, take the value from Map2CheckerTicketMethod::getValue method template, and compare with the ticket that contains the function method (if Copy Job ticket not contains the value of fbs ticket .... Sorry, you need to modify intents of cpp too).

- I need a new value.
In this case, you need to create a new table, with the expected format, and add on CopyIntentValues union.

Then goes to CopyJobDynamicConstraintRulesLargeFormatMapper.h on Map2CheckerTicketMethod namespace.
And create a new getValue method with the type conversion to fbs that you expect, this type must to be on new table as you can imagine, as example BOOL table, contains a bool value, that when is called will be a ```getValue<bool>``` call.

### Is there any problem when I try to use a setting cdm on settingName on Force sets?

On this case, that normally will cause a crash.

You need to check next 3 maps on CopyJobDynamicConstraintRulesLargeFormatMapper.h:
- Map2CheckerCdmTableProperty::MAP
This map, check on Job ticket table cdm is there is a value on current job ticket table.
Imitate the format as a serialization/deserialization.

Example:
```cpp
{
    "src/scan/colorMode",
    [](const std::shared_ptr<dune::cdm::jobTicket_1::JobTicketTable>& updatedJobTicketTable, bool& settingIsSetOnCdm, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
    { 
        if(updatedJobTicketTable == nullptr || updatedJobTicketTable->src.get() == nullptr || updatedJobTicketTable->src.get()->scan.get() == nullptr)
        {
            CopyJobDynamicConstraintRulesLargeFormatMapperLogger::checkpointInfo("Map2CheckerCdmTableProperty::MAP src/scan/colorMode there is any table that not have value, return false");
            return false;
        }
        return Map2CheckerCdmTableProperty::checkProperty(updatedJobTicketTable->src.get()->scan.get()->colorMode,settingIsSetOnCdm,currentConstraints);
    }
},
```
Take a look if you have a supported checkProperty method with the type that you expected.

- Map2CheckerCopyJobTicketProperty::MAP
Similar than previous map, but on this case, the check will be the cpp job ticket model.

Example:
```cpp
{
    "src/scan/colorMode",
    [](std::shared_ptr<ICopyJobTicket> ticket, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
    { 
        return checkType(dune::job::cdm::mapToCdm(ticket->getIntent()->getColorMode()),currentConstraints);
    }
},
```

As previous map, here there is a checkType method and a mapToCdm method, that must to contains, the types that you will need to support, check the types an update the methods that you will need it

- Map2UpdateTableProperty::MAP

Same situation than first map, but this map is to *modify* the current job ticket table from cdm.
An example:
```cpp
{
    "src/scan/colorMode",
    [](const std::shared_ptr<JobTicketTable>& updatedJobTicketTable, std::shared_ptr<dune::framework::data::constraints::Constraints> currentConstraints) -> bool 
    { 
        checkScanTableMutables(updatedJobTicketTable);                
        return Map2UpdateTableProperty::setFirstValueOnProperty(currentConstraints,updatedJobTicketTable->src.getMutable()->scan.getMutable()->colorMode);
    }
},
```

Same as previous example, take care that method used have the expected supported types needed by your changes.

**On all of this examples, if there is any cdm setting that is not currently set, add it with a mostly similar spec definition than the examples, and the same methods if they are needed.**