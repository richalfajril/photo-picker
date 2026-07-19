# Graph Report - .  (2026-07-19)

## Corpus Check
- Corpus is ~15,017 words - fits in a single context window. You may not need a graph.

## Summary
- 579 nodes · 564 edges · 18 communities (16 shown, 2 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- UI Specification
- Task Breakdown
- System Architecture
- Product Requirements
- AI Agent Guidelines
- Error Handling
- Component Specification
- User Flow
- Configuration
- Changelog
- State Machine
- File Structure
- Shortcut Spec
- Test Plan
- Storage Architecture
- Class Diagram
- Graphify Workflow
- Graphify Rules

## God Nodes (most connected - your core abstractions)
1. `UI_SPEC` - 58 edges
2. `TASK_BREAKDOWN` - 49 edges
3. `SYSTEM_ARCHITECTURE` - 47 edges
4. `PRD` - 45 edges
5. `AGENTS` - 42 edges
6. `ERROR_HANDLING` - 42 edges
7. `COMPONENT_SPEC` - 40 edges
8. `USERFLOW` - 37 edges
9. `CONFIGURATION` - 31 edges
10. `CHANGELOG` - 30 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (18 total, 2 thin omitted)

### Community 0 - "UI Specification"
Cohesion: 0.03
Nodes (58): 10. Zoom, 11. Pan, 12. Exit Dialog, 13. Workspace Recovery Dialog, 14. Keyboard Interaction, 15. Mouse Interaction, 16. UI States, 17. Visual Hierarchy (+50 more)

### Community 1 - "Task Breakdown"
Cohesion: 0.04
Nodes (49): 1.1 Initialize Project, 1.2 Create Project Structure, 1.3 Application Entry, 2.1 Workspace, 2.2 WorkspaceRepository, 2.3 SettingsRepository, 2.4 Storage, 3.1 UI (+41 more)

### Community 2 - "System Architecture"
Cohesion: 0.04
Nodes (47): 1. Overview, 2.1 Simplicity First, 2.2 Keyboard First, 2.3 Offline First, 2.4 Workspace Based, 2.5 Separation of Responsibility, 2. Design Principles, 3. High-Level Architecture (+39 more)

### Community 3 - "Product Requirements"
Cohesion: 0.04
Nodes (45): 10. User Interface, 11. Keyboard Shortcut, 12. Success Metrics, 13. MVP Scope, 14. Future Roadmap, 1. Overview, 2. Problem Statement, 3. Goals (+37 more)

### Community 4 - "AI Agent Guidelines"
Cohesion: 0.05
Nodes (42): AGENTS, AI Agent Responsibilities, AI Agent Restrictions, Architecture, Coding Standards, Configuration, Definition of Done, Development Principles (+34 more)

### Community 5 - "Error Handling"
Cohesion: 0.05
Nodes (42): 10. Recovery Errors, 11. Exit Errors, 12. Logging, 13. User Messages, 14. Recovery Strategy, 15. Critical Failure, 16. Summary, 1. Overview (+34 more)

### Community 6 - "Component Specification"
Cohesion: 0.05
Nodes (40): 10. Lifecycle, 11. Future Components (v2.0), 12. Summary, 1. Overview, 2. Component Overview, 3. Presentation Layer, 4. Controller Layer, 5. Domain Layer (+32 more)

### Community 7 - "User Flow"
Cohesion: 0.05
Nodes (38): 1. Launch Application, 2. Configuration Window, 3. Scan Folder, 4. Loading, 5. Fullscreen Viewer, 📷 Photo Picker, Auto Next after Copy, Complete User Flow (+30 more)

### Community 8 - "Configuration"
Cohesion: 0.06
Nodes (31): 10. System Configuration, 11. Configuration Lifecycle, 12. Validation Rules, 13. Save Strategy, 14. Configuration Ownership, 15. Future Configuration (v2.0), 16. Summary, 1. Overview (+23 more)

### Community 9 - "Changelog"
Cohesion: 0.07
Nodes (28): [0.1.0] - Initial Planning, Added, Architecture, Changed, CHANGELOG, Changelog Rules, Commit Convention, Deprecated (+20 more)

### Community 10 - "State Machine"
Cohesion: 0.07
Nodes (28): 10. Exiting State, 11. Closed State, 12. Invalid Transitions, 13. Event Summary, 14. State Rules, 15. Summary, 1. Overview, 2. State Overview (+20 more)

### Community 11 - "File Structure"
Cohesion: 0.07
Nodes (27): assets/, Class, config/, controllers/, Dependency Mapping, Directory Description, docs/, domain/ (+19 more)

### Community 12 - "Shortcut Spec"
Cohesion: 0.07
Nodes (26): 10. Shortcut Priority, 11. Shortcut Availability, 12. Future Shortcuts (v2.0), 13. Summary, 1. Overview, 2. Design Principles, 3. Keyboard Shortcut Reference, 4. Mouse Interaction (+18 more)

### Community 13 - "Test Plan"
Cohesion: 0.09
Nodes (22): 10. Overlay, 11. Sound Feedback, 12. Zoom & Pan, 13. Workspace Recovery, 14. Error Handling, 15. Performance, 16. Packaging, 17. Regression Checklist (+14 more)

### Community 14 - "Storage Architecture"
Cohesion: 0.10
Nodes (20): 1. Overview, 2. Storage Structure, 3. Storage Components, 4. Workspace Storage, 5. Cache, 6. Logs, 7. Repository Mapping, 8. Data Flow (+12 more)

### Community 15 - "Class Diagram"
Cohesion: 0.11
Nodes (18): CacheManager, CLASS_DIAGRAM, Controller, Dependency Rules, Domain, FileOperationService, ImageLoaderService, Layer Description (+10 more)

## Knowledge Gaps
- **547 isolated node(s):** `graphify`, `Workflow: graphify`, `Photo Picker AI Development Guide`, `Project Overview`, `Mandatory Rules` (+542 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `graphify`, `Workflow: graphify`, `Photo Picker AI Development Guide` to the rest of the system?**
  _547 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `UI Specification` be split into smaller, more focused modules?**
  _Cohesion score 0.03389830508474576 - nodes in this community are weakly interconnected._
- **Should `Task Breakdown` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._
- **Should `System Architecture` be split into smaller, more focused modules?**
  _Cohesion score 0.041666666666666664 - nodes in this community are weakly interconnected._
- **Should `Product Requirements` be split into smaller, more focused modules?**
  _Cohesion score 0.043478260869565216 - nodes in this community are weakly interconnected._
- **Should `AI Agent Guidelines` be split into smaller, more focused modules?**
  _Cohesion score 0.046511627906976744 - nodes in this community are weakly interconnected._
- **Should `Error Handling` be split into smaller, more focused modules?**
  _Cohesion score 0.046511627906976744 - nodes in this community are weakly interconnected._