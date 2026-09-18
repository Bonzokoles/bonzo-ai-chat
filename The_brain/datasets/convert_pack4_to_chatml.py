#!/usr/bin/env python3
"""
Konwersja pack4_MERGED (168 monologów) do ChatML format
Każdy monolog → assistant message z style-specific system prompt
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

def convert_monologs_to_chatml(input_file: Path, output_file: Path):
    """
    Konwertuje monologi {style, text} → ChatML {messages: [system, assistant]}
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
                    print(f"⚠️ Line {line_num}: brak tekstu, pomijam")
                    continue
                
                # Wybierz system prompt na podstawie stylu
                system_prompt = SYSTEM_PROMPTS.get(style, SYSTEM_PROMPTS['jimbo_core'])
                
                # ChatML format: system + assistant (monolog)
                example = {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "assistant", "content": text}
                    ]
                }
                
                examples.append(example)
                
            except json.JSONDecodeError as e:
                print(f"❌ Line {line_num}: błąd JSON - {e}")
                continue
    
    # Zapisz w formacie JSONL
    with open(output_file, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    return len(examples)

def main():
    input_file = Path("M:/MISTRAL_BONZO_TOOLS/DATASETMOJA/cha_llm_dialogs_pack4_MERGED.jsonl")
    output_file = Path("M:/MISTRAL_BONZO_TOOLS/DATASETMOJA/cha_llm_dialogs_pack4_chatml.jsonl")
    
    print("🔄 Konwersja pack4_MERGED → ChatML format...")
    print(f"📂 Input:  {input_file}")
    print(f"📂 Output: {output_file}")
    
    total = convert_monologs_to_chatml(input_file, output_file)
    
    print(f"\n✅ Zapisano {total} przykładów ChatML")
    print(f"📊 Rozmiar: {output_file.stat().st_size / 1024:.2f} KB")
    
    # Weryfikacja: pokaż pierwszy przykład
    with open(output_file, 'r', encoding='utf-8') as f:
        first = json.loads(f.readline())
        print("\n📋 Pierwszy przykład:")
        print(json.dumps(first, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
