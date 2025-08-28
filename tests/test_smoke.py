from app.models import NutritionProfile

def test_schema_works():
    p = NutritionProfile(name="banana", serving_grams=118, calories=105,
                         macros={"protein_g":1.3,"carbs_g":27,"fat_g":0.3}, micronutrients={})
    assert p.name == "banana"