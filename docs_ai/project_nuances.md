# Pymodoro Project Nuances

## UI Rendering Issues

### Long Break Screen Flickering (RESOLVED)

**Issue**: Long Break screen experienced flickering and missing title issues when displayed in terminal.

**Root Cause**: The `🛋️` (couch/sofa) emoji used for Long Break icon caused terminal rendering instability.

**Symptoms**:
- Screen flickering during Long Break sessions
- Title appearing and disappearing intermittently
- Layout appearing to "shift" or recalculate repeatedly

**Initial Incorrect Hypotheses**:
- ❌ Terminal color support issues (tested with different colors)
- ❌ ASCII art character count differences (tested identical art)
- ❌ Rich component caching problems (tested cache behavior)
- ❌ Text length differences (tested identical character counts)

**Actual Root Cause**:
- ✅ **Emoji rendering instability**: The `🛋️` emoji cannot be rendered consistently in the terminal environment
- Rich library struggles with certain emoji characters, causing layout recalculation loops
- Terminal font/rendering engine has issues with specific Unicode characters

**Solution**:
- Use stable, well-supported emoji icons only
- `☕` (coffee) emoji is stable and renders consistently
- `🍅` (tomato) emoji is stable and renders consistently
- Avoid furniture/object emojis like `🛋️`, `🪑`, `🛏️` which may cause rendering issues

**Lesson Learned**:
- Always test emoji choices thoroughly in target terminal environments
- Terminal emoji support varies significantly between systems
- Stick to food/drink emojis which tend to have better terminal support
- When debugging UI issues, consider emoji rendering as a potential cause

**Current Stable Configuration**:
- Work Session: `🍅` (tomato) - stable
- Short Break: `☕` (coffee) - stable  
- Long Break: `☕` (coffee) - stable (uses same icon as Short Break to avoid rendering issues)

**Alternative Visual Distinction**:
- Long Break uses cyan progress bar color instead of emoji differentiation
- This provides visual distinction without emoji rendering risks

## General Guidelines

### Emoji Usage in Terminal UIs
- Prefer simple, common emoji characters
- Food/drink emoji tend to be more stable than object emoji
- Always test emoji rendering in the actual deployment terminal environment
- Have fallback strategies for emoji that don't render properly
- Consider using text symbols or colors instead of complex emoji for critical UI elements

### Rich Library Considerations
- Text length consistency is important for stable layouts
- Complex Unicode characters can cause layout recalculation issues
- Cache invalidation can occur with unstable rendering elements
- Test all visual elements thoroughly in target terminal environments