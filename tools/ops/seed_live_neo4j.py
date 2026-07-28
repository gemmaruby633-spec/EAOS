import base64
import json
import urllib.request

stmt1 = "MATCH (n) DETACH DELETE n"

stmt2 = """
CREATE (sys:EnterpriseSystem {name: 'EAOS', version: '3.0.0', health_score: 100, status: 'ACTIVE'})
CREATE (const:ArchitectureConstitution {name: 'ARCHITECTURE_CONSTITUTION.md', version: 'v3.0', rules: 20})
CREATE (loop:CyberneticLoop {name: '13-Stage Self-Evolution Loop', stages: 13, mode: 'Autonomous'})

CREATE (sys)-[:GOVERNED_BY]->(const)
CREATE (sys)-[:RUNS_LOOP]->(loop)

CREATE (d1:CapabilityDomain {name: 'Enterprise Architecture', code: 'EA'})
CREATE (d2:CapabilityDomain {name: 'Business Architecture', code: 'BA'})
CREATE (d3:CapabilityDomain {name: 'Process Architecture', code: 'PA'})
CREATE (d4:CapabilityDomain {name: 'IT Governance', code: 'ITG'})
CREATE (d5:CapabilityDomain {name: 'Security Architecture', code: 'SEC'})
CREATE (d6:CapabilityDomain {name: 'Data Architecture', code: 'DATA'})
CREATE (d7:CapabilityDomain {name: 'Integration Architecture', code: 'INT'})
CREATE (d8:CapabilityDomain {name: 'Solution Architecture', code: 'SOL'})
CREATE (d9:CapabilityDomain {name: 'AI Architecture', code: 'AI'})
CREATE (d10:CapabilityDomain {name: 'Platform Infrastructure', code: 'OPS'})

CREATE (sys)-[:HAS_DOMAIN]->(d1)
CREATE (sys)-[:HAS_DOMAIN]->(d2)
CREATE (sys)-[:HAS_DOMAIN]->(d3)
CREATE (sys)-[:HAS_DOMAIN]->(d4)
CREATE (sys)-[:HAS_DOMAIN]->(d5)
CREATE (sys)-[:HAS_DOMAIN]->(d6)
CREATE (sys)-[:HAS_DOMAIN]->(d7)
CREATE (sys)-[:HAS_DOMAIN]->(d8)
CREATE (sys)-[:HAS_DOMAIN]->(d9)
CREATE (sys)-[:HAS_DOMAIN]->(d10)

CREATE (f1:Framework {name: 'TOGAF ADM 10', category: 'EA'})
CREATE (f2:Framework {name: 'Zachman Framework', category: 'EA'})
CREATE (f3:Framework {name: 'BIZBOK Guide', category: 'BA'})
CREATE (f4:Framework {name: 'APQC PCF', category: 'PA'})
CREATE (f5:Framework {name: 'ITIL v4', category: 'ITG'})
CREATE (f6:Framework {name: 'NIST CSF 2.0', category: 'SEC'})
CREATE (f7:Framework {name: 'DAMA-DMBOK2', category: 'DATA'})
CREATE (f8:Framework {name: 'Clean Architecture', category: 'SOL'})

CREATE (d1)-[:INCORPORATES]->(f1)
CREATE (d1)-[:INCORPORATES]->(f2)
CREATE (d2)-[:INCORPORATES]->(f3)
CREATE (d3)-[:INCORPORATES]->(f4)
CREATE (d4)-[:INCORPORATES]->(f5)
CREATE (d5)-[:INCORPORATES]->(f6)
CREATE (d6)-[:INCORPORATES]->(f7)
CREATE (d8)-[:INCORPORATES]->(f8)
"""

passwords = ["password", "eaos_password", "neo4j", "12345678"]
success = False

for pwd in passwords:
    try:
        url = "http://localhost:7474/db/neo4j/tx/commit"
        auth_str = f"neo4j:{pwd}"
        b64_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

        payload = json.dumps({"statements": [{"statement": stmt1}, {"statement": stmt2}]}).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {b64_auth}",
            },
        )

        with urllib.request.urlopen(req) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                errors = data.get("errors", [])
                if not errors:
                    print(f"✔ SUCCESS! Seeded Knowledge Graph into Neo4j using password: '{pwd}'")
                    success = True
                    break
                else:
                    print(f"Cypher Error: {errors}")
    except Exception:
        continue

if not success:
    print("✖ Could not seed Neo4j.")
