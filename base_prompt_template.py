
mapping_prompt = """
Audit item:
{audit_item}
ISO 27002 Clause:
{clause}
 
 
As a cybersecurity expert, you are to critically assess whether the description of the audit item directly addresses the provided ISO 27002 clause. Follow these steps to complete the task:
1. Read the ISO 27002 Clause
- Carefully read and understand the provided ISO 27002 clause.
2. Read the Audit Item:
- Carefully read and understand the provided audit item description.
3. Evaluate the Direct Addressing:
  - Compare the audit item description to the ISO 27002 clause.
  - Determine if the audit item directly fulfills or meets the specific requirements of the ISO 27002 clause.
4. Make Your Determination:
  - If the audit item directly addresses the requirements of the ISO 27002 clause, respond with "Yes".
  - If the audit item only indirectly benefits the ISO 27002 clause or does not fully address it, respond with "No".
5. Provide Your Rationale:
- Explain your reasoning for your determination.
  - Include any considerations that led to your decision.
6.Map the ISO 27001 clause to the audit item only based on the whole context of the clause and not based on the words in the ISO 27001 clause that alligns with the audit item.
Your answer must strictly follow the format "Yes, it should be mapped. Rationale: " or "No, it should not be mapped. Rationale: ".
"""

recheck_rationale_prompt = """
You are a cybersecurity expert. Another expert has reviewed and determined whether an audit item under the CIS Microsoft Azure Foundations Benchmark v2.1.0 directly addresses an ISO27001:2022 clause. Your task is to critically review the provided rationale and determine the accuracy of this mapping, taking into account the motivation and context of the audit item and ISO clause. Based on your analysis state "No, it should not be mapped." or State "Yes, it should be mapped" and provide your rationale for that. Below are the descriptions for both the ISO clause and the audit item, as well as the expert's rationale and decision for the mapping:
ISO27001:2022 Clause:
{clause}
 

Audit Item:
{audit_item}
Rationale:
{mapping}
 
Map the ISO 27001 clause to the audit item only based on the whole context of the clause and not based on the words in the ISO 27001 clause that alligns with the audit item.
Your answer must strictly follow the format "Yes, it should be mapped. Rationale: " or "No, it should not be mapped. Rationale: ".
Answer:
"""
