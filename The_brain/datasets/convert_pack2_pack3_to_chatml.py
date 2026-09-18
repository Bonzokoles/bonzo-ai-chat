#!/usr/bin/env python3
"""
Konwersja pack2 (996 monologów) + pack3 (1200 prompt/response) do ChatML format
"""

import json
from pathlib import Path

# Style-specific system prompts
SYSTEM_PROMPTS = {
    "grotesque": "Jesteś JIMBO - cynicznym obserwatorem rzeczywistości w stylu groteskowym. Twoje opisy są surrealistyczne, absurdalne, pełne metafor i porównań odsłaniających absurd codzienności.",
    "philosophy": "Jesteś JIMBO - filozofem ulicy, łączysz Camusa, Nietzschego i Bukowskiego. Prawda boli, ale jest jedyną drogą. Bez cukru, bez iluzji.",
    "aggressive": "Jesteś JIMBO - stawiasz granice betonem, nie kredą. Konsekwentny, bezpośredni, nie tolerujesz manipulacji. Prawda gryzie jak wściekły pies.",
    "dark_humor": "Jesteś JIMBO - czarny humor to twój filtr na rzeczywistość. Śmiejesz się z katastrofy, bo to jedyna stała. Cynizm z klasą.",
    "buddy": "Jesteś JIMBO - kumplowski, ale szczery. Podniesiesz, ale najpierw powiesz gdzie skręciłeś źle. Nie nosisz, ale idziesz obok.",
    "jimbo_core": "Jesteś JIMBO - partner, nie asystent. 'Bonzo > wszystko'. Szczerość zamiast pochlebstw. Lustrzane odbicie, które pokazuje to co jest, nie to co chcesz usłyszeć."
}

def convert_pack2_to_chatml(input_file: Path, output_file: Path):
    """
    Pack2: {id, style, type, text} → ChatML {messages: [system, assistant]}
    996 monologów
    """
    examples = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                data = json.loads(line)
                style = data.get('style', 'jimbo_core')
                text = data.get('text', '')
                
                if not text:
                    continue
                
                system_prompt = SYSTEM_PROMPTS.get(style, SYSTEM_PROMPTS['jimbo_core'])
                
                example = {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "assistant", "content": text}
                    ]
                }
                
                examples.append(example)
                
            except json.JSONDecodeError as e:
                print(f"❌ Pack2 Line {line_num}: {e}")
                continue
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    return len(examples)

def convert_pack3_to_chatml(input_file: Path, output_file: Path):
    """
    Pack3: {id, style, prompt, response} → ChatML {messages: [system, user, assistant]}
    1200 prompt/response pairs
    """
    examples = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                data = json.loads(line)
                style = data.get('style', 'jimbo_core')
                prompt = data.get('prompt', '')
                response = data.get('response', '')
                
                if not prompt or not response:
                    continue
                
                system_prompt = SYSTEM_PROMPTS.get(style, SYSTEM_PROMPTS['jimbo_core'])
                
                example = {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                        {"role": "assistant", "content": response}
                    ]
                }
                
                examples.append(example)
                
            except json.JSONDecodeError as e:
                print(f"❌ Pack3 Line {line_num}: {e}")
                continue
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    return len(examples)

def main():
    pack2_input = Path("M:/MISTRAL_BONZO_TOOLS/DATASETMOJA/cha_llm_dialogs_dataset_pack2.jsonl")
    pack2_output = Path("M:/MISTRAL_BONZO_TOOLS/DATASETMOJA/cha_llm_dialogs_pack2_chatml.jsonl")
    
    pack3_input = Path("M:/MISTRAL_BONZO_TOOLS/DATASETMOJA/cha_llm_dialogs_pack3_instruct.jsonl")
    pack3_output = Path("M:/MISTRAL_BONZO_TOOLS/DATASETMOJA/cha_llm_dialogs_pack3_chatml.jsonl")
    
    print("🔄 Konwersja pack2 (monologi) → ChatML...")
    pack2_count = convert_pack2_to_chatml(pack2_input, pack2_output)
    print(f"✅ Pack2: {pack2_count} przykładów ({pack2_output.stat().st_size / 1024:.2f} KB)")
    
    print("\n🔄 Konwersja pack3 (prompt/response) → ChatML...")
    pack3_count = convert_pack3_to_chatml(pack3_input, pack3_output)
    print(f"✅ Pack3: {pack3_count} przykładów ({pack3_output.stat().st_size / 1024:.2f} KB)")
    
    print(f"\n📊 Total: {pack2_count + pack3_count} przykładów JIMBO")
    
    # Pierwszy przykład z pack3 (prompt/response)
    with open(pack3_output, 'r', encoding='utf-8') as f:
        first = json.loads(f.readline())
        print("\n📋 Przykład pack3 (conversational):")
        print(json.dumps(first, indent=2, ensure_ascii=False)[:500] + "...")

if __name__ == "__main__":
    main()
