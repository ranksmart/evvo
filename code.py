import re 
import json
 
df_iso_clauses = pd.read_excel("Downloads/ISO_Clauses_Processed.xlsx")
 
iso_clause_list = df_iso_clauses["Clause"].astype(str).tolist()
 
 
 
# Read Excel file
df_audit_items = pd.read_excel('Downloads/Audit_Items_Processed.xlsx', header=None)
 
# Convert DataFrame to a list of strings
audit_item_list = df_audit_items[0].astype(str).tolist()
 
 
 
 
def mapping_prompt(clause, audit_item):
    return f"""
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
 
def recheck_rationale_prompt(mapping, clause, audit_item):
    return f"""
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
 
# def load_iso_clauses(num_items=None, from_start=True):
#     # Load the data from the specified file
#     df_iso_clauses = pd.read_excel("Downloads/ISO_Clauses_Processed.xlsx")
#     iso_clauses =  df_iso_clauses["Clause"].astype(str).tolist()
#     # Determine which items to return based on input
#     if num_items is None:
#         return iso_clauses  # Return all items if no number specified
#     elif from_start:
#         return iso_clauses[0:num_items]  # Return the first 'num_items' elements
#     else:
#         return iso_clauses[-num_items:]  # Return the last 'num_items' elements
# def load_audit_items(num_items=None, from_start=True):
#     # Load the data from the specified file
#     df_audit_items = pd.read_excel('Downloads/Audit_Items_Processed.xlsx', header=None)
#     # Convert the first column to string
#     audit_items = df_audit_items[0].astype(str).tolist()
#     # Determine which items to return based on input
#     if num_items is None:
#         return audit_items[1:]  # Return all items if no number specified
#     elif from_start:
#         return audit_items[1:num_items]  # Return the first 'num_items' elements
#     else:
#         return audit_items[-num_items:]  # Return the last 'num_items' elements
def extract_decision(mapping):
    mapping_match = re.search(r'^(Yes|No)', mapping.strip(), re.IGNORECASE)
    return mapping_match.group(0) if mapping_match else None
def extract_rationale(mapping):
    rationale_match = re.search(r'Rationale:\s*(.*)', mapping.strip(), re.IGNORECASE | re.DOTALL)
    return rationale_match.group(1).strip() if rationale_match else None
def find_mapping_for_clause(iso_clause_list, audit_item):
    evidence_list = []
    for clause in iso_clause_list:
        response = client.chat.completions.create(
            model=model_key,
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert."},
                {"role": "user", "content": mapping_prompt(clause, audit_item)}
            ],
            temperature=0
        )
        mapping = response.choices[0].message.content.strip()
        initial_decision = extract_decision(mapping)
        print(f"initial decision : {initial_decision}\n")
        initial_rationale = extract_rationale(mapping)
        print(f"initial rationale : {initial_rationale}\n")

 
        recheck_response = client.chat.completions.create(
                model=model_key,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert."},
                    {"role": "user", "content": recheck_rationale_prompt(mapping, clause, audit_item)}
                ],
                temperature=0,
            )
        recheck = recheck_response.choices[0].message.content.strip()
        checker_decision = extract_decision(recheck)
        print(f"checker decision : {checker_decision}\n")
        checker_rationale = extract_rationale(recheck)
        print(f"checker rationale : {checker_rationale}\n")
        if "yes" in recheck.lower() :
            evidence_list.append((audit_item, clause, initial_decision,initial_rationale,checker_decision,checker_rationale))
    return evidence_list, mapping, recheck
 
 
# columns = ['CIS MS Azure foundations Benchmark Audit Item', 'Description of Audit Item', 'Mapped ISO 27001:2022 Clauses', 'Initial Decision', 'Initial Rationale','Checker Decision','Checker Rationale','Final Rationale']
# mappings_df = pd.DataFrame(columns=columns)
 
 
# Compare the first MAS TRM clause with the policy chunks for testing
# new_rows = []
for audit_item in audit_item_list[120:122] :
    new_rows = []
    evidence_list , mapping, recheck= find_mapping_for_clause(iso_clause_list, audit_item)
 
    
    if evidence_list:
        for evidence in evidence_list:
            audit_item, clause, initial_decision, intial_rationale, checker_decision, checker_rationale = evidence
            new_row = {
                'CIS MS Azure foundations Benchmark Audit Item':audit_item[:5] ,
                'Description of Audit Item': audit_item[5:],
                'Mapped ISO 27001:2022 Clauses': clause,
                'Initial Decision': initial_decision,
                'Initial Rationale': intial_rationale,
                'Checker Decision' : checker_decision,
                'Checker Rationale': checker_rationale
            }
            new_rows.append(new_row)
            new_rows_df = pd.DataFrame(new_rows)
            output_path = f"Downloads/audititem{audit_item[:5]}.json"
            new_rows_df.to_excel(f"Downloads/audititem{audit_item[:5]}.xlsx", index=False)
            with open(output_path, 'w') as json_file:
                json.dump(new_rows, json_file, indent=4)
    
        print("json saved successfully")
        print(" Excel saved successfully")

