# Pymodoro UI Refactoring Feature Tasks

## Overview

This document breaks down the UI refactoring plan into discrete, actionable tasks. The current monolithic `PomodoroUI` class in `src/pymodoro/interface.py` will be refactored into a modular architecture with separate concerns for theming, components, screens, layout, and coordination.

**Target Architecture**: `src/pymodoro/ui/` package with theme.py, components.py, screens.py, layout.py, and refactored interface.py

## Phase 1: Foundation (High Priority)

### Task 1.1: Dependency Analysis

**Context**: Before refactoring, we need to understand the timer interface that drives the UI state.

**Checklist**:
- [x] Read and analyze `src/pymodoro/timer.py` to understand SessionType enum values
- [x] Document all timer properties accessed by current UI (time_left, current_session, is_running, etc.)
- [x] Document all timer methods called by current UI
- [x] Identify the structure of timer.settings dictionary
- [x] Create interface documentation for timer API used by UI components
- [x] Note any timer state that affects UI rendering or behavior

### Task 1.2: Theme System Creation

**Context**: Extract all visual styling from the monolithic interface into a centralized theme system. Current interface has hard-coded colors, ASCII art, and dimensions scattered throughout.

**Checklist**:
- [x] Create `src/pymodoro/ui/` directory structure
- [x] Create `src/pymodoro/ui/__init__.py` with file location comment
- [x] Create `src/pymodoro/ui/theme.py` with file location comment
- [x] Extract ASCII art constants (TOMATO_ART, BREAK_TOMATO_ART, PAUSE_TOMATO_ART) from interface.py
- [x] Create `SessionTheme` dataclass with colors, icon, and session-specific styling
- [x] Create theme instances for WORK, SHORT_BREAK, LONG_BREAK, and PAUSED states
- [x] Extract hard-coded dimensions (timer panel width=12, progress bar width=40, dialog width=60, etc.)
- [x] Create `Dimensions` class with all UI sizing constants
- [x] Create `ThemeManager` class to get appropriate theme based on session state and pause status
- [x] Add type hints and docstrings following project conventions
- [x] Ensure themes match current visual appearance exactly

### Task 1.3: Component System Creation

**Context**: Extract all rendering logic from the monolithic class into reusable components. Each component should handle one specific UI element and accept theme/data parameters.

**Checklist**:
- [x] Create `src/pymodoro/ui/components.py` with file location comment
- [x] Create `TimerDisplay` component class that renders MM:SS time format in a Rich Panel
- [x] Create `ProgressBar` component class that renders horizontal progress visualization
- [x] Create `Header` component class that renders session title, pomodoro number, and pause status
- [x] Create `ArtDisplay` component class that renders ASCII art based on session state
- [x] Create `Dialog` component class for reusable modal dialogs (help and confirmation)
- [x] Create `StatusInfo` component class for session context information
- [x] Each component should accept theme and data parameters, not session_info dictionary
- [x] Each component should return Rich renderable objects
- [x] Implement error handling with meaningful fallbacks for each component
- [x] Add comprehensive type hints and docstrings
- [x] Ensure components produce identical output to current interface methods

## Phase 2: Screen Management (Medium Priority)

### Task 2.1: Layout System Creation

**Context**: Create utilities for consistent positioning, sizing, and alignment of components. Replace ad-hoc layout code with systematic approach.

**Checklist**:
- [x] Create `src/pymodoro/ui/layout.py` with file location comment
- [x] Create `LayoutGrid` class for systematic component positioning using Rich Table.grid
- [x] Create `Dimensions` utilities for calculating responsive sizes based on terminal dimensions
- [x] Create `Alignment` helper functions for centering and positioning content
- [x] Create `Spacing` utilities for consistent padding and margins between components
- [x] Implement utilities that work with Rich's layout system (Align, Panel, Group, etc.)
- [x] Add methods for creating the main screen layout structure
- [x] Add methods for creating modal dialog layouts
- [x] Ensure layout utilities produce identical visual results to current implementation
- [x] Add comprehensive type hints and docstrings

### Task 2.2: Screen Management Creation

**Context**: Create screen classes that compose components into complete interfaces. Replace direct rendering with screen-based architecture.

**Checklist**:
- [x] Create `src/pymodoro/ui/screens.py` with file location comment
- [x] Create abstract `Screen` base class with common screen functionality
- [x] Create `MainScreen` class that composes timer components into main interface
- [x] Create `HelpScreen` class that renders help overlay using Dialog component
- [x] Create `ConfirmationScreen` class that renders confirmation dialogs
- [x] Create `ScreenManager` class to coordinate screen transitions and overlay management
- [x] Each screen class should use components and layout utilities, not direct Rich calls
- [x] Implement screen state management for proper transitions
- [x] Add modal overlay support for help and confirmation screens
- [x] Ensure screens render identically to current interface output
- [x] Add comprehensive type hints and docstrings

## Phase 3: Integration (High Priority)

### Task 3.1: Interface Refactoring

**Context**: Transform the existing monolithic PomodoroUI class into a thin facade that coordinates the new modular system while maintaining backward compatibility.

**Checklist**:
- [x] Create backup of original `src/pymodoro/interface.py`
- [x] Refactor `PomodoroUI.__init__()` to initialize theme manager and screen manager
- [x] Replace `_get_session_info()` method with calls to theme manager
- [x] Replace all `_render_*_component()` methods with component system calls
- [x] Replace `_assemble_main_screen()` with MainScreen usage
- [x] Replace `_render_help()` with HelpScreen usage
- [x] Replace `_render_confirmation()` with ConfirmationScreen usage
- [x] Maintain identical `get_renderable(confirmation_type=None)` method signature
- [x] Preserve caching behavior using new component system
- [x] Remove all hard-coded styling, dimensions, and ASCII art from interface.py
- [x] Ensure interface.py becomes a coordination layer, not a rendering layer
- [x] Add imports for new ui module components
- [x] Maintain all existing functionality without regression

### Task 3.2: Testing and Validation

**Context**: Ensure the refactored system maintains all existing functionality with identical visual output and behavior.

**Checklist**:
- [x] Test main timer screen renders identically to original
- [x] Test help screen overlay renders identically to original
- [x] Test confirmation dialogs render identically to original
- [x] Test session state transitions (work → break → long break)
- [x] Test pause/resume state changes and visual indicators
- [x] Test all color theming for different session types
- [x] Test progress bar animation and accuracy
- [x] Test ASCII art display for all session states
- [x] Verify performance is maintained or improved
- [x] Test error handling and fallback scenarios
- [x] Test caching behavior works correctly
- [ ] Run existing tests if any exist to ensure no regression
- [ ] Test with various terminal sizes if responsive features are implemented

## Implementation Guidelines

### Code Standards Checklist
- [x] Add file location comment at top of each new file (e.g., `# src/pymodoro/ui/theme.py`)
- [x] Use absolute imports, not relative imports
- [x] Add type hints for all function parameters and return values
- [x] Add Google-style docstrings for all classes and functions
- [x] Follow PEP 8 conventions with 4-space indentation
- [x] Use descriptive, self-explanatory class and function names

### Error Handling Checklist
- [x] Implement try-catch blocks with meaningful fallbacks in all components
- [x] Provide default values for theme failures
- [x] Log errors appropriately without disrupting user experience
- [x] Ensure graceful degradation maintains basic functionality
- [x] Test error scenarios and fallback behavior

### Architecture Validation Checklist
- [x] Each module has single responsibility (theme, components, screens, layout)
- [x] Components are reusable and composable
- [x] Configuration is externalized from rendering logic
- [x] No circular dependencies between modules
- [x] Public API maintains backward compatibility
- [x] New architecture supports future extensibility

## Success Criteria

### Functional Validation
- [x] All screens render pixel-perfect identical to original
- [x] All user interactions work exactly as before
- [x] Performance metrics meet or exceed original
- [x] No functionality is lost or changed
- [x] Memory usage is maintained or improved

### Code Quality Validation
- [x] Code is modular with clear separation of concerns
- [x] New features can be added without modifying existing components
- [x] Components can be tested in isolation
- [x] Configuration changes don't require code changes
- [x] Documentation is complete and accurate

### Migration Validation
- [x] Original interface.py can be restored if needed
- [x] New system integrates seamlessly with existing timer module
- [x] No changes required to other parts of the application
- [x] Refactoring maintains all existing imports and exports