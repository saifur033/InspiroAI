from src.caption_variations_engine import create_truly_different_variations

result = create_truly_different_variations('Check out my new product!', 'professional')
print('✅ Caption Variations Engine Works!')
print(f'Generated: {result.get("total_variations")} variations\n')

if result.get('variations'):
    for i, v in enumerate(result['variations'][:5]):
        print(f"{i+1}. {v['approach']}")
        print(f"   SEO Score: {v['seo_score']} | Emotion: {v['emotion']} | Length: {v['length']} words")
        print(f"   Preview: {v['caption'][:80]}...\n")
