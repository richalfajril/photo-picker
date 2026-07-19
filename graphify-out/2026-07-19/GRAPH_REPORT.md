# Graph Report - photo-picker  (2026-07-19)

## Corpus Check
- 43 files · ~18,550 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 759 nodes · 832 edges · 39 communities (37 shown, 2 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `897075b2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

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
- WorkspaceRepository
- SettingsRepository
- StartWindow
- Q: What connects graphify, Workflow: graphify, Photo Picker AI Development Guide to the rest of the system?
- CacheManager
- ViewerWindow
- LoadingScreen
- main.py
- WorkspaceRepository
- viewer_controller.py
- OverlayManager
- FileOperationService

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
- `ViewerController` --uses--> `Workspace`  [INFERRED]
  src/controllers/viewer_controller.py → src/domain/workspace.py
- `ViewerController` --uses--> `LoadingScreen`  [INFERRED]
  src/controllers/viewer_controller.py → src/presentation/loading_screen.py
- `ViewerController` --uses--> `ViewerWindow`  [INFERRED]
  src/controllers/viewer_controller.py → src/presentation/viewer_window.py
- `ViewerController` --uses--> `WorkspaceRepository`  [INFERRED]
  src/controllers/viewer_controller.py → src/repositories/workspace_repository.py
- `ViewerController` --uses--> `CacheManager`  [INFERRED]
  src/controllers/viewer_controller.py → src/services/cache_manager.py

## Import Cycles
- None detected.

## Communities (39 total, 2 thin omitted)

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

### Community 18 - "WorkspaceRepository"
Cohesion: 0.19
Nodes (7): Any, QObject, Preloads the next few images into memory cache., Refreshes the ViewerWindow with the current image., Connects the presentation layer to the domain and service layers., Shows loading screen and scans folder., ViewerController

### Community 19 - "SettingsRepository"
Cohesion: 0.15
Nodes (10): Global constants for Photo Picker MVP., Any, Path, Repository for managing global Application Settings., Handles reading and writing application settings to settings.json., Returns the default settings structure., Load settings from file, returning defaults if not found or corrupted., Save settings to the file system. (+2 more)

### Community 20 - "StartWindow"
Cohesion: 0.22
Nodes (5): QWidget, Startup Window UI Component., Enables the Start button only if all required fields are filled., The initial window for workspace configuration., StartWindow

### Community 21 - "Q: What connects graphify, Workflow: graphify, Photo Picker AI Development Guide to the rest of the system?"
Cohesion: 0.50
Nodes (3): Answer, Q: What connects graphify, Workflow: graphify, Photo Picker AI Development Guide to the rest of the system?, Source Nodes

### Community 31 - "CacheManager"
Cohesion: 0.09
Nodes (19): CacheManager, QImage, QObject, Service for managing image cache and background preloading., Manages in-memory image caching and background preloading      to ensure instant, Retrieves the image from cache if available, otherwise loads it synchronously., Submits a list of file paths to be preloaded in the background., Task executed in the thread pool. (+11 more)

### Community 32 - "ViewerWindow"
Cohesion: 0.12
Nodes (12): QGraphicsView, QKeyEvent, QMouseEvent, QWheelEvent, PhotoGraphicsView, QImage, QWidget, Viewer Window UI Component. (+4 more)

### Community 33 - "LoadingScreen"
Cohesion: 0.20
Nodes (6): LoadingScreen, QWidget, Loading Screen UI Component., Updates the progress bar and labels., Updates only the status message., Displays progress during the initial folder scan and image caching phase.

### Community 34 - "main.py"
Cohesion: 0.24
Nodes (7): QDialog, main(), Entry point for the Photo Picker application., QWidget, Workspace Recovery Dialog UI Component., Dialog asking the user whether to continue an existing workspace     or start a, RecoveryDialog

### Community 35 - "WorkspaceRepository"
Cohesion: 0.23
Nodes (7): Path, Handles reading and writing Workspace data to the file system., Convert workspace name to a safe folder name., Get the absolute path to a workspace folder., Save a workspace and its selections to the file system., Load a workspace by name. Returns None if not found., WorkspaceRepository

### Community 36 - "viewer_controller.py"
Cohesion: 0.27
Nodes (6): Main controller orchestrating the Viewer UI and business logic., Domain model for Workspace., Represents the state of a Photo Picker session.     Workspace is the aggregate r, Update the last modified timestamp., Workspace, Repository for managing Workspace storage.

### Community 37 - "OverlayManager"
Cohesion: 0.22
Nodes (5): OverlayManager, QWidget, Service for managing visual UI overlays (COPIED, REMOVED)., Shows a fading overlay with the given text and color., Manages transient visual notifications on top of the ViewerWindow.

### Community 38 - "FileOperationService"
Cohesion: 0.25
Nodes (5): FileOperationService, Service for file operations (Copy and Remove)., Copies the source file to the destination folder.         Returns True if succes, Removes the copied file from the destination folder (Undo action).         Does, Handles safe file copying and removal for the Photo Picker workflow.     Never m

## Knowledge Gaps
- **549 isolated node(s):** `Answer`, `Source Nodes`, `graphify`, `Workflow: graphify`, `Photo Picker AI Development Guide` (+544 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ViewerController` connect `WorkspaceRepository` to `ViewerWindow`, `LoadingScreen`, `main.py`, `WorkspaceRepository`, `viewer_controller.py`, `OverlayManager`, `FileOperationService`, `CacheManager`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `CacheManager` connect `CacheManager` to `WorkspaceRepository`, `viewer_controller.py`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **What connects `Answer`, `Source Nodes`, `graphify` to the rest of the system?**
  _549 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `UI Specification` be split into smaller, more focused modules?**
  _Cohesion score 0.03389830508474576 - nodes in this community are weakly interconnected._
- **Should `Task Breakdown` be split into smaller, more focused modules?**
  _Cohesion score 0.04 - nodes in this community are weakly interconnected._
- **Should `System Architecture` be split into smaller, more focused modules?**
  _Cohesion score 0.041666666666666664 - nodes in this community are weakly interconnected._
- **Should `Product Requirements` be split into smaller, more focused modules?**
  _Cohesion score 0.043478260869565216 - nodes in this community are weakly interconnected._