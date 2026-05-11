# pyCycle AI Prompting PPT Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 產生一份正體中文教學 PPT，教學生用 AI 提示詞、uv、pyCycle 與 PySide6 建立接近 GasTurb 入門功能的 CFM56-7B 高旁通比渦扇教學專案。

**Architecture:** 以 repo wrapper 保存教學文件與來源資料，不修改 `upstream/pyCycle`。PPT 用 `python-pptx` 由腳本生成，內容包含階段規劃、可複製提示詞、pyCycle 輸出說明、資料來源管理與 UI 雛形。

**Tech Stack:** PowerShell, uv, python-pptx, Pillow, pyCycle upstream examples, PySide6 planning content.

---

### Task 1: Reference Sources

**Files:**
- Create: `Reference_sources/README.md`
- Create: `Reference_sources/source_manifest.md`
- Create/download: `Reference_sources/nasa-20170000232-pycycle-openmdao.pdf`
- Create/download: `Reference_sources/openmdao-pycycle-readme.md`
- Create/download: `Reference_sources/aircraft-commerce-cfm56-7b-specs.pdf`

- [x] **Step 1: Create source folder rules**

Write a short README explaining that every AI-sourced datum must be stored or logged before being used.

- [x] **Step 2: Download accessible sources**

Run:

```powershell
Invoke-WebRequest -Uri 'https://ntrs.nasa.gov/api/citations/20170000232/downloads/20170000232.pdf' -OutFile 'D:\45_pyCycle_edu\Reference_sources\nasa-20170000232-pycycle-openmdao.pdf'
Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/OpenMDAO/pyCycle/master/README.md' -OutFile 'D:\45_pyCycle_edu\Reference_sources\openmdao-pycycle-readme.md'
Invoke-WebRequest -Uri 'https://www.aircraft-commerce.com/wp-content/uploads/aircraft-commerce-docs/Aircraft%20guides/CFM56-7B/ISSUE58_CFM56_7B_SPECS.pdf' -OutFile 'D:\45_pyCycle_edu\Reference_sources\aircraft-commerce-cfm56-7b-specs.pdf'
```

Expected: each command exits 0 and files exist.

- [x] **Step 3: Record blocked official downloads**

Record CFM International and Safran URLs with the observed Vercel / Cloudflare block status so students can see the source governance trail.

### Task 2: PPT Generator

**Files:**
- Create: `docs/slides/build_pycycle_ai_prompting_ppt.py`
- Generate: `docs/slides/pycycle_ai_prompting_course.pptx`

- [x] **Step 1: Build slide generator**

Use `python-pptx` helpers for title slides, tables, prompt cards, process diagrams, turbofan schematic, and UI mockup.

- [x] **Step 2: Generate PPTX through uv**

Run:

```powershell
uv run --with python-pptx --with pillow python docs/slides/build_pycycle_ai_prompting_ppt.py
```

Expected: script prints the output path and creates `docs/slides/pycycle_ai_prompting_course.pptx`.

### Task 3: Dev Log and Verification

**Files:**
- Create: `docs/dev-log/2026-05-11-pycycle-ai-prompting-ppt.md`

- [x] **Step 1: Write dev log**

Record GitNexus analysis, changed files, source download status, PPT generation, and verification commands.

- [x] **Step 2: Verify upstream submodule**

Run:

```powershell
./scripts/verify-upstream-submodule.ps1
```

Expected: the script reports the upstream submodule is unchanged.

- [x] **Step 3: Detect changed scope**

Run GitNexus detect changes with scope `all` and review that only docs/reference/slide generator files are affected.

