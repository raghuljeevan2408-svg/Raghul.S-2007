from services.gemini_utils import home_recommendations

print("Starting test...")

result = home_recommendations(
    budget=50000,
    room="Living Room",
    requirements="Sofa, lighting, coffee table and wall decor"
)

print("\n===== POCKETSMART AI RECOMMENDATION =====\n")
print(result)