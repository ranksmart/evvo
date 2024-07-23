import pandas as pd
from base_llm import mistral
from base_prompt_template import mapping_prompt, recheck_rationale_prompt
import asyncio
from decision_rationale_extractor import Extractor
import time
import json




async def find_mapping_for_clause(iso_clause_list, audit_item):
    evidence_list = []
    # client = mistral()
    for clause in iso_clause_list:

        content = mapping_prompt.format(audit_item = audit_item, clause = clause)
        client.append_to_conversation_history('user', content)
        prompt = client.conversation
        response = await client.async_generate_response(prompt=prompt)
        mapping = response.choices[0].message.content.strip()
        client.delete_conversation_history()
        # print(mapping)

        initial_decision = Extractor.extract_decision(mapping)
        print(f"initial decision : {initial_decision}\n")
        initial_rationale = Extractor.extract_rationale(mapping)
        print(f"initial rationale : {initial_rationale}\n")

        content = recheck_rationale_prompt.format(audit_item = audit_item, clause = clause, mapping = mapping)
        client.append_to_conversation_history('user', content)
        prompt = client.conversation
        recheck_response = await client.async_generate_response(prompt=prompt)
        recheck = recheck_response.choices[0].message.content.strip()
        client.delete_conversation_history()

        
        checker_decision = Extractor.extract_decision(recheck)
        print(f"checker decision : {checker_decision}\n")
        checker_rationale = Extractor.extract_rationale(recheck)
        print(f"checker rationale : {checker_rationale}\n")

        if "yes" in recheck.lower() :
            evidence_list.append((audit_item, clause, initial_decision,initial_rationale,checker_decision,checker_rationale))
    return evidence_list, mapping, recheck
 

async def main():
    # client = mistral()
    for audit_item in audit_item_list:
        evidence_list, mapping, recheck = await find_mapping_for_clause(iso_clause_list, audit_item)
        print(evidence_list)

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

                new_rows_df = pd.DataFrame([new_row])
                output_path = f"./audititem{audit_item[:5]}.json"
                new_rows_df.to_excel(f"./audititem{audit_item[:5]}.xlsx", index=False)
                with open(output_path, 'w') as json_file:
                    json.dump([new_row], json_file, indent=4)
    
            print("json saved successfully")
            print(" Excel saved successfully")

if __name__ == "__main__":

    audit_item_list = [
    "Access Control Policy - Clause A.9.1.1",
    "Information Security Policy - Clause 5.1.1",
    # "Asset Management - Clause A.8.1.1",
    # "Cryptographic Controls - Clause A.10.1.1",
    # "Physical Security Perimeter - Clause A.11.1.1"
    ]

    iso_clause_list = [
        "ISO/IEC 27001:2013 - Clause A.9.1.1",
        "ISO/IEC 27001:2013 - Clause 5.1.1",
        # "ISO/IEC 27001:2013 - Clause A.8.1.1",
        # "ISO/IEC 27001:2013 - Clause A.10.1.1",
        # "ISO/IEC 27001:2013 - Clause A.11.1.1"
    ]

    start = time.time()
    client = mistral()
    asyncio.run(main())
    end = time.time()

    total = end - start
    print('total time taken is: ', total)


