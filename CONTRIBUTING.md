# Contributing to NutriGuide+

Thank you for your interest in contributing to NutriGuide+! This document provides guidelines for contributing to this computer vision-powered nutrition analysis platform.

## Development Setup

### Prerequisites
- Python 3.11 or higher
- Git for version control
- Code editor (VS Code recommended)

### Local Environment Setup

1. **Fork and clone the repository**
```bash
git clone https://github.com/your-username/NutriGuide-Plus.git
cd NutriGuide-Plus
```

2. **Create virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the development servers**
```bash
# Terminal 1: API Server
uvicorn app.main:api --reload --port 8000

# Terminal 2: UI Server
streamlit run web/app.py
```

## Code Standards

### Python Style
- Follow PEP 8 conventions
- Use type hints for all function parameters and return values
- Maintain 90%+ test coverage for new features
- Document all public functions with docstrings

### File Organization
```
app/
├── main.py           # API configuration
├── models.py         # Data models
├── routers/          # API endpoints
└── services/         # Business logic
```

### Commit Messages
Use conventional commit format:
```
feat: add new food recognition algorithm
fix: resolve nutrition calculation accuracy
docs: update API documentation
test: add computer vision test cases
```

## Contributing Guidelines

### Bug Reports
When reporting bugs, include:
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Screenshots for UI issues

### Feature Requests
For new features, provide:
- Clear problem statement
- Proposed solution approach
- Expected user impact
- Implementation complexity estimate

### Pull Request Process

1. **Create feature branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Implement changes**
- Follow code standards
- Add appropriate tests
- Update documentation

3. **Test thoroughly**
```bash
pytest -v
python -m uvicorn app.main:api --reload  # Verify API works
streamlit run web/app.py                 # Verify UI works
```

4. **Submit pull request**
- Provide clear description
- Link related issues
- Include screenshots for UI changes

## Areas for Contribution

### High Priority
- **Computer Vision Accuracy**: Improve food detection algorithms
- **Nutrition Database**: Expand USDA data coverage
- **Performance**: Optimize image processing speed
- **Testing**: Add comprehensive test coverage

### Medium Priority
- **UI/UX**: Enhance user interface design
- **Documentation**: Improve API and user docs
- **Accessibility**: Add screen reader support
- **Mobile**: Responsive design improvements

### Future Enhancements
- **Multi-language**: Internationalization support
- **Allergen Detection**: Food safety features
- **Meal Planning**: Recipe scheduling system
- **Analytics**: Usage tracking and insights

## Development Workflow

### Backend Development
```bash
# Start API in development mode
uvicorn app.main:api --reload --host 0.0.0.0 --port 8000

# Run tests
pytest tests/ -v

# Check API docs
open http://localhost:8000/docs
```

### Frontend Development
```bash
# Start Streamlit in development mode
streamlit run web/app.py

# Test UI
open http://localhost:8501
```

### Computer Vision Development
```bash
# Test food recognition locally
python -c "
from app.services.vision import classify_topk
# Add your test code here
"
```

## Code Review Criteria

### Functionality
- ✅ Code works as intended
- ✅ Handles edge cases gracefully
- ✅ Maintains backward compatibility
- ✅ Follows security best practices

### Quality
- ✅ Clean, readable code
- ✅ Appropriate comments and docstrings
- ✅ No code duplication
- ✅ Efficient algorithms

### Testing
- ✅ Unit tests for new functions
- ✅ Integration tests for API endpoints
- ✅ Manual testing completed
- ✅ No regression in existing features

## Getting Help

### Technical Questions
- Review existing code and documentation
- Check API documentation at `/docs`
- Search existing GitHub issues

### Collaboration
- Join discussions in GitHub issues
- Propose architectural changes via issues first
- Coordinate on large features before implementation

## Recognition

Contributors will be acknowledged in:
- Project README
- Release notes
- GitHub contributor graph

Thank you for helping make NutriGuide+ better!

---
**NutriGuide+ Development Team**